"""
Performance Monitoring and ETA Tracking System
Provides real-time ETA estimates, tool explanations, and MCP server monitoring
"""

import time
import threading
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class AnalysisType(Enum):
    QUICK_OVERVIEW = "quick_overview"
    COMPREHENSIVE = "comprehensive"
    SECURITY = "security"
    CODE_QUALITY = "code_quality"
    VISUALIZATIONS = "visualizations"
    SMART_SUMMARY = "smart_summary"
    ULTRA_FAST = "ultra_fast"

@dataclass
class ToolInfo:
    """Information about a specific tool"""
    name: str
    server: str
    description: str
    typical_duration: float  # in seconds
    complexity: str  # "low", "medium", "high"
    dependencies: List[str]
    what_it_does: str
    when_to_use: str

@dataclass
class ServerStatus:
    """Status information for an MCP server"""
    name: str
    running: bool
    utilization: float  # 0-100
    response_time: float  # in seconds
    tools_available: List[str]
    last_used: Optional[datetime]
    error_count: int
    success_count: int

class PerformanceMonitor:
    """Comprehensive performance monitoring and ETA tracking"""
    
    def __init__(self):
        self.analysis_history = {}
        self.tool_performance = {}
        self.server_status = {}
        self.current_analysis = None
        self.start_time = None
        self.lock = threading.Lock()
        
        # Initialize tool information
        self.tools_info = self._initialize_tools_info()
        
        # Initialize server information
        self.servers_info = self._initialize_servers_info()
        
        # Analysis type ETAs (in seconds)
        self.analysis_etas = {
            AnalysisType.ULTRA_FAST: 15,
            AnalysisType.QUICK_OVERVIEW: 30,
            AnalysisType.SMART_SUMMARY: 45,
            AnalysisType.SECURITY: 60,
            AnalysisType.CODE_QUALITY: 75,
            AnalysisType.VISUALIZATIONS: 90,
            AnalysisType.COMPREHENSIVE: 120
        }
    
    def _initialize_tools_info(self) -> Dict[str, ToolInfo]:
        """Initialize comprehensive tool information"""
        return {
            # File Content Server Tools
            "file_content.get_file_content": ToolInfo(
                name="Get File Content",
                server="file_content",
                description="Retrieves the content of a specific file from the repository",
                typical_duration=2.0,
                complexity="low",
                dependencies=[],
                what_it_does="Reads and returns the raw content of files like source code, configuration files, or documentation",
                when_to_use="When you need to examine specific file contents, analyze code, or read configuration files"
            ),
            "file_content.list_directory": ToolInfo(
                name="List Directory",
                server="file_content",
                description="Lists all files and subdirectories in a given path",
                typical_duration=1.5,
                complexity="low",
                dependencies=[],
                what_it_does="Scans directory structure and returns a tree-like listing of files and folders",
                when_to_use="To understand project structure, find specific file types, or explore repository organization"
            ),
            "file_content.get_readme_content": ToolInfo(
                name="Get README Content",
                server="file_content",
                description="Retrieves the main README file content",
                typical_duration=1.0,
                complexity="low",
                dependencies=[],
                what_it_does="Finds and reads the primary README file to understand project purpose and setup",
                when_to_use="For quick project overview, understanding purpose, installation instructions, or project description"
            ),
            "file_content.analyze_file_content": ToolInfo(
                name="Analyze File Content",
                server="file_content",
                description="Performs code analysis on file content",
                typical_duration=5.0,
                complexity="medium",
                dependencies=["get_file_content"],
                what_it_does="Analyzes code structure, identifies patterns, and extracts meaningful insights from source files",
                when_to_use="When you need to understand code complexity, patterns, or extract specific information from source code"
            ),
            
            # Repository Structure Server Tools
            "repository_structure.get_file_structure": ToolInfo(
                name="Get File Structure",
                server="repository_structure",
                description="Gets complete repository file structure and hierarchy",
                typical_duration=3.0,
                complexity="medium",
                dependencies=[],
                what_it_does="Creates a comprehensive tree view of all files and directories in the repository",
                when_to_use="To understand project organization, identify key directories, or analyze project structure"
            ),
            "repository_structure.analyze_project_structure": ToolInfo(
                name="Analyze Project Structure",
                server="repository_structure",
                description="Analyzes project structure and organization patterns",
                typical_duration=8.0,
                complexity="high",
                dependencies=["get_file_structure"],
                what_it_does="Identifies architectural patterns, analyzes directory organization, and provides insights about project structure",
                when_to_use="For architectural analysis, understanding project organization, or identifying structural patterns"
            ),
            
            # Commit History Server Tools
            "commit_history.get_recent_commits": ToolInfo(
                name="Get Recent Commits",
                server="commit_history",
                description="Retrieves recent commit history and messages",
                typical_duration=2.5,
                complexity="low",
                dependencies=[],
                what_it_does="Fetches recent commit information including messages, authors, dates, and changes",
                when_to_use="To understand recent development activity, track changes, or analyze development patterns"
            ),
            "commit_history.get_commit_statistics": ToolInfo(
                name="Get Commit Statistics",
                server="commit_history",
                description="Analyzes commit patterns and statistics",
                typical_duration=6.0,
                complexity="medium",
                dependencies=["get_recent_commits"],
                what_it_does="Calculates commit frequency, author activity, file change patterns, and development metrics",
                when_to_use="For development activity analysis, contributor insights, or project health assessment"
            ),
            "commit_history.get_development_patterns": ToolInfo(
                name="Get Development Patterns",
                server="commit_history",
                description="Identifies development patterns and trends",
                typical_duration=10.0,
                complexity="high",
                dependencies=["get_commit_statistics"],
                what_it_does="Analyzes long-term development trends, identifies patterns in commits, and provides development insights",
                when_to_use="For long-term project analysis, development trend identification, or project maturity assessment"
            ),
            
            # Code Search Server Tools
            "code_search.search_code": ToolInfo(
                name="Search Code",
                server="code_search",
                description="Searches for specific code patterns or text",
                typical_duration=4.0,
                complexity="medium",
                dependencies=[],
                what_it_does="Searches through all source files to find specific code patterns, functions, or text content",
                when_to_use="To find specific functions, patterns, or code implementations across the codebase"
            ),
            "code_search.find_functions": ToolInfo(
                name="Find Functions",
                server="code_search",
                description="Locates specific function definitions",
                typical_duration=3.0,
                complexity="medium",
                dependencies=[],
                what_it_does="Searches for function definitions, method signatures, and function implementations",
                when_to_use="To locate specific functions, understand function usage, or analyze function patterns"
            ),
            "code_search.get_code_metrics": ToolInfo(
                name="Get Code Metrics",
                server="code_search",
                description="Calculates code complexity and quality metrics",
                typical_duration=12.0,
                complexity="high",
                dependencies=["search_code"],
                what_it_does="Analyzes code complexity, calculates metrics like cyclomatic complexity, and assesses code quality",
                when_to_use="For code quality assessment, complexity analysis, or technical debt identification"
            ),
            "code_search.analyze_code_complexity": ToolInfo(
                name="Analyze Code Complexity",
                server="code_search",
                description="Performs detailed code complexity analysis",
                typical_duration=15.0,
                complexity="high",
                dependencies=["get_code_metrics"],
                what_it_does="Performs deep analysis of code complexity, identifies complex functions, and provides refactoring suggestions",
                when_to_use="For detailed code analysis, refactoring recommendations, or complexity assessment"
            )
        }
    
    def _initialize_servers_info(self) -> Dict[str, Dict[str, Any]]:
        """Initialize server information"""
        return {
            "file_content": {
                "name": "File Content Server",
                "description": "Handles file reading and content analysis",
                "tools": ["get_file_content", "list_directory", "get_readme_content", "analyze_file_content"],
                "typical_response_time": 2.0,
                "max_concurrent_requests": 5
            },
            "repository_structure": {
                "name": "Repository Structure Server",
                "description": "Manages repository structure and organization analysis",
                "tools": ["get_file_structure", "analyze_project_structure"],
                "typical_response_time": 4.0,
                "max_concurrent_requests": 3
            },
            "commit_history": {
                "name": "Commit History Server",
                "description": "Handles commit history and development pattern analysis",
                "tools": ["get_recent_commits", "get_commit_statistics", "get_development_patterns"],
                "typical_response_time": 3.0,
                "max_concurrent_requests": 4
            },
            "code_search": {
                "name": "Code Search Server",
                "description": "Provides code search and analysis capabilities",
                "tools": ["search_code", "find_functions", "get_code_metrics", "analyze_code_complexity"],
                "typical_response_time": 5.0,
                "max_concurrent_requests": 3
            }
        }
    
    def start_analysis(self, analysis_type: AnalysisType, repo_url: str) -> Dict[str, Any]:
        """Start tracking a new analysis"""
        with self.lock:
            self.current_analysis = {
                "type": analysis_type,
                "repo_url": repo_url,
                "start_time": time.time(),
                "tools_used": [],
                "server_usage": {},
                "estimated_completion": time.time() + self.analysis_etas[analysis_type],
                "progress": 0.0
            }
            self.start_time = time.time()
            
            return {
                "eta_seconds": self.analysis_etas[analysis_type],
                "eta_formatted": self._format_duration(self.analysis_etas[analysis_type]),
                "analysis_type": analysis_type.value,
                "tools_expected": self._get_expected_tools(analysis_type)
            }
    
    def update_progress(self, progress: float, current_tool: str = None):
        """Update analysis progress"""
        with self.lock:
            if self.current_analysis:
                self.current_analysis["progress"] = progress
                if current_tool:
                    self.current_analysis["tools_used"].append(current_tool)
                    self._update_server_usage(current_tool)
    
    def record_tool_usage(self, tool_name: str, duration: float, success: bool):
        """Record tool usage for performance tracking"""
        with self.lock:
            if tool_name not in self.tool_performance:
                self.tool_performance[tool_name] = {
                    "total_calls": 0,
                    "total_duration": 0,
                    "success_count": 0,
                    "error_count": 0,
                    "avg_duration": 0
                }
            
            perf = self.tool_performance[tool_name]
            perf["total_calls"] += 1
            perf["total_duration"] += duration
            perf["avg_duration"] = perf["total_duration"] / perf["total_calls"]
            
            if success:
                perf["success_count"] += 1
            else:
                perf["error_count"] += 1
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current analysis status with ETA"""
        with self.lock:
            if not self.current_analysis:
                return {"status": "idle"}
            
            elapsed = time.time() - self.current_analysis["start_time"]
            remaining = max(0, self.current_analysis["estimated_completion"] - time.time())
            
            return {
                "status": "running",
                "analysis_type": self.current_analysis["type"].value,
                "progress": self.current_analysis["progress"],
                "elapsed_seconds": elapsed,
                "elapsed_formatted": self._format_duration(elapsed),
                "remaining_seconds": remaining,
                "remaining_formatted": self._format_duration(remaining),
                "eta_formatted": self._format_duration(remaining),
                "tools_used": self.current_analysis["tools_used"],
                "server_usage": self.current_analysis["server_usage"]
            }
    
    def get_tool_explanation(self, tool_name: str) -> Dict[str, Any]:
        """Get detailed explanation of what a tool does"""
        tool_info = self.tools_info.get(tool_name)
        if not tool_info:
            return {"error": f"Tool {tool_name} not found"}
        
        return {
            "name": tool_info.name,
            "server": tool_info.server,
            "description": tool_info.description,
            "what_it_does": tool_info.what_it_does,
            "when_to_use": tool_info.when_to_use,
            "typical_duration": tool_info.typical_duration,
            "complexity": tool_info.complexity,
            "dependencies": tool_info.dependencies
        }
    
    def get_server_status(self) -> Dict[str, ServerStatus]:
        """Get current status of all MCP servers"""
        with self.lock:
            return self.server_status.copy()
    
    def update_server_status(self, server_name: str, status: Dict[str, Any]):
        """Update server status information"""
        with self.lock:
            if server_name not in self.server_status:
                self.server_status[server_name] = ServerStatus(
                    name=server_name,
                    running=False,
                    utilization=0.0,
                    response_time=0.0,
                    tools_available=[],
                    last_used=None,
                    error_count=0,
                    success_count=0
                )
            
            # Update server status
            server = self.server_status[server_name]
            server.running = status.get("running", server.running)
            server.utilization = status.get("utilization", server.utilization)
            server.response_time = status.get("response_time", server.response_time)
            server.tools_available = status.get("tools_available", server.tools_available)
            server.last_used = status.get("last_used", server.last_used)
            server.error_count = status.get("error_count", server.error_count)
            server.success_count = status.get("success_count", server.success_count)
    
    def get_analysis_eta(self, analysis_type: AnalysisType) -> Dict[str, Any]:
        """Get ETA for a specific analysis type"""
        eta_seconds = self.analysis_etas[analysis_type]
        expected_tools = self._get_expected_tools(analysis_type)
        
        return {
            "analysis_type": analysis_type.value,
            "eta_seconds": eta_seconds,
            "eta_formatted": self._format_duration(eta_seconds),
            "expected_tools": expected_tools,
            "tool_count": len(expected_tools),
            "complexity": self._get_analysis_complexity(analysis_type)
        }
    
    def _get_expected_tools(self, analysis_type: AnalysisType) -> List[str]:
        """Get expected tools for an analysis type"""
        tool_mapping = {
            AnalysisType.ULTRA_FAST: [
                "file_content.get_readme_content",
                "repository_structure.get_file_structure"
            ],
            AnalysisType.QUICK_OVERVIEW: [
                "file_content.get_readme_content",
                "file_content.list_directory",
                "repository_structure.get_file_structure",
                "commit_history.get_recent_commits"
            ],
            AnalysisType.SMART_SUMMARY: [
                "file_content.get_readme_content",
                "file_content.list_directory",
                "repository_structure.get_file_structure",
                "commit_history.get_recent_commits",
                "code_search.search_code"
            ],
            AnalysisType.SECURITY: [
                "file_content.list_directory",
                "file_content.analyze_file_content",
                "code_search.search_code",
                "code_search.get_code_metrics"
            ],
            AnalysisType.CODE_QUALITY: [
                "file_content.list_directory",
                "code_search.get_code_metrics",
                "code_search.analyze_code_complexity",
                "repository_structure.analyze_project_structure"
            ],
            AnalysisType.VISUALIZATIONS: [
                "repository_structure.get_file_structure",
                "repository_structure.analyze_project_structure",
                "commit_history.get_commit_statistics",
                "code_search.get_code_metrics"
            ],
            AnalysisType.COMPREHENSIVE: [
                "file_content.get_readme_content",
                "file_content.list_directory",
                "file_content.analyze_file_content",
                "repository_structure.get_file_structure",
                "repository_structure.analyze_project_structure",
                "commit_history.get_recent_commits",
                "commit_history.get_commit_statistics",
                "commit_history.get_development_patterns",
                "code_search.search_code",
                "code_search.get_code_metrics",
                "code_search.analyze_code_complexity"
            ]
        }
        
        return tool_mapping.get(analysis_type, [])
    
    def _get_analysis_complexity(self, analysis_type: AnalysisType) -> str:
        """Get complexity level for analysis type"""
        complexity_mapping = {
            AnalysisType.ULTRA_FAST: "Very Low",
            AnalysisType.QUICK_OVERVIEW: "Low",
            AnalysisType.SMART_SUMMARY: "Medium",
            AnalysisType.SECURITY: "Medium",
            AnalysisType.CODE_QUALITY: "High",
            AnalysisType.VISUALIZATIONS: "High",
            AnalysisType.COMPREHENSIVE: "Very High"
        }
        return complexity_mapping.get(analysis_type, "Unknown")
    
    def _update_server_usage(self, tool_name: str):
        """Update server usage tracking"""
        if '.' in tool_name:
            server_name = tool_name.split('.')[0]
            if server_name not in self.current_analysis["server_usage"]:
                self.current_analysis["server_usage"][server_name] = 0
            self.current_analysis["server_usage"][server_name] += 1
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

# Global performance monitor instance
_performance_monitor = None

def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance"""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor 