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
from agno.tools.reasoning import ReasoningTools
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from fastmcp import Client
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import functools

class FastMCPTools:
    """Enhanced tools wrapper for all FastMCP v2 servers with comprehensive data gathering and optimized performance"""
    
    def __init__(self, max_workers: int = 8, timeout: int = 30):
        self.servers = {
            "file_content": "src/servers/file_content_server.py",
            "repository_structure": "src/servers/repository_structure_server.py", 
            "commit_history": "src/servers/commit_history_server.py",
            "code_search": "src/servers/code_search_server.py"
        }
        self.tools_used = []
        self.servers_used = []
        self.cache = {}
        self.max_workers = max_workers
        self.timeout = timeout
        self._client_pool = {}
        self._pool_lock = threading.Lock()
        
        # Performance tracking
        self.call_times = {}
        self.total_calls = 0
        self.cache_hits = 0
    
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
                    self._client_pool[server_name] = Client(script_path)
                client = self._client_pool[server_name]
            
            # Add timeout to prevent hanging
            try:
                result = await asyncio.wait_for(
                    client.call_tool(tool_name, kwargs), 
                    timeout=self.timeout
                )
                
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
                
                self.cache[cache_key] = response
                self.call_times[f"{server_name}.{tool_name}"] = time.time() - start_time
                return response
                
            except asyncio.TimeoutError:
                return {
                    "error": f"Timeout after {self.timeout} seconds", 
                    "success": False, 
                    "server": server_name, 
                    "tool": tool_name,
                    "execution_time": time.time() - start_time
                }
                
        except Exception as e:
            return {
                "error": str(e), 
                "success": False, 
                "server": server_name, 
                "tool": tool_name,
                "execution_time": time.time() - start_time
            }
    
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
        """Execute multiple tool calls in parallel with optimized batching"""
        results = {}
        
        # Group tools by server for better connection reuse
        server_groups = {}
        for server_name, tool_name, kwargs in tool_calls:
            if server_name not in server_groups:
                server_groups[server_name] = []
            server_groups[server_name].append((tool_name, kwargs))
        
        # Execute each server's tools in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_key = {}
            
            for server_name, tools in server_groups.items():
                for tool_name, kwargs in tools:
                    key = f"{server_name}.{tool_name}"
                    future = executor.submit(
                        self._sync_call, server_name, tool_name, **kwargs
                    )
                    future_to_key[future] = key
            
            # Collect results as they complete
            for future in as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    result = future.result()
                    results[key] = json.loads(result)
                except Exception as exc:
                    results[key] = {"error": str(exc), "success": False}
        
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
    
    def optimize_tool_selection(self, question: str) -> List[str]:
        """Intelligently select tools based on the question type"""
        question_lower = question.lower()
        
        # Define tool categories and their keywords
        tool_categories = {
            "structure": ["structure", "organization", "files", "directories", "layout"],
            "content": ["content", "code", "implementation", "function", "class"],
            "history": ["history", "commits", "changes", "development", "timeline"],
            "search": ["search", "find", "pattern", "dependency", "import"]
        }
        
        selected_tools = []
        
        # Determine which categories are relevant
        for category, keywords in tool_categories.items():
            if any(keyword in question_lower for keyword in keywords):
                if category == "structure":
                    selected_tools.extend(["get_directory_tree", "get_file_structure", "analyze_project_structure"])
                elif category == "content":
                    selected_tools.extend(["get_readme_content", "get_code_metrics", "analyze_code_complexity"])
                elif category == "history":
                    selected_tools.extend(["get_recent_commits", "get_commit_statistics", "get_development_patterns"])
                elif category == "search":
                    selected_tools.extend(["search_dependencies", "get_code_patterns"])
        
        # Always include essential tools if none selected
        if not selected_tools:
            selected_tools = ["get_readme_content", "get_file_structure", "get_repository_overview"]
        
        return selected_tools
    
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
        self.tools = FastMCPTools(max_workers=12, timeout=25)  # Increased workers, reduced timeout
        
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
            tools=ReasoningTools()
        )
    
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
- Provide detailed, actionable insights
- Consider code quality, architecture, security, and maintainability
- Support your conclusions with specific evidence from the codebase
- Be thorough but concise in your analysis

