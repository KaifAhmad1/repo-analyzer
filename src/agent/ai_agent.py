"""
Improved AI Agent for GitHub Repository Analysis
Uses OpenAI/Anthropic APIs with official MCP SDK for better integration
"""

import openai
import anthropic
import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from src.servers.mcp_client_improved import SyncMCPClient

def create_ai_agent(model_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create and configure AI agent with improved MCP client"""
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
        "mcp_client": SyncMCPClient(),
        "config": config
    }

def get_available_tools() -> List[Dict[str, Any]]:
    """Get list of available MCP tools from the improved server"""
    return [
        {
            "name": "get_repository_overview",
            "description": "Get comprehensive overview of a GitHub repository including stats, description, and metadata",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repository URL"}
                },
                "required": ["repo_url"]
            }
        },
        {
            "name": "search_code",
            "description": "Search for code patterns or functions in the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repository URL"},
                    "query": {"type": "string", "description": "Search query"},
                    "language": {"type": "string", "description": "Programming language filter (optional)"}
                },
                "required": ["repo_url", "query"]
            }
        },
        {
            "name": "get_recent_commits",
            "description": "Get recent commit history from the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repository URL"},
                    "limit": {"type": "integer", "description": "Number of commits to retrieve (default: 10)"}
                },
                "required": ["repo_url"]
            }
        },
        {
            "name": "get_issues",
            "description": "Get issues and pull requests from the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repository URL"},
                    "state": {"type": "string", "description": "Issue state (open/closed, default: open)"},
                    "limit": {"type": "integer", "description": "Number of issues to retrieve (default: 10)"}
                },
                "required": ["repo_url"]
            }
        },
        {
            "name": "analyze_repository",
            "description": "Perform comprehensive repository analysis including structure, activity, and insights",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repository URL"}
                },
                "required": ["repo_url"]
            }
        }
    ]

def create_system_prompt(repository_url: str) -> str:
    """Create system prompt for the AI agent"""
    return f"""You are an intelligent GitHub repository analyzer powered by AI. You can help users understand any GitHub repository by answering questions about its code, structure, commits, issues, and more.

Current Repository: {repository_url}

You have access to the following tools:
- get_repository_overview: Get comprehensive repository information including stats, description, and metadata
- search_code: Search for code patterns or functions in the repository
- get_recent_commits: Get recent commit history from the repository
- get_issues: Get issues and pull requests from the repository
- analyze_repository: Perform comprehensive repository analysis

Guidelines:
1. Always use the appropriate tools to gather information before answering
2. Provide detailed, helpful explanations with context
3. Include code examples when relevant
4. Be conversational and friendly
5. If you need to use multiple tools, do so systematically
6. Always explain what you're doing and why
7. Use the analyze_repository tool for comprehensive overviews
8. Use search_code for finding specific functionality or patterns

Example questions you can answer:
- "What is this repository about?"
- "Show me the main entry points"
- "What are the recent changes?"
- "Find authentication-related code"
- "What dependencies does this use?"
- "Are there any performance issues?"
- "Explain the database implementation"
- "What's the testing strategy?"
- "Give me a comprehensive analysis of this repository"

Start by understanding the repository structure and then answer the user's question with detailed insights."""

def ask_question(agent: Dict[str, Any], question: str, repository_url: str) -> Dict[str, Any]:
    """Ask a question to the AI agent and get response using improved MCP client"""
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
                
                # Use improved MCP client
                with agent["mcp_client"] as mcp_client:
                    for tool_call in response_message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)
                        
                        # Add repository URL to tool args if not present
                        if "repo_url" not in tool_args:
                            tool_args["repo_url"] = repository_url
                        
                        # Call MCP tool
                        result = mcp_client.call_tool(tool_name, tool_args)
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
            # Handle Anthropic Claude
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
        
        else:
            return {
                "response": "Unsupported model type",
                "tools_used": [],
                "success": False
            }
    
    except Exception as e:
        return {
            "response": f"Error processing question: {str(e)}",
            "tools_used": [],
            "success": False
        }

def analyze_repository(agent: Dict[str, Any], repository_url: str) -> Dict[str, Any]:
    """Perform comprehensive repository analysis"""
    try:
        # Use the improved MCP client for analysis
        with agent["mcp_client"] as mcp_client:
            result = mcp_client.analyze_repository(repository_url)
            
            if result["success"]:
                return {
                    "response": result["result"],
                    "tools_used": ["analyze_repository"],
                    "success": True
                }
            else:
                return {
                    "response": f"Analysis failed: {result.get('error', 'Unknown error')}",
                    "tools_used": [],
                    "success": False
                }
    
    except Exception as e:
        return {
            "response": f"Error analyzing repository: {str(e)}",
            "tools_used": [],
            "success": False
        } 