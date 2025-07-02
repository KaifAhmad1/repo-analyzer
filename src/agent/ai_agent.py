"""
GitHub Repository Analyzer - Enhanced AI Agent System
Simple but powerful agents using Agno FastMCP with all available servers
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.reasoning import ReasoningTools
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from fastmcp import Client

class FastMCPTools:
    """Enhanced tools wrapper for all FastMCP v2 servers"""
    
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
    
    # File Content Tools
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
    
    # Repository Structure Tools
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
    
    # Commit History Tools
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
    
    # Code Search Tools
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
    
    def get_tools_used(self) -> List[str]:
        """Get list of tools used in this session"""
        return self.tools_used.copy()
    
    def get_servers_used(self) -> List[str]:
        """Get list of servers used in this session"""
        return self.servers_used.copy()

class RepositoryAnalyzerAgent:
    """Enhanced Repository Analyzer Agent with memory and reasoning"""
    
    def __init__(self, model_name: str = "llama-3.1-70b-versatile"):
        self.model_name = model_name
        self.tools = FastMCPTools()
        
        # Initialize memory and storage
        self.memory = Memory(
            model=Groq(id=model_name),
            db=SqliteMemoryDb(table_name="repo_analyzer_memories", db_file="tmp/agent.db"),
            delete_memories=True,
            clear_memories=True,
        )
        
        self.storage = SqliteStorage(table_name="repo_analyzer_sessions", db_file="tmp/agent.db")
        
        # Create the main agent
        self.agent = Agent(
            name="Repository Analyzer",
            model=Groq(id=model_name),
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "You are an expert GitHub repository analyzer.",
                "Use the available tools to gather comprehensive information about repositories.",
                "Provide detailed, accurate, and helpful responses.",
                "Use tables and structured formatting when presenting data.",
                "Always include sources and references in your responses.",
                "Be thorough but concise in your analysis."
            ],
            memory=self.memory,
            storage=self.storage,
            enable_agentic_memory=True,
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_runs=5,
            markdown=True,
        )
    
    def _create_tool_functions(self, repo_url: str):
        """Create tool functions for the agent"""
        tools = self.tools
        
        def get_file_content(file_path: str) -> str:
            return tools.get_file_content(repo_url, file_path)
        
        def list_directory(path: str = "") -> str:
            return tools.list_directory(repo_url, path)
        
        def get_readme_content() -> str:
            return tools.get_readme_content(repo_url)
        
        def get_directory_tree(max_depth: int = 3) -> str:
            return tools.get_directory_tree(repo_url, max_depth)
        
        def get_file_structure() -> str:
            return tools.get_file_structure(repo_url)
        
        def analyze_project_structure() -> str:
            return tools.analyze_project_structure(repo_url)
        
        def get_recent_commits(limit: int = 20) -> str:
            return tools.get_recent_commits(repo_url, limit)
        
        def get_commit_details(commit_sha: str) -> str:
            return tools.get_commit_details(repo_url, commit_sha)
        
        def get_commit_statistics(days: int = 30) -> str:
            return tools.get_commit_statistics(repo_url, days)
        
        def search_code(query: str, language: str = "") -> str:
            return tools.search_code(repo_url, query, language)
        
        def search_files(filename_pattern: str) -> str:
            return tools.search_files(repo_url, filename_pattern)
        
        def find_functions(function_name: str, language: str = "") -> str:
            return tools.find_functions(repo_url, function_name, language)
        
        def get_code_metrics() -> str:
            return tools.get_code_metrics(repo_url)
        
        def search_dependencies() -> str:
            return tools.search_dependencies(repo_url)
        
        return {
            "get_file_content": get_file_content,
            "list_directory": list_directory,
            "get_readme_content": get_readme_content,
            "get_directory_tree": get_directory_tree,
            "get_file_structure": get_file_structure,
            "analyze_project_structure": analyze_project_structure,
            "get_recent_commits": get_recent_commits,
            "get_commit_details": get_commit_details,
            "get_commit_statistics": get_commit_statistics,
            "search_code": search_code,
            "search_files": search_files,
            "find_functions": find_functions,
            "get_code_metrics": get_code_metrics,
            "search_dependencies": search_dependencies,
        }
    
    def ask_question(self, question: str, repo_url: str, user_id: str = "default") -> Tuple[str, List[str]]:
        """Ask a question about the repository"""
        try:
            # Set user ID for memory
            self.agent.user_id = user_id
            
            # Create tool functions for this repository
            tool_functions = self._create_tool_functions(repo_url)
            
            # Add tools to agent temporarily
            original_tools = self.agent.tools
            self.agent.tools = list(original_tools) + list(tool_functions.values())
            
            # Get response
            response = self.agent.run_response(question, stream=False)
            
            # Restore original tools
            self.agent.tools = original_tools
            
            return response.content, self.tools.get_tools_used()
        except Exception as e:
            return f"Error: {str(e)}", []
    
    def generate_summary(self, repo_url: str, user_id: str = "default") -> Tuple[str, List[str]]:
        """Generate a comprehensive repository summary"""
        try:
            # Set user ID for memory
            self.agent.user_id = user_id
            
            # Create tool functions for this repository
            tool_functions = self._create_tool_functions(repo_url)
            
            # Add tools to agent temporarily
            original_tools = self.agent.tools
            self.agent.tools = list(original_tools) + list(tool_functions.values())
            
            # Create comprehensive summary prompt
            summary_prompt = """
            Generate a comprehensive summary of this GitHub repository. Include:
            
            1. **Repository Overview**: Purpose, main features, and key components
            2. **Project Structure**: Architecture and organization
            3. **Technology Stack**: Languages, frameworks, and dependencies
            4. **Code Quality**: Metrics, patterns, and best practices
            5. **Development Activity**: Recent commits and activity patterns
            6. **Key Files**: Important configuration and source files
            7. **Recommendations**: Suggestions for improvement or exploration
            
            Use the available tools to gather all necessary information and present it in a well-structured format.
            """
            
            # Get response
            response = self.agent.run_response(summary_prompt, stream=False)
            
            # Restore original tools
            self.agent.tools = original_tools
            
            return response.content, self.tools.get_tools_used()
        except Exception as e:
            return f"Error: {str(e)}", []
    
    def analyze_code_patterns(self, repo_url: str, user_id: str = "default") -> Tuple[str, List[str]]:
        """Analyze code patterns and architecture"""
        try:
            # Set user ID for memory
            self.agent.user_id = user_id
            
            # Create tool functions for this repository
            tool_functions = self._create_tool_functions(repo_url)
            
            # Add tools to agent temporarily
            original_tools = self.agent.tools
            self.agent.tools = list(original_tools) + list(tool_functions.values())
            
            # Create analysis prompt
            analysis_prompt = """
            Analyze the code patterns and architecture of this repository. Focus on:
            
            1. **Design Patterns**: Identify common design patterns used
            2. **Code Organization**: How the code is structured and organized
            3. **Dependencies**: External libraries and their purposes
            4. **Code Quality**: Metrics, complexity, and maintainability
            5. **Testing**: Test coverage and testing strategies
            6. **Documentation**: Code documentation and README quality
            7. **Best Practices**: Adherence to language-specific best practices
            
            Provide actionable insights and recommendations.
            """
            
            # Get response
            response = self.agent.run_response(analysis_prompt, stream=False)
            
            # Restore original tools
            self.agent.tools = original_tools
            
            return response.content, self.tools.get_tools_used()
        except Exception as e:
            return f"Error: {str(e)}", []
    
    def get_repository_overview(self, repo_url: str) -> str:
        """Get basic repository overview"""
        try:
            # Use multiple tools to get comprehensive overview
            overview_data = {}
            
            # Get README content
            readme_result = asyncio.run(self.tools._call_server_tool("file_content", "get_readme_content", repo_url=repo_url))
            if readme_result.get("success"):
                overview_data["readme"] = readme_result.get("result", "")
            
            # Get file structure
            structure_result = asyncio.run(self.tools._call_server_tool("repository_structure", "get_file_structure", repo_url=repo_url))
            if structure_result.get("success"):
                overview_data["structure"] = structure_result.get("result", "")
            
            # Get recent commits
            commits_result = asyncio.run(self.tools._call_server_tool("commit_history", "get_recent_commits", repo_url=repo_url, limit=5))
            if commits_result.get("success"):
                overview_data["recent_commits"] = commits_result.get("result", "")
            
            # Get dependencies
            deps_result = asyncio.run(self.tools._call_server_tool("code_search", "search_dependencies", repo_url=repo_url))
            if deps_result.get("success"):
                overview_data["dependencies"] = deps_result.get("result", "")
            
            return json.dumps(overview_data, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

# Convenience functions for easy integration with UI
def create_analyzer_agent(model_name: str = "llama-3.1-70b-versatile") -> RepositoryAnalyzerAgent:
    """Create a new repository analyzer agent"""
    return RepositoryAnalyzerAgent(model_name)

def ask_repository_question(question: str, repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default") -> Tuple[str, List[str]]:
    """Ask a question about a repository"""
    agent = RepositoryAnalyzerAgent(model_name)
    return agent.ask_question(question, repo_url, user_id)

def generate_repository_summary(repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default") -> Tuple[str, List[str]]:
    """Generate a comprehensive repository summary"""
    agent = RepositoryAnalyzerAgent(model_name)
    return agent.generate_summary(repo_url, user_id)

def analyze_repository_patterns(repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default") -> Tuple[str, List[str]]:
    """Analyze repository code patterns"""
    agent = RepositoryAnalyzerAgent(model_name)
    return agent.analyze_code_patterns(repo_url, user_id)

def get_repository_overview(repo_url: str) -> str:
    """Get basic repository overview"""
    agent = RepositoryAnalyzerAgent()
    return agent.get_repository_overview(repo_url)

# Legacy functions for backward compatibility
def ask_question(question: str, repository_url: str) -> tuple[str, list[str]]:
    """Legacy function for backward compatibility"""
    return ask_repository_question(question, repository_url)

def analyze_repository(repository_url: str) -> tuple[str, list[str]]:
    """Legacy function for backward compatibility"""
    return generate_repository_summary(repository_url)

def search_repository_code(repository_url: str, search_query: str) -> str:
    """Legacy function for backward compatibility"""
    agent = RepositoryAnalyzerAgent()
    tools = agent.tools
    return tools.search_code(repository_url, search_query)

def analyze_repository_structure(repository_url: str) -> str:
    """Legacy function for backward compatibility"""
    agent = RepositoryAnalyzerAgent()
    tools = agent.tools
    return tools.analyze_project_structure(repository_url)

def get_recent_activity(repository_url: str) -> str:
    """Legacy function for backward compatibility"""
    agent = RepositoryAnalyzerAgent()
    tools = agent.tools
    return tools.get_recent_commits(repository_url, limit=10) 