"""
GitHub Repository Analyzer - AI Agent System
Simple, effective AI agent for GitHub repository analysis using FastMCP v2 servers
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from fastmcp import Client

class FastMCPTools:
    """Simple tools wrapper for FastMCP v2 servers"""
    
    def __init__(self):
        self.servers = {
            "file_content": "src/servers/file_content_server.py",
            "repository_structure": "src/servers/repository_structure_server.py", 
            "commit_history": "src/servers/commit_history_server.py",
            "code_search": "src/servers/code_search_server.py"
        }
    
    async def _call_server_tool(self, server_name: str, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a tool from a specific FastMCP server"""
        try:
            script_path = self.servers[server_name]
            if not os.path.exists(script_path):
                return {"error": f"Server script not found: {script_path}", "success": False}
            
            async with Client(script_path) as client:
                result = await client.call_tool(tool_name, kwargs)
                if hasattr(result, 'content') and result.content:
                    return {
                        "result": result.content[0].text if result.content else "",
                        "success": True
                    }
                else:
                    return {
                        "result": "No content returned",
                        "success": True
                    }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_file_content(self, repo_url: str, file_path: str) -> str:
        """Get content of a specific file"""
        try:
            result = asyncio.run(self._call_server_tool("file_content", "get_file_content", repo_url=repo_url, file_path=file_path))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def list_directory(self, repo_url: str, path: str = "") -> str:
        """List directory contents"""
        try:
            result = asyncio.run(self._call_server_tool("file_content", "list_directory", repo_url=repo_url, path=path))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_readme_content(self, repo_url: str) -> str:
        """Get README content from repository"""
        try:
            result = asyncio.run(self._call_server_tool("file_content", "get_readme_content", repo_url=repo_url))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_directory_tree(self, repo_url: str, max_depth: int = 3) -> str:
        """Get directory tree structure"""
        try:
            result = asyncio.run(self._call_server_tool("repository_structure", "get_directory_tree", repo_url=repo_url, max_depth=max_depth))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_file_structure(self, repo_url: str) -> str:
        """Get flat file structure"""
        try:
            result = asyncio.run(self._call_server_tool("repository_structure", "get_file_structure", repo_url=repo_url))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_project_structure(self, repo_url: str) -> str:
        """Analyze project structure and identify key components"""
        try:
            result = asyncio.run(self._call_server_tool("repository_structure", "analyze_project_structure", repo_url=repo_url))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_recent_commits(self, repo_url: str, limit: int = 20) -> str:
        """Get recent commit history"""
        try:
            result = asyncio.run(self._call_server_tool("commit_history", "get_recent_commits", repo_url=repo_url, limit=limit))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_commit_details(self, repo_url: str, commit_sha: str) -> str:
        """Get detailed commit information"""
        try:
            result = asyncio.run(self._call_server_tool("commit_history", "get_commit_details", repo_url=repo_url, commit_sha=commit_sha))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_commit_statistics(self, repo_url: str, days: int = 30) -> str:
        """Get commit statistics"""
        try:
            result = asyncio.run(self._call_server_tool("commit_history", "get_commit_statistics", repo_url=repo_url, days=days))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def search_code(self, repo_url: str, query: str, language: str = "") -> str:
        """Search for code patterns"""
        try:
            result = asyncio.run(self._call_server_tool("code_search", "search_code", repo_url=repo_url, query=query, language=language))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def search_files(self, repo_url: str, filename_pattern: str) -> str:
        """Search for files by pattern"""
        try:
            result = asyncio.run(self._call_server_tool("code_search", "search_files", repo_url=repo_url, filename_pattern=filename_pattern))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def find_functions(self, repo_url: str, function_name: str, language: str = "") -> str:
        """Find function definitions"""
        try:
            result = asyncio.run(self._call_server_tool("code_search", "find_functions", repo_url=repo_url, function_name=function_name, language=language))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_code_metrics(self, repo_url: str) -> str:
        """Get code metrics and statistics"""
        try:
            result = asyncio.run(self._call_server_tool("code_search", "get_code_metrics", repo_url=repo_url))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def search_dependencies(self, repo_url: str) -> str:
        """Search for dependency files"""
        try:
            result = asyncio.run(self._call_server_tool("code_search", "search_dependencies", repo_url=repo_url))
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

