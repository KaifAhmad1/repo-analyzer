"""
Comprehensive Analysis Interface for GitHub Repository Analyzer
Provides systematic repository analysis with multiple analysis types and visualizations
"""

import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, Callable
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from ..analysis.analysis_engine import (
    analyze_repository,
    quick_analysis,
    security_analysis,
    code_quality_analysis,
    generate_visualizations,
    smart_summarization
)
from ..utils.config import get_analysis_presets, get_analysis_settings
from ..utils.repository_manager import get_repository_manager, get_analysis_history

def render_analysis_interface(repo_url: Optional[str] = None) -> None:
    """Render the comprehensive analysis interface"""
    
    if not repo_url:
        st.info("🎯 Please select a repository to start systematic analysis.")
        return
    
    st.markdown("### 🔍 Systematic Repository Analysis")
    st.markdown("Choose your analysis type and get comprehensive insights about the repository.")
    
    # Get analysis presets and settings
    presets = get_analysis_presets()
    settings = get_analysis_settings()
    
    # Analysis Type Selection
    st.markdown("#### 📊 Analysis Types")
    
    # Create tabs for different analysis types
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🚀 Quick Overview", 
        "🔍 Comprehensive", 
        "🔒 Security", 
        "📊 Code Quality",
        "🗺️ Visualizations",
        "🧠 Smart Summary",
        "📈 History"
    ])
    
    with tab1:
        render_quick_analysis_tab(repo_url)
    
    with tab2:
        render_comprehensive_analysis_tab(repo_url, presets)
    
    with tab3:
        render_security_analysis_tab(repo_url)
    
    with tab4:
        render_code_quality_tab(repo_url)
    
    with tab5:
        render_visualizations_tab(repo_url)
    
    with tab6:
        render_smart_summary_tab(repo_url)
    
    with tab7:
        render_analysis_history_tab(repo_url)

def render_quick_analysis_tab(repo_url: str) -> None:
    """Render quick analysis tab"""
    st.markdown("#### ⚡ Quick Repository Overview")
    st.markdown("Get a fast overview of the repository with basic insights.")
    
    if st.button("🚀 Start Quick Analysis", type="primary", use_container_width=True):
        with st.spinner("⚡ Performing quick analysis..."):
            def status_callback(msg):
                st.text(msg)
            
            result = quick_analysis(repo_url, status_callback)
            display_quick_analysis_results(result)

def render_comprehensive_analysis_tab(repo_url: str, presets: Dict[str, Any]) -> None:
    """Render comprehensive analysis tab"""
    st.markdown("#### 🔍 Comprehensive Repository Analysis")
    st.markdown("Get detailed insights with multiple analysis dimensions.")
    
    # Preset selection
    preset_options = {preset["name"]: preset_id for preset_id, preset in presets.items()}
    selected_preset = st.selectbox(
        "Choose Analysis Preset:",
        options=list(preset_options.keys()),
        format_func=lambda x: f"{x} - {presets[preset_options[x]]['description']}"
    )
    
    # Analysis options
    col1, col2 = st.columns(2)
    with col1:
        include_metrics = st.checkbox("Include Code Metrics", value=True)
        include_security = st.checkbox("Include Security Analysis", value=True)
    with col2:
        include_dependencies = st.checkbox("Include Dependency Analysis", value=True)
        include_commits = st.checkbox("Include Commit History", value=True)
    
    if st.button("🔍 Start Comprehensive Analysis", type="primary", use_container_width=True):
        preset_id = preset_options[selected_preset]
        
        with st.spinner("🔍 Performing comprehensive analysis..."):
            def status_callback(msg):
                st.text(msg)
            
            result = analyze_repository(repo_url, "comprehensive", preset_id, status_callback)
            display_comprehensive_analysis_results(result)

def render_security_analysis_tab(repo_url: str) -> None:
    """Render security analysis tab"""
    st.markdown("#### 🔒 Security Analysis")
    st.markdown("Analyze security aspects and potential vulnerabilities.")
    
    # Security analysis options
    col1, col2 = st.columns(2)
    with col1:
        check_dependencies = st.checkbox("Check Dependency Vulnerabilities", value=True)
        check_patterns = st.checkbox("Check Security Patterns", value=True)
    with col2:
        check_credentials = st.checkbox("Check for Hardcoded Credentials", value=True)
        check_permissions = st.checkbox("Check File Permissions", value=True)
    
    if st.button("🔒 Start Security Analysis", type="primary", use_container_width=True):
        with st.spinner("🔒 Performing security analysis..."):
            def status_callback(msg):
                st.text(msg)
            
            result = security_analysis(repo_url, status_callback)
            display_security_analysis_results(result)

