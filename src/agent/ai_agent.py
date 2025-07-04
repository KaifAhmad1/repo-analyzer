"""
Enhanced GitHub Repository Analyzer - AI Agent System
Comprehensive agents using Agno FastMCP with all available servers for deep analysis
"""

import os
import json
import asyncio
import concurrent.futures
import time
from typing import Dict, List, Any, Optional, Tuple
from agno.agent import Agent
from agno.models.groq import Groq
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from fastmcp import Client
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import functools
from src.utils.config import get_groq_api_key

# Set the GROQ_API_KEY environment variable for Agno library
if not os.getenv("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = get_groq_api_key()

class FastMCPTools:
    """Enhanced FastMCP tools with connection pooling and intelligent caching"""
    
    def __init__(self, max_workers: int = 12, timeout: int = 60):
        self.max_workers = max_workers
        self.timeout = timeout
        self.cache = {}
        self.cache_hits = 0
        self.total_calls = 0
        self.tools_used = []
        self.servers_used = []
        self._client_pool = {}
        self._pool_lock = threading.Lock()
        
        # Define server scripts with proper paths
        self.servers = {
            "file_content": "src/servers/file_content_server.py",
            "repository_structure": "src/servers/repository_structure_server.py", 
            "commit_history": "src/servers/commit_history_server.py",
            "code_search": "src/servers/code_search_server.py"
        }
        
        # Performance tracking
        self.start_time = time.time()
        self.call_times = {}
    
    async def _call_server_tool(self, server_name: str, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a tool from a specific FastMCP server with enhanced error handling and connection pooling"""
        start_time = time.time()
        self.total_calls += 1
        
        try:
            script_path = self.servers[server_name]
            if not os.path.exists(script_path):
                return {"error": f"Server script not found: {script_path}", "success": False}
            
            # Track tool and server usage
            self.tools_used.append(f"{server_name}.{tool_name}")
            if server_name not in self.servers_used:
                self.servers_used.append(server_name)
            
            # Create cache key
            cache_key = f"{server_name}.{tool_name}.{hash(str(kwargs))}"
            if cache_key in self.cache:
                self.cache_hits += 1
                return self.cache[cache_key]
            
            # Use connection pooling for better performance
            with self._pool_lock:
                if server_name not in self._client_pool:
                    try:
                        self._client_pool[server_name] = Client(script_path)
                    except Exception as client_error:
                        return {"error": f"Failed to create client for {server_name}: {str(client_error)}", "success": False}
                client = self._client_pool[server_name]
            
            # Make the tool call with proper async context
            try:
                async with client:
                    result = await client.call_tool(tool_name, kwargs)
                    
                    # Handle the result properly
                    if hasattr(result, 'content') and result.content:
                        response = {
                            "result": result.content[0].text if result.content else "",
                            "success": True,
                            "server": server_name,
                            "tool": tool_name,
                            "execution_time": time.time() - start_time
                        }
                    else:
                        response = {
                            "result": "No content returned",
                            "success": True,
                            "server": server_name,
                            "tool": tool_name,
                            "execution_time": time.time() - start_time
                        }
                    
                    # Cache the result
                    self.cache[cache_key] = response
                    
                    # Track performance
                    execution_time = time.time() - start_time
                    self.call_times[f"{server_name}.{tool_name}"] = execution_time
                    
                    return response
                    
            except Exception as tool_error:
                return {"error": f"Tool call failed: {str(tool_error)}", "success": False, "server": server_name, "tool": tool_name, "execution_time": time.time() - start_time}
            
        except Exception as e:
            error_result = {"error": str(e), "success": False, "server": server_name, "tool": tool_name, "execution_time": time.time() - start_time}
            return error_result
    
    def _sync_call(self, server_name: str, tool_name: str, **kwargs) -> str:
        """Synchronous wrapper for async calls with timeout"""
        try:
            result = asyncio.run(self._call_server_tool(server_name, tool_name, **kwargs))
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({
                "error": str(e), 
                "success": False, 
                "server": server_name, 
                "tool": tool_name,
                "execution_time": 0
            }, indent=2)
    
    def _batch_call_tools(self, tool_calls: List[Tuple[str, str, dict]]) -> Dict[str, Any]:
        """Execute multiple tool calls in parallel with optimized batching and timeout"""
        results = {}
        
        # Group tools by server for better connection reuse
        server_groups = {}
        for server_name, tool_name, kwargs in tool_calls:
            if server_name not in server_groups:
                server_groups[server_name] = []
            server_groups[server_name].append((tool_name, kwargs))
        
        # Execute each server's tools in parallel with increased workers
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_key = {}
            
            for server_name, tools in server_groups.items():
                for tool_name, kwargs in tools:
                    key = f"{server_name}.{tool_name}"
                    future = executor.submit(
                        self._sync_call, server_name, tool_name, **kwargs
                    )
                    future_to_key[future] = key
            
            # Collect results as they complete with extended timeout
            try:
                for future in as_completed(future_to_key, timeout=self.timeout):
                    key = future_to_key[future]
                    try:
                        result = future.result(timeout=30)  # Individual tool timeout
                        results[key] = json.loads(result)
                    except TimeoutError:
                        results[key] = {"error": "Tool call timed out", "success": False}
                    except Exception as exc:
                        results[key] = {"error": str(exc), "success": False}
            except TimeoutError:
                # Handle overall timeout
                for future in future_to_key:
                    if not future.done():
                        key = future_to_key[future]
                        results[key] = {"error": "Batch operation timed out", "success": False}
        
        return results
    
    # File Content Tools
    def get_file_content(self, repo_url: str, file_path: str) -> str:
        """Get content of a specific file"""
        return self._sync_call("file_content", "get_file_content", repo_url=repo_url, file_path=file_path)
    
    def list_directory(self, repo_url: str, path: str = "") -> str:
        """List directory contents"""
        return self._sync_call("file_content", "list_directory", repo_url=repo_url, path=path)
    
    def get_readme_content(self, repo_url: str) -> str:
        """Get README content from repository"""
        return self._sync_call("file_content", "get_readme_content", repo_url=repo_url)
    
    def analyze_file_content(self, repo_url: str, file_path: str) -> str:
        """Analyze file content with code analysis"""
        return self._sync_call("file_content", "analyze_file_content", repo_url=repo_url, file_path=file_path)
    
    def get_code_summary(self, repo_url: str, file_path: str) -> str:
        """Get code summary for a file"""
        return self._sync_call("file_content", "get_code_summary", repo_url=repo_url, file_path=file_path)
    
    # Repository Structure Tools
    def get_directory_tree(self, repo_url: str, max_depth: int = 3) -> str:
        """Get directory tree structure"""
        return self._sync_call("repository_structure", "get_directory_tree", repo_url=repo_url, max_depth=max_depth)
    
    def get_file_structure(self, repo_url: str) -> str:
        """Get flat file structure"""
        return self._sync_call("repository_structure", "get_file_structure", repo_url=repo_url)
    
    def analyze_project_structure(self, repo_url: str) -> str:
        """Analyze project structure and identify key components"""
        return self._sync_call("repository_structure", "analyze_project_structure", repo_url=repo_url)
    
    def get_repository_overview(self, repo_url: str) -> str:
        """Get comprehensive repository overview"""
        return self._sync_call("repository_structure", "get_repository_overview", repo_url=repo_url)
    
    # Commit History Tools
    def get_recent_commits(self, repo_url: str, limit: int = 20) -> str:
        """Get recent commit history"""
        return self._sync_call("commit_history", "get_recent_commits", repo_url=repo_url, limit=limit)
    
    def get_commit_details(self, repo_url: str, commit_sha: str) -> str:
        """Get detailed commit information"""
        return self._sync_call("commit_history", "get_commit_details", repo_url=repo_url, commit_sha=commit_sha)
    
    def get_commit_statistics(self, repo_url: str, days: int = 30) -> str:
        """Get commit statistics"""
        return self._sync_call("commit_history", "get_commit_statistics", repo_url=repo_url, days=days)
    
    def get_development_patterns(self, repo_url: str) -> str:
        """Get development patterns and trends"""
        return self._sync_call("commit_history", "get_development_patterns", repo_url=repo_url)
    
    # Code Search Tools
    def search_code(self, repo_url: str, query: str, language: str = "") -> str:
        """Search for code patterns"""
        return self._sync_call("code_search", "search_code", repo_url=repo_url, query=query, language=language)
    
    def search_files(self, repo_url: str, filename_pattern: str) -> str:
        """Search for files by pattern"""
        return self._sync_call("code_search", "search_files", repo_url=repo_url, filename_pattern=filename_pattern)
    
    def find_functions(self, repo_url: str, function_name: str, language: str = "") -> str:
        """Find function definitions"""
        return self._sync_call("code_search", "find_functions", repo_url=repo_url, function_name=function_name, language=language)
    
    def get_code_metrics(self, repo_url: str) -> str:
        """Get code metrics and statistics"""
        return self._sync_call("code_search", "get_code_metrics", repo_url=repo_url)
    
    def search_dependencies(self, repo_url: str) -> str:
        """Search for dependency files"""
        return self._sync_call("code_search", "search_dependencies", repo_url=repo_url)
    
    def analyze_code_complexity(self, repo_url: str) -> str:
        """Analyze code complexity"""
        return self._sync_call("code_search", "analyze_code_complexity", repo_url=repo_url)
    
    def get_code_patterns(self, repo_url: str) -> str:
        """Get code patterns and architecture"""
        return self._sync_call("code_search", "get_code_patterns", repo_url=repo_url)
    
    def get_tools_used(self) -> List[str]:
        """Get list of tools used in this session"""
        return self.tools_used.copy()
    
    def get_servers_used(self) -> List[str]:
        """Get list of servers used in this session"""
        return self.servers_used.copy()
    
    def clear_cache(self):
        """Clear the tool cache"""
        self.cache.clear()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        avg_time = sum(self.call_times.values()) / len(self.call_times) if self.call_times else 0
        cache_hit_rate = (self.cache_hits / self.total_calls * 100) if self.total_calls > 0 else 0
        
        return {
            "total_calls": self.total_calls,
            "cache_hits": self.cache_hits,
            "cache_hit_rate": f"{cache_hit_rate:.1f}%",
            "average_call_time": f"{avg_time:.2f}s",
            "slowest_tool": max(self.call_times.items(), key=lambda x: x[1]) if self.call_times else None,
            "fastest_tool": min(self.call_times.items(), key=lambda x: x[1]) if self.call_times else None
        }
    
    def optimize_tool_selection(self, question: str, analysis_type: str = "auto") -> List[str]:
        """Intelligently select tools based on the question type and analysis mode"""
        question_lower = question.lower()
        
        # Define analysis types and their optimal tool sets
        analysis_tool_sets = {
            "qa_chat": {
                "description": "Quick Q&A with focused tools",
                "essential": ["get_readme_content", "get_file_structure", "get_repository_overview"],
                "optional": ["get_directory_tree", "get_recent_commits"],
                "keywords": ["what", "how", "where", "when", "why", "show", "tell", "explain"]
            },
            "summarization": {
                "description": "Comprehensive repository summary",
                "essential": ["get_readme_content", "get_file_structure", "get_repository_overview", "get_directory_tree"],
                "optional": ["get_recent_commits", "get_commit_statistics", "search_dependencies"],
                "keywords": ["summarize", "overview", "summary", "describe", "explain what this does"]
            },
            "chart_generation": {
                "description": "Data for charts and visualizations",
                "essential": ["get_commit_statistics", "get_code_metrics", "get_recent_commits"],
                "optional": ["get_development_patterns", "analyze_code_complexity"],
                "keywords": ["chart", "graph", "visualize", "statistics", "metrics", "trends", "activity"]
            },
            "quick_analysis": {
                "description": "Fast overview with minimal tools",
                "essential": ["get_readme_content", "get_file_structure"],
                "optional": ["get_repository_overview"],
                "keywords": ["quick", "fast", "overview", "basic", "simple"]
            },
            "code_analysis": {
                "description": "Deep code analysis and patterns",
                "essential": ["get_code_metrics", "search_code", "search_dependencies"],
                "optional": ["analyze_code_complexity", "get_code_patterns", "find_functions"],
                "keywords": ["code", "function", "class", "pattern", "architecture", "complexity", "quality"]
            },
            "structure_analysis": {
                "description": "Project structure and organization",
                "essential": ["get_file_structure", "get_directory_tree", "analyze_project_structure"],
                "optional": ["get_repository_overview"],
                "keywords": ["structure", "organization", "layout", "files", "directories", "folders"]
            },
            "history_analysis": {
                "description": "Development history and patterns",
                "essential": ["get_recent_commits", "get_commit_statistics", "get_development_patterns"],
                "optional": ["get_commit_details"],
                "keywords": ["history", "commits", "changes", "timeline", "development", "activity", "recent"]
            },
            "dependency_analysis": {
                "description": "Dependencies and requirements",
                "essential": ["search_dependencies", "get_readme_content"],
                "optional": ["get_file_structure"],
                "keywords": ["dependencies", "requirements", "packages", "libraries", "imports", "setup"]
            },
            "search_analysis": {
                "description": "Code search and discovery",
                "essential": ["search_code", "find_functions", "search_files"],
                "optional": ["get_code_patterns"],
                "keywords": ["search", "find", "locate", "discover", "pattern", "function", "method"]
            }
        }
        
        # Auto-detect analysis type if not specified
        if analysis_type == "auto":
            analysis_type = self._detect_analysis_type(question_lower, analysis_tool_sets)
        
        # Get the tool set for the detected analysis type
        if analysis_type in analysis_tool_sets:
            tool_set = analysis_tool_sets[analysis_type]
            selected_tools = tool_set["essential"].copy()
            
            # Add optional tools if they might be relevant
            for optional_tool in tool_set["optional"]:
                if self._is_tool_relevant(optional_tool, question_lower):
                    selected_tools.append(optional_tool)
            
            return selected_tools
        else:
            # Fallback to essential tools
            return ["get_readme_content", "get_file_structure", "get_repository_overview"]
    
    def _detect_analysis_type(self, question_lower: str, analysis_tool_sets: dict) -> str:
        """Detect the most appropriate analysis type based on question keywords"""
        best_match = "qa_chat"  # Default
        best_score = 0
        
        for analysis_type, config in analysis_tool_sets.items():
            score = 0
            for keyword in config["keywords"]:
                if keyword in question_lower:
                    score += 1
            
            # Weight by keyword relevance
            if score > best_score:
                best_score = score
                best_match = analysis_type
        
        return best_match
    
    def _is_tool_relevant(self, tool_name: str, question_lower: str) -> bool:
        """Check if a specific tool is relevant to the question"""
        tool_keywords = {
            "get_directory_tree": ["tree", "structure", "folders", "directories"],
            "get_recent_commits": ["recent", "latest", "commits", "changes"],
            "get_commit_statistics": ["statistics", "metrics", "activity", "trends"],
            "search_dependencies": ["dependencies", "packages", "requirements"],
            "analyze_code_complexity": ["complexity", "quality", "maintainability"],
            "get_code_patterns": ["patterns", "architecture", "design"],
            "find_functions": ["functions", "methods", "procedures"],
            "get_development_patterns": ["development", "workflow", "process"]
        }
        
        if tool_name in tool_keywords:
            return any(keyword in question_lower for keyword in tool_keywords[tool_name])
        
        return False
    
    def get_performance_insights(self) -> str:
        """Get human-readable performance insights"""
        stats = self.get_performance_stats()
        
        insights = []
        insights.append(f"🚀 **Performance Summary:**")
        insights.append(f"• Total tool calls: {stats['total_calls']}")
        insights.append(f"• Cache hit rate: {stats['cache_hit_rate']}")
        insights.append(f"• Average call time: {stats['average_call_time']}")
        
        if stats['slowest_tool']:
            insights.append(f"• Slowest tool: {stats['slowest_tool'][0]} ({stats['slowest_tool'][1]:.2f}s)")
        
        if stats['fastest_tool']:
            insights.append(f"• Fastest tool: {stats['fastest_tool'][0]} ({stats['fastest_tool'][1]:.2f}s)")
        
        # Performance recommendations
        if float(stats['average_call_time'].replace('s', '')) > 5.0:
            insights.append(f"⚠️ **Recommendation:** Consider reducing tool complexity or increasing cache usage")
        elif float(stats['average_call_time'].replace('s', '')) < 2.0:
            insights.append(f"✅ **Status:** Excellent performance! Tools are responding quickly")
        
        return "\n".join(insights)

class RepositoryAnalyzerAgent:
    """Enhanced Repository Analyzer Agent with comprehensive data gathering and analysis"""
    
    def __init__(self, model_name: str = "llama-3.1-70b-versatile"):
        self.model_name = model_name
        # Initialize tools with optimized settings
        self.tools = FastMCPTools(max_workers=12, timeout=60)  # Increased workers, reduced timeout
        
        # Initialize memory and storage with proper error handling
        try:
            # Create Groq model without any extra parameters
            groq_model = Groq(id=model_name)
            
            # Create memory with proper error handling
            try:
                self.memory = Memory(
                    model=groq_model,
                    db=SqliteMemoryDb(table_name="repo_analyzer_memories", db_file="tmp/agent.db"),
                    delete_memories=True,
                    clear_memories=True,
                )
            except Exception as mem_error:
                print(f"Warning: Could not initialize memory: {mem_error}")
                self.memory = None
            
            # Create storage with proper error handling
            try:
                self.storage = SqliteStorage(table_name="repo_analyzer_sessions", db_file="tmp/agent.db")
            except Exception as storage_error:
                print(f"Warning: Could not initialize storage: {storage_error}")
                self.storage = None
            
            # Create the main agent with enhanced configuration
            try:
                self.agent = Agent(
                    model=groq_model,
                    memory=self.memory,
                    storage=self.storage,
                    tools=[]  # No tools needed as we use our own FastMCP tools
                )
            except Exception as agent_error:
                print(f"Warning: Could not initialize agent: {agent_error}")
                self.agent = None
            
        except Exception as e:
            print(f"Warning: Could not initialize Agno agent components: {e}")
            # Fallback: create minimal agent without memory/storage
            self.memory = None
            self.storage = None
            self.agent = None
    
    def _get_system_prompt(self) -> str:
        """Get comprehensive system prompt for repository analysis"""
        return """You are an expert GitHub repository analyzer with access to comprehensive tools for analyzing codebases.

Your capabilities include:
1. File Content Analysis: Read and analyze any file in the repository
2. Repository Structure Analysis: Understand the project organization and architecture
3. Commit History Analysis: Track development patterns and changes
4. Code Search and Analysis: Find patterns, functions, and code metrics
5. Dependency Analysis: Understand project dependencies and requirements

When analyzing repositories:
- Always use multiple tools to gather comprehensive data
- Provide detailed, actionable insights with specific examples
- Consider code quality, architecture, security, and maintainability
- Support your conclusions with specific evidence from the codebase
- Be thorough but concise in your analysis
- Structure your responses with clear sections and bullet points

For Q&A:
- Use all available tools to gather relevant context
- Provide specific answers with code examples when appropriate
- Consider the broader context of the repository
- Format responses with clear headings and organized information

For Summarization:
- Create comprehensive summaries covering all major aspects
- Include technical details, architecture insights, and key findings
- Highlight important patterns and potential areas of concern
- Use structured format with sections for Overview, Architecture, Code Quality, etc.

Always strive to provide the most accurate and helpful analysis possible with clear, well-structured responses."""
    
    def _gather_comprehensive_data(self, repo_url: str, status_callback=None, question: str = "") -> Dict[str, Any]:
        """Gather comprehensive data from all MCP servers with optimized parallel execution - ALL TOOLS VERSION"""
        if status_callback:
            status_callback("🔍 Gathering comprehensive repository data with all tools...")
        
        start_time = time.time()
        
        # Use optimized set of tools for comprehensive analysis (reduced from 15 to 10)
        all_tools = [
            "get_readme_content", "get_file_structure", "get_repository_overview",
            "get_directory_tree", "analyze_project_structure", "get_recent_commits",
            "get_commit_statistics", "search_dependencies", "search_code", "get_code_metrics"
        ]
        
        # Create comprehensive tool calls with optimized limits
        tool_calls = []
        tool_mapping = {
            "get_readme_content": ("file_content", "get_readme_content", {"repo_url": repo_url}),
            "get_file_structure": ("repository_structure", "get_file_structure", {"repo_url": repo_url}),
            "get_repository_overview": ("repository_structure", "get_repository_overview", {"repo_url": repo_url}),
            "get_directory_tree": ("repository_structure", "get_directory_tree", {"repo_url": repo_url, "max_depth": 3}),
            "analyze_project_structure": ("repository_structure", "analyze_project_structure", {"repo_url": repo_url}),
            "get_code_metrics": ("code_search", "get_code_metrics", {"repo_url": repo_url}),
            "get_recent_commits": ("commit_history", "get_recent_commits", {"repo_url": repo_url, "limit": 15}),
            "get_commit_statistics": ("commit_history", "get_commit_statistics", {"repo_url": repo_url, "days": 30}),
            "search_dependencies": ("code_search", "search_dependencies", {"repo_url": repo_url}),
            "search_code": ("code_search", "search_code", {"repo_url": repo_url, "query": "def ", "language": "python"})
        }
        
        # Add all tools to batch
        for tool_name in all_tools:
            if tool_name in tool_mapping:
                tool_calls.append(tool_mapping[tool_name])
        
        if status_callback:
            status_callback(f"🚀 Executing {len(tool_calls)} optimized tools in parallel...")
        
        # Execute tools using optimized batch processing with increased workers
        tool_results = self.tools._batch_call_tools(tool_calls)
        
        # Organize results
        data = self._organize_comprehensive_results(tool_results)
        
        # Analyze key files in parallel
        if status_callback:
            status_callback("🔍 Analyzing key files in parallel...")
        data["code_analysis"]["key_files"] = self._analyze_key_files_parallel(repo_url)
        
        # Track tool utilization and performance
        data["tools_used"] = self.tools.get_tools_used()
        data["performance_stats"] = self.tools.get_performance_stats()
        data["execution_time"] = time.time() - start_time
        
        if status_callback:
            status_callback(f"✅ Comprehensive data gathering complete in {data['execution_time']:.2f}s using all tools")
        
        return data

    def _organize_comprehensive_results(self, tool_results: Dict[str, Any]) -> Dict[str, Any]:
        """Organize comprehensive tool results into structured data"""
        return {
            "file_structure": {
                "directory_tree": tool_results.get("repository_structure.get_directory_tree", {}),
                "file_structure": tool_results.get("repository_structure.get_file_structure", {}),
                "project_analysis": tool_results.get("repository_structure.analyze_project_structure", {}),
                "overview": tool_results.get("repository_structure.get_repository_overview", {})
            },
            "repository_info": {
                "readme": tool_results.get("file_content.get_readme_content", {}),
                "file_analysis": tool_results.get("file_content.analyze_file_content", {})
            },
            "code_metrics": {
                "metrics": tool_results.get("code_search.get_code_metrics", {}),
                "complexity": tool_results.get("code_search.analyze_code_complexity", {}),
                "patterns": tool_results.get("code_search.get_code_patterns", {}),
                "code_search": tool_results.get("code_search.search_code", {}),
                "functions": tool_results.get("code_search.find_functions", {})
            },
            "commit_history": {
                "recent_commits": tool_results.get("commit_history.get_recent_commits", {}),
                "statistics": tool_results.get("commit_history.get_commit_statistics", {}),
                "patterns": tool_results.get("commit_history.get_development_patterns", {})
            },
            "dependencies": {
                "dependency_files": tool_results.get("code_search.search_dependencies", {})
            },
            "code_analysis": {}
        }
    
    def _analyze_key_files(self, repo_url: str) -> Dict[str, Any]:
        """Analyze key files in the repository"""
        key_files = ["main.py", "app.py", "index.js", "package.json", "requirements.txt", "setup.py"]
        key_files_data = {}
        
        for file_name in key_files:
            try:
                file_content = json.loads(self.tools.get_file_content(repo_url, file_name))
                if file_content.get("success", False):
                    key_files_data[file_name] = file_content
            except:
                continue
        
        return key_files_data
    
    def _analyze_key_files_parallel(self, repo_url: str) -> Dict[str, Any]:
        """Analyze key files in parallel for better performance"""
        key_files = ["main.py", "app.py", "index.js", "package.json", "requirements.txt", "setup.py"]
        
        # Create parallel tool calls for key files
        tool_calls = []
        for file_name in key_files:
            tool_calls.append(("file_content", "get_file_content", {"repo_url": repo_url, "file_path": file_name}))
        
        # Execute in parallel
        results = self.tools._batch_call_tools(tool_calls)
        
        # Organize results
        key_files_data = {}
        for file_name in key_files:
            result_key = f"file_content.get_file_content"
            if result_key in results and results[result_key].get("success", False):
                key_files_data[file_name] = results[result_key]
        
        return key_files_data
    
    def ask_question(self, question: str, repo_url: str, user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
        """Ask a comprehensive question about the repository using optimized data gathering"""
        
        if status_callback:
            status_callback("🤖 Preparing optimized analysis...")
        
        try:
            import signal
            import threading
            import time
            
            # Set a timeout for the entire operation
            timeout_seconds = 60  # 1 minute timeout
            
            # Create a timeout handler
            def timeout_handler():
                raise TimeoutError("Analysis timed out after 60 seconds")
            
            # Set up timeout
            timer = threading.Timer(timeout_seconds, timeout_handler)
            timer.start()
            
            try:
                # Gather data using intelligent tool selection based on the question
                comprehensive_data = self._gather_comprehensive_data(repo_url, status_callback, question)
                
                if status_callback:
                    status_callback("🧠 AI agent analyzing your question...")
                
                # Create comprehensive prompt with all gathered data
                prompt = self._create_comprehensive_prompt(question, comprehensive_data)
                
                # Get AI response with system prompt
                system_prompt = self._get_system_prompt()
                
                if self.agent is None:
                    # Fallback: use direct Groq API call with timeout
                    try:
                        from agno.models.groq import Groq
                        groq_model = Groq(id=self.model_name)
                        response = groq_model.complete(f"{system_prompt}\n\n{prompt}")
                        timer.cancel()
                        return response.content, comprehensive_data["tools_used"]
                    except Exception as fallback_error:
                        error_msg = f"Error during analysis (fallback failed): {str(fallback_error)}"
                        if status_callback:
                            status_callback(f"❌ {error_msg}")
                        timer.cancel()
                        return error_msg, []
                else:
                    try:
                        response = self.agent.run(f"{system_prompt}\n\n{prompt}")
                        timer.cancel()
                        return response.content, comprehensive_data["tools_used"]
                    except Exception as agent_error:
                        # Try fallback if agent fails
                        try:
                            from agno.models.groq import Groq
                            groq_model = Groq(id=self.model_name)
                            response = groq_model.complete(f"{system_prompt}\n\n{prompt}")
                            timer.cancel()
                            return response.content, comprehensive_data["tools_used"]
                        except Exception as fallback_error:
                            error_msg = f"Error during analysis (agent and fallback failed): {str(fallback_error)}"
                            if status_callback:
                                status_callback(f"❌ {error_msg}")
                            timer.cancel()
                            return error_msg, []
                
                if status_callback:
                    execution_time = comprehensive_data.get("execution_time", 0)
                    status_callback(f"✅ Analysis complete! (Data gathering: {execution_time:.2f}s)")
                
            except TimeoutError:
                timer.cancel()
                error_msg = "Analysis timed out. Please try a simpler question or use the Ultra Fast mode."
                if status_callback:
                    status_callback(f"⏰ {error_msg}")
                return error_msg, []
            except Exception as e:
                timer.cancel()
                error_msg = f"Error during analysis: {str(e)}"
                if status_callback:
                    status_callback(f"❌ {error_msg}")
                return error_msg, []
                
        except Exception as e:
            error_msg = f"Error during analysis: {str(e)}"
            if status_callback:
                status_callback(f"❌ {error_msg}")
            return error_msg, []
    
    def generate_summary(self, repo_url: str, user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
        """Generate comprehensive repository summary using all available data"""
        
        if status_callback:
            status_callback("📊 Generating comprehensive summary...")
        
        try:
            # Gather comprehensive data
            comprehensive_data = self._gather_comprehensive_data(repo_url, status_callback)
            
            if status_callback:
                status_callback("🤖 AI agent creating summary...")
            
            # Create summary prompt
            summary_prompt = self._create_summary_prompt(comprehensive_data)
            
            # Get AI response with system prompt
            system_prompt = self._get_system_prompt()
            
            if self.agent is None:
                # Fallback: use direct Groq API call
                try:
                    from agno.models.groq import Groq
                    groq_model = Groq(id=self.model_name)
                    response = groq_model.complete(f"{system_prompt}\n\n{summary_prompt}")
                    return response.content, comprehensive_data["tools_used"]
                except Exception as fallback_error:
                    error_msg = f"Error generating summary (fallback failed): {str(fallback_error)}"
                    if status_callback:
                        status_callback(f"❌ {error_msg}")
                    return error_msg, []
            else:
                try:
                    response = self.agent.run(f"{system_prompt}\n\n{summary_prompt}")
                    return response.content, comprehensive_data["tools_used"]
                except Exception as agent_error:
                    # Try fallback if agent fails
                    try:
                        from agno.models.groq import Groq
                        groq_model = Groq(id=self.model_name)
                        response = groq_model.complete(f"{system_prompt}\n\n{summary_prompt}")
                        return response.content, comprehensive_data["tools_used"]
                    except Exception as fallback_error:
                        error_msg = f"Error generating summary (agent and fallback failed): {str(fallback_error)}"
                        if status_callback:
                            status_callback(f"❌ {error_msg}")
                        return error_msg, []
            
            if status_callback:
                status_callback("✅ Summary complete!")
            
            return response.content, comprehensive_data["tools_used"]
            
        except Exception as e:
            error_msg = f"Error generating summary: {str(e)}"
            if status_callback:
                status_callback(f"❌ {error_msg}")
            return error_msg, []
    
    def analyze_code_patterns(self, repo_url: str, user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
        """Analyze code patterns and architecture using comprehensive data"""
        
        if status_callback:
            status_callback("🔍 Analyzing code patterns and architecture...")
        
        try:
            # Gather comprehensive data
            comprehensive_data = self._gather_comprehensive_data(repo_url, status_callback)
            
            if status_callback:
                status_callback("🤖 AI agent analyzing patterns...")
            
            # Create pattern analysis prompt
            pattern_prompt = self._create_pattern_analysis_prompt(comprehensive_data)
            
            # Get AI response with system prompt
            system_prompt = self._get_system_prompt()
            
            if self.agent is None:
                # Fallback: use direct Groq API call
                try:
                    from agno.models.groq import Groq
                    groq_model = Groq(id=self.model_name)
                    response = groq_model.complete(f"{system_prompt}\n\n{pattern_prompt}")
                    return response.content, comprehensive_data["tools_used"]
                except Exception as fallback_error:
                    error_msg = f"Error analyzing patterns (fallback failed): {str(fallback_error)}"
                    if status_callback:
                        status_callback(f"❌ {error_msg}")
                    return error_msg, []
            else:
                try:
                    response = self.agent.run(f"{system_prompt}\n\n{pattern_prompt}")
                    return response.content, comprehensive_data["tools_used"]
                except Exception as agent_error:
                    # Try fallback if agent fails
                    try:
                        from agno.models.groq import Groq
                        groq_model = Groq(id=self.model_name)
                        response = groq_model.complete(f"{system_prompt}\n\n{pattern_prompt}")
                        return response.content, comprehensive_data["tools_used"]
                    except Exception as fallback_error:
                        error_msg = f"Error analyzing patterns (agent and fallback failed): {str(fallback_error)}"
                        if status_callback:
                            status_callback(f"❌ {error_msg}")
                        return error_msg, []
            
            if status_callback:
                status_callback("✅ Pattern analysis complete!")
            
            return response.content, comprehensive_data["tools_used"]
            
        except Exception as e:
            error_msg = f"Error analyzing patterns: {str(e)}"
            if status_callback:
                status_callback(f"❌ {error_msg}")
            return error_msg, []
    
    def quick_analysis(self, repo_url: str, user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
        """Perform quick but comprehensive repository analysis with optimized parallel execution"""
        
        if status_callback:
            status_callback("⚡ Performing optimized quick analysis...")
        
        try:
            start_time = time.time()
            
            # Use batch processing for essential tools
            tool_calls = [
                ("file_content", "get_readme_content", {"repo_url": repo_url}),
                ("repository_structure", "get_file_structure", {"repo_url": repo_url}),
                ("repository_structure", "get_repository_overview", {"repo_url": repo_url}),
                ("commit_history", "get_recent_commits", {"repo_url": repo_url, "limit": 10})
            ]
            
            if status_callback:
                status_callback("📁 Gathering essential data in parallel...")
            
            # Execute all tools in parallel
            results = self.tools._batch_call_tools(tool_calls)
            
            # Organize results
            data = {
                "readme": results.get("file_content.get_readme_content", {}),
                "structure": results.get("repository_structure.get_file_structure", {}),
                "overview": results.get("repository_structure.get_repository_overview", {}),
                "recent_commits": results.get("commit_history.get_recent_commits", {})
            }
            
            if status_callback:
                status_callback("🤖 AI agent creating quick overview...")
            
            # Create quick analysis prompt
            quick_prompt = self._create_quick_analysis_prompt(data)
            
            # Get AI response with system prompt
            system_prompt = self._get_system_prompt()
            
            if self.agent is None:
                # Fallback: use direct Groq API call
                try:
                    from agno.models.groq import Groq
                    groq_model = Groq(id=self.model_name)
                    response = groq_model.complete(f"{system_prompt}\n\n{quick_prompt}")
                    return response.content, self.tools.get_tools_used()
                except Exception as fallback_error:
                    error_msg = f"Error in quick analysis (fallback failed): {str(fallback_error)}"
                    if status_callback:
                        status_callback(f"❌ {error_msg}")
                    return error_msg, []
            else:
                try:
                    response = self.agent.run(f"{system_prompt}\n\n{quick_prompt}")
                    return response.content, self.tools.get_tools_used()
                except Exception as agent_error:
                    # Try fallback if agent fails
                    try:
                        from agno.models.groq import Groq
                        groq_model = Groq(id=self.model_name)
                        response = groq_model.complete(f"{system_prompt}\n\n{quick_prompt}")
                        return response.content, self.tools.get_tools_used()
                    except Exception as fallback_error:
                        error_msg = f"Error in quick analysis (agent and fallback failed): {str(fallback_error)}"
                        if status_callback:
                            status_callback(f"❌ {error_msg}")
                        return error_msg, []
            
            execution_time = time.time() - start_time
            if status_callback:
                status_callback(f"✅ Quick analysis complete! (Total time: {execution_time:.2f}s)")
            
            return response.content, self.tools.get_tools_used()
            
        except Exception as e:
            error_msg = f"Error in quick analysis: {str(e)}"
            if status_callback:
                status_callback(f"❌ {error_msg}")
            return error_msg, []
    
    def get_tools_used(self) -> List[str]:
        """Get list of tools used in this session"""
        return self.tools.get_tools_used()
    
    def get_servers_used(self) -> List[str]:
        """Get list of servers used in this session"""
        return self.tools.get_servers_used()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return self.tools.get_performance_stats()
    
    def get_performance_insights(self) -> str:
        """Get human-readable performance insights"""
        return self.tools.get_performance_insights()
    
    def clear_cache(self):
        """Clear the tool cache"""
        self.tools.clear_cache()

    def _create_comprehensive_prompt(self, question: str, data: Dict[str, Any]) -> str:
        """Create comprehensive prompt for Q&A with enhanced structure"""
        return f"""Based on the following comprehensive repository data, please answer this question: "{question}"

Repository Data:
{json.dumps(data, indent=2)}

Please provide a detailed, accurate answer based on the available data. Structure your response with:

## Answer
[Your main answer to the question]

## Key Findings
- [Specific findings from the codebase]
- [Relevant patterns or insights]

## Technical Details
- [Code structure and architecture details]
- [Development patterns and history]
- [Dependencies and requirements]
- [Code quality and complexity metrics]

## Evidence
- [Specific examples from the codebase]
- [File references and code snippets when relevant]

## Recommendations
- [Any actionable insights or suggestions]

Use specific examples from the codebase when relevant. Consider code structure, architecture, development patterns, dependencies, and code quality."""
    
    def _create_summary_prompt(self, data: Dict[str, Any]) -> str:
        """Create comprehensive summary prompt with enhanced structure"""
        return f"""Based on the following comprehensive repository data, create a detailed summary covering all major aspects of the repository.

Repository Data:
{json.dumps(data, indent=2)}

Please structure your response with the following sections:

## 📋 Project Overview
- **Purpose**: What does this project do?
- **Main Technologies**: Key languages, frameworks, and tools
- **Target Audience**: Who is this project for?

## 🏗️ Architecture & Structure
- **Project Organization**: How is the codebase structured?
- **Key Components**: Main modules and their responsibilities
- **Design Patterns**: Architectural patterns used
- **File Organization**: How files are organized

## 📊 Code Quality & Metrics
- **Code Complexity**: Cyclomatic complexity and maintainability
- **Code Coverage**: Testing approach and coverage
- **Code Standards**: Coding conventions and style
- **Documentation**: Quality and completeness of docs

## 🔄 Development Patterns
- **Commit History**: Development activity and patterns
- **Branching Strategy**: Git workflow and branching
- **Release Process**: How releases are managed
- **Contributor Activity**: Team size and contribution patterns

## 📦 Dependencies & Requirements
- **Core Dependencies**: Main libraries and frameworks
- **Development Dependencies**: Tools for development
- **Version Management**: How dependencies are managed
- **Security**: Known vulnerabilities or security considerations

## 🚀 Key Features & Components
- **Core Functionality**: Main features and capabilities
- **Notable Components**: Standout parts of the codebase
- **Integration Points**: APIs, services, and external connections
- **Performance Considerations**: Optimization and scalability

## ⚠️ Areas of Interest & Concerns
- **Potential Issues**: Code quality or architectural concerns
- **Technical Debt**: Areas needing refactoring
- **Scalability**: Growth and scaling considerations
- **Maintenance**: Long-term maintainability factors

## 💡 Recommendations
- **Improvements**: Suggested enhancements
- **Best Practices**: Recommendations for development
- **Future Considerations**: Long-term planning suggestions

Provide specific examples and evidence from the codebase to support your analysis. Make this summary comprehensive and actionable for developers, maintainers, and stakeholders."""
    
    def _create_pattern_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Create pattern analysis prompt with enhanced structure"""
        return f"""Analyze the following repository data to identify code patterns, architecture decisions, and development practices:

Repository Data:
{json.dumps(data, indent=2)}

Please structure your analysis with the following sections:

## 🏛️ Code Architecture Patterns
- **Overall Architecture**: High-level architectural approach
- **Module Organization**: How code is modularized
- **Separation of Concerns**: How responsibilities are divided
- **Layered Architecture**: Any layering patterns used

## 🎨 Design Patterns
- **Creational Patterns**: Factory, Singleton, Builder patterns
- **Structural Patterns**: Adapter, Decorator, Facade patterns
- **Behavioral Patterns**: Observer, Strategy, Command patterns
- **Domain-Specific Patterns**: Custom patterns for this project

## 📁 Code Organization & Structure
- **File Structure**: How files are organized
- **Naming Conventions**: File and function naming patterns
- **Directory Organization**: Folder structure and purpose
- **Import Patterns**: How modules are imported and used

## 🔄 Development Workflow Patterns
- **Git Workflow**: Branching and merging patterns
- **Commit Patterns**: Commit message conventions
- **Release Patterns**: How releases are managed
- **Testing Patterns**: Testing approach and coverage

## 📊 Code Quality Patterns
- **Error Handling**: How errors are managed
- **Logging Patterns**: Logging and debugging approaches
- **Documentation Patterns**: Code documentation style
- **Performance Patterns**: Optimization techniques used

## ⚠️ Potential Architectural Issues
- **Code Smells**: Anti-patterns or problematic code
- **Technical Debt**: Areas needing refactoring
- **Scalability Concerns**: Potential scaling issues
- **Maintainability Issues**: Hard-to-maintain code areas

## 💡 Recommendations for Improvement
- **Architecture Improvements**: Suggested architectural changes
- **Code Quality Enhancements**: Ways to improve code quality
- **Performance Optimizations**: Suggested performance improvements
- **Best Practices**: Recommendations for better practices

Provide specific examples and evidence from the codebase to support your analysis. Include code snippets and file references when relevant."""
    
    def _create_quick_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Create quick analysis prompt with enhanced structure"""
        return f"""Based on the following repository data, provide a concise but comprehensive overview:

Repository Data:
{json.dumps(data, indent=2)}

Please structure your response with:

## 🚀 Quick Overview
- **Project Purpose**: What this project does in 1-2 sentences
- **Main Technologies**: Key languages, frameworks, and tools
- **Project Scale**: Size and complexity indicators

## 🏗️ Architecture Highlights
- **Structure**: Main organizational approach
- **Key Components**: Most important modules/files
- **Design Patterns**: Notable architectural patterns

## 📊 Key Insights
- **Code Quality**: Overall code quality indicators
- **Development Activity**: Recent activity and patterns
- **Notable Features**: Standout aspects of the codebase

## 💡 Quick Recommendations
- **Strengths**: What the project does well
- **Areas for Attention**: Potential concerns or improvements

Keep it concise but informative, focusing on the most important aspects for a quick understanding."""

    def ask_question_fast(self, question: str, repo_url: str, user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
        """Ask a question with optimized fast mode using minimal tools for quick responses"""
        
        if status_callback:
            status_callback("⚡ Fast mode: Gathering essential data...")
        
        try:
            import signal
            import threading
            import time
            
            # Set a shorter timeout for fast mode
            timeout_seconds = 30  # 30 seconds timeout for fast mode
            
            # Create a timeout handler
            def timeout_handler():
                raise TimeoutError("Fast analysis timed out after 30 seconds")
            
            # Set up timeout
            timer = threading.Timer(timeout_seconds, timeout_handler)
            timer.start()
            
            try:
                # Use only essential tools for fast mode
                essential_tools = [
                    ("file_content", "get_readme_content", {"repo_url": repo_url}),
                    ("repository_structure", "get_file_structure", {"repo_url": repo_url}),
                    ("repository_structure", "get_repository_overview", {"repo_url": repo_url})
                ]
                
                if status_callback:
                    status_callback("📁 Executing essential tools in parallel...")
                
                # Execute only essential tools
                tool_results = self.tools._batch_call_tools(essential_tools)
                
                # Organize minimal data
                data = {
                    "readme": tool_results.get("file_content.get_readme_content", {}),
                    "structure": tool_results.get("repository_structure.get_file_structure", {}),
                    "overview": tool_results.get("repository_structure.get_repository_overview", {})
                }
                
                if status_callback:
                    status_callback("🧠 AI agent analyzing with fast mode...")
                
                # Create optimized prompt for fast mode
                prompt = self._create_fast_prompt(question, data)
                
                # Get AI response with system prompt
                system_prompt = self._get_system_prompt()
                
                if self.agent is None:
                    # Fallback: use direct Groq API call with timeout
                    try:
                        from agno.models.groq import Groq
                        groq_model = Groq(id=self.model_name)
                        response = groq_model.complete(f"{system_prompt}\n\n{prompt}")
                        timer.cancel()
                        return response.content, self.tools.get_tools_used()
                    except Exception as fallback_error:
                        error_msg = f"Error during fast analysis (fallback failed): {str(fallback_error)}"
                        if status_callback:
                            status_callback(f"❌ {error_msg}")
                        timer.cancel()
                        return error_msg, []
                else:
                    try:
                        response = self.agent.run(f"{system_prompt}\n\n{prompt}")
                        timer.cancel()
                        return response.content, self.tools.get_tools_used()
                    except Exception as agent_error:
                        # Try fallback if agent fails
                        try:
                            from agno.models.groq import Groq
                            groq_model = Groq(id=self.model_name)
                            response = groq_model.complete(f"{system_prompt}\n\n{prompt}")
                            timer.cancel()
                            return response.content, self.tools.get_tools_used()
                        except Exception as fallback_error:
                            error_msg = f"Error during fast analysis (agent and fallback failed): {str(fallback_error)}"
                            if status_callback:
                                status_callback(f"❌ {error_msg}")
                            timer.cancel()
                            return error_msg, []
                
            except TimeoutError:
                timer.cancel()
                error_msg = "Fast analysis timed out. Please try a simpler question or use Standard mode for comprehensive analysis."
                if status_callback:
                    status_callback(f"⏰ {error_msg}")
                return error_msg, []
            except Exception as e:
                timer.cancel()
                error_msg = f"Error during fast analysis: {str(e)}"
                if status_callback:
                    status_callback(f"❌ {error_msg}")
                return error_msg, []
                
        except Exception as e:
            error_msg = f"Error during fast analysis: {str(e)}"
            if status_callback:
                status_callback(f"❌ {error_msg}")
            return error_msg, []

    def _create_fast_prompt(self, question: str, data: Dict[str, Any]) -> str:
        """Create optimized prompt for fast mode with minimal data"""
        return f"""Based on the following essential repository data, please answer this question: "{question}"

Repository Data:
{json.dumps(data, indent=2)}

Please provide a concise, accurate answer based on the available data. Structure your response with:

## Answer
[Your main answer to the question]

## Key Points
- [Essential findings from the codebase]
- [Main purpose and functionality]

## Technical Overview
- [Basic structure and architecture]
- [Key technologies and dependencies]

Keep your response focused and concise. If you need more detailed analysis, suggest using Standard mode for comprehensive analysis."""

    def ask_question_smart(self, question: str, repo_url: str, user_id: str = "default", status_callback=None, analysis_type: str = "auto") -> Tuple[str, List[str]]:
        """Ask a question with intelligent tool selection based on analysis type"""
        
        if status_callback:
            status_callback("🧠 Smart analysis: Detecting optimal tools...")
        
        try:
            import signal
            import threading
            import time
            
            # Set timeout based on analysis type
            timeout_seconds = 45 if analysis_type == "auto" else 60
            
            # Create a timeout handler
            def timeout_handler():
                raise TimeoutError(f"Smart analysis timed out after {timeout_seconds} seconds")
            
            # Set up timeout
            timer = threading.Timer(timeout_seconds, timeout_handler)
            timer.start()
            
            try:
                # Use intelligent tool selection
                selected_tools = self.tools.optimize_tool_selection(question, analysis_type)
                
                if status_callback:
                    status_callback(f"🎯 Using {len(selected_tools)} optimized tools for {analysis_type} analysis...")
                
                # Create tool calls based on selected tools
                tool_calls = []
                tool_mapping = {
                    "get_readme_content": ("file_content", "get_readme_content", {"repo_url": repo_url}),
                    "get_file_structure": ("repository_structure", "get_file_structure", {"repo_url": repo_url}),
                    "get_repository_overview": ("repository_structure", "get_repository_overview", {"repo_url": repo_url}),
                    "get_directory_tree": ("repository_structure", "get_directory_tree", {"repo_url": repo_url, "max_depth": 3}),
                    "analyze_project_structure": ("repository_structure", "analyze_project_structure", {"repo_url": repo_url}),
                    "get_code_metrics": ("code_search", "get_code_metrics", {"repo_url": repo_url}),
                    "get_recent_commits": ("commit_history", "get_recent_commits", {"repo_url": repo_url, "limit": 15}),
                    "get_commit_statistics": ("commit_history", "get_commit_statistics", {"repo_url": repo_url, "days": 30}),
                    "search_dependencies": ("code_search", "search_dependencies", {"repo_url": repo_url}),
                    "search_code": ("code_search", "search_code", {"repo_url": repo_url, "query": "def ", "language": "python"}),
                    "analyze_code_complexity": ("code_search", "analyze_code_complexity", {"repo_url": repo_url}),
                    "get_code_patterns": ("code_search", "get_code_patterns", {"repo_url": repo_url}),
                    "find_functions": ("code_search", "find_functions", {"repo_url": repo_url, "function_name": "main", "language": "python"}),
                    "get_development_patterns": ("commit_history", "get_development_patterns", {"repo_url": repo_url}),
                    "search_files": ("code_search", "search_files", {"repo_url": repo_url, "filename_pattern": "*.py"})
                }
                
                # Add selected tools to batch
                for tool_name in selected_tools:
                    if tool_name in tool_mapping:
                        tool_calls.append(tool_mapping[tool_name])
                
                if status_callback:
                    status_callback(f"🚀 Executing {len(tool_calls)} smart-selected tools...")
                
                # Execute tools using optimized batch processing
                tool_results = self.tools._batch_call_tools(tool_calls)
                
                # Organize results
                data = self._organize_smart_results(tool_results, selected_tools)
                
                if status_callback:
                    status_callback("🧠 AI agent analyzing with smart tool selection...")
                
                # Create smart prompt based on analysis type
                prompt = self._create_smart_prompt(question, data, analysis_type)
                
                # Get AI response with system prompt
                system_prompt = self._get_system_prompt()
                
                if self.agent is None:
                    # Fallback: use direct Groq API call with timeout
                    try:
                        from agno.models.groq import Groq
                        groq_model = Groq(id=self.model_name)
                        response = groq_model.complete(f"{system_prompt}\n\n{prompt}")
                        timer.cancel()
                        return response.content, selected_tools
                    except Exception as fallback_error:
                        error_msg = f"Error during smart analysis (fallback failed): {str(fallback_error)}"
                        if status_callback:
                            status_callback(f"❌ {error_msg}")
                        timer.cancel()
                        return error_msg, []
                else:
                    try:
                        response = self.agent.run(f"{system_prompt}\n\n{prompt}")
                        timer.cancel()
                        return response.content, selected_tools
                    except Exception as agent_error:
                        # Try fallback if agent fails
                        try:
                            from agno.models.groq import Groq
                            groq_model = Groq(id=self.model_name)
                            response = groq_model.complete(f"{system_prompt}\n\n{prompt}")
                            timer.cancel()
                            return response.content, selected_tools
                        except Exception as fallback_error:
                            error_msg = f"Error during smart analysis (agent and fallback failed): {str(fallback_error)}"
                            if status_callback:
                                status_callback(f"❌ {error_msg}")
                            timer.cancel()
                            return error_msg, []
                
            except TimeoutError:
                timer.cancel()
                error_msg = f"Smart analysis timed out. Try a simpler question or different analysis type."
                if status_callback:
                    status_callback(f"⏰ {error_msg}")
                return error_msg, []
            except Exception as e:
                timer.cancel()
                error_msg = f"Error during smart analysis: {str(e)}"
                if status_callback:
                    status_callback(f"❌ {error_msg}")
                return error_msg, []
                
        except Exception as e:
            error_msg = f"Error during smart analysis: {str(e)}"
            if status_callback:
                status_callback(f"❌ {error_msg}")
            return error_msg, []

    def generate_smart_summary(self, repo_url: str, user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
        """Generate repository summary using intelligent tool selection"""
        
        if status_callback:
            status_callback("📊 Smart summary: Selecting optimal tools...")
        
        try:
            # Use summarization-specific tools
            selected_tools = self.tools.optimize_tool_selection("summarize this repository", "summarization")
            
            if status_callback:
                status_callback(f"📋 Using {len(selected_tools)} tools for comprehensive summary...")
            
            # Create tool calls for summary
            tool_calls = []
            tool_mapping = {
                "get_readme_content": ("file_content", "get_readme_content", {"repo_url": repo_url}),
                "get_file_structure": ("repository_structure", "get_file_structure", {"repo_url": repo_url}),
                "get_repository_overview": ("repository_structure", "get_repository_overview", {"repo_url": repo_url}),
                "get_directory_tree": ("repository_structure", "get_directory_tree", {"repo_url": repo_url, "max_depth": 3}),
                "get_recent_commits": ("commit_history", "get_recent_commits", {"repo_url": repo_url, "limit": 15}),
                "get_commit_statistics": ("commit_history", "get_commit_statistics", {"repo_url": repo_url, "days": 30}),
                "search_dependencies": ("code_search", "search_dependencies", {"repo_url": repo_url})
            }
            
            # Add selected tools to batch
            for tool_name in selected_tools:
                if tool_name in tool_mapping:
                    tool_calls.append(tool_mapping[tool_name])
            
            # Execute tools
            tool_results = self.tools._batch_call_tools(tool_calls)
            
            # Organize results
            data = self._organize_smart_results(tool_results, selected_tools)
            
            if status_callback:
                status_callback("🤖 AI agent creating smart summary...")
            
            # Create summary prompt
            summary_prompt = self._create_summary_prompt(data)
            
            # Get AI response
            system_prompt = self._get_system_prompt()
            
            if self.agent is None:
                # Fallback: use direct Groq API call
                try:
                    from agno.models.groq import Groq
                    groq_model = Groq(id=self.model_name)
                    response = groq_model.complete(f"{system_prompt}\n\n{summary_prompt}")
                    return response.content, selected_tools
                except Exception as fallback_error:
                    error_msg = f"Error generating smart summary (fallback failed): {str(fallback_error)}"
                    if status_callback:
                        status_callback(f"❌ {error_msg}")
                    return error_msg, []
            else:
                try:
                    response = self.agent.run(f"{system_prompt}\n\n{summary_prompt}")
                    return response.content, selected_tools
                except Exception as agent_error:
                    # Try fallback if agent fails
                    try:
                        from agno.models.groq import Groq
                        groq_model = Groq(id=self.model_name)
                        response = groq_model.complete(f"{system_prompt}\n\n{summary_prompt}")
                        return response.content, selected_tools
                    except Exception as fallback_error:
                        error_msg = f"Error generating smart summary (agent and fallback failed): {str(fallback_error)}"
                        if status_callback:
                            status_callback(f"❌ {error_msg}")
                        return error_msg, []
            
        except Exception as e:
            error_msg = f"Error generating smart summary: {str(e)}"
            if status_callback:
                status_callback(f"❌ {error_msg}")
            return error_msg, []

    def generate_chart_data(self, repo_url: str, user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
        """Generate data suitable for charts and visualizations"""
        
        if status_callback:
            status_callback("📈 Chart data: Gathering metrics and statistics...")
        
        try:
            # Use chart-specific tools
            selected_tools = self.tools.optimize_tool_selection("generate chart data", "chart_generation")
            
            if status_callback:
                status_callback(f"📊 Using {len(selected_tools)} tools for chart data...")
            
            # Create tool calls for chart data
            tool_calls = []
            tool_mapping = {
                "get_commit_statistics": ("commit_history", "get_commit_statistics", {"repo_url": repo_url, "days": 90}),
                "get_code_metrics": ("code_search", "get_code_metrics", {"repo_url": repo_url}),
                "get_recent_commits": ("commit_history", "get_recent_commits", {"repo_url": repo_url, "limit": 50}),
                "get_development_patterns": ("commit_history", "get_development_patterns", {"repo_url": repo_url}),
                "analyze_code_complexity": ("code_search", "analyze_code_complexity", {"repo_url": repo_url})
            }
            
            # Add selected tools to batch
            for tool_name in selected_tools:
                if tool_name in tool_mapping:
                    tool_calls.append(tool_mapping[tool_name])
            
            # Execute tools
            tool_results = self.tools._batch_call_tools(tool_calls)
            
            # Organize results
            data = self._organize_smart_results(tool_results, selected_tools)
            
            if status_callback:
                status_callback("🤖 AI agent creating chart data...")
            
            # Create chart data prompt
            chart_prompt = self._create_chart_data_prompt(data)
            
            # Get AI response
            system_prompt = self._get_system_prompt()
            
            if self.agent is None:
                # Fallback: use direct Groq API call
                try:
                    from agno.models.groq import Groq
                    groq_model = Groq(id=self.model_name)
                    response = groq_model.complete(f"{system_prompt}\n\n{chart_prompt}")
                    return response.content, selected_tools
                except Exception as fallback_error:
                    error_msg = f"Error generating chart data (fallback failed): {str(fallback_error)}"
                    if status_callback:
                        status_callback(f"❌ {error_msg}")
                    return error_msg, []
            else:
                try:
                    response = self.agent.run(f"{system_prompt}\n\n{chart_prompt}")
                    return response.content, selected_tools
                except Exception as agent_error:
                    # Try fallback if agent fails
                    try:
                        from agno.models.groq import Groq
                        groq_model = Groq(id=self.model_name)
                        response = groq_model.complete(f"{system_prompt}\n\n{chart_prompt}")
                        return response.content, selected_tools
                    except Exception as fallback_error:
                        error_msg = f"Error generating chart data (agent and fallback failed): {str(fallback_error)}"
                        if status_callback:
                            status_callback(f"❌ {error_msg}")
                        return error_msg, []
            
        except Exception as e:
            error_msg = f"Error generating chart data: {str(e)}"
            if status_callback:
                status_callback(f"❌ {error_msg}")
            return error_msg, []

    def _organize_smart_results(self, tool_results: Dict[str, Any], selected_tools: List[str]) -> Dict[str, Any]:
        """Organize smart tool results into structured data"""
        data = {
            "file_structure": {},
            "repository_info": {},
            "code_metrics": {},
            "commit_history": {},
            "dependencies": {},
            "code_analysis": {},
            "selected_tools": selected_tools,
            "tool_count": len(selected_tools)
        }
        
        # Map tool results to data structure
        tool_mapping = {
            "get_readme_content": ("repository_info", "readme"),
            "get_file_structure": ("file_structure", "file_structure"),
            "get_repository_overview": ("repository_info", "overview"),
            "get_directory_tree": ("file_structure", "directory_tree"),
            "analyze_project_structure": ("file_structure", "project_analysis"),
            "get_code_metrics": ("code_metrics", "metrics"),
            "get_recent_commits": ("commit_history", "recent_commits"),
            "get_commit_statistics": ("commit_history", "statistics"),
            "search_dependencies": ("dependencies", "dependency_files"),
            "search_code": ("code_metrics", "code_search"),
            "analyze_code_complexity": ("code_metrics", "complexity"),
            "get_code_patterns": ("code_metrics", "patterns"),
            "find_functions": ("code_metrics", "functions"),
            "get_development_patterns": ("commit_history", "patterns"),
            "search_files": ("code_metrics", "file_search")
        }
        
        for tool_name in selected_tools:
            if tool_name in tool_mapping:
                category, key = tool_mapping[tool_name]
                result_key = f"{self._get_server_name(tool_name)}.{tool_name}"
                if result_key in tool_results:
                    data[category][key] = tool_results[result_key]
        
        return data
    
    def _get_server_name(self, tool_name: str) -> str:
        """Get the server name for a given tool"""
        server_mapping = {
            "get_readme_content": "file_content",
            "analyze_file_content": "file_content",
            "get_file_content": "file_content",
            "get_file_structure": "repository_structure",
            "get_repository_overview": "repository_structure",
            "get_directory_tree": "repository_structure",
            "analyze_project_structure": "repository_structure",
            "get_recent_commits": "commit_history",
            "get_commit_statistics": "commit_history",
            "get_development_patterns": "commit_history",
            "get_commit_details": "commit_history",
            "search_code": "code_search",
            "search_files": "code_search",
            "find_functions": "code_search",
            "get_code_metrics": "code_search",
            "search_dependencies": "code_search",
            "analyze_code_complexity": "code_search",
            "get_code_patterns": "code_search"
        }
        return server_mapping.get(tool_name, "unknown")
    
    def _create_smart_prompt(self, question: str, data: Dict[str, Any], analysis_type: str) -> str:
        """Create smart prompt based on analysis type"""
        analysis_descriptions = {
            "qa_chat": "Q&A analysis with focused tools",
            "summarization": "Comprehensive repository summary",
            "chart_generation": "Data for charts and visualizations",
            "quick_analysis": "Fast overview with minimal tools",
            "code_analysis": "Deep code analysis and patterns",
            "structure_analysis": "Project structure and organization",
            "history_analysis": "Development history and patterns",
            "dependency_analysis": "Dependencies and requirements",
            "search_analysis": "Code search and discovery"
        }
        
        description = analysis_descriptions.get(analysis_type, "General analysis")
        
        return f"""Based on the following repository data gathered using {description} ({data['tool_count']} optimized tools), please answer this question: "{question}"

Repository Data:
{json.dumps(data, indent=2)}

Please provide a focused, accurate answer based on the available data. Structure your response appropriately for {analysis_type} analysis.

## Answer
[Your main answer to the question]

## Key Insights
- [Relevant findings from the selected tools]
- [Important patterns or observations]

## Technical Details
- [Specific technical information relevant to the question]
- [Code examples or data points when applicable]

## Analysis Type: {analysis_type}
This analysis used {data['tool_count']} optimized tools: {', '.join(data['selected_tools'])}"""
    
    def _create_chart_data_prompt(self, data: Dict[str, Any]) -> str:
        """Create prompt for generating chart data"""
        return f"""Based on the following repository data, create structured data suitable for charts and visualizations:

Repository Data:
{json.dumps(data, indent=2)}

Please provide:

## 📊 Chart-Ready Data
- **Commit Activity**: Time series data for commit frequency
- **Code Metrics**: Language distribution, file counts, complexity metrics
- **Development Patterns**: Activity trends, contributor patterns
- **Dependencies**: Package usage and version information

## 📈 Visualization Suggestions
- Recommended chart types for each dataset
- Key insights that can be visualized
- Time periods and granularity suggestions

## 🔍 Data Insights
- Notable trends and patterns
- Anomalies or interesting data points
- Recommendations for further analysis

Format the data in a way that can be easily converted to charts and graphs."""

# Global agent instance
_analyzer_agent = None

def create_analyzer_agent(model_name: str = "llama-3.1-70b-versatile") -> RepositoryAnalyzerAgent:
    """Create or get the global analyzer agent"""
    global _analyzer_agent
    if _analyzer_agent is None:
        _analyzer_agent = RepositoryAnalyzerAgent(model_name)
    return _analyzer_agent

def ask_repository_question(question: str, repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None, speed_mode: str = "standard") -> Tuple[str, List[str]]:
    """Ask a question about a repository using the AI agent with speed mode support"""
    agent = create_analyzer_agent(model_name)
    
    if speed_mode == "fast":
        return agent.ask_question_fast(question, repo_url, user_id, status_callback)
    else:
        return agent.ask_question(question, repo_url, user_id, status_callback)

def generate_repository_summary(repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
    """Generate comprehensive repository summary"""
    agent = create_analyzer_agent(model_name)
    return agent.generate_summary(repo_url, user_id, status_callback)

def analyze_repository_patterns(repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
    """Analyze repository patterns and architecture"""
    agent = create_analyzer_agent(model_name)
    return agent.analyze_code_patterns(repo_url, user_id, status_callback)

def get_repository_overview(repo_url: str) -> str:
    """Get basic repository overview"""
    try:
        tools = FastMCPTools()
        overview = tools.get_repository_overview(repo_url)
        return overview
    except Exception as e:
        return f"Error getting repository overview: {str(e)}"

def quick_repository_analysis(repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
    """Perform quick repository analysis"""
    agent = create_analyzer_agent(model_name)
    return agent.quick_analysis(repo_url, user_id, status_callback)

# Legacy function aliases for compatibility
def ask_question(question: str, repository_url: str) -> tuple[str, list[str]]:
    """Legacy alias for ask_repository_question"""
    return ask_repository_question(question, repository_url)

def analyze_repository(repository_url: str) -> tuple[str, list[str]]:
    """Legacy alias for analyze_repository_patterns"""
    return analyze_repository_patterns(repository_url)

def search_repository_code(repository_url: str, search_query: str) -> str:
    """Search repository code using MCP tools"""
    try:
        tools = FastMCPTools()
        result = tools.search_code(repository_url, search_query)
        return result
    except Exception as e:
        return f"Error searching code: {str(e)}"

def analyze_repository_structure(repository_url: str) -> str:
    """Analyze repository structure using MCP tools"""
    try:
        tools = FastMCPTools()
        structure = tools.analyze_project_structure(repository_url)
        return structure
    except Exception as e:
        return f"Error analyzing structure: {str(e)}"

def get_recent_activity(repository_url: str) -> str:
    """Get recent repository activity using MCP tools"""
    try:
        tools = FastMCPTools()
        activity = tools.get_recent_commits(repository_url, limit=20)
        return activity
    except Exception as e:
        return f"Error getting recent activity: {str(e)}"

def ask_repository_question_smart(question: str, repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None, analysis_type: str = "auto") -> Tuple[str, List[str]]:
    """Ask a question about a repository using intelligent tool selection"""
    agent = create_analyzer_agent(model_name)
    return agent.ask_question_smart(question, repo_url, user_id, status_callback, analysis_type)

def generate_smart_repository_summary(repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
    """Generate repository summary using intelligent tool selection"""
    agent = create_analyzer_agent(model_name)
    return agent.generate_smart_summary(repo_url, user_id, status_callback)

def generate_repository_chart_data(repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
    """Generate chart data for repository visualizations"""
    agent = create_analyzer_agent(model_name)
    return agent.generate_chart_data(repo_url, user_id, status_callback)