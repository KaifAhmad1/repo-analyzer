"""
Simplified AI Agent for GitHub Repository Analysis
Uses OpenAI/Anthropic APIs directly for natural language Q&A
"""

import openai
import anthropic
import os
import json
from typing import Dict, List, Any, Optional
from src.servers.mcp_client import MCPClient

def create_ai_agent(model_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create and configure AI agent"""
    api_key = None
    
    if model_name.startswith("gpt"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        client = openai.OpenAI(api_key=api_key)
    elif model_name.startswith("claude"):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")
        client = anthropic.Anthropic(api_key=api_key)
    else:
        raise ValueError(f"Unsupported model: {model_name}")
    
    return {
        "client": client,
        "model": model_name,
        "mcp_client": MCPClient(),
        "config": config
    }

def get_available_tools() -> List[Dict[str, Any]]:
    """Get list of available MCP tools"""
    return [
        {
            "name": "get_file_content",
            "description": "Get the content of a specific file from the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the file"}
                },
                "required": ["file_path"]
            }
        },
        {
            "name": "get_repository_structure",
            "description": "Get the directory structure of the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path (optional)"}
                }
            }
        },
        {
            "name": "get_commit_history",
            "description": "Get recent commits from the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of commits to retrieve"}
                }
            }
        },
        {
            "name": "search_code",
            "description": "Search for code patterns or functions in the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "file_type": {"type": "string", "description": "File type filter (optional)"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_issues",
            "description": "Get issues and pull requests from the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {"type": "string", "description": "Issue state (open/closed)"},
                    "limit": {"type": "integer", "description": "Number of issues to retrieve"}
                }
            }
        }
    ]

def create_system_prompt(repository_url: str) -> str:
    """Create system prompt for the AI agent"""
    return f"""You are an intelligent GitHub repository analyzer. You can help users understand any GitHub repository by answering questions about its code, structure, commits, issues, and more.

Current Repository: {repository_url}

You have access to the following tools:
- get_file_content: Read file contents
- get_repository_structure: Get directory structure
- get_commit_history: Get recent commits
- search_code: Search for code patterns
- get_issues: Get issues and pull requests

Guidelines:
1. Always use the appropriate tools to gather information before answering
2. Provide detailed, helpful explanations
3. Include code examples when relevant
4. Be conversational and friendly
5. If you need to use multiple tools, do so systematically
6. Always explain what you're doing and why

Example questions you can answer:
- "What is this repository about?"
- "Show me the main entry points"
- "What are the recent changes?"
- "Find authentication-related code"
- "What dependencies does this use?"
- "Are there any performance issues?"
- "Explain the database implementation"
- "What's the testing strategy?"

Start by understanding the repository structure and then answer the user's question."""

def ask_question(agent: Dict[str, Any], question: str, repository_url: str) -> Dict[str, Any]:
    """Ask a question to the AI agent and get response"""
    try:
        # Create system prompt
        system_prompt = create_system_prompt(repository_url)
        
        # Get available tools
        tools = get_available_tools()
        
        # Prepare messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        
        # Make API call
        if agent["model"].startswith("gpt"):
            response = agent["client"].chat.completions.create(
                model=agent["model"],
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=2000
            )
            
            # Process response
            response_message = response.choices[0].message
            
            # Handle tool calls
            if response_message.tool_calls:
                tool_results = []
                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    # Call MCP tool
                    result = agent["mcp_client"].call_tool(tool_name, tool_args)
                    tool_results.append({
                        "tool": tool_name,
                        "result": result
                    })
                
                # Add tool results to conversation
                messages.append(response_message)
                for result in tool_results:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result["result"])
                    })
                
                # Get final response
                final_response = agent["client"].chat.completions.create(
                    model=agent["model"],
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000
                )
                
                return {
                    "response": final_response.choices[0].message.content,
                    "tools_used": [r["tool"] for r in tool_results],
                    "success": True
                }
            else:
                return {
                    "response": response_message.content,
                    "tools_used": [],
                    "success": True
                }
        
        elif agent["model"].startswith("claude"):
            # For Claude, we'll use a simpler approach
            response = agent["client"].messages.create(
                model=agent["model"],
                max_tokens=2000,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": question}]
            )
            
            return {
                "response": response.content[0].text,
                "tools_used": [],
                "success": True
            }
    
    except Exception as e:
        return {
            "response": f"Error: {str(e)}",
            "tools_used": [],
            "success": False
        }

def analyze_repository(agent: Dict[str, Any], repository_url: str) -> Dict[str, Any]:
    """Perform comprehensive repository analysis"""
    analysis = {
        "overview": "",
        "structure": "",
        "recent_changes": "",
        "dependencies": "",
        "issues": ""
    }
    
    try:
        # Get repository structure
        structure_result = agent["mcp_client"].call_tool("get_repository_structure", {})
        analysis["structure"] = structure_result
        
        # Get recent commits
        commits_result = agent["mcp_client"].call_tool("get_commit_history", {"limit": 10})
        analysis["recent_changes"] = commits_result
        
        # Get issues
        issues_result = agent["mcp_client"].call_tool("get_issues", {"state": "open", "limit": 5})
        analysis["issues"] = issues_result
        
        # Generate overview using AI
        overview_prompt = f"""Based on this repository structure and recent activity, provide a comprehensive overview of what this repository does:

Structure: {analysis['structure']}
Recent Changes: {analysis['recent_changes']}
Issues: {analysis['issues']}

Please provide a clear, concise overview of the repository's purpose and main functionality."""
        
        overview_response = ask_question(agent, overview_prompt, repository_url)
        analysis["overview"] = overview_response["response"]
        
        return analysis
    
    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}",
            "success": False
        } 