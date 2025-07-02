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
        self.tools_used = []
        self.servers_used = []
    
    async def _call_server_tool(self, server_name: str, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a tool from a specific FastMCP server"""
        try:
            script_path = self.servers[server_name]
            if not os.path.exists(script_path):
                return {"error": f"Server script not found: {script_path}", "success": False}
            
            # Track tool and server usage
            self.tools_used.append(f"{server_name}.{tool_name}")
            if server_name not in self.servers_used:
                self.servers_used.append(server_name)
            
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
    
    def get_repository_overview(self, repo_url: str) -> str:
        """Get repository overview information"""
        try:
            # Use multiple tools to get comprehensive overview
            overview_data = {}
            
            # Get README content
            readme_result = asyncio.run(self._call_server_tool("file_content", "get_readme_content", repo_url=repo_url))
            if readme_result.get("success"):
                overview_data["readme"] = readme_result.get("result", "")
            
            # Get file structure
            structure_result = asyncio.run(self._call_server_tool("repository_structure", "get_file_structure", repo_url=repo_url))
            if structure_result.get("success"):
                overview_data["structure"] = structure_result.get("result", "")
            
            # Get recent commits
            commits_result = asyncio.run(self._call_server_tool("commit_history", "get_recent_commits", repo_url=repo_url, limit=5))
            if commits_result.get("success"):
                overview_data["recent_commits"] = commits_result.get("result", "")
            
            # Get dependencies
            deps_result = asyncio.run(self._call_server_tool("code_search", "search_dependencies", repo_url=repo_url))
            if deps_result.get("success"):
                overview_data["dependencies"] = deps_result.get("result", "")
            
            return json.dumps(overview_data, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_tools_used(self) -> List[str]:
        """Get list of tools used in this session"""
        return self.tools_used.copy()
    
    def get_servers_used(self) -> List[str]:
        """Get list of servers used in this session"""
        return self.servers_used.copy()

def create_repository_analyzer_agent(model_name: str = "llama-3.1-70b-versatile") -> Agent:
    """Create an AI agent for repository analysis"""
    try:
        # Initialize the agent with Groq model
        agent = Agent(
            model=Groq(model=model_name),
            tools=ReasoningTools()
        )
        return agent
    except Exception as e:
        print(f"Error creating agent: {e}")
        return None

def ask_question(question: str, repository_url: str) -> tuple[str, list[str]]:
    """Ask a question about a repository and get AI response with tool tracking"""
    try:
        # Create tools instance for tracking
        tools = FastMCPTools()
        
        def create_tracking_agent():
            """Create agent with tracking capabilities"""
            agent = create_repository_analyzer_agent()
            if not agent:
                return None
            
            # Add tracked tool functions
            def tracked_get_file_content(repo_url: str, file_path: str) -> str:
                return tools.get_file_content(repo_url, file_path)
            
            def tracked_list_directory(repo_url: str, path: str = "") -> str:
                return tools.list_directory(repo_url, path)
            
            def tracked_get_readme_content(repo_url: str) -> str:
                return tools.get_readme_content(repo_url)
            
            def tracked_get_directory_tree(repo_url: str, max_depth: int = 3) -> str:
                return tools.get_directory_tree(repo_url, max_depth)
            
            def tracked_get_file_structure(repo_url: str) -> str:
                return tools.get_file_structure(repo_url)
            
            def tracked_analyze_project_structure(repo_url: str) -> str:
                return tools.analyze_project_structure(repo_url)
            
            def tracked_get_recent_commits(repo_url: str, limit: int = 20) -> str:
                return tools.get_recent_commits(repo_url, limit)
            
            def tracked_get_commit_details(repo_url: str, commit_sha: str) -> str:
                return tools.get_commit_details(repo_url, commit_sha)
            
            def tracked_get_commit_statistics(repo_url: str, days: int = 30) -> str:
                return tools.get_commit_statistics(repo_url, days)
            
            def tracked_search_code(repo_url: str, query: str, language: str = "") -> str:
                return tools.search_code(repo_url, query, language)
            
            def tracked_search_files(repo_url: str, filename_pattern: str) -> str:
                return tools.search_files(repo_url, filename_pattern)
            
            def tracked_find_functions(repo_url: str, function_name: str, language: str = "") -> str:
                return tools.find_functions(repo_url, function_name, language)
            
            def tracked_get_code_metrics(repo_url: str) -> str:
                return tools.get_code_metrics(repo_url)
            
            def tracked_search_dependencies(repo_url: str) -> str:
                return tools.search_dependencies(repo_url)
            
            # Add tools to agent
            agent.add_tool(tracked_get_file_content)
            agent.add_tool(tracked_list_directory)
            agent.add_tool(tracked_get_readme_content)
            agent.add_tool(tracked_get_directory_tree)
            agent.add_tool(tracked_get_file_structure)
            agent.add_tool(tracked_analyze_project_structure)
            agent.add_tool(tracked_get_recent_commits)
            agent.add_tool(tracked_get_commit_details)
            agent.add_tool(tracked_get_commit_statistics)
            agent.add_tool(tracked_search_code)
            agent.add_tool(tracked_search_files)
            agent.add_tool(tracked_find_functions)
            agent.add_tool(tracked_get_code_metrics)
            agent.add_tool(tracked_search_dependencies)
            
            return agent
        
        # Create agent with tracking
        agent = create_tracking_agent()
        if not agent:
            return "Error: Could not create AI agent", []
        
        # Create prompt with repository context
        prompt = f"""
        You are an AI assistant specialized in analyzing GitHub repositories. 
        The user is asking about this repository: {repository_url}
        
        Question: {question}
        
        Please analyze the repository using the available tools and provide a comprehensive answer.
        Use the tools to gather information about the repository structure, code, dependencies, and recent activity.
        
        Provide a detailed, well-structured response that directly answers the user's question.
        """
        
        # Get response from agent
        response = agent.run(prompt)
        
        # Get tools and servers used
        tools_used = tools.get_tools_used()
        servers_used = tools.get_servers_used()
        
        return response, tools_used
        
    except Exception as e:
        return f"Error analyzing repository: {str(e)}", []

def analyze_repository(repository_url: str) -> tuple[str, list[str]]:
    """Analyze a repository and provide comprehensive overview"""
    try:
        tools = FastMCPTools()
        
        # Get comprehensive repository analysis
        overview = tools.get_repository_overview(repository_url)
        
        # Create analysis prompt
        prompt = f"""
        Please provide a comprehensive analysis of this GitHub repository: {repository_url}
        
        Repository data: {overview}
        
        Please provide:
        1. What this repository is about
        2. Main technologies and dependencies used
        3. Project structure and key files
        4. Recent activity and development status
        5. Key features and functionality
        
        Format your response in a clear, structured manner.
        """
        
        # Get AI analysis
        agent = create_repository_analyzer_agent()
        if agent:
            response = agent.run(prompt)
            tools_used = tools.get_tools_used()
            return response, tools_used
        else:
            return f"Repository Overview: {overview}", tools.get_tools_used()
            
    except Exception as e:
        return f"Error analyzing repository: {str(e)}", []

def get_repository_overview(repository_url: str) -> str:
    """Get basic repository overview"""
    try:
        tools = FastMCPTools()
        return tools.get_repository_overview(repository_url)
    except Exception as e:
        return f"Error getting repository overview: {str(e)}"

def search_repository_code(repository_url: str, search_query: str) -> str:
    """Search for code in repository"""
    try:
        tools = FastMCPTools()
        return tools.search_code(repository_url, search_query)
    except Exception as e:
        return f"Error searching code: {str(e)}"

def analyze_repository_structure(repository_url: str) -> str:
    """Analyze repository structure"""
    try:
        tools = FastMCPTools()
        return tools.analyze_project_structure(repository_url)
    except Exception as e:
        return f"Error analyzing structure: {str(e)}"

def get_recent_activity(repository_url: str) -> str:
    """Get recent repository activity"""
    try:
        tools = FastMCPTools()
        commits = tools.get_recent_commits(repository_url, limit=10)
        return commits
    except Exception as e:
        return f"Error getting recent activity: {str(e)}"

def create_ai_agent(model_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create AI agent with configuration"""
    try:
        agent = create_repository_analyzer_agent(model_name)
        return {"success": True, "agent": agent}
    except Exception as e:
        return {"success": False, "error": str(e)}

def ask_question_advanced(question: str, repository_url: str, use_team: bool = False) -> str:
    """Advanced question asking with team support"""
    return ask_question(question, repository_url)[0]

def analyze_repository_advanced(repository_url: str) -> str:
    """Advanced repository analysis"""
    return analyze_repository(repository_url)[0]

def test_fastmcp_connection() -> Dict[str, Any]:
    """Test FastMCP connection"""
    try:
        tools = FastMCPTools()
        # Test a simple operation
        test_result = tools.get_file_structure("https://github.com/test/test")
        return {
            "success": True,
            "message": "FastMCP connection successful",
            "test_result": test_result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "FastMCP connection failed"
        }

def list_available_tools() -> List[str]:
    """List all available tools"""
    tools = FastMCPTools()
    return [
        "get_file_content",
        "list_directory", 
        "get_readme_content",
        "get_directory_tree",
        "get_file_structure",
        "analyze_project_structure",
        "get_recent_commits",
        "get_commit_details",
        "get_commit_statistics",
        "search_code",
        "search_files",
        "find_functions",
        "get_code_metrics",
        "search_dependencies",
        "get_repository_overview"
    ] 
