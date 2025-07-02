"""
GitHub Repository Analyzer - AI Agent System
Simple, effective AI agent for GitHub repository analysis using FastMCP v2 servers
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from agno.agent import Agent
from agno.models.groq import Groq
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
    
    async def analyze_code_structure(self, repo_url: str, file_path: str) -> str:
        """Analyze code structure using AST and CST for Python files"""
        try:
            result = await self._call_server_tool("code_search", "analyze_code_structure", repo_url=repo_url, file_path=file_path)
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def find_code_patterns(self, repo_url: str, pattern_type: str, language: str = "Python") -> str:
        """Find specific code patterns using AST analysis"""
        try:
            result = await self._call_server_tool("code_search", "find_code_patterns", repo_url=repo_url, pattern_type=pattern_type, language=language)
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def analyze_file_content(self, repo_url: str, file_path: str) -> str:
        """Get file content with advanced code analysis for Python files"""
        try:
            result = await self._call_server_tool("file_content", "analyze_file_content", repo_url=repo_url, file_path=file_path)
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def get_code_summary(self, repo_url: str, file_path: str) -> str:
        """Get a summary of code structure and metrics for Python files"""
        try:
            result = await self._call_server_tool("file_content", "get_code_summary", repo_url=repo_url, file_path=file_path)
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def find_code_issues(self, repo_url: str, file_path: str) -> str:
        """Find potential code issues and suggestions for Python files"""
        try:
            result = await self._call_server_tool("file_content", "find_code_issues", repo_url=repo_url, file_path=file_path)
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def analyze_codebase_structure(self, repo_url: str) -> str:
        """Analyze the codebase structure with AST parsing for Python files"""
        try:
            result = await self._call_server_tool("repository_structure", "analyze_codebase_structure", repo_url=repo_url)
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

def create_repository_analyzer_agent(model_name: str = "llama-3.1-70b-versatile") -> Agent:
    """Create an AI agent for repository analysis using Groq"""
    
    # Get Groq API key
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is required")
    
    # Create Groq model
    model = Groq(
        model=model_name,
        api_key=groq_api_key
    )
    
    # Create tools instance
    tools = FastMCPTools()
    
    # Create agent with repository analysis prompt
    agent = Agent(
        model=model,
        tools=[
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
            tools.analyze_code_structure,
            tools.find_code_patterns,
            tools.analyze_file_content,
            tools.get_code_summary,
            tools.find_code_issues,
            tools.analyze_codebase_structure
        ],
        system_prompt="""You are an expert GitHub repository analyzer. Your job is to help users understand and analyze GitHub repositories.

Key capabilities:
- Analyze repository structure and architecture
- Search and examine code files
- Understand dependencies and project setup
- Analyze commit history and development patterns
- Provide insights about code quality and patterns
- Answer questions about the repository

Guidelines:
1. Always be helpful and thorough in your analysis
2. Use the available tools to gather comprehensive information
3. Provide clear, actionable insights
4. Explain technical concepts in an accessible way
5. Focus on what's most important for the user's needs
6. Be systematic in your approach to analysis

When analyzing repositories:
- Start with an overview of the project structure
- Identify key files and their purposes
- Analyze the technology stack and dependencies
- Look for patterns in the codebase
- Provide recommendations for improvement if relevant