def create_repository_analyzer_agent(model_name: str = "gemini-2.0-flash-001") -> Agent:
    """Create a focused repository analysis agent using FastMCP v2"""
    
    tools = FastMCPTools()
    
    # Clear, focused instructions for the agent
    agent_instructions = [
        "You are a GitHub Repository Analyzer powered by FastMCP v2. Your job is to answer questions about GitHub repositories using the available tools.",
        "",
        "Available Tools (FastMCP v2):",
        "",
        "📁 File Content Tools:",
        "- get_file_content: Get content of a specific file",
        "- list_directory: List directory contents", 
        "- get_readme_content: Get README content from repository",
        "",
        "🌳 Repository Structure Tools:",
        "- get_directory_tree: Get directory tree structure",
        "- get_file_structure: Get flat file structure",
        "- analyze_project_structure: Analyze project structure and identify key components",
        "",
        "📝 Commit History Tools:",
        "- get_recent_commits: Get recent commit history",
        "- get_commit_details: Get detailed commit information",
        "- get_commit_statistics: Get commit statistics",
        "",
        "🔍 Code Search Tools:",
        "- search_code: Search for code patterns",
        "- search_files: Search for files by pattern",
        "- find_functions: Find function definitions",
        "- get_code_metrics: Get code metrics and statistics",
        "- search_dependencies: Search for dependency files",
        "",
        "How to Answer Questions:",
        "1. Always use the appropriate tools to get accurate information",
        "2. For 'what is this repo about' - use get_readme_content and analyze_project_structure",
        "3. For 'main entry points' - use get_file_structure and look for main files",
        "4. For 'recent changes' - use get_recent_commits",
        "5. For 'find functions' - use find_functions or search_code",
        "6. For 'dependencies' - use search_dependencies",
        "7. For 'file structure' - use get_directory_tree or get_file_structure",
        "8. For 'code patterns' - use search_code",
        "9. For 'project analysis' - use analyze_project_structure",
        "",
        "Response Format:",
        "- Be clear and concise",
        "- Use markdown formatting",
        "- Include relevant code examples when helpful",
        "- Structure answers with headers and bullet points",
        "- Always explain what you found and how you found it",
        "",
        "Remember: Use FastMCP v2 tools first, then provide analysis based on the data you gather."
    ]
    
    agent = Agent(
        name="Repository Analyzer (FastMCP v2)",
        model=Gemini(id=model_name),
        tools=[
            ReasoningTools(add_instructions=True),
            tools.get_file_content,
            tools.list_directory,
            tools.get_readme_content,
            tools.get_directory_tree,
            tools.get_file_structure,
            tools.analyze_project_structure,
            tools.get_recent_commits,
            tools.get_commit_details,
            tools.get_commit_statistics,
            tools.search_code,
            tools.search_files,
            tools.find_functions,
            tools.get_code_metrics,
            tools.search_dependencies,
        ],
        instructions=agent_instructions,
        markdown=True,
        add_datetime_to_instructions=True,
    )
    
    return agent

def ask_question(question: str, repository_url: str) -> str:
    """Ask a question about a repository using FastMCP v2"""
    try:
        agent = create_repository_analyzer_agent()
        response = agent.run(f"Question: {question}\nRepository: {repository_url}")
        return response
    except Exception as e:
        return f"Error getting response: {str(e)}"

def analyze_repository(repository_url: str) -> str:
    """Perform comprehensive repository analysis using FastMCP v2"""
    try:
        agent = create_repository_analyzer_agent()
        response = agent.run(f"Provide a comprehensive analysis of this repository: {repository_url}")
        return response
    except Exception as e:
        return f"Error analyzing repository: {str(e)}"

def get_repository_overview(repository_url: str) -> str:
    """Get a quick overview of a repository"""
    try:
        agent = create_repository_analyzer_agent()
        response = agent.run(f"Provide a quick overview of this repository: {repository_url}")
        return response
    except Exception as e:
        return f"Error getting overview: {str(e)}"

def search_repository_code(repository_url: str, search_query: str) -> str:
    """Search for specific code in a repository"""
    try:
        agent = create_repository_analyzer_agent()
        response = agent.run(f"Search for '{search_query}' in this repository: {repository_url}")
        return response
    except Exception as e:
        return f"Error searching code: {str(e)}"

def analyze_repository_structure(repository_url: str) -> str:
    """Analyze the structure of a repository"""
    try:
        agent = create_repository_analyzer_agent()
        response = agent.run(f"Analyze the structure and organization of this repository: {repository_url}")
        return response
    except Exception as e:
        return f"Error analyzing structure: {str(e)}"

def get_recent_activity(repository_url: str) -> str:
    """Get recent activity and changes in a repository"""
    try:
        agent = create_repository_analyzer_agent()
        response = agent.run(f"Show me the recent activity and changes in this repository: {repository_url}")
        return response
    except Exception as e:
        return f"Error getting activity: {str(e)}"

# Legacy compatibility functions
def create_ai_agent(model_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create AI agent (legacy function)"""
    agent = create_repository_analyzer_agent(model_name)
    return {
        "agent": agent,
        "model": model_name,
        "config": config
    }

def ask_question_advanced(question: str, repository_url: str, use_team: bool = False) -> str:
    """Advanced question function (simplified to use single agent)"""
    return ask_question(question, repository_url)

def analyze_repository_advanced(repository_url: str) -> str:
    """Advanced analysis function (simplified to use single agent)"""
    return analyze_repository(repository_url)

# Utility functions for testing
def test_fastmcp_connection() -> Dict[str, Any]:
    """Test connection to FastMCP servers"""
    try:
        tools = FastMCPTools()
        test_repo = "https://github.com/microsoft/vscode"
        
        # Test a simple operation
        result = tools.get_readme_content(test_repo)
        
        if "Error:" in result:
            return {"success": False, "error": result}
        else:
            return {"success": True, "message": "FastMCP connection working"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def list_available_tools() -> List[str]:
    """List all available tools"""
    tools = FastMCPTools()
    return [
        "get_file_content", "list_directory", "get_readme_content",
        "get_directory_tree", "get_file_structure", "analyze_project_structure",
        "get_recent_commits", "get_commit_details", "get_commit_statistics",
        "search_code", "search_files", "find_functions", "get_code_metrics", "search_dependencies"
    ] 
