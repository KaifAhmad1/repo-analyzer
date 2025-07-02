"""
🚀 GitHub Repository Analyzer - Clean & Simple
A streamlined interface for analyzing GitHub repositories using FastMCP v2 servers and Groq AI
"""

import streamlit as st
import os
from datetime import datetime
from src.ui.repository_selector import render_repository_selector
from src.ui.chat_interface import render_chat_interface
from src.agent.ai_agent import (
    get_repository_overview, 
    analyze_repository, 
    FastMCPTools,
    ask_repository_question,
    generate_repository_summary,
    analyze_repository_patterns,
    create_analyzer_agent,
    quick_repository_analysis
)
from src.servers.server_manager import get_servers_status, start_mcp_servers

def display_tools_used(tools_used):
    """Helper function to display tools used grouped by server"""
    if not tools_used:
        return
    
    st.markdown("#### 🔧 Analysis Tools Used:")
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
            st.markdown(f"  - {tool}")
        st.markdown("")

# Page config
st.set_page_config(
    page_title="🚀 GitHub Repository Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("src/ui/modern_styles.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_repo' not in st.session_state:
    st.session_state.current_repo = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'processing' not in st.session_state:
    st.session_state.processing = False

# --- SIDEBAR ---
with st.sidebar:
    # Repository Selector Section
    st.markdown("## 📁 Repository")
    repo_url = render_repository_selector()
    
    # Repository Info
    if repo_url and repo_url != st.session_state.get('current_repo'):
        st.session_state.current_repo = repo_url
        try:
            repo_info = get_repository_overview(repo_url)
            # Handle both old string format and new tuple format
            if isinstance(repo_info, tuple):
                repo_info_text, tools_used = repo_info
                if isinstance(repo_info_text, str):
                    import json
                    try:
                        repo_info = json.loads(repo_info_text)
                    except:
                        repo_info = {"name": "Repository", "description": repo_info_text}
            elif isinstance(repo_info, str):
                import json
                try:
                    repo_info = json.loads(repo_info)
                except:
                    repo_info = {"name": "Repository", "description": repo_info}
            
            if repo_info and isinstance(repo_info, dict):
                st.markdown("### 📋 Repository Info")
                st.markdown(f"**{repo_info.get('name', 'Repository')}**")
                st.caption(repo_info.get('description', 'No description'))
                st.write(f"⭐ {repo_info.get('stars', 0)} | 🍴 {repo_info.get('forks', 0)} | 🕒 Updated: {repo_info.get('last_updated', repo_info.get('updated_at', ''))}")
        except Exception as e:
            st.error(f"❌ Error loading repository: {str(e)}")
    
    st.markdown("---")
    
    # Settings Section
    from src.ui.settings_sidebar import render_settings_sidebar
    settings = render_settings_sidebar()
    
    # Auto-start servers if not running
    if settings.get("system_health", 0) < 100:
        if st.button("🚀 Auto-Start Servers", use_container_width=True):
            with st.spinner("🔄 Starting MCP servers..."):
                start_mcp_servers()
                st.rerun()

# --- MAIN AREA ---
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🚀 GitHub Repository Analyzer</h1>
    <p class="header-subtitle">AI-Powered Repository Analysis with FastMCP v2 & Groq</p>
</div>
""", unsafe_allow_html=True)

# System Status Banner
server_status = get_servers_status()
if server_status['running_servers'] < server_status['total_servers']:
    st.warning(f"⚠️ {server_status['total_servers'] - server_status['running_servers']} MCP servers are offline. Some features may be limited.")

# Enhanced System Status Display
st.markdown("### 🔧 System Status")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🖥️ Total Servers", server_status['total_servers'])
with col2:
    st.metric("✅ Running", server_status['running_servers'])
with col3:
    st.metric("❌ Offline", server_status['total_servers'] - server_status['running_servers'])
with col4:
    health_percentage = (server_status['running_servers'] / server_status['total_servers']) * 100
    st.metric("🏥 Health", f"{health_percentage:.0f}%")

# Show individual server status
st.markdown("#### 📊 MCP Server Status")
server_cols = st.columns(len(server_status['servers']))
for i, (server_name, server_info) in enumerate(server_status['servers'].items()):
    with server_cols[i]:
        server_icon = {
            'file_content': '📄',
            'repository_structure': '📁',
            'commit_history': '📝',
            'code_search': '🔍'
        }.get(server_name, '🖥️')
        
        status_icon = "✅" if server_info['running'] else "❌"
        status_color = "green" if server_info['running'] else "red"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 8px; background-color: {'#f0f9ff' if server_info['running'] else '#fef2f2'};">
            <div style="font-size: 24px;">{server_icon}</div>
            <div style="font-weight: bold; margin: 5px 0;">{server_name.replace('_', ' ').title()}</div>
            <div style="color: {status_color}; font-weight: bold;">{status_icon} {server_info['status']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Simplified tabs - only core functionality
st.markdown("### 🎯 Choose Your Analysis Tool")
st.markdown("Select the feature you want to use for repository analysis:")

# Create simplified tabs
TABS = [
    {"icon": "💬", "title": "Q&A Chat", "desc": "Ask questions about the repository"},
    {"icon": "🔍", "title": "Quick Analysis", "desc": "Get structured repository insights"},
    {"icon": "📊", "title": "Smart Summary", "desc": "Generate comprehensive AI reports"}
]

# Create tab selection
tab_options = [f"{tab['icon']} {tab['title']}" for tab in TABS]
selected_tab = st.selectbox(
    "Select Analysis Tool:",
    tab_options,
    format_func=lambda x: x,
    help="Choose the analysis tool you want to use"
)

# Get selected tab index
tab_index = tab_options.index(selected_tab)

# Display selected tab content
if tab_index == 0:
    st.markdown("## 💬 Q&A Chat Interface")
    st.markdown("Ask natural language questions about the repository and get AI-powered responses.")
    render_chat_interface(repo_url)

elif tab_index == 1:
    st.markdown("## 🔍 Quick Analysis Dashboard")
    st.markdown("Get structured insights about the repository with customizable analysis options.")
    
    if repo_url:
        # Analysis Controls with better layout
        st.markdown("### ⚙️ Analysis Configuration")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            analysis_type = st.selectbox(
                "📋 Analysis Type:",
                ["Repository Overview", "File Structure", "Dependencies", "Code Patterns", "Commit History"],
                help="Select what type of analysis you want to perform"
            )
        
        with col2:
            analysis_depth = st.slider(
                "🔍 Depth:",
                min_value=1,
                max_value=5,
                value=settings.get("analysis_depth", 3),
                help="Analysis depth"
            )
        
        with col3:
            if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
                st.session_state.run_analysis = True
        
        # Run analysis if requested
        if st.session_state.get("run_analysis", False):
            st.session_state.run_analysis = False
            
            # Enhanced progress display
            with st.spinner("🔄 Initializing AI analysis..."):
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        status_text.text("🔍 AI agent is analyzing repository...")
                        progress_bar.progress(25)
                        
                        # Use enhanced AI agent for analysis
                        if analysis_type == "Repository Overview":
                            status_text.text("📊 Generating comprehensive overview...")
                            progress_bar.progress(50)
                            
                            def status_callback(msg):
                                status_text.text(msg)
                            
                            with st.spinner("🤖 AI is analyzing repository structure..."):
                                analysis_result, tools_used = quick_repository_analysis(repo_url, status_callback=status_callback)
                            
                            progress_bar.progress(100)
                            st.success("✅ Repository overview complete!")
                            
                            st.markdown("### 📊 Repository Overview")
                            st.markdown(analysis_result)
                            
                            # Show tools used
                            display_tools_used(tools_used)
                        
                        elif analysis_type == "File Structure":
                            status_text.text("📁 Analyzing file structure...")
                            progress_bar.progress(50)
                            
                            def status_callback(msg):
                                status_text.text(msg)
                            
                            with st.spinner("🤖 AI is analyzing file organization..."):
                                analysis_result, tools_used = ask_repository_question(
                                    "Analyze the file structure and explain how the project is organized. What are the main directories and their purposes?", 
                                    repo_url,
                                    status_callback=status_callback
                                )
                            
                            progress_bar.progress(100)
                            st.success("✅ File structure analysis complete!")
                            
                            st.markdown("### 📁 File Structure Analysis")
                            st.markdown(analysis_result)
                            
                            # Show tools used
                            display_tools_used(tools_used)
                        
                        elif analysis_type == "Dependencies":
                            status_text.text("📦 Analyzing dependencies...")
                            progress_bar.progress(50)
                            
                            def status_callback(msg):
                                status_text.text(msg)
                            
                            with st.spinner("🤖 AI is analyzing project dependencies..."):
                                analysis_result, tools_used = ask_repository_question(
                                    "What dependencies does this project use? Analyze the package files and explain the purpose of key dependencies.", 
                                    repo_url,
                                    status_callback=status_callback
                                )
                            
                            progress_bar.progress(100)
                            st.success("✅ Dependency analysis complete!")
                            
                            st.markdown("### 📦 Dependencies Analysis")
                            st.markdown(analysis_result)
                            
                            # Show tools used
                            display_tools_used(tools_used)
                        
                        elif analysis_type == "Code Patterns":
                            status_text.text("🔍 Analyzing code patterns...")
                            progress_bar.progress(50)
                            
                            def status_callback(msg):
                                status_text.text(msg)
                            
                            with st.spinner("🤖 AI is analyzing code patterns and architecture..."):
                                analysis_result, tools_used = analyze_repository_patterns(repo_url, status_callback=status_callback)
                            
                            progress_bar.progress(100)
                            st.success("✅ Code pattern analysis complete!")
                            
                            st.markdown("### 🔍 Code Patterns Analysis")
                            st.markdown(analysis_result)
                            
                            # Show tools used
                            display_tools_used(tools_used)
                        
                        elif analysis_type == "Commit History":
                            status_text.text("📝 Analyzing commit history...")
                            progress_bar.progress(50)
                            
                            def status_callback(msg):
                                status_text.text(msg)
                            
                            with st.spinner("🤖 AI is analyzing development activity..."):
                                analysis_result, tools_used = ask_repository_question(
                                    "Analyze the recent commit history. What are the main development activities, who are the contributors, and what patterns do you see in the commits?", 
                                    repo_url,
                                    status_callback=status_callback
                                )
                            
                            progress_bar.progress(100)
                            st.success("✅ Commit history analysis complete!")
                            
                            st.markdown("### 📝 Commit History Analysis")
                            st.markdown(analysis_result)
                            
                            # Show tools used
                            display_tools_used(tools_used)
                        
                        # Clear progress indicators
                        progress_bar.empty()
                        status_text.empty()
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                        progress_bar.empty()
                        status_text.empty()
    else:
        st.info("🎯 Please select a repository to perform analysis.")

elif tab_index == 2:
    st.markdown("## 📊 Smart Summary")
    st.markdown("Generate comprehensive AI-powered reports about the repository.")
    
    if repo_url:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            summary_type = st.selectbox(
                "📋 Summary Type:",
                ["Complete Overview", "Technical Analysis", "Code Quality Report", "Architecture Review"],
                help="Select the type of summary you want to generate"
            )
        
        with col2:
            if st.button("📊 Generate Summary", type="primary", use_container_width=True):
                st.session_state.generate_summary = True
        
        if st.session_state.get("generate_summary", False):
            st.session_state.generate_summary = False
            
            with st.spinner("📊 Generating comprehensive summary..."):
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        status_text.text("🔍 Analyzing repository structure...")
                        progress_bar.progress(20)
                        
                        status_text.text("📊 Gathering metrics...")
                        progress_bar.progress(40)
                        
                        status_text.text("🤖 AI is generating summary...")
                        progress_bar.progress(60)
                        
                        # Generate summary based on type
                        if summary_type == "Complete Overview":
                            def status_callback(msg):
                                status_text.text(msg)
                            summary_result, tools_used = generate_repository_summary(repo_url, status_callback=status_callback)
                        elif summary_type == "Technical Analysis":
                            def status_callback(msg):
                                status_text.text(msg)
                            summary_result, tools_used = analyze_repository_patterns(repo_url, status_callback=status_callback)
                        elif summary_type == "Code Quality Report":
                            def status_callback(msg):
                                status_text.text(msg)
                            summary_result, tools_used = ask_repository_question(
                                "Generate a comprehensive code quality report. Analyze code metrics, complexity, maintainability, testing coverage, and provide specific recommendations for improvement.", 
                                repo_url,
                                status_callback=status_callback
                            )
                        else:  # Architecture Review
                            def status_callback(msg):
                                status_text.text(msg)
                            summary_result, tools_used = ask_repository_question(
                                "Provide a detailed architecture review. Analyze the system design, component relationships, design patterns used, scalability considerations, and architectural recommendations.", 
                                repo_url,
                                status_callback=status_callback
                            )
                        
                        status_text.text("✅ Summary complete!")
                        progress_bar.progress(100)
                        
                        st.markdown(f"### 📊 {summary_type}")
                        st.markdown(summary_result)
                        
                        # Show tools used with enhanced display
                        display_tools_used(tools_used)
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                    except Exception as e:
                        st.error(f"❌ Summary generation failed: {str(e)}")
                        progress_bar.empty()
                        status_text.empty()
    else:
        st.info("🎯 Please select a repository to generate a summary.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    🚀 GitHub Repository Analyzer | Powered by FastMCP v2 & Groq AI
</div>
""", unsafe_allow_html=True) 