def render_code_quality_tab(repo_url: str) -> None:
    """Render code quality analysis tab"""
    st.markdown("#### 📊 Code Quality Analysis")
    st.markdown("Analyze code quality, patterns, and best practices.")
    
    # Quality analysis options
    col1, col2 = st.columns(2)
    with col1:
        analyze_patterns = st.checkbox("Analyze Code Patterns", value=True)
        check_documentation = st.checkbox("Check Documentation", value=True)
    with col2:
        analyze_testing = st.checkbox("Analyze Testing", value=True)
        check_metrics = st.checkbox("Check Code Metrics", value=True)
    
    if st.button("📊 Start Code Quality Analysis", type="primary", use_container_width=True):
        with st.spinner("📊 Performing code quality analysis..."):
            def status_callback(msg):
                st.text(msg)
            
            result = code_quality_analysis(repo_url, status_callback)
            display_code_quality_results(result)

def render_visualizations_tab(repo_url: str) -> None:
    """Render repository visualizations tab"""
    st.markdown("#### 🗺️ Repository Visualizations")
    st.markdown("Generate interactive visualizations and repository maps.")
    
    # Visualization options
    col1, col2 = st.columns(2)
    with col1:
        include_tree = st.checkbox("Directory Tree", value=True)
        include_structure = st.checkbox("File Structure", value=True)
        include_dependencies = st.checkbox("Dependency Graph", value=True)
    with col2:
        include_heatmap = st.checkbox("Activity Heatmap", value=True)
        include_languages = st.checkbox("Language Distribution", value=True)
        include_sizes = st.checkbox("File Size Distribution", value=True)
    
    if st.button("🗺️ Generate Visualizations", type="primary", use_container_width=True):
        with st.spinner("🗺️ Generating visualizations..."):
            def status_callback(msg):
                st.text(msg)
            
            result = generate_visualizations(repo_url, status_callback)
            display_visualization_results(result)

def render_smart_summary_tab(repo_url: str) -> None:
    """Render smart summarization tab"""
    st.markdown("#### 🧠 Smart Repository Summarization")
    st.markdown("Generate comprehensive AI-powered summaries with deep insights.")
    
    # Summary options
    col1, col2 = st.columns(2)
    with col1:
        include_overview = st.checkbox("Project Overview", value=True)
        include_architecture = st.checkbox("Architecture Analysis", value=True)
        include_quality = st.checkbox("Code Quality Assessment", value=True)
    with col2:
        include_dependencies = st.checkbox("Dependency Analysis", value=True)
        include_patterns = st.checkbox("Code Patterns", value=True)
        include_recommendations = st.checkbox("Recommendations", value=True)
    
    if st.button("🧠 Generate Smart Summary", type="primary", use_container_width=True):
        with st.spinner("🧠 Generating smart summary..."):
            def status_callback(msg):
                st.text(msg)
            
            result = smart_summarization(repo_url, status_callback)
            display_smart_summary_results(result)

def render_analysis_history_tab(repo_url: str) -> None:
    """Render analysis history tab"""
    st.markdown("#### 📈 Analysis History")
    st.markdown("View previous analysis results and track progress.")
    
    # Get analysis history
    history = get_analysis_history()
    
    if not history:
        st.info("📝 No analysis history found. Run an analysis to see results here.")
        return
    
    # Display history
    for entry in reversed(history):
        with st.expander(f"📊 {entry['type'].title()} Analysis - {entry['timestamp']}"):
            display_analysis_entry(entry)