For Q&A:
- Use all available tools to gather relevant context
- Provide specific answers with code examples when appropriate
- Consider the broader context of the repository

For Summarization:
- Create comprehensive summaries covering all major aspects
- Include technical details, architecture insights, and key findings
- Highlight important patterns and potential areas of concern

Always strive to provide the most accurate and helpful analysis possible."""
    
    def _gather_comprehensive_data(self, repo_url: str, status_callback=None, question: str = "") -> Dict[str, Any]:
        """Gather comprehensive data from all MCP servers with optimized parallel execution"""
        if status_callback:
            status_callback("🔍 Gathering comprehensive repository data...")
        
        start_time = time.time()
        
        # Use intelligent tool selection if question is provided
        if question:
            selected_tools = self.tools.optimize_tool_selection(question)
            if status_callback:
                status_callback(f"🎯 Using {len(selected_tools)} optimized tools for your question...")
        else:
            # Default comprehensive tool set
            selected_tools = [
                "get_directory_tree", "get_file_structure", "analyze_project_structure",
                "get_readme_content", "get_code_metrics", "analyze_code_complexity",
                "get_code_patterns", "get_recent_commits", "get_commit_statistics",
                "get_development_patterns", "search_dependencies"
            ]
        
        # Create optimized tool calls using batch processing
        tool_calls = []
        tool_mapping = {
            "get_directory_tree": ("repository_structure", "get_directory_tree", {"repo_url": repo_url, "max_depth": 5}),
            "get_file_structure": ("repository_structure", "get_file_structure", {"repo_url": repo_url}),
            "analyze_project_structure": ("repository_structure", "analyze_project_structure", {"repo_url": repo_url}),
            "get_readme_content": ("file_content", "get_readme_content", {"repo_url": repo_url}),
            "get_code_metrics": ("code_search", "get_code_metrics", {"repo_url": repo_url}),
            "analyze_code_complexity": ("code_search", "analyze_code_complexity", {"repo_url": repo_url}),
            "get_code_patterns": ("code_search", "get_code_patterns", {"repo_url": repo_url}),
            "get_recent_commits": ("commit_history", "get_recent_commits", {"repo_url": repo_url, "limit": 50}),
            "get_commit_statistics": ("commit_history", "get_commit_statistics", {"repo_url": repo_url, "days": 90}),
            "get_development_patterns": ("commit_history", "get_development_patterns", {"repo_url": repo_url}),
            "search_dependencies": ("code_search", "search_dependencies", {"repo_url": repo_url})
        }
        
        # Add selected tools to batch
        for tool_name in selected_tools:
            if tool_name in tool_mapping:
                tool_calls.append(tool_mapping[tool_name])
        
        if status_callback:
            status_callback(f"🚀 Executing {len(tool_calls)} tools in parallel...")
        
        # Execute tools using optimized batch processing
        tool_results = self.tools._batch_call_tools(tool_calls)
        
        # Organize results
        data = self._organize_results(tool_results)
        
        # Analyze key files in parallel if needed
        if "get_file_content" in selected_tools or not question:
            if status_callback:
                status_callback("🔍 Analyzing key files...")
            data["code_analysis"]["key_files"] = self._analyze_key_files_parallel(repo_url)
        
        # Track tool utilization and performance
        data["tools_used"] = self.tools.get_tools_used()
        data["performance_stats"] = self.tools.get_performance_stats()
        data["execution_time"] = time.time() - start_time
        
        if status_callback:
            status_callback(f"✅ Data gathering complete in {data['execution_time']:.2f}s")
        
        return data
    
    def _execute_tools_parallel(self, tool_map: Dict[str, callable]) -> Dict[str, Any]:
        """Execute tools in parallel and return results"""
        tool_results = {}
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_key = {executor.submit(func): key for key, func in tool_map.items()}
            
            for future in concurrent.futures.as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    tool_results[key] = json.loads(future.result())
                except Exception as exc:
                    tool_results[key] = {"error": str(exc)}
        
        return tool_results
    
    def _organize_results(self, tool_results: Dict[str, Any]) -> Dict[str, Any]:
        """Organize tool results into structured data"""
        return {
            "file_structure": {
                "directory_tree": tool_results.get("directory_tree", {}),
                "file_structure": tool_results.get("file_structure", {}),
                "project_analysis": tool_results.get("project_analysis", {})
            },
            "repository_info": {
                "readme": tool_results.get("readme", {})
            },
            "code_metrics": {
                "metrics": tool_results.get("metrics", {}),
                "complexity": tool_results.get("complexity", {}),
                "patterns": tool_results.get("patterns", {})
            },
            "commit_history": {
                "recent_commits": tool_results.get("recent_commits", {}),
                "statistics": tool_results.get("commit_statistics", {})
            },
            "development_patterns": {
                "patterns": tool_results.get("dev_patterns", {})
            },
            "dependencies": {
                "dependency_files": tool_results.get("dependency_files", {})
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
            # Gather data using intelligent tool selection based on the question
            comprehensive_data = self._gather_comprehensive_data(repo_url, status_callback, question)
            
            if status_callback:
                status_callback("🧠 AI agent analyzing your question...")
            
            # Create comprehensive prompt with all gathered data
            prompt = self._create_comprehensive_prompt(question, comprehensive_data)
            
            # Get AI response with system prompt
            system_prompt = self._get_system_prompt()
            response = self.agent.run(f"{system_prompt}\n\n{prompt}")
            
            if status_callback:
                execution_time = comprehensive_data.get("execution_time", 0)
                status_callback(f"✅ Analysis complete! (Data gathering: {execution_time:.2f}s)")
            
            return response.content, comprehensive_data["tools_used"]
            
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
            response = self.agent.run(f"{system_prompt}\n\n{summary_prompt}")
            
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
            response = self.agent.run(f"{system_prompt}\n\n{pattern_prompt}")
            
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
            response = self.agent.run(f"{system_prompt}\n\n{quick_prompt}")
            
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
        """Create comprehensive prompt for Q&A"""
        return f"""Based on the following comprehensive repository data, please answer this question: "{question}"

