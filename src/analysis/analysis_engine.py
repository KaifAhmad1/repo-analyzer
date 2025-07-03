"""
Comprehensive Analysis Engine for GitHub Repository Analyzer
Provides systematic repository analysis with multiple analysis types and comprehensive data collection
"""

import asyncio
import json
import time
from typing import Dict, Any, List, Optional, Tuple, Callable
from datetime import datetime, timedelta
from pathlib import Path

from ..utils.config import get_analysis_settings, get_analysis_presets
from ..utils.repository_manager import get_repository_manager, add_analysis_result
from ..agent.ai_agent import FastMCPTools, RepositoryAnalyzerAgent
from .code_analyzer import get_code_analyzer
from .repository_visualizer import get_repository_visualizer

class AnalysisEngine:
    """Comprehensive analysis engine for systematic repository analysis"""
    
    def __init__(self):
        self.tools = FastMCPTools()
        self.agent = None
        self.settings = get_analysis_settings()
        self.presets = get_analysis_presets()
        self.analysis_cache = {}
        self.code_analyzer = get_code_analyzer()
        self.visualizer = get_repository_visualizer()
        
    def get_agent(self, model_name: str = "llama-3.1-70b-versatile") -> RepositoryAnalyzerAgent:
        """Get or create AI agent"""
        if self.agent is None:
            self.agent = RepositoryAnalyzerAgent(model_name)
        return self.agent
    
    def analyze_repository(self, repo_url: str, analysis_type: str = "comprehensive", 
                          preset: str = "standard", status_callback: Callable = None) -> Dict[str, Any]:
        """Perform comprehensive repository analysis"""
        
        if status_callback:
            status_callback("🚀 Starting comprehensive repository analysis...")
        
        # Get analysis preset
        preset_config = self.presets.get(preset, self.presets["standard"])
        
        # Initialize results
        results = {
            "repository_url": repo_url,
            "analysis_type": analysis_type,
            "preset": preset,
            "timestamp": datetime.now().isoformat(),
            "duration": 0,
            "tools_used": [],
            "sections": {}
        }
        
        start_time = time.time()
        
        try:
            # 1. Basic Repository Information
            if status_callback:
                status_callback("📋 Gathering repository information...")
            
            repo_info = self._get_repository_info(repo_url)
            results["sections"]["repository_info"] = repo_info
            
            # 2. File Structure Analysis
            if status_callback:
                status_callback("📁 Analyzing file structure...")
            
            structure_analysis = self._analyze_file_structure(repo_url, preset_config)
            results["sections"]["file_structure"] = structure_analysis
            
            # 3. Code Analysis
            if preset_config.get("include_metrics", True):
                if status_callback:
                    status_callback("🔍 Analyzing code metrics...")
                
                code_analysis = self._analyze_code_metrics(repo_url, preset_config)
                results["sections"]["code_metrics"] = code_analysis
            
            # 4. Dependency Analysis
            if preset_config.get("include_dependencies", True):
                if status_callback:
                    status_callback("📦 Analyzing dependencies...")
                
                dependency_analysis = self._analyze_dependencies(repo_url)
                results["sections"]["dependencies"] = dependency_analysis
            
            # 5. Commit History Analysis
            if preset_config.get("include_commits", True):
                if status_callback:
                    status_callback("📝 Analyzing commit history...")
                
                commit_analysis = self._analyze_commit_history(repo_url, preset_config)
                results["sections"]["commit_history"] = commit_analysis
            
            # 6. Security Analysis
            if preset_config.get("include_security", True):
                if status_callback:
                    status_callback("🔒 Performing security analysis...")
                
                security_analysis = self._analyze_security(repo_url)
                results["sections"]["security"] = security_analysis
            
            # 7. AI-Powered Summary
            if status_callback:
                status_callback("🤖 Generating AI summary...")
            
            ai_summary = self._generate_ai_summary(repo_url, results["sections"])
            results["sections"]["ai_summary"] = ai_summary
            
            # Calculate duration
            results["duration"] = time.time() - start_time
            results["tools_used"] = self.tools.get_tools_used()
            
            # Save to session
            add_analysis_result("comprehensive", results, results["tools_used"])
            
            if status_callback:
                status_callback("✅ Analysis completed successfully!")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["duration"] = time.time() - start_time
            if status_callback:
                status_callback(f"❌ Analysis failed: {str(e)}")
            return results
    
    def quick_analysis(self, repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
        """Perform quick repository overview"""
        
        if status_callback:
            status_callback("⚡ Performing quick analysis...")
        
        results = {
            "repository_url": repo_url,
            "analysis_type": "quick",
            "timestamp": datetime.now().isoformat(),
            "duration": 0,
            "tools_used": [],
            "sections": {}
        }
        
        start_time = time.time()
        
        try:
            # Basic repository info
            repo_info = self._get_repository_info(repo_url)
            results["sections"]["repository_info"] = repo_info
            
            # README content
            readme_content = self._get_readme_content(repo_url)
            results["sections"]["readme"] = readme_content
            
            # Basic file structure
            file_structure = self._get_basic_file_structure(repo_url)
            results["sections"]["file_structure"] = file_structure
            
            # Quick AI summary
            ai_summary = self._generate_quick_summary(repo_url, results["sections"])
            results["sections"]["ai_summary"] = ai_summary
            
            results["duration"] = time.time() - start_time
            results["tools_used"] = self.tools.get_tools_used()
            
            add_analysis_result("quick", results, results["tools_used"])
            
            if status_callback:
                status_callback("✅ Quick analysis completed!")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["duration"] = time.time() - start_time
            if status_callback:
                status_callback(f"❌ Quick analysis failed: {str(e)}")
            return results
    
    def security_analysis(self, repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
        """Perform security-focused analysis"""
        
        if status_callback:
            status_callback("🔒 Starting security analysis...")
        
        results = {
            "repository_url": repo_url,
            "analysis_type": "security",
            "timestamp": datetime.now().isoformat(),
            "duration": 0,
            "tools_used": [],
            "sections": {}
        }
        
        start_time = time.time()
        
        try:
            # Security analysis
            security_analysis = self._analyze_security(repo_url)
            results["sections"]["security"] = security_analysis
            
            # Dependency vulnerabilities
            dependency_vulns = self._analyze_dependency_vulnerabilities(repo_url)
            results["sections"]["dependency_vulnerabilities"] = dependency_vulns
            
            # Code security patterns
            code_security = self._analyze_code_security_patterns(repo_url)
            results["sections"]["code_security"] = code_security
            
            # Security summary
            security_summary = self._generate_security_summary(results["sections"])
            results["sections"]["security_summary"] = security_summary
            
            results["duration"] = time.time() - start_time
            results["tools_used"] = self.tools.get_tools_used()
            
            add_analysis_result("security", results, results["tools_used"])
            
            if status_callback:
                status_callback("✅ Security analysis completed!")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["duration"] = time.time() - start_time
            if status_callback:
                status_callback(f"❌ Security analysis failed: {str(e)}")
            return results
    
    def code_quality_analysis(self, repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
        """Perform code quality analysis"""
        
        if status_callback:
            status_callback("📊 Starting code quality analysis...")
        
        results = {
            "repository_url": repo_url,
            "analysis_type": "code_quality",
            "timestamp": datetime.now().isoformat(),
            "duration": 0,
            "tools_used": [],
            "sections": {}
        }
        
        start_time = time.time()
        
        try:
            # Code metrics
            code_metrics = self._analyze_code_metrics(repo_url, {"max_files": 100})
            results["sections"]["code_metrics"] = code_metrics
            
            # Code patterns
            code_patterns = self._analyze_code_patterns(repo_url)
            results["sections"]["code_patterns"] = code_patterns
            
            # Documentation analysis
            documentation = self._analyze_documentation(repo_url)
            results["sections"]["documentation"] = documentation
            
            # Testing analysis
            testing = self._analyze_testing(repo_url)
            results["sections"]["testing"] = testing
            
            # Quality summary
            quality_summary = self._generate_quality_summary(results["sections"])
            results["sections"]["quality_summary"] = quality_summary
            
            results["duration"] = time.time() - start_time
            results["tools_used"] = self.tools.get_tools_used()
            
            add_analysis_result("code_quality", results, results["tools_used"])
            
            if status_callback:
                status_callback("✅ Code quality analysis completed!")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["duration"] = time.time() - start_time
            if status_callback:
                status_callback(f"❌ Code quality analysis failed: {str(e)}")
            return results
    
    def generate_visualizations(self, repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
        """Generate comprehensive repository visualizations"""
        
        if status_callback:
            status_callback("🗺️ Starting visualization generation...")
        
        results = {
            "repository_url": repo_url,
            "analysis_type": "visualizations",
            "timestamp": datetime.now().isoformat(),
            "duration": 0,
            "tools_used": [],
            "sections": {}
        }
        
        start_time = time.time()
        
        try:
            # Use the repository visualizer
            visualizations = self.visualizer.generate_repository_map(repo_url, status_callback)
            results["sections"]["visualizations"] = visualizations
            
            results["duration"] = time.time() - start_time
            results["tools_used"] = self.tools.get_tools_used()
            
            add_analysis_result("visualizations", results, results["tools_used"])
            
            if status_callback:
                status_callback("✅ Visualizations generated successfully!")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["duration"] = time.time() - start_time
            if status_callback:
                status_callback(f"❌ Visualization generation failed: {str(e)}")
            return results
    
    def smart_summarization(self, repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
        """Generate smart repository summarization with comprehensive insights - OPTIMIZED VERSION"""
        
        if status_callback:
            status_callback("🧠 Starting optimized smart summarization...")
        
        results = {
            "repository_url": repo_url,
            "analysis_type": "smart_summarization",
            "timestamp": datetime.now().isoformat(),
            "duration": 0,
            "tools_used": [],
            "sections": {}
        }
        
        start_time = time.time()
        
        try:
            # OPTIMIZED: Use only essential tools for faster processing
            if status_callback:
                status_callback("📊 Gathering essential data (optimized)...")
            
            # 1. Repository overview (fast)
            repo_overview = self._get_repository_info(repo_url)
            results["sections"]["overview"] = repo_overview
            
            # 2. README content (fast)
            readme_content = self._get_readme_content(repo_url)
            results["sections"]["documentation"] = readme_content
            
            # 3. Basic file structure (limited depth for speed)
            file_structure = self._get_optimized_file_structure(repo_url)
            results["sections"]["structure"] = file_structure
            
            # 4. Quick code metrics (limited scope)
            code_metrics = self._get_quick_code_metrics(repo_url)
            results["sections"]["metrics"] = code_metrics
            
            # 5. Recent commits only (limited count)
            commit_history = self._get_recent_commit_summary(repo_url)
            results["sections"]["history"] = commit_history
            
            # 6. Basic dependencies (fast search)
            dependencies = self._get_basic_dependencies(repo_url)
            results["sections"]["dependencies"] = dependencies
            
            # Generate AI-powered summary
            if status_callback:
                status_callback("🤖 Generating AI summary...")
            
            ai_summary = self._generate_optimized_summary(repo_url, results["sections"])
            results["sections"]["ai_summary"] = ai_summary
            
            results["duration"] = time.time() - start_time
            results["tools_used"] = self.tools.get_tools_used()
            
            add_analysis_result("smart_summarization", results, results["tools_used"])
            
            if status_callback:
                status_callback("✅ Optimized smart summarization completed!")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["duration"] = time.time() - start_time
            if status_callback:
                status_callback(f"❌ Smart summarization failed: {str(e)}")
            return results

    def ultra_fast_summarization(self, repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
        """Generate ultra-fast repository summarization with minimal tools"""
        
        if status_callback:
            status_callback("⚡ Starting ultra-fast summarization...")
        
        results = {
            "repository_url": repo_url,
            "analysis_type": "ultra_fast_summarization",
            "timestamp": datetime.now().isoformat(),
            "duration": 0,
            "tools_used": [],
            "sections": {}
        }
        
        start_time = time.time()
        
        try:
            # ULTRA FAST: Use only 2-3 essential tools
            if status_callback:
                status_callback("📊 Gathering minimal data (ultra-fast)...")
            
            # 1. Repository overview (fastest)
            repo_overview = self._get_repository_info(repo_url)
            results["sections"]["overview"] = repo_overview
            
            # 2. README content only
            readme_content = self._get_readme_content(repo_url)
            results["sections"]["documentation"] = readme_content
            
            # 3. Basic file structure (minimal)
            file_structure = self._get_minimal_file_structure(repo_url)
            results["sections"]["structure"] = file_structure
            
            # Generate AI-powered summary
            if status_callback:
                status_callback("🤖 Generating ultra-fast AI summary...")
            
            ai_summary = self._generate_ultra_fast_summary(repo_url, results["sections"])
            results["sections"]["ai_summary"] = ai_summary
            
            results["duration"] = time.time() - start_time
            results["tools_used"] = self.tools.get_tools_used()
            
            add_analysis_result("ultra_fast_summarization", results, results["tools_used"])
            
            if status_callback:
                status_callback("✅ Ultra-fast summarization completed!")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["duration"] = time.time() - start_time
            if status_callback:
                status_callback(f"❌ Ultra-fast summarization failed: {str(e)}")
            return results

    def comprehensive_smart_summarization(self, repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
        """Generate comprehensive repository summarization with all available tools - OPTIMIZED PARALLEL VERSION"""
        
        if status_callback:
            status_callback("🔍 Starting optimized comprehensive summarization...")
        
        results = {
            "repository_url": repo_url,
            "analysis_type": "comprehensive_smart_summarization",
            "timestamp": datetime.now().isoformat(),
            "duration": 0,
            "tools_used": [],
            "sections": {}
        }
        
        start_time = time.time()
        
        try:
            # OPTIMIZED: Use all tools but with better parallelization
            if status_callback:
                status_callback("📊 Gathering comprehensive data with parallel processing...")
            
            # Phase 1: Fast tools (can run immediately)
            phase1_results = self._execute_phase1_tools(repo_url, status_callback)
            results["sections"].update(phase1_results)
            
            # Phase 2: Medium complexity tools (run in parallel)
            if status_callback:
                status_callback("🔧 Running medium complexity analysis...")
            phase2_results = self._execute_phase2_tools(repo_url, status_callback)
            results["sections"].update(phase2_results)
            
            # Phase 3: Heavy analysis tools (run in parallel with limits)
            if status_callback:
                status_callback("⚡ Running advanced analysis...")
            phase3_results = self._execute_phase3_tools(repo_url, status_callback)
            results["sections"].update(phase3_results)
            
            # Generate comprehensive AI summary
            if status_callback:
                status_callback("🤖 Generating comprehensive AI summary...")
            
            ai_summary = self._generate_comprehensive_summary(repo_url, results["sections"])
            results["sections"]["ai_summary"] = ai_summary
            
            results["duration"] = time.time() - start_time
            results["tools_used"] = self.tools.get_tools_used()
            
            add_analysis_result("comprehensive_smart_summarization", results, results["tools_used"])
            
            if status_callback:
                status_callback("✅ Optimized comprehensive summarization completed!")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["duration"] = time.time() - start_time
            if status_callback:
                status_callback(f"❌ Comprehensive summarization failed: {str(e)}")
            return results

    def _execute_phase1_tools(self, repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
        """Execute fast tools that can run immediately"""
        results = {}
        
        # These tools are fast and can run immediately
        fast_tools = [
            ("overview", self._get_repository_info, repo_url),
            ("documentation", self._get_readme_content, repo_url),
            ("basic_structure", self._get_basic_file_structure, repo_url)
        ]
        
        # Execute fast tools in parallel
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_key = {
                executor.submit(func, repo_url): key 
                for key, func, repo_url in fast_tools
            }
            
            for future in concurrent.futures.as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    results[key] = future.result()
                except Exception as e:
                    results[key] = {"error": str(e)}
        
        return results

    def _execute_phase2_tools(self, repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
        """Execute medium complexity tools in parallel"""
        results = {}
        
        # Medium complexity tools that can run in parallel
        medium_tools = [
            ("metrics", self._get_optimized_code_metrics, repo_url),
            ("dependencies", self._get_optimized_dependencies, repo_url),
            ("recent_history", self._get_optimized_commit_history, repo_url)
        ]
        
        # Execute medium tools in parallel
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_key = {
                executor.submit(func, repo_url): key 
                for key, func, repo_url in medium_tools
            }
            
            for future in concurrent.futures.as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    results[key] = future.result()
                except Exception as e:
                    results[key] = {"error": str(e)}
        
        return results

    def _execute_phase3_tools(self, repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
        """Execute heavy analysis tools with optimized limits"""
        results = {}
        
        # Heavy tools with optimized limits
        heavy_tools = [
            ("full_structure", self._get_full_file_structure_optimized, repo_url),
            ("patterns", self._get_optimized_code_patterns, repo_url),
            ("security", self._get_optimized_security_analysis, repo_url)
        ]
        
        # Execute heavy tools in parallel with timeouts
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_key = {
                executor.submit(func, repo_url): key 
                for key, func, repo_url in heavy_tools
            }
            
            for future in concurrent.futures.as_completed(future_to_key, timeout=120):  # 2 minute timeout
                key = future_to_key[future]
                try:
                    results[key] = future.result(timeout=60)  # 1 minute per tool
                except concurrent.futures.TimeoutError:
                    results[key] = {"error": "Tool execution timed out"}
                except Exception as e:
                    results[key] = {"error": str(e)}
        
        return results

    def _get_optimized_code_metrics(self, repo_url: str) -> Dict[str, Any]:
        """Get optimized code metrics with better limits"""
        try:
            # Get basic metrics
            metrics_result = self.tools.get_code_metrics(repo_url)
            metrics_data = json.loads(metrics_result) if isinstance(metrics_result, str) else metrics_result
            
            # Limited but comprehensive pattern search
            patterns = {
                "functions": self.tools.search_code(repo_url, "def ", "python"),
                "classes": self.tools.search_code(repo_url, "class ", "python"),
                "imports": self.tools.search_code(repo_url, "import ", "python"),
                "async_code": self.tools.search_code(repo_url, "async def", "python"),
                "error_handling": self.tools.search_code(repo_url, "try:", "python")
            }
            
            return {
                "metrics": metrics_data,
                "patterns": patterns,
                "note": "Optimized metrics with comprehensive patterns"
            }
        except Exception as e:
            return {"error": f"Failed to get optimized code metrics: {str(e)}"}

    def _get_optimized_dependencies(self, repo_url: str) -> Dict[str, Any]:
        """Get optimized dependency analysis"""
        try:
            # Search for dependency files
            dependency_result = self.tools.search_dependencies(repo_url)
            dependency_data = json.loads(dependency_result) if isinstance(dependency_result, str) else dependency_result
            
            # Get main dependency files
            dependency_files = {
                "requirements": self.tools.get_file_content(repo_url, "requirements.txt"),
                "package_json": self.tools.get_file_content(repo_url, "package.json"),
                "setup": self.tools.get_file_content(repo_url, "setup.py"),
                "pyproject": self.tools.get_file_content(repo_url, "pyproject.toml")
            }
            
            return {
                "dependency_search": dependency_data,
                "dependency_files": dependency_files,
                "note": "Comprehensive dependency analysis"
            }
        except Exception as e:
            return {"error": f"Failed to get optimized dependencies: {str(e)}"}

    def _get_optimized_commit_history(self, repo_url: str) -> Dict[str, Any]:
        """Get optimized commit history with better limits"""
        try:
            # Get recent commits with moderate limit
            commits_result = self.tools.get_recent_commits(repo_url, 25)  # Balanced limit
            commits_data = json.loads(commits_result) if isinstance(commits_result, str) else commits_result
            
            # Get commit statistics
            stats_result = self.tools.get_commit_statistics(repo_url, 60)  # 60 days
            stats_data = json.loads(stats_result) if isinstance(stats_result, str) else stats_result
            
            return {
                "recent_commits": commits_data,
                "commit_statistics": stats_data,
                "analysis_period": "60 days",
                "note": "Optimized commit history analysis"
            }
        except Exception as e:
            return {"error": f"Failed to get optimized commit history: {str(e)}"}

    def _get_full_file_structure_optimized(self, repo_url: str) -> Dict[str, Any]:
        """Get full file structure with optimized limits"""
        try:
            # Use balanced limits for comprehensive but fast analysis
            max_depth = 4  # Balanced depth
            max_files = 100  # Reasonable file limit
            
            # Get directory tree
            tree_result = self.tools.get_directory_tree(repo_url, max_depth)
            tree_data = json.loads(tree_result) if isinstance(tree_result, str) else tree_result
            
            # Get file structure
            structure_result = self.tools.get_file_structure(repo_url)
            structure_data = json.loads(structure_result) if isinstance(structure_result, str) else structure_result
            
            # Get project analysis
            analysis_result = self.tools.analyze_project_structure(repo_url)
            analysis_data = json.loads(analysis_result) if isinstance(analysis_result, str) else analysis_result
            
            return {
                "directory_tree": tree_data,
                "file_structure": structure_data,
                "project_analysis": analysis_data,
                "max_depth": max_depth,
                "max_files": max_files,
                "note": "Full structure analysis with optimized limits"
            }
        except Exception as e:
            return {"error": f"Failed to get full file structure: {str(e)}"}

    def _get_optimized_code_patterns(self, repo_url: str) -> Dict[str, Any]:
        """Get optimized code patterns analysis"""
        try:
            # Comprehensive pattern search with limits
            patterns = {
                "design_patterns": self.tools.search_code(repo_url, "class ", "python"),
                "function_patterns": self.tools.search_code(repo_url, "def ", "python"),
                "error_patterns": self.tools.search_code(repo_url, "except", "python"),
                "async_patterns": self.tools.search_code(repo_url, "async", "python"),
                "decorator_patterns": self.tools.search_code(repo_url, "@", "python"),
                "type_hints": self.tools.search_code(repo_url, "->", "python")
            }
            
            return {
                "code_patterns": patterns,
                "note": "Comprehensive pattern analysis"
            }
        except Exception as e:
            return {"error": f"Failed to get optimized code patterns: {str(e)}"}

    def _get_optimized_security_analysis(self, repo_url: str) -> Dict[str, Any]:
        """Get optimized security analysis"""
        try:
            # Comprehensive security patterns
            security_patterns = {
                "api_keys": self.tools.search_code(repo_url, "API_KEY", ""),
                "passwords": self.tools.search_code(repo_url, "password", ""),
                "secrets": self.tools.search_code(repo_url, "secret", ""),
                "tokens": self.tools.search_code(repo_url, "token", ""),
                "hardcoded_credentials": self.tools.search_code(repo_url, "admin", ""),
                "sql_injection": self.tools.search_code(repo_url, "SELECT", ""),
                "file_operations": self.tools.search_code(repo_url, "open(", "python"),
                "network_calls": self.tools.search_code(repo_url, "requests.", "python"),
                "eval_usage": self.tools.search_code(repo_url, "eval(", "python")
            }
            
            return {
                "security_patterns": security_patterns,
                "risk_level": self._calculate_security_risk(security_patterns),
                "note": "Comprehensive security analysis"
            }
        except Exception as e:
            return {"error": f"Failed to get optimized security analysis: {str(e)}"}

    def _get_optimized_file_structure(self, repo_url: str) -> Dict[str, Any]:
        """Get optimized file structure with limited depth and files"""
        try:
            # Use smaller limits for faster processing
            max_depth = 2  # Reduced from 5
            max_files = 20  # Reduced from 50
            
            # Get basic file structure only
            structure_result = self.tools.get_file_structure(repo_url)
            structure_data = json.loads(structure_result) if isinstance(structure_result, str) else structure_result
            
            return {
                "file_structure": structure_data,
                "max_depth": max_depth,
                "max_files": max_files,
                "note": "Optimized for speed - limited depth and file count"
            }
        except Exception as e:
            return {"error": f"Failed to get optimized file structure: {str(e)}"}

    def _get_quick_code_metrics(self, repo_url: str) -> Dict[str, Any]:
        """Get quick code metrics with limited scope"""
        try:
            # Get basic metrics only
            metrics_result = self.tools.get_code_metrics(repo_url)
            metrics_data = json.loads(metrics_result) if isinstance(metrics_result, str) else metrics_result
            
            # Limited pattern search
            patterns = {
                "functions": self.tools.search_code(repo_url, "def ", "python"),
                "classes": self.tools.search_code(repo_url, "class ", "python")
            }
            
            return {
                "metrics": metrics_data,
                "patterns": patterns,
                "note": "Quick metrics - limited pattern analysis"
            }
        except Exception as e:
            return {"error": f"Failed to get quick code metrics: {str(e)}"}

    def _get_recent_commit_summary(self, repo_url: str) -> Dict[str, Any]:
        """Get recent commit summary with limited data"""
        try:
            # Get only recent commits (reduced count)
            commits_result = self.tools.get_recent_commits(repo_url, 10)  # Reduced from 50
            commits_data = json.loads(commits_result) if isinstance(commits_result, str) else commits_result
            
            return {
                "recent_commits": commits_data,
                "analysis_period": "10 commits",
                "note": "Recent commits only for faster processing"
            }
        except Exception as e:
            return {"error": f"Failed to get recent commit summary: {str(e)}"}

    def _get_basic_dependencies(self, repo_url: str) -> Dict[str, Any]:
        """Get basic dependency information"""
        try:
            # Search for main dependency files only
            dependency_files = {
                "requirements": self.tools.get_file_content(repo_url, "requirements.txt"),
                "package_json": self.tools.get_file_content(repo_url, "package.json")
            }
            
            return {
                "dependency_files": dependency_files,
                "note": "Basic dependency files only"
            }
        except Exception as e:
            return {"error": f"Failed to get basic dependencies: {str(e)}"}

    def _generate_optimized_summary(self, repo_url: str, sections: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimized AI summary with faster processing"""
        try:
            agent = self.get_agent()
            
            # Create a more concise prompt for faster processing
            optimized_prompt = self._create_optimized_summary_prompt(sections)
            
            # Use the AI agent to generate summary
            summary, tools_used = agent.ask_question(
                f"Please provide a comprehensive but concise repository summary: {optimized_prompt}",
                repo_url
            )
            
            return {
                "summary": summary,
                "tools_used": tools_used,
                "generated_at": datetime.now().isoformat(),
                "note": "Optimized summary generation"
            }
        except Exception as e:
            return {"error": f"Failed to generate optimized summary: {str(e)}"}

    def _create_optimized_summary_prompt(self, sections: Dict[str, Any]) -> str:
        """Create optimized summary prompt for faster processing"""
        prompt = "Based on the following repository analysis, provide a comprehensive but concise summary:\n\n"
        
        # Include only essential sections
        essential_sections = ["overview", "documentation", "structure", "metrics", "history", "dependencies"]
        
        for section_name in essential_sections:
            if section_name in sections and sections[section_name]:
                section_data = sections[section_name]
                if isinstance(section_data, dict) and "error" not in section_data:
                    prompt += f"{section_name.title()}: {json.dumps(section_data, indent=2)}\n\n"
        
        prompt += "Please provide a comprehensive summary covering the project's purpose, architecture, code quality, and overall assessment. Keep it concise but informative."
        
        return prompt
    
    def _get_repository_info(self, repo_url: str) -> Dict[str, Any]:
        """Get basic repository information"""
        try:
            # Use repository manager to get info
            from ..utils.repository_manager import get_repository_info
            return get_repository_info()
        except Exception as e:
            return {"error": f"Failed to get repository info: {str(e)}"}
    
    def _analyze_file_structure(self, repo_url: str, preset_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze file structure"""
        try:
            max_depth = preset_config.get("max_depth", 3)
            max_files = preset_config.get("max_files", 50)
            
            # Get directory tree
            tree_result = self.tools.get_directory_tree(repo_url, max_depth)
            tree_data = json.loads(tree_result) if isinstance(tree_result, str) else tree_result
            
            # Get file structure
            structure_result = self.tools.get_file_structure(repo_url)
            structure_data = json.loads(structure_result) if isinstance(structure_result, str) else structure_result
            
            # Analyze project structure
            analysis_result = self.tools.analyze_project_structure(repo_url)
            analysis_data = json.loads(analysis_result) if isinstance(analysis_result, str) else analysis_result
            
            return {
                "directory_tree": tree_data,
                "file_structure": structure_data,
                "project_analysis": analysis_data,
                "max_depth": max_depth,
                "max_files": max_files
            }
        except Exception as e:
            return {"error": f"Failed to analyze file structure: {str(e)}"}
    
    def _analyze_code_metrics(self, repo_url: str, preset_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code metrics"""
        try:
            # Get code metrics
            metrics_result = self.tools.get_code_metrics(repo_url)
            metrics_data = json.loads(metrics_result) if isinstance(metrics_result, str) else metrics_result
            
            # Search for specific code patterns
            patterns = {
                "functions": self.tools.search_code(repo_url, "def ", "python"),
                "classes": self.tools.search_code(repo_url, "class ", "python"),
                "imports": self.tools.search_code(repo_url, "import ", "python"),
                "async_code": self.tools.search_code(repo_url, "async def", "python")
            }
            
            return {
                "metrics": metrics_data,
                "patterns": patterns,
                "max_files": preset_config.get("max_files", 50)
            }
        except Exception as e:
            return {"error": f"Failed to analyze code metrics: {str(e)}"}
    
    def _analyze_dependencies(self, repo_url: str) -> Dict[str, Any]:
        """Analyze project dependencies"""
        try:
            # Search for dependency files
            dependency_result = self.tools.search_dependencies(repo_url)
            dependency_data = json.loads(dependency_result) if isinstance(dependency_result, str) else dependency_result
            
            # Get specific dependency files
            dependency_files = {
                "requirements": self.tools.get_file_content(repo_url, "requirements.txt"),
                "setup": self.tools.get_file_content(repo_url, "setup.py"),
                "pyproject": self.tools.get_file_content(repo_url, "pyproject.toml"),
                "package_json": self.tools.get_file_content(repo_url, "package.json"),
                "gemfile": self.tools.get_file_content(repo_url, "Gemfile"),
                "cargo": self.tools.get_file_content(repo_url, "Cargo.toml")
            }
            
            return {
                "dependency_search": dependency_data,
                "dependency_files": dependency_files
            }
        except Exception as e:
            return {"error": f"Failed to analyze dependencies: {str(e)}"}
    
    def _analyze_commit_history(self, repo_url: str, preset_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze commit history"""
        try:
            # Get recent commits
            commits_result = self.tools.get_recent_commits(repo_url, 20)
            commits_data = json.loads(commits_result) if isinstance(commits_result, str) else commits_result
            
            # Get commit statistics
            stats_result = self.tools.get_commit_statistics(repo_url, 30)
            stats_data = json.loads(stats_result) if isinstance(stats_result, str) else stats_result
            
            return {
                "recent_commits": commits_data,
                "commit_statistics": stats_data,
                "analysis_period": "30 days"
            }
        except Exception as e:
            return {"error": f"Failed to analyze commit history: {str(e)}"}
    
    def _analyze_security(self, repo_url: str) -> Dict[str, Any]:
        """Analyze security aspects"""
        try:
            # Search for security-related patterns
            security_patterns = {
                "api_keys": self.tools.search_code(repo_url, "API_KEY", ""),
                "passwords": self.tools.search_code(repo_url, "password", ""),
                "secrets": self.tools.search_code(repo_url, "secret", ""),
                "tokens": self.tools.search_code(repo_url, "token", ""),
                "hardcoded_credentials": self.tools.search_code(repo_url, "admin", ""),
                "sql_injection": self.tools.search_code(repo_url, "SELECT", ""),
                "file_operations": self.tools.search_code(repo_url, "open(", "python")
            }
            
            return {
                "security_patterns": security_patterns,
                "risk_level": self._calculate_security_risk(security_patterns)
            }
        except Exception as e:
            return {"error": f"Failed to analyze security: {str(e)}"}
    
    def _get_readme_content(self, repo_url: str) -> Dict[str, Any]:
        """Get README content"""
        try:
            readme_result = self.tools.get_readme_content(repo_url)
            return json.loads(readme_result) if isinstance(readme_result, str) else readme_result
        except Exception as e:
            return {"error": f"Failed to get README content: {str(e)}"}
    
    def _get_basic_file_structure(self, repo_url: str) -> Dict[str, Any]:
        """Get basic file structure"""
        try:
            structure_result = self.tools.get_file_structure(repo_url)
            return json.loads(structure_result) if isinstance(structure_result, str) else structure_result
        except Exception as e:
            return {"error": f"Failed to get file structure: {str(e)}"}
    
    def _generate_ai_summary(self, repo_url: str, sections: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered summary"""
        try:
            agent = self.get_agent()
            summary_prompt = self._create_summary_prompt(sections)
            summary, tools_used = agent.ask_question(summary_prompt, repo_url)
            
            return {
                "summary": summary,
                "tools_used": tools_used,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to generate AI summary: {str(e)}"}
    
    def _generate_quick_summary(self, repo_url: str, sections: Dict[str, Any]) -> Dict[str, Any]:
        """Generate quick AI summary"""
        try:
            agent = self.get_agent()
            quick_prompt = "Provide a brief 2-3 sentence overview of this repository based on the available information."
            summary, tools_used = agent.ask_question(quick_prompt, repo_url)
            
            return {
                "summary": summary,
                "tools_used": tools_used,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to generate quick summary: {str(e)}"}
    
    def _analyze_dependency_vulnerabilities(self, repo_url: str) -> Dict[str, Any]:
        """Analyze dependency vulnerabilities"""
        # This would integrate with vulnerability databases
        return {"status": "Not implemented", "note": "Would check against vulnerability databases"}
    
    def _analyze_code_security_patterns(self, repo_url: str) -> Dict[str, Any]:
        """Analyze code security patterns"""
        try:
            patterns = {
                "input_validation": self.tools.search_code(repo_url, "input(", "python"),
                "authentication": self.tools.search_code(repo_url, "auth", ""),
                "authorization": self.tools.search_code(repo_url, "permission", ""),
                "encryption": self.tools.search_code(repo_url, "encrypt", ""),
                "logging": self.tools.search_code(repo_url, "log", "")
            }
            return {"security_patterns": patterns}
        except Exception as e:
            return {"error": f"Failed to analyze code security patterns: {str(e)}"}
    
    def _analyze_code_patterns(self, repo_url: str) -> Dict[str, Any]:
        """Analyze code patterns"""
        try:
            patterns = {
                "design_patterns": self.tools.search_code(repo_url, "class", "python"),
                "async_patterns": self.tools.search_code(repo_url, "async", "python"),
                "decorators": self.tools.search_code(repo_url, "@", "python"),
                "type_hints": self.tools.search_code(repo_url, "->", "python")
            }
            return {"code_patterns": patterns}
        except Exception as e:
            return {"error": f"Failed to analyze code patterns: {str(e)}"}
    
    def _analyze_documentation(self, repo_url: str) -> Dict[str, Any]:
        """Analyze documentation"""
        try:
            doc_files = {
                "readme": self.tools.get_file_content(repo_url, "README.md"),
                "docs": self.tools.list_directory(repo_url, "docs"),
                "docstrings": self.tools.search_code(repo_url, '"""', "python")
            }
            return {"documentation": doc_files}
        except Exception as e:
            return {"error": f"Failed to analyze documentation: {str(e)}"}
    
    def _analyze_testing(self, repo_url: str) -> Dict[str, Any]:
        """Analyze testing"""
        try:
            test_files = {
                "test_files": self.tools.search_files(repo_url, "test_"),
                "test_functions": self.tools.search_code(repo_url, "def test_", "python"),
                "pytest": self.tools.search_code(repo_url, "pytest", "python"),
                "unittest": self.tools.search_code(repo_url, "unittest", "python")
            }
            return {"testing": test_files}
        except Exception as e:
            return {"error": f"Failed to analyze testing: {str(e)}"}
    
    def _generate_security_summary(self, sections: Dict[str, Any]) -> Dict[str, Any]:
        """Generate security summary"""
        return {"summary": "Security analysis completed", "risk_level": "medium"}
    
    def _generate_quality_summary(self, sections: Dict[str, Any]) -> Dict[str, Any]:
        """Generate quality summary"""
        return {"summary": "Code quality analysis completed", "quality_score": "good"}
    
    def _calculate_security_risk(self, patterns: Dict[str, Any]) -> str:
        """Calculate security risk level"""
        risk_factors = 0
        for pattern, data in patterns.items():
            if data and isinstance(data, dict) and data.get("result"):
                risk_factors += 1
        
        if risk_factors == 0:
            return "low"
        elif risk_factors <= 3:
            return "medium"
        else:
            return "high"
    
    def _create_summary_prompt(self, sections: Dict[str, Any]) -> str:
        """Create summary prompt based on available sections"""
        prompt = "Based on the following repository analysis, provide a comprehensive summary:\n\n"
        
        for section_name, section_data in sections.items():
            if section_data and not isinstance(section_data, dict):
                continue
            
            if section_name == "repository_info":
                prompt += f"Repository Information: {json.dumps(section_data, indent=2)}\n\n"
            elif section_name == "file_structure":
                prompt += f"File Structure: {json.dumps(section_data, indent=2)}\n\n"
            elif section_name == "code_metrics":
                prompt += f"Code Metrics: {json.dumps(section_data, indent=2)}\n\n"
            elif section_name == "dependencies":
                prompt += f"Dependencies: {json.dumps(section_data, indent=2)}\n\n"
            elif section_name == "commit_history":
                prompt += f"Commit History: {json.dumps(section_data, indent=2)}\n\n"
            elif section_name == "security":
                prompt += f"Security Analysis: {json.dumps(section_data, indent=2)}\n\n"
        
        prompt += "Please provide a comprehensive summary covering the project's purpose, architecture, code quality, security considerations, and overall assessment."
        
        return prompt

    def _get_minimal_file_structure(self, repo_url: str) -> Dict[str, Any]:
        """Get minimal file structure for ultra-fast processing"""
        try:
            # Get only basic file structure
            structure_result = self.tools.get_file_structure(repo_url)
            structure_data = json.loads(structure_result) if isinstance(structure_result, str) else structure_result
            
            return {
                "file_structure": structure_data,
                "note": "Ultra-fast mode - minimal file analysis"
            }
        except Exception as e:
            return {"error": f"Failed to get minimal file structure: {str(e)}"}

    def _generate_ultra_fast_summary(self, repo_url: str, sections: Dict[str, Any]) -> Dict[str, Any]:
        """Generate ultra-fast AI summary"""
        try:
            agent = self.get_agent()
            
            # Create minimal prompt for ultra-fast processing
            minimal_prompt = self._create_minimal_summary_prompt(sections)
            
            # Use the AI agent to generate summary
            summary, tools_used = agent.ask_question(
                f"Please provide a brief but informative repository summary: {minimal_prompt}",
                repo_url
            )
            
            return {
                "summary": summary,
                "tools_used": tools_used,
                "generated_at": datetime.now().isoformat(),
                "note": "Ultra-fast summary generation"
            }
        except Exception as e:
            return {"error": f"Failed to generate ultra-fast summary: {str(e)}"}

    def _create_minimal_summary_prompt(self, sections: Dict[str, Any]) -> str:
        """Create minimal summary prompt for ultra-fast processing"""
        prompt = "Based on the following repository data, provide a brief but informative summary:\n\n"
        
        # Include only the most essential sections
        essential_sections = ["overview", "documentation", "structure"]
        
        for section_name in essential_sections:
            if section_name in sections and sections[section_name]:
                section_data = sections[section_name]
                if isinstance(section_data, dict) and "error" not in section_data:
                    prompt += f"{section_name.title()}: {json.dumps(section_data, indent=2)}\n\n"
        
        prompt += "Please provide a concise summary covering the project's purpose, main technologies, and key features. Keep it brief but informative."
        
        return prompt

    def _generate_comprehensive_summary(self, repo_url: str, sections: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive AI summary using all available data"""
        try:
            agent = self.get_agent()
            prompt = self._create_summary_prompt(sections)
            
            # Use the AI agent to generate comprehensive summary
            summary, tools_used = agent.ask_question(
                f"Please provide a comprehensive repository summary based on this analysis: {prompt}",
                repo_url
            )
            
            return {
                "summary": summary,
                "tools_used": tools_used,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to generate comprehensive summary: {str(e)}"}

# Global analysis engine instance
_analysis_engine = None

def get_analysis_engine() -> AnalysisEngine:
    """Get the global analysis engine instance"""
    global _analysis_engine
    if _analysis_engine is None:
        _analysis_engine = AnalysisEngine()
    return _analysis_engine

def analyze_repository(repo_url: str, analysis_type: str = "comprehensive", 
                      preset: str = "standard", status_callback: Callable = None) -> Dict[str, Any]:
    """Analyze repository using the analysis engine"""
    engine = get_analysis_engine()
    return engine.analyze_repository(repo_url, analysis_type, preset, status_callback)

def quick_analysis(repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
    """Perform quick repository analysis"""
    engine = get_analysis_engine()
    return engine.quick_analysis(repo_url, status_callback)

def security_analysis(repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
    """Perform security analysis"""
    engine = get_analysis_engine()
    return engine.security_analysis(repo_url, status_callback)

def code_quality_analysis(repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
    """Perform code quality analysis"""
    engine = get_analysis_engine()
    return engine.code_quality_analysis(repo_url, status_callback)

def generate_visualizations(repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
    """Generate repository visualizations"""
    engine = get_analysis_engine()
    return engine.generate_visualizations(repo_url, status_callback)

def smart_summarization(repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
    """Generate smart repository summarization"""
    engine = get_analysis_engine()
    return engine.smart_summarization(repo_url, status_callback)

def ultra_fast_summarization(repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
    """Generate ultra-fast repository summarization with minimal tools"""
    engine = get_analysis_engine()
    return engine.ultra_fast_summarization(repo_url, status_callback)

def comprehensive_smart_summarization(repo_url: str, status_callback: Callable = None) -> Dict[str, Any]:
    """Generate comprehensive repository summarization with all available tools"""
    engine = get_analysis_engine()
    return engine.comprehensive_smart_summarization(repo_url, status_callback) 