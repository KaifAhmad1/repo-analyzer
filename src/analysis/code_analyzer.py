"""
Comprehensive Code Analysis Module
Provides deep code quality analysis, complexity metrics, and pattern detection
"""

import json
import ast
import re
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

from agent.ai_agent import FastMCPTools

class CodeAnalyzer:
    """Comprehensive code analyzer with quality metrics, complexity analysis, and pattern detection"""
    
    def __init__(self):
        self.tools = FastMCPTools()
        self.analysis_cache = {}
    
    def analyze_code_quality(self, repo_url: str, status_callback=None) -> Dict[str, Any]:
        """Perform comprehensive code quality analysis"""
        
        if status_callback:
            status_callback("🔍 Starting comprehensive code quality analysis...")
        
        analysis = {
            "repository_url": repo_url,
            "timestamp": datetime.now().isoformat(),
            "metrics": {},
            "complexity": {},
            "patterns": {},
            "quality_score": 0,
            "recommendations": [],
            "visualizations": {}
        }
        
        try:
            # 1. Code Metrics Analysis
            if status_callback:
                status_callback("📊 Analyzing code metrics...")
            
            metrics_data = self._analyze_code_metrics(repo_url)
            analysis["metrics"] = metrics_data
            
            # 2. Complexity Analysis
            if status_callback:
                status_callback("🧮 Analyzing code complexity...")
            
            complexity_data = self._analyze_code_complexity(repo_url)
            analysis["complexity"] = complexity_data
            
            # 3. Pattern Analysis
            if status_callback:
                status_callback("🔍 Detecting code patterns...")
            
            patterns_data = self._analyze_code_patterns(repo_url)
            analysis["patterns"] = patterns_data
            
            # 4. Quality Assessment
            if status_callback:
                status_callback("📈 Calculating quality score...")
            
            quality_data = self._calculate_quality_score(analysis)
            analysis["quality_score"] = quality_data["score"]
            analysis["recommendations"] = quality_data["recommendations"]
            
            # 5. Generate Visualizations
            if status_callback:
                status_callback("📊 Generating visualizations...")
            
            visualizations = self._generate_visualizations(analysis)
            analysis["visualizations"] = visualizations
            
            if status_callback:
                status_callback("✅ Code quality analysis complete!")
            
            return analysis
            
        except Exception as e:
            if status_callback:
                status_callback(f"❌ Code quality analysis failed: {str(e)}")
            analysis["error"] = str(e)
            return analysis
    
    def _analyze_code_metrics(self, repo_url: str) -> Dict[str, Any]:
        """Analyze code metrics using MCP tools"""
        try:
            # Get code metrics from MCP server
            metrics_result = self.tools.get_code_metrics(repo_url)
            metrics_data = json.loads(metrics_result) if isinstance(metrics_result, str) else metrics_result
            
            # Extract and enhance metrics
            enhanced_metrics = {
                "total_files": 0,
                "total_lines": 0,
                "code_lines": 0,
                "comment_lines": 0,
                "blank_lines": 0,
                "functions": 0,
                "classes": 0,
                "imports": 0,
                "languages": {},
                "file_types": {},
                "average_file_size": 0,
                "largest_file": "",
                "most_complex_file": ""
            }
            
            if isinstance(metrics_data, dict) and "result" in metrics_data:
                result = metrics_data["result"]
                if isinstance(result, str):
                    # Parse the result string
                    enhanced_metrics.update(self._parse_metrics_string(result))
                elif isinstance(result, dict):
                    enhanced_metrics.update(result)
            
            return enhanced_metrics
            
        except Exception as e:
            return {"error": f"Failed to analyze code metrics: {str(e)}"}
    
    def _analyze_code_complexity(self, repo_url: str) -> Dict[str, Any]:
        """Analyze code complexity using MCP tools"""
        try:
            # Get complexity analysis from MCP server
            complexity_result = self.tools.analyze_code_complexity(repo_url)
            complexity_data = json.loads(complexity_result) if isinstance(complexity_result, str) else complexity_result
            
            # Extract complexity metrics
            complexity_metrics = {
                "cyclomatic_complexity": {},
                "cognitive_complexity": {},
                "nesting_depth": {},
                "function_length": {},
                "class_complexity": {},
                "overall_complexity_score": 0
            }
            
            if isinstance(complexity_data, dict) and "result" in complexity_data:
                result = complexity_data["result"]
                if isinstance(result, str):
                    complexity_metrics.update(self._parse_complexity_string(result))
                elif isinstance(result, dict):
                    complexity_metrics.update(result)
            
            return complexity_metrics
            
        except Exception as e:
            return {"error": f"Failed to analyze code complexity: {str(e)}"}
    
    def _analyze_code_patterns(self, repo_url: str) -> Dict[str, Any]:
        """Analyze code patterns and architecture"""
        try:
            # Get code patterns from MCP server
            patterns_result = self.tools.get_code_patterns(repo_url)
            patterns_data = json.loads(patterns_result) if isinstance(patterns_result, str) else patterns_result
            
            # Extract pattern information
            pattern_analysis = {
                "design_patterns": [],
                "architectural_patterns": [],
                "coding_patterns": [],
                "anti_patterns": [],
                "best_practices": [],
                "code_smells": []
            }
            
            if isinstance(patterns_data, dict) and "result" in patterns_data:
                result = patterns_data["result"]
                if isinstance(result, str):
                    pattern_analysis.update(self._parse_patterns_string(result))
                elif isinstance(result, dict):
                    pattern_analysis.update(result)
            
            # Additional pattern detection
            pattern_analysis.update(self._detect_additional_patterns(repo_url))
            
            return pattern_analysis
            
        except Exception as e:
            return {"error": f"Failed to analyze code patterns: {str(e)}"}
    
    def _detect_additional_patterns(self, repo_url: str) -> Dict[str, Any]:
        """Detect additional patterns using code search"""
        patterns = {
            "async_patterns": [],
            "decorator_patterns": [],
            "type_hints": [],
            "error_handling": [],
            "logging_patterns": [],
            "testing_patterns": []
        }
        
        try:
            # Search for async patterns
            async_result = self.tools.search_code(repo_url, "async def", "python")
            if async_result:
                patterns["async_patterns"] = self._extract_search_results(async_result)
            
            # Search for decorators
            decorator_result = self.tools.search_code(repo_url, "@", "python")
            if decorator_result:
                patterns["decorator_patterns"] = self._extract_search_results(decorator_result)
            
            # Search for type hints
            type_hint_result = self.tools.search_code(repo_url, "->", "python")
            if type_hint_result:
                patterns["type_hints"] = self._extract_search_results(type_hint_result)
            
            # Search for error handling
            error_result = self.tools.search_code(repo_url, "try:", "python")
            if error_result:
                patterns["error_handling"] = self._extract_search_results(error_result)
            
            # Search for logging
            logging_result = self.tools.search_code(repo_url, "log", "")
            if logging_result:
                patterns["logging_patterns"] = self._extract_search_results(logging_result)
            
            # Search for testing
            test_result = self.tools.search_code(repo_url, "test_", "python")
            if test_result:
                patterns["testing_patterns"] = self._extract_search_results(test_result)
            
        except Exception as e:
            patterns["error"] = f"Failed to detect additional patterns: {str(e)}"
        
        return patterns
    
    def _extract_search_results(self, search_result: str) -> List[str]:
        """Extract results from search response"""
        try:
            if isinstance(search_result, str):
                data = json.loads(search_result)
                if isinstance(data, dict) and "result" in data:
                    result = data["result"]
                    if isinstance(result, str):
                        # Parse the result string to extract file paths or matches
                        return [line.strip() for line in result.split('\n') if line.strip()]
                    elif isinstance(result, list):
                        return result
            return []
        except:
            return []
    
    def _calculate_quality_score(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall code quality score"""
        score = 0
        recommendations = []
        
        try:
            metrics = analysis.get("metrics", {})
            complexity = analysis.get("complexity", {})
            patterns = analysis.get("patterns", {})
            
            # Score based on metrics
            if metrics.get("total_lines", 0) > 0:
                comment_ratio = metrics.get("comment_lines", 0) / metrics.get("total_lines", 1)
                if comment_ratio < 0.1:
                    score -= 10
                    recommendations.append("Low comment ratio - consider adding more documentation")
                elif comment_ratio > 0.3:
                    score += 10
                    recommendations.append("Good documentation coverage")
            
            # Score based on complexity
            overall_complexity = complexity.get("overall_complexity_score", 0)
            if overall_complexity > 7:
                score -= 15
                recommendations.append("High code complexity - consider refactoring complex functions")
            elif overall_complexity < 3:
                score += 10
                recommendations.append("Good code complexity management")
            
            # Score based on patterns
            anti_patterns = patterns.get("anti_patterns", [])
            if anti_patterns:
                score -= len(anti_patterns) * 5
                recommendations.append(f"Found {len(anti_patterns)} anti-patterns - consider refactoring")
            
            best_practices = patterns.get("best_practices", [])
            if best_practices:
                score += len(best_practices) * 2
                recommendations.append(f"Good use of {len(best_practices)} best practices")
            
            # Normalize score to 0-100
            score = max(0, min(100, score + 50))  # Start at 50 and adjust
            
        except Exception as e:
            score = 50
            recommendations.append(f"Error calculating quality score: {str(e)}")
        
        return {
            "score": score,
            "recommendations": recommendations
        }
    
    def _generate_visualizations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate interactive visualizations for code analysis"""
        visualizations = {}
        
        try:
            metrics = analysis.get("metrics", {})
            complexity = analysis.get("complexity", {})
            patterns = analysis.get("patterns", {})
            
            # 1. Code Metrics Pie Chart
            if metrics.get("total_lines", 0) > 0:
                fig_metrics = go.Figure(data=[go.Pie(
                    labels=['Code Lines', 'Comment Lines', 'Blank Lines'],
                    values=[
                        metrics.get("code_lines", 0),
                        metrics.get("comment_lines", 0),
                        metrics.get("blank_lines", 0)
                    ],
                    hole=0.3
                )])
                fig_metrics.update_layout(title="Code Line Distribution")
                visualizations["code_metrics_pie"] = fig_metrics.to_json()
            
            # 2. Complexity Distribution
            if complexity.get("cyclomatic_complexity"):
                complexity_values = list(complexity["cyclomatic_complexity"].values())
                if complexity_values:
                    fig_complexity = px.histogram(
                        x=complexity_values,
                        title="Cyclomatic Complexity Distribution",
                        labels={'x': 'Complexity', 'y': 'Count'}
                    )
                    visualizations["complexity_distribution"] = fig_complexity.to_json()
            
            # 3. Quality Score Gauge
            quality_score = analysis.get("quality_score", 50)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=quality_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Code Quality Score"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgray"},
                        {'range': [30, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            visualizations["quality_gauge"] = fig_gauge.to_json()
            
            # 4. Pattern Analysis Bar Chart
            pattern_counts = {
                "Design Patterns": len(patterns.get("design_patterns", [])),
                "Anti-Patterns": len(patterns.get("anti_patterns", [])),
                "Best Practices": len(patterns.get("best_practices", [])),
                "Code Smells": len(patterns.get("code_smells", []))
            }
            
            fig_patterns = px.bar(
                x=list(pattern_counts.keys()),
                y=list(pattern_counts.values()),
                title="Code Pattern Analysis",
                labels={'x': 'Pattern Type', 'y': 'Count'}
            )
            visualizations["pattern_analysis"] = fig_patterns.to_json()
            
        except Exception as e:
            visualizations["error"] = f"Failed to generate visualizations: {str(e)}"
        
        return visualizations
    
    def _parse_metrics_string(self, metrics_str: str) -> Dict[str, Any]:
        """Parse metrics from string response"""
        metrics = {}
        try:
            # Extract numbers from the string
            lines_match = re.search(r'(\d+)\s*(?:total\s*)?lines?', metrics_str, re.IGNORECASE)
            if lines_match:
                metrics["total_lines"] = int(lines_match.group(1))
            
            files_match = re.search(r'(\d+)\s*files?', metrics_str, re.IGNORECASE)
            if files_match:
                metrics["total_files"] = int(files_match.group(1))
            
            functions_match = re.search(r'(\d+)\s*functions?', metrics_str, re.IGNORECASE)
            if functions_match:
                metrics["functions"] = int(functions_match.group(1))
            
            classes_match = re.search(r'(\d+)\s*classes?', metrics_str, re.IGNORECASE)
            if classes_match:
                metrics["classes"] = int(classes_match.group(1))
            
        except Exception as e:
            metrics["parse_error"] = str(e)
        
        return metrics
    
    def _parse_complexity_string(self, complexity_str: str) -> Dict[str, Any]:
        """Parse complexity from string response"""
        complexity = {}
        try:
            # Extract complexity scores
            score_match = re.search(r'complexity\s*score[:\s]*(\d+(?:\.\d+)?)', complexity_str, re.IGNORECASE)
            if score_match:
                complexity["overall_complexity_score"] = float(score_match.group(1))
            
        except Exception as e:
            complexity["parse_error"] = str(e)
        
        return complexity
    
    def _parse_patterns_string(self, patterns_str: str) -> Dict[str, Any]:
        """Parse patterns from string response"""
        patterns = {}
        try:
            # Extract pattern information
            design_patterns = re.findall(r'design\s*pattern[:\s]*([^\n]+)', patterns_str, re.IGNORECASE)
            patterns["design_patterns"] = [p.strip() for p in design_patterns]
            
            anti_patterns = re.findall(r'anti\s*pattern[:\s]*([^\n]+)', patterns_str, re.IGNORECASE)
            patterns["anti_patterns"] = [p.strip() for p in anti_patterns]
            
        except Exception as e:
            patterns["parse_error"] = str(e)
        
        return patterns

# Global analyzer instance
_code_analyzer = None

def get_code_analyzer() -> CodeAnalyzer:
    """Get the global code analyzer instance"""
    global _code_analyzer
    if _code_analyzer is None:
        _code_analyzer = CodeAnalyzer()
    return _code_analyzer

def analyze_code_quality(repo_url: str, status_callback=None) -> Dict[str, Any]:
    """Analyze code quality for a repository"""
    analyzer = get_code_analyzer()
    return analyzer.analyze_code_quality(repo_url, status_callback) 