def display_quick_analysis_results(result: Dict[str, Any]) -> None:
    """Display quick analysis results"""
    if "error" in result:
        st.error(f"❌ Analysis failed: {result['error']}")
        return
    
    st.success(f"✅ Quick analysis completed in {result.get('duration', 0):.2f} seconds")
    
    # Display performance statistics if available
    if "performance_stats" in result:
        perf_stats = result["performance_stats"]
        st.markdown("#### 📊 Performance Statistics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Calls", perf_stats.get("total_calls", 0))
        with col2:
            st.metric("Cache Hit Rate", perf_stats.get("cache_hit_rate", "0%"))
        with col3:
            st.metric("Avg Call Time", perf_stats.get("average_call_time", "0s"))
        
        # Show performance insights
        if "execution_time" in result:
            st.info(f"⚡ Data gathering completed in {result['execution_time']:.2f}s")
    
    # Display tool utilization
    if "tools_used" in result and result["tools_used"]:
        st.markdown("#### 🔧 Tools Used")
        tools_used = result["tools_used"]
        
        # Group tools by server
        server_tools = {}
        for tool in tools_used:
            if '.' in tool:
                server, tool_name = tool.split('.', 1)
                if server not in server_tools:
                    server_tools[server] = []
                server_tools[server].append(tool_name)
            else:
                if 'unknown' not in server_tools:
                    server_tools['unknown'] = []
                server_tools['unknown'].append(tool)
        
        # Display grouped by server
        for server, tools in server_tools.items():
            server_icon = {
                'file_content': '📄',
                'repository_structure': '📁',
                'commit_history': '📝',
                'code_search': '🔍',
                'unknown': '❓'
            }.get(server, '🔧')
            
            st.markdown(f"**{server_icon} {server.replace('_', ' ').title()} Server:**")
            st.write(f"  - {', '.join(tools)}")
            st.markdown("")
    
    # Display sections
    sections = result.get("sections", {})
    
    # Repository Info
    if "repository_info" in sections:
        repo_info = sections["repository_info"]
        if not isinstance(repo_info, dict) or "error" in repo_info:
            st.warning("⚠️ Could not fetch repository information")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⭐ Stars", repo_info.get("stars", 0))
            with col2:
                st.metric("🍴 Forks", repo_info.get("forks", 0))
            with col3:
                st.metric("👀 Watchers", repo_info.get("watchers", 0))
    
    # AI Summary
    if "ai_summary" in sections:
        ai_summary = sections["ai_summary"]
        if isinstance(ai_summary, dict) and "summary" in ai_summary:
            st.markdown("#### 🤖 AI Summary")
            st.write(ai_summary["summary"])
    
    # File Structure
    if "file_structure" in sections:
        file_structure = sections["file_structure"]
        if isinstance(file_structure, dict) and "result" in file_structure:
            st.markdown("#### 📁 File Structure")
            st.json(file_structure["result"])

def display_comprehensive_analysis_results(result: Dict[str, Any]) -> None:
    """Display comprehensive analysis results"""
    if "error" in result:
        st.error(f"❌ Analysis failed: {result['error']}")
        return
    
    st.success(f"✅ Comprehensive analysis completed in {result.get('duration', 0):.2f} seconds")
    
    # Display tool utilization
    if "tools_used" in result and result["tools_used"]:
        st.markdown("#### 🔧 Tools Used")
        tools_used = result["tools_used"]
        
        # Group tools by server
        server_tools = {}
        for tool in tools_used:
            if '.' in tool:
                server, tool_name = tool.split('.', 1)
                if server not in server_tools:
                    server_tools[server] = []
                server_tools[server].append(tool_name)
            else:
                if 'unknown' not in server_tools:
                    server_tools['unknown'] = []
                server_tools['unknown'].append(tool)
        
        # Display grouped by server
        for server, tools in server_tools.items():
            server_icon = {
                'file_content': '📄',
                'repository_structure': '📁',
                'commit_history': '📝',
                'code_search': '🔍',
                'unknown': '❓'
            }.get(server, '🔧')
            
            st.markdown(f"**{server_icon} {server.replace('_', ' ').title()} Server:**")
            for tool in tools:
                st.write(f"  - {tool}")
            st.markdown("")
    
    # Display sections
    sections = result.get("sections", {})
    
    # Create tabs for different sections
    tab_names = list(sections.keys())
    if tab_names:
        tabs = st.tabs([name.replace("_", " ").title() for name in tab_names])
        
        for i, (section_name, section_data) in enumerate(sections.items()):
            with tabs[i]:
                display_analysis_section(section_name, section_data)