Repository Data:
{json.dumps(data, indent=2)}

Please provide a detailed, accurate answer based on the available data. Use specific examples from the codebase when relevant. Consider:
- Code structure and architecture
- Development patterns and history
- Dependencies and requirements
- Code quality and complexity
- Any relevant technical details

Answer:"""
    
    def _create_summary_prompt(self, data: Dict[str, Any]) -> str:
        """Create comprehensive summary prompt"""
        return f"""Based on the following comprehensive repository data, create a detailed summary covering:

1. Project Overview and Purpose
2. Architecture and Structure
3. Code Quality and Complexity
4. Development Patterns and History
5. Dependencies and Requirements
6. Key Features and Components
7. Potential Areas of Interest or Concern

Repository Data:
{json.dumps(data, indent=2)}

Please provide a comprehensive, well-structured summary that would be useful for developers, maintainers, and stakeholders."""
    
    def _create_pattern_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Create pattern analysis prompt"""
        return f"""Analyze the following repository data to identify code patterns, architecture decisions, and development practices:

Repository Data:
{json.dumps(data, indent=2)}

Please analyze and report on:
1. Code Architecture Patterns
2. Design Patterns Used
3. Code Organization and Structure
4. Development Workflow Patterns
5. Code Quality Patterns
6. Potential Architectural Issues
7. Recommendations for Improvement

Provide specific examples and evidence from the codebase to support your analysis."""
    
    def _create_quick_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Create quick analysis prompt"""
        return f"""Based on the following repository data, provide a concise but comprehensive overview:

Repository Data:
{json.dumps(data, indent=2)}

Please provide:
1. Brief project description
2. Main technologies and architecture
3. Key insights about the codebase
4. Notable patterns or characteristics

Keep it concise but informative."""

# Global agent instance
_analyzer_agent = None

def create_analyzer_agent(model_name: str = "llama-3.1-70b-versatile") -> RepositoryAnalyzerAgent:
    """Create or get the global analyzer agent"""
    global _analyzer_agent
    if _analyzer_agent is None:
        _analyzer_agent = RepositoryAnalyzerAgent(model_name)
    return _analyzer_agent

def ask_repository_question(question: str, repo_url: str, model_name: str = "llama-3.1-70b-versatile", user_id: str = "default", status_callback=None) -> Tuple[str, List[str]]:
    """Ask a question about a repository using comprehensive analysis"""
    agent = create_analyzer_agent(model_name)
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