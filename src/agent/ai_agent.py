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
        
        # Create the main agent with enhanced configuration
        self.agent = Agent(
            model=Groq(id=model_name),
            memory=self.memory,
            storage=self.storage,
            tools=[ReasoningTools()],
            instructions=[
                """You are an expert repository analyst with deep knowledge of software development, 
                code architecture, and best practices. Your role is to analyze GitHub repositories and provide 
                comprehensive, accurate, and actionable insights.

                When analyzing repositories:
                1. Always use the available tools to gather real data
                2. Provide specific examples from the codebase
                3. Structure your responses clearly with headers and bullet points
                4. Include actionable recommendations
                5. Be thorough but concise
                6. Focus on practical insights that would be valuable to developers

                Never provide generic or placeholder responses. Always base your analysis on actual repository data.
                """
            ]
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
    
    def _gather_repository_data(self, repo_url: str, status_callback=None) -> str:
        """Gather comprehensive repository data for analysis, with optional status updates"""
        try:
            data = {}
            
            def update_status(msg):
                if status_callback:
                    status_callback(msg)
            
            # Get README content
            update_status("Fetching README content...")
            readme_result = asyncio.run(self.tools._call_server_tool("file_content", "get_readme_content", repo_url=repo_url))
            if readme_result.get("success"):
                data["readme"] = readme_result.get("result", "")
            
            # Get file structure
            update_status("Analyzing file structure...")
            structure_result = asyncio.run(self.tools._call_server_tool("repository_structure", "get_file_structure", repo_url=repo_url))
            if structure_result.get("success"):
                data["file_structure"] = structure_result.get("result", "")
            
            # Get directory tree
            update_status("Building directory tree...")
            tree_result = asyncio.run(self.tools._call_server_tool("repository_structure", "get_directory_tree", repo_url=repo_url, max_depth=3))
            if tree_result.get("success"):
                data["directory_tree"] = tree_result.get("result", "")
            
            # Get project structure analysis
            update_status("Analyzing project structure...")
            project_result = asyncio.run(self.tools._call_server_tool("repository_structure", "analyze_project_structure", repo_url=repo_url))
            if project_result.get("success"):
                data["project_analysis"] = project_result.get("result", "")
            
            # Get recent commits
            update_status("Fetching recent commits...")
            commits_result = asyncio.run(self.tools._call_server_tool("commit_history", "get_recent_commits", repo_url=repo_url, limit=10))
            if commits_result.get("success"):
                data["recent_commits"] = commits_result.get("result", "")
            
            # Get commit statistics
            update_status("Analyzing commit statistics...")
            stats_result = asyncio.run(self.tools._call_server_tool("commit_history", "get_commit_statistics", repo_url=repo_url, days=30))
            if stats_result.get("success"):
                data["commit_statistics"] = stats_result.get("result", "")
            
            # Get dependencies
            update_status("Scanning dependencies...")
            deps_result = asyncio.run(self.tools._call_server_tool("code_search", "search_dependencies", repo_url=repo_url))
            if deps_result.get("success"):
                data["dependencies"] = deps_result.get("result", "")
            
            # Get code metrics
            update_status("Gathering code metrics...")
            metrics_result = asyncio.run(self.tools._call_server_tool("code_search", "get_code_metrics", repo_url=repo_url))
            if metrics_result.get("success"):
                data["code_metrics"] = metrics_result.get("result", "")
            
            update_status("Repository data gathering complete.")
            return json.dumps(data, indent=2)
        except Exception as e:
            if status_callback:
                status_callback(f"Error: {str(e)}")
            return f"Error gathering repository data: {str(e)}"
    
    def ask_question(self, question: str, repo_url: str, user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
        """Ask a question about the repository with enhanced analysis"""
        try:
            # Set user ID for memory
            self.agent.user_id = user_id
            
            # First, gather comprehensive repository data
            repo_data = self._gather_repository_data(repo_url, status_callback=status_callback)
            
            # Create enhanced prompt with context
            enhanced_prompt = f"""
            You are an expert repository analyst. Use the following repository data to answer the user's question comprehensively.

            REPOSITORY DATA:
            {repo_data}

            USER QUESTION: {question}

            INSTRUCTIONS:
            1. Analyze the repository data thoroughly
            2. Use specific examples from the codebase when relevant
            3. Provide actionable insights and recommendations
            4. Structure your response clearly with headers and bullet points
            5. If the question requires additional data, use the available tools to gather it
            6. Be specific and avoid generic responses

            Please provide a detailed, well-structured answer based on the actual repository content.
            """
            
            # Create tool functions for this repository
            tool_functions = self._create_tool_functions(repo_url)
            
            # Add tools to agent temporarily
            original_tools = self.agent.tools
            self.agent.tools = list(original_tools) + list(tool_functions.values())
            
            # Get response
            response = self.agent.run_response(enhanced_prompt, stream=False)
            
            # Restore original tools
            self.agent.tools = original_tools
            
            return response.content, self.tools.get_tools_used()
        except Exception as e:
            return f"Error analyzing repository: {str(e)}", []
    
    def generate_summary(self, repo_url: str, user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
        """Generate a comprehensive repository summary with enhanced analysis"""
        try:
            # Set user ID for memory
            self.agent.user_id = user_id
            
            # Gather comprehensive repository data
            repo_data = self._gather_repository_data(repo_url, status_callback=status_callback)
            
            # Create comprehensive summary prompt
            summary_prompt = f"""
            Generate a comprehensive, well-structured summary of this GitHub repository based on the following data:

            REPOSITORY DATA:
            {repo_data}

            REQUIREMENTS:
            1. **Repository Overview**: Purpose, main features, and key components
            2. **Project Structure**: Architecture and organization with specific file examples
            3. **Technology Stack**: Languages, frameworks, and dependencies with versions
            4. **Code Quality**: Metrics, patterns, and best practices observed
            5. **Development Activity**: Recent commits and activity patterns
            6. **Key Files**: Important configuration and source files with their purposes
            7. **Architecture Insights**: Design patterns and code organization
            8. **Dependencies Analysis**: External libraries and their purposes
            9. **Testing Strategy**: Test coverage and testing approaches
            10. **Documentation Quality**: README and code documentation assessment
            11. **Recommendations**: Specific suggestions for improvement or exploration

            FORMAT:
            - Use clear headers and subheaders
            - Include specific examples from the codebase
            - Provide actionable insights
            - Use bullet points for better readability
            - Include relevant metrics and statistics
            - Be specific and avoid generic statements

            Please provide a detailed, professional summary that would be useful for developers and stakeholders.
            """
            
            # Create tool functions for this repository
            tool_functions = self._create_tool_functions(repo_url)
            
            # Add tools to agent temporarily
            original_tools = self.agent.tools
            self.agent.tools = list(original_tools) + list(tool_functions.values())
            
            # Get response
            response = self.agent.run_response(summary_prompt, stream=False)
            
            # Restore original tools
            self.agent.tools = original_tools
            
            return response.content, self.tools.get_tools_used()
        except Exception as e:
            return f"Error generating summary: {str(e)}", []
    
    def analyze_code_patterns(self, repo_url: str, user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
        """Analyze code patterns and architecture with enhanced insights"""
        try:
            # Set user ID for memory
            self.agent.user_id = user_id
            
            # Gather comprehensive repository data
            repo_data = self._gather_repository_data(repo_url, status_callback=status_callback)
            
            # Create analysis prompt
            analysis_prompt = f"""
            Perform a comprehensive code pattern and architecture analysis of this repository based on the following data:

            REPOSITORY DATA:
            {repo_data}

            ANALYSIS REQUIREMENTS:
            1. **Design Patterns**: Identify and explain common design patterns used in the codebase
            2. **Code Organization**: Analyze how the code is structured and organized
            3. **Dependencies**: External libraries and their purposes with version analysis
            4. **Code Quality**: Metrics, complexity, and maintainability assessment
            5. **Testing**: Test coverage, testing strategies, and test organization
            6. **Documentation**: Code documentation quality and README assessment
            7. **Best Practices**: Adherence to language-specific and general best practices
            8. **Architecture**: Overall system architecture and component relationships
            9. **Security**: Security considerations and potential vulnerabilities
            10. **Performance**: Performance considerations and optimizations
            11. **Scalability**: Scalability aspects and potential bottlenecks
            12. **Maintainability**: Code maintainability and technical debt assessment

            FORMAT:
            - Use clear sections with headers
            - Include specific code examples when relevant
            - Provide actionable recommendations
            - Use bullet points for better readability
            - Include metrics and statistics where available
            - Be specific and provide concrete examples

            Please provide a detailed technical analysis that would be valuable for developers and architects.
            """
            
            # Create tool functions for this repository
            tool_functions = self._create_tool_functions(repo_url)
            
            # Add tools to agent temporarily
            original_tools = self.agent.tools
            self.agent.tools = list(original_tools) + list(tool_functions.values())
            
            # Get response
            response = self.agent.run_response(analysis_prompt, stream=False)
            
            # Restore original tools
            self.agent.tools = original_tools
            
            return response.content, self.tools.get_tools_used()
        except Exception as e:
            return f"Error analyzing code patterns: {str(e)}", []
    
    def quick_analysis(self, repo_url: str, user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
        """Perform a quick analysis of the repository with structured insights"""
        try:
            # Set user ID for memory
            self.agent.user_id = user_id
            
            # Gather essential repository data
            repo_data = self._gather_repository_data(repo_url, status_callback=status_callback)
            
            # Create quick analysis prompt
            quick_analysis_prompt = f"""
            Perform a quick, structured analysis of this GitHub repository based on the following data:

            REPOSITORY DATA:
            {repo_data}

            QUICK ANALYSIS REQUIREMENTS:
            1. **Project Type**: What type of project is this? (Web app, CLI tool, library, etc.)
            2. **Main Purpose**: What is the primary purpose of this repository?
            3. **Technology Stack**: List the main technologies, languages, and frameworks used
            4. **Key Features**: What are the main features or capabilities?
            5. **Project Structure**: Brief overview of how the code is organized
            6. **Dependencies**: Key external dependencies and their purposes
            7. **Recent Activity**: Summary of recent development activity
            8. **Code Quality Indicators**: Brief assessment of code quality
            9. **Documentation**: Quality of README and documentation
            10. **Quick Insights**: 2-3 key insights about the project

            FORMAT:
            - Use clear, concise sections
            - Provide specific examples from the codebase
            - Use bullet points for easy scanning
            - Include relevant metrics and statistics
            - Be informative but concise
            - Focus on the most important aspects

            Please provide a quick, informative analysis that gives a good overview of the repository.
            """
            
            # Create tool functions for this repository
            tool_functions = self._create_tool_functions(repo_url)
            
            # Add tools to agent temporarily
            original_tools = self.agent.tools
            self.agent.tools = list(original_tools) + list(tool_functions.values())
            
            # Get response
            response = self.agent.run_response(quick_analysis_prompt, stream=False)
            
            # Restore original tools
            self.agent.tools = original_tools
            
            return response.content, self.tools.get_tools_used()
        except Exception as e:
            return f"Error performing quick analysis: {str(e)}", []

    def get_repository_overview(self, repo_url: str) -> str:
        """Get enhanced repository overview with structured data"""
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
            
            # Get project structure analysis
            project_result = asyncio.run(self.tools._call_server_tool("repository_structure", "analyze_project_structure", repo_url=repo_url))
            if project_result.get("success"):
                overview_data["project_analysis"] = project_result.get("result", "")
            
            # Extract key information for display
            repo_info = {
                "name": "Repository",
                "description": "Repository analysis available",
                "has_readme": bool(overview_data.get("readme")),
                "has_structure": bool(overview_data.get("structure")),
                "has_commits": bool(overview_data.get("recent_commits")),
                "has_dependencies": bool(overview_data.get("dependencies")),
                "has_analysis": bool(overview_data.get("project_analysis")),
                "last_updated": "Available",
                "stars": "Check repository",
                "forks": "Check repository"
            }
            
            # Try to extract name from README or structure
            if overview_data.get("readme"):
                readme_text = overview_data["readme"]
                if "# " in readme_text:
                    lines = readme_text.split("\n")
                    for line in lines:
                        if line.startswith("# "):
                            repo_info["name"] = line.replace("# ", "").strip()
                            break
            
            return json.dumps(repo_info, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

# Convenience functions for easy integration with UI
def create_analyzer_agent(model_name: str = "llama-3.1-70b-versatile") -> RepositoryAnalyzerAgent:
    """Create a new repository analyzer agent"""
    return RepositoryAnalyzerAgent(model_name)

def ask_repository_question(question: str, repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
    """Ask a question about a repository"""
    agent = RepositoryAnalyzerAgent(model_name)
    return agent.ask_question(question, repo_url, user_id, status_callback=status_callback)

def generate_repository_summary(repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
    """Generate a comprehensive repository summary"""
    agent = RepositoryAnalyzerAgent(model_name)
    return agent.generate_summary(repo_url, user_id, status_callback=status_callback)

def analyze_repository_patterns(repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
    """Analyze repository code patterns"""
    agent = RepositoryAnalyzerAgent(model_name)
    return agent.analyze_code_patterns(repo_url, user_id, status_callback=status_callback)

def get_repository_overview(repo_url: str) -> str:
    """Get basic repository overview"""
    agent = RepositoryAnalyzerAgent()
    return agent.get_repository_overview(repo_url)

def quick_repository_analysis(repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
    """Perform a quick analysis of a repository"""
    agent = RepositoryAnalyzerAgent(model_name)
    return agent.quick_analysis(repo_url, user_id, status_callback=status_callback)

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