def display_security_analysis_results(result: Dict[str, Any]) -> None:
    """Display security analysis results"""
    if "error" in result:
        st.error(f"❌ Security analysis failed: {result['error']}")
        return
    
    st.success(f"✅ Security analysis completed in {result.get('duration', 0):.2f} seconds")
    
    # Display tool utilization
    if "tools_used" in result and result["tools_used"]:
        st.markdown("#### 🔧 Tools Used")
        tools_used = result["tools_used"]
        
        # Group tools by server
        server_tools = {}
        for tool in tools_used:
            if '.' in tool:
                server, tool_name = tool.split('.', 1)
                if server not in server_tools:
                    server_tools[server] = []
                server_tools[server].append(tool_name)
            else:
                if 'unknown' not in server_tools:
                    server_tools['unknown'] = []
                server_tools['unknown'].append(tool)
        
        # Display grouped by server
        for server, tools in server_tools.items():
            server_icon = {
                'file_content': '📄',
                'repository_structure': '📁',
                'commit_history': '📝',
                'code_search': '🔍',
                'unknown': '❓'
            }.get(server, '🔧')
            
            st.markdown(f"**{server_icon} {server.replace('_', ' ').title()} Server:**")
            for tool in tools:
                st.write(f"  - {tool}")
            st.markdown("")
    
    sections = result.get("sections", {})
    
    # Security Risk Level
    if "security" in sections:
        security_data = sections["security"]
        if isinstance(security_data, dict) and "risk_level" in security_data:
            risk_level = security_data["risk_level"]
            risk_color = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(risk_level, "⚪")
            st.metric("🔒 Security Risk Level", f"{risk_color} {risk_level.upper()}")
    
    # Security Patterns
    if "security" in sections:
        security_data = sections["security"]
        if isinstance(security_data, dict) and "security_patterns" in security_data:
            patterns = security_data["security_patterns"]
            st.markdown("#### 🔍 Security Patterns Found")
            
            for pattern_name, pattern_data in patterns.items():
                if pattern_data and isinstance(pattern_data, dict) and pattern_data.get("result"):
                    st.warning(f"⚠️ {pattern_name.replace('_', ' ').title()}")
                    st.json(pattern_data["result"])

def display_code_quality_results(result: Dict[str, Any]) -> None:
    """Display code quality analysis results"""
    if "error" in result:
        st.error(f"❌ Code quality analysis failed: {result['error']}")
        return
    
    st.success(f"✅ Code quality analysis completed in {result.get('duration', 0):.2f} seconds")
    
    # Display tool utilization
    if "tools_used" in result and result["tools_used"]:
        st.markdown("#### 🔧 Tools Used")
        tools_used = result["tools_used"]
        
        # Group tools by server
        server_tools = {}
        for tool in tools_used:
            if '.' in tool:
                server, tool_name = tool.split('.', 1)
                if server not in server_tools:
                    server_tools[server] = []
                server_tools[server].append(tool_name)
            else:
                if 'unknown' not in server_tools:
                    server_tools['unknown'] = []
                server_tools['unknown'].append(tool)
        
        # Display grouped by server
        for server, tools in server_tools.items():
            server_icon = {
                'file_content': '📄',
                'repository_structure': '📁',
                'commit_history': '📝',
                'code_search': '🔍',
                'unknown': '❓'
            }.get(server, '🔧')
            
            st.markdown(f"**{server_icon} {server.replace('_', ' ').title()} Server:**")
            st.write(f"  - {', '.join(tools)}")
            st.markdown("")
    
    sections = result.get("sections", {})
    
    # Code Metrics
    if "code_metrics" in sections:
        metrics_data = sections["code_metrics"]
        if isinstance(metrics_data, dict) and "metrics" in metrics_data:
            metrics = metrics_data["metrics"]
            if isinstance(metrics, dict) and "result" in metrics:
                st.markdown("#### 📊 Code Metrics")
                st.json(metrics["result"])
    
    # Code Patterns
    if "code_patterns" in sections:
        patterns_data = sections["code_patterns"]
        if isinstance(patterns_data, dict) and "code_patterns" in patterns_data:
            patterns = patterns_data["code_patterns"]
            st.markdown("#### 🔍 Code Patterns")
            
            for pattern_name, pattern_data in patterns.items():
                if pattern_data and isinstance(pattern_data, dict) and pattern_data.get("result"):
                    st.info(f"📝 {pattern_name.replace('_', ' ').title()}")
                    st.json(pattern_data["result"])

