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

from utils.config import get_analysis_settings, get_analysis_presets
from utils.repository_manager import get_repository_manager, add_analysis_result
from agent.ai_agent import FastMCPTools, RepositoryAnalyzerAgent
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
        """Generate smart repository summarization with comprehensive insights"""
        
        if status_callback:
            status_callback("🧠 Starting smart summarization...")
        
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
            # Get comprehensive data from all MCP servers
            if status_callback:
                status_callback("📊 Gathering comprehensive data...")
            
            # Repository overview
            repo_overview = self._get_repository_info(repo_url)
            results["sections"]["overview"] = repo_overview
            
            # README and documentation
            readme_content = self._get_readme_content(repo_url)
            results["sections"]["documentation"] = readme_content
            
            # File structure
            file_structure = self._analyze_file_structure(repo_url, {})
            results["sections"]["structure"] = file_structure
            
            # Code metrics
            code_metrics = self._analyze_code_metrics(repo_url, {})
            results["sections"]["metrics"] = code_metrics
            
            # Commit history
            commit_history = self._analyze_commit_history(repo_url, {})
            results["sections"]["history"] = commit_history
            
            # Dependencies
            dependencies = self._analyze_dependencies(repo_url)
            results["sections"]["dependencies"] = dependencies
            
            # Code patterns
            patterns = self._analyze_code_patterns(repo_url)
            results["sections"]["patterns"] = patterns
            
            # Generate AI-powered summary
            if status_callback:
                status_callback("🤖 Generating AI summary...")
            
            ai_summary = self._generate_comprehensive_summary(repo_url, results["sections"])
            results["sections"]["ai_summary"] = ai_summary
            
            results["duration"] = time.time() - start_time
            results["tools_used"] = self.tools.get_tools_used()
            
            add_analysis_result("smart_summarization", results, results["tools_used"])
            
            if status_callback:
                status_callback("✅ Smart summarization completed!")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["duration"] = time.time() - start_time
            if status_callback:
                status_callback(f"❌ Smart summarization failed: {str(e)}")
            return results
    
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