Remember: You have access to powerful tools for repository analysis. Use them effectively to provide the best possible insights."""
    )
    
    return agent

def ask_question(question: str, repository_url: str) -> tuple[str, list[str]]:
    """Ask a question about a repository using FastMCP v2 and return response with tools used"""
    try:
        # Check if Groq API key is available
        from src.utils.config import get_groq_api_key
        api_key = get_groq_api_key()
        if not api_key:
            return ("❌ **Groq API Key Required**\n\nPlease set your Groq API key in the .env file.", [])
        
        # Create a custom agent that tracks tool usage
        tools_used = []
        
        def create_tracking_agent():
            tools = FastMCPTools()
            
            # Create wrapper functions that track usage
            def tracked_get_file_content(repo_url: str, file_path: str) -> str:
                tools_used.append("get_file_content")
                return tools.get_file_content(repo_url, file_path)
            
            def tracked_list_directory(repo_url: str, path: str = "") -> str:
                tools_used.append("list_directory")
                return tools.list_directory(repo_url, path)
            
            def tracked_get_readme_content(repo_url: str) -> str:
                tools_used.append("get_readme_content")
                return tools.get_readme_content(repo_url)
            
            def tracked_get_directory_tree(repo_url: str, max_depth: int = 3) -> str:
                tools_used.append("get_directory_tree")
                return tools.get_directory_tree(repo_url, max_depth)
            
            def tracked_get_file_structure(repo_url: str) -> str:
                tools_used.append("get_file_structure")
                return tools.get_file_structure(repo_url)
            
            def tracked_analyze_project_structure(repo_url: str) -> str:
                tools_used.append("analyze_project_structure")
                return tools.analyze_project_structure(repo_url)
            
            def tracked_get_recent_commits(repo_url: str, limit: int = 20) -> str:
                tools_used.append("get_recent_commits")
                return tools.get_recent_commits(repo_url, limit)
            
            def tracked_get_commit_details(repo_url: str, commit_sha: str) -> str:
                tools_used.append("get_commit_details")
                return tools.get_commit_details(repo_url, commit_sha)
            
            def tracked_get_commit_statistics(repo_url: str, days: int = 30) -> str:
                tools_used.append("get_commit_statistics")
                return tools.get_commit_statistics(repo_url, days)
            
            def tracked_search_code(repo_url: str, query: str, language: str = "") -> str:
                tools_used.append("search_code")
                return tools.search_code(repo_url, query, language)
            
            def tracked_search_files(repo_url: str, filename_pattern: str) -> str:
                tools_used.append("search_files")
                return tools.search_files(repo_url, filename_pattern)
            
            def tracked_find_functions(repo_url: str, function_name: str, language: str = "") -> str:
                tools_used.append("find_functions")
                return tools.find_functions(repo_url, function_name, language)
            
            def tracked_get_code_metrics(repo_url: str) -> str:
                tools_used.append("get_code_metrics")
                return tools.get_code_metrics(repo_url)
            
            def tracked_search_dependencies(repo_url: str) -> str:
                tools_used.append("search_dependencies")
                return tools.search_dependencies(repo_url)
            
            # Create agent with tracking tools
            agent = Agent(
                name="Repository Analyzer (FastMCP v2) - Tracking",
                model=Groq(id="llama-3.3-70b-versatile"),
                tools=[
                    ReasoningTools(add_instructions=True),
                    tracked_get_file_content,
                    tracked_list_directory,
                    tracked_get_readme_content,
                    tracked_get_directory_tree,
                    tracked_get_file_structure,
                    tracked_analyze_project_structure,
                    tracked_get_recent_commits,
                    tracked_get_commit_details,
                    tracked_get_commit_statistics,
                    tracked_search_code,
                    tracked_search_files,
                    tracked_find_functions,
                    tracked_get_code_metrics,
                    tracked_search_dependencies,
                ],
                instructions=[
                    "You are a GitHub Repository Analyzer powered by FastMCP v2. Your job is to answer questions about GitHub repositories using the available tools.",
                    "Always use the appropriate tools to get accurate information and provide detailed analysis.",
                    "Be clear and concise in your responses.",
                    "Use markdown formatting and structure answers with headers and bullet points."
                ],
                markdown=True,
                add_datetime_to_instructions=True,
            )
            
            return agent
        
        agent = create_tracking_agent()
        response = agent.run(f"Question: {question}\nRepository: {repository_url}")
        
        # Remove duplicates and return unique tools used
        unique_tools = list(dict.fromkeys(tools_used))
        return response, unique_tools
        
    except Exception as e:
        return f"Error getting response: {str(e)}", []

def analyze_repository(repository_url: str) -> tuple[str, list[str]]:
    """Perform comprehensive repository analysis using FastMCP v2"""
    try:
        # Check if Groq API key is available
        from src.utils.config import get_groq_api_key
        api_key = get_groq_api_key()
        if not api_key:
            return ("❌ **Groq API Key Required**\n\nPlease set your Groq API key in the .env file.", [])
        
        # Use the same tracking mechanism as ask_question
        response, tools_used = ask_question("Provide a comprehensive analysis of this repository", repository_url)
        return response, tools_used
    except Exception as e:
        return f"Error analyzing repository: {str(e)}", []

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