def display_analysis_section(section_name: str, section_data: Any) -> None:
    """Display a specific analysis section"""
    if not section_data:
        st.info("No data available for this section.")
        return
    
    if isinstance(section_data, dict) and "error" in section_data:
        st.error(f"Error in {section_name}: {section_data['error']}")
        return
    
    # Handle different section types
    if section_name == "repository_info":
        display_repository_info(section_data)
    elif section_name == "file_structure":
        display_file_structure(section_data)
    elif section_name == "code_metrics":
        display_code_metrics(section_data)
    elif section_name == "dependencies":
        display_dependencies(section_data)
    elif section_name == "commit_history":
        display_commit_history(section_data)
    elif section_name == "security":
        display_security_data(section_data)
    elif section_name == "ai_summary":
        display_ai_summary(section_data)
    else:
        st.json(section_data)

def display_repository_info(info: Dict[str, Any]) -> None:
    """Display repository information"""
    if not isinstance(info, dict):
        st.json(info)
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Name", info.get("name", "N/A"))
        st.metric("Language", info.get("language", "N/A"))
        st.metric("Stars", info.get("stars", 0))
        st.metric("Forks", info.get("forks", 0))
    
    with col2:
        st.metric("Watchers", info.get("watchers", 0))
        st.metric("Open Issues", info.get("open_issues", 0))
        st.metric("Size", f"{info.get('size', 0)} KB")
        st.metric("License", info.get("license", "N/A"))
    
    if info.get("description"):
        st.markdown("#### Description")
        st.write(info["description"])
    
    if info.get("topics"):
        st.markdown("#### Topics")
        for topic in info["topics"]:
            st.markdown(f"`{topic}`")

def display_file_structure(structure: Dict[str, Any]) -> None:
    """Display file structure"""
    if not isinstance(structure, dict):
        st.json(structure)
        return
    
    if "directory_tree" in structure:
        tree_data = structure["directory_tree"]
        if isinstance(tree_data, dict) and "result" in tree_data:
            st.markdown("#### Directory Tree")
            st.code(tree_data["result"], language="text")
    
    if "file_structure" in structure:
        file_data = structure["file_structure"]
        if isinstance(file_data, dict) and "result" in file_data:
            st.markdown("#### File Structure")
            st.json(file_data["result"])

def display_code_metrics(metrics: Dict[str, Any]) -> None:
    """Display code metrics"""
    if not isinstance(metrics, dict):
        st.json(metrics)
        return
    
    if "metrics" in metrics:
        metrics_data = metrics["metrics"]
        if isinstance(metrics_data, dict) and "result" in metrics_data:
            st.markdown("#### Code Metrics")
            st.json(metrics_data["result"])
    
    if "patterns" in metrics:
        patterns_data = metrics["patterns"]
        st.markdown("#### Code Patterns")
        for pattern_name, pattern_data in patterns_data.items():
            if pattern_data and isinstance(pattern_data, dict) and pattern_data.get("result"):
                st.markdown(f"**{pattern_name.replace('_', ' ').title()}**")
                st.json(pattern_data["result"])

def display_dependencies(dependencies: Dict[str, Any]) -> None:
    """Display dependencies"""
    if not isinstance(dependencies, dict):
        st.json(dependencies)
        return
    
    if "dependency_files" in dependencies:
        files_data = dependencies["dependency_files"]
        st.markdown("#### Dependency Files")
        for file_name, file_data in files_data.items():
            if file_data and isinstance(file_data, dict) and file_data.get("result"):
                st.markdown(f"**{file_name}**")
                st.code(file_data["result"], language="text")

def display_commit_history(history: Dict[str, Any]) -> None:
    """Display commit history"""
    if not isinstance(history, dict):
        st.json(history)
        return
    
    if "recent_commits" in history:
        commits_data = history["recent_commits"]
        if isinstance(commits_data, dict) and "result" in commits_data:
            st.markdown("#### Recent Commits")
            st.json(commits_data["result"])

def display_security_data(security: Dict[str, Any]) -> None:
    """Display security data"""
    if not isinstance(security, dict):
        st.json(security)
        return
    
    if "risk_level" in security:
        risk_level = security["risk_level"]
        risk_color = {"low": "green", "medium": "orange", "high": "red"}.get(risk_level, "gray")
        st.metric("🔒 Security Risk Level", risk_level.upper(), delta_color=risk_color)
    
    if "security_patterns" in security:
        patterns = security["security_patterns"]
        st.markdown("#### Security Patterns")
        for pattern_name, pattern_data in patterns.items():
            if pattern_data and isinstance(pattern_data, dict) and pattern_data.get("result"):
                st.warning(f"⚠️ {pattern_name.replace('_', ' ').title()}")
                st.json(pattern_data["result"])

def display_ai_summary(summary: Dict[str, Any]) -> None:
    """Display AI summary"""
    if not isinstance(summary, dict):
        st.json(summary)
        return
    
    if "summary" in summary:
        st.markdown("#### 🤖 AI Summary")
        st.write(summary["summary"])
    
    if "tools_used" in summary:
        st.markdown("#### 🔧 Tools Used")
        for tool in summary["tools_used"]:
            st.markdown(f"- {tool}")

def display_analysis_entry(entry: Dict[str, Any]) -> None:
    """Display a single analysis history entry"""
    st.markdown(f"**Type:** {entry['type']}")
    st.markdown(f"**Timestamp:** {entry['timestamp']}")
    
    if "tools_used" in entry:
        st.markdown("**Tools Used:**")
        for tool in entry["tools_used"]:
            st.markdown(f"- {tool}")
    
    if "result" in entry:
        result = entry["result"]
        if isinstance(result, dict) and "sections" in result:
            sections = result["sections"]
            if "ai_summary" in sections:
                ai_summary = sections["ai_summary"]
                if isinstance(ai_summary, dict) and "summary" in ai_summary:
                    st.markdown("**Summary:**")
                    st.write(ai_summary["summary"])
    
    if st.button("View Full Results", key=f"view_{entry['timestamp']}"):
        st.json(entry["result"])

def display_visualization_results(result: Dict[str, Any]) -> None:
    """Display visualization results"""
    if "error" in result:
        st.error(f"❌ Visualization generation failed: {result['error']}")
        return
    
    st.success(f"✅ Visualizations generated in {result.get('duration', 0):.2f} seconds")
    
    # Display tool utilization
    if "tools_used" in result and result["tools_used"]:
        st.markdown("#### 🔧 Tools Used")
        tools_used = result["tools_used"]
        
        # Group tools by server
        server_tools = {}
        for tool in tools_used:
            if '.' in tool:
                server, tool_name = tool.split('.', 1)
                if server not in server_tools:
                    server_tools[server] = []
                server_tools[server].append(tool_name)
            else:
                if 'unknown' not in server_tools:
                    server_tools['unknown'] = []
                server_tools['unknown'].append(tool)
        
        # Display grouped by server
        for server, tools in server_tools.items():
            server_icon = {
                'file_content': '📄',
                'repository_structure': '📁',
                'commit_history': '📝',
                'code_search': '🔍',
                'unknown': '❓'
            }.get(server, '🔧')
            
            st.markdown(f"**{server_icon} {server.replace('_', ' ').title()} Server:**")
            st.write(f"  - {', '.join(tools)}")
            st.markdown("")
    
    # Display sections
    sections = result.get("sections", {})
    
    if "visualizations" in sections:
        viz_data = sections["visualizations"]
        if isinstance(viz_data, dict):
            # Directory Tree
            if "directory_tree" in viz_data and viz_data["directory_tree"]:
                st.markdown("#### 📁 Directory Tree")
                tree_viz = viz_data["directory_tree"]
                if isinstance(tree_viz, dict) and "data" in tree_viz:
                    try:
                        fig = go.Figure.from_json(tree_viz["data"])
                        st.plotly_chart(fig, use_container_width=True)
                    except:
                        st.write("Could not display directory tree")
            
            # File Structure
            if "file_structure" in viz_data and viz_data["file_structure"]:
                st.markdown("#### 📊 File Structure")
                structure_viz = viz_data["file_structure"]
                if isinstance(structure_viz, dict) and "data" in structure_viz:
                    try:
                        fig = go.Figure.from_json(structure_viz["data"])
                        st.plotly_chart(fig, use_container_width=True)
                    except:
                        st.write("Could not display file structure")
            
            # Dependency Graph
            if "dependency_graph" in viz_data and viz_data["dependency_graph"]:
                st.markdown("#### 🔗 Dependency Graph")
                dep_viz = viz_data["dependency_graph"]
                if isinstance(dep_viz, dict) and "data" in dep_viz:
                    try:
                        fig = go.Figure.from_json(dep_viz["data"])
                        st.plotly_chart(fig, use_container_width=True)
                    except:
                        st.write("Could not display dependency graph")
            
            # Language Distribution
            if "language_distribution" in viz_data and viz_data["language_distribution"]:
                st.markdown("#### 🌐 Language Distribution")
                lang_viz = viz_data["language_distribution"]
                if isinstance(lang_viz, dict) and "data" in lang_viz:
                    try:
                        fig = go.Figure.from_json(lang_viz["data"])
                        st.plotly_chart(fig, use_container_width=True)
                    except:
                        st.write("Could not display language distribution")
            
            # Activity Heatmap
            if "code_heatmap" in viz_data and viz_data["code_heatmap"]:
                st.markdown("#### 📈 Activity Heatmap")
                heatmap_viz = viz_data["code_heatmap"]
                if isinstance(heatmap_viz, dict) and "data" in heatmap_viz:
                    try:
                        fig = go.Figure.from_json(heatmap_viz["data"])
                        st.plotly_chart(fig, use_container_width=True)
                    except:
                        st.write("Could not display activity heatmap")

def display_smart_summary_results(result: Dict[str, Any]) -> None:
    """Display smart summarization results"""
    if "error" in result:
        st.error(f"❌ Smart summarization failed: {result['error']}")
        return
    
    st.success(f"✅ Smart summarization completed in {result.get('duration', 0):.2f} seconds")
    
    # Display tool utilization
    if "tools_used" in result and result["tools_used"]:
        st.markdown("#### 🔧 Tools Used")
        tools_used = result["tools_used"]
        
        # Group tools by server
        server_tools = {}
        for tool in tools_used:
            if '.' in tool:
                server, tool_name = tool.split('.', 1)
                if server not in server_tools:
                    server_tools[server] = []
                server_tools[server].append(tool_name)
            else:
                if 'unknown' not in server_tools:
                    server_tools['unknown'] = []
                server_tools['unknown'].append(tool)
        
        # Display grouped by server
        for server, tools in server_tools.items():
            server_icon = {
                'file_content': '📄',
                'repository_structure': '📁',
                'commit_history': '📝',
                'code_search': '🔍',
                'unknown': '❓'
            }.get(server, '🔧')
            
            st.markdown(f"**{server_icon} {server.replace('_', ' ').title()} Server:**")
            st.write(f"  - {', '.join(tools)}")
            st.markdown("")
    
    # Display sections
    sections = result.get("sections", {})
    
    # AI Summary (comprehensive)
    if "ai_summary" in sections:
        ai_summary = sections["ai_summary"]
        if isinstance(ai_summary, dict) and "summary" in ai_summary:
            st.markdown("#### 🧠 AI-Powered Comprehensive Summary")
            st.markdown(ai_summary["summary"])
            
            # Tools used
            if "tools_used" in ai_summary:
                st.markdown("**🔧 Analysis Tools Used:**")
                tools = ai_summary["tools_used"]
                if isinstance(tools, list):
                    for tool in tools:
                        st.write(f"• {tool}")
    
    # Overview
    if "overview" in sections:
        st.markdown("#### 📋 Project Overview")
        display_repository_info(sections["overview"])
    
    # Structure
    if "structure" in sections:
        st.markdown("#### 🏗️ Architecture & Structure")
        display_file_structure(sections["structure"])
    
    # Metrics
    if "metrics" in sections:
        st.markdown("#### 📊 Code Metrics")
        display_code_metrics(sections["metrics"])
    
    # Dependencies
    if "dependencies" in sections:
        st.markdown("#### 📦 Dependencies")
        display_dependencies(sections["dependencies"])
    
    # Patterns
    if "patterns" in sections:
        st.markdown("#### 🔍 Code Patterns")
        patterns = sections["patterns"]
        if isinstance(patterns, dict) and "code_patterns" in patterns:
            for pattern_type, pattern_data in patterns["code_patterns"].items():
                st.write(f"**{pattern_type.title()}:**")
                if isinstance(pattern_data, dict) and "result" in pattern_data:
                    st.code(pattern_data["result"][:300] + "..." if len(str(pattern_data["result"])) > 300 else pattern_data["result"]) 