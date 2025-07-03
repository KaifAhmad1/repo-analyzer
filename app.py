"""
🚀 GitHub Repository Analyzer - Systematic & Comprehensive
A systematic interface for analyzing GitHub repositories using FastMCP v2 servers and Groq AI
"""

import streamlit as st
import os
from datetime import datetime
from src.ui.repository_selector import render_repository_selector
from src.ui.chat_interface import render_chat_interface
from src.ui.analysis_interface import render_analysis_interface
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
from src.utils.config import (
    get_ui_settings, 
    save_ui_settings, 
    get_analysis_settings,
    save_analysis_settings,
    get_analysis_presets,
    has_required_keys,
    get_groq_api_key
)
from src.utils.repository_manager import (
    get_repository_manager,
    set_current_repository,
    get_current_repository,
    get_repository_info,
    add_analysis_result,
    get_analysis_history,
    export_session_data,
    clear_current_session
)

def display_tools_used(tools_used):
    """Display tools used grouped by server"""
    if not tools_used:
        return
    
    st.markdown("#### 🔧 Analysis Tools Used:")
    
    # Group tools by server
    server_tools = {}
    for tool in tools_used:
        if '.' in tool:
            server, tool_name = tool.split('.', 1)
            server_tools.setdefault(server, []).append(tool_name)
        else:
            server_tools.setdefault('unknown', []).append(tool)
    
    # Display grouped by server
    server_icons = {
        'file_content': '📄',
        'repository_structure': '📁', 
        'commit_history': '📝',
        'code_search': '🔍',
        'unknown': '❓'
    }
    
    for server, tools in server_tools.items():
        icon = server_icons.get(server, '🔧')
        server_name = server.replace('_', ' ').title()
        st.markdown(f"**{icon} {server_name} Server:**")
        for tool in tools:
            st.markdown(f"  - {tool}")
        st.markdown("")

# API key setup function removed for company assignment

def render_session_management():
    """Render session management interface"""
    st.markdown("### 📊 Session Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export Session", use_container_width=True):
            session_data = export_session_data()
            st.download_button(
                label="💾 Download Session Data",
                data=str(session_data),
                file_name=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🗑️ Clear Session", use_container_width=True):
            clear_current_session()
            st.success("✅ Session cleared!")
            st.rerun()
    
    with col3:
        if st.button("📈 View History", use_container_width=True):
            history = get_analysis_history()
            if history:
                st.markdown("#### Analysis History")
                for entry in reversed(history[-5:]):  # Show last 5 entries
                    st.markdown(f"- **{entry['type']}** ({entry['timestamp']})")
            else:
                st.info("No analysis history found")

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
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session_{int(datetime.now().timestamp())}"

# Initialize repository manager
repo_manager = get_repository_manager()
repo_manager.set_session_id(st.session_state.session_id)

# --- SIDEBAR ---
with st.sidebar:
    # Repository Selector Section
    st.markdown("## 📁 Repository")
    repo_url = render_repository_selector()
    
    # Update repository manager if URL changed
    if repo_url and repo_url != get_current_repository():
        if set_current_repository(repo_url):
            st.session_state.current_repo = repo_url
            st.success("✅ Repository set successfully!")
        else:
            st.error("❌ Failed to set repository")
    
    # Repository Info
    current_repo = get_current_repository()
    if current_repo:
        try:
            repo_info = get_repository_info()
            if repo_info and isinstance(repo_info, dict) and "error" not in repo_info:
                st.markdown("### 📋 Repository Info")
                st.markdown(f"**{repo_info.get('name', 'Repository')}**")
                st.caption(repo_info.get('description', 'No description'))
                st.write(f"⭐ {repo_info.get('stars', 0)} | 🍴 {repo_info.get('forks', 0)} | 🕒 Updated: {repo_info.get('updated_at', 'Unknown')}")
            else:
                st.warning("⚠️ Could not fetch repository information")
        except Exception as e:
            st.error(f"❌ Error loading repository: {str(e)}")
    
    st.markdown("---")
    
    # API Key Setup Section
    st.markdown("## 🔑 API Configuration")
    
    # Check if API key is already set in session state
    if 'groq_api_key' not in st.session_state:
        st.session_state.groq_api_key = ""
    
    # API Key Input
    api_key = st.text_input(
        "🔑 Groq API Key",
        value=st.session_state.groq_api_key,
        type="password",
        placeholder="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        help="Enter your Groq API key. Get one from https://console.groq.com/"
    )
    
    # Update session state if API key changed
    if api_key != st.session_state.groq_api_key:
        st.session_state.groq_api_key = api_key
        if api_key:
            # Set environment variable
            os.environ["GROQ_API_KEY"] = api_key
            st.success("✅ API key set successfully!")
        else:
            # Clear environment variable
            if "GROQ_API_KEY" in os.environ:
                del os.environ["GROQ_API_KEY"]
            st.warning("⚠️ API key cleared")
    
    # API Key Status
    if st.session_state.groq_api_key:
        st.success("🔑 API Key: Configured")
        
        # Test API key button
        if st.button("🧪 Test API Key", use_container_width=True):
            with st.spinner("Testing API key..."):
                try:
                    from agno.models.groq import Groq
                    groq_model = Groq(id="llama-3.1-70b-versatile")
                    response = groq_model.complete("Hello, this is a test.")
                    if response and response.content:
                        st.success("✅ API key is valid and working!")
                    else:
                        st.error("❌ API key test failed - no response received")
                except Exception as e:
                    st.error(f"❌ API key test failed: {str(e)}")
    else:
        st.warning("🔑 API Key: Not configured")
        st.info("💡 Get your free API key from [Groq Console](https://console.groq.com/)")
    
    # GitHub Token Input (Optional)
    if 'github_token' not in st.session_state:
        st.session_state.github_token = ""
    
    github_token = st.text_input(
        "🐙 GitHub Token (Optional)",
        value=st.session_state.github_token,
        type="password",
        placeholder="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        help="Optional: For private repositories and higher rate limits. Get from https://github.com/settings/tokens"
    )
    
    # Update GitHub token if changed
    if github_token != st.session_state.github_token:
        st.session_state.github_token = github_token
        if github_token:
            os.environ["GITHUB_TOKEN"] = github_token
            st.success("✅ GitHub token set successfully!")
        else:
            if "GITHUB_TOKEN" in os.environ:
                del os.environ["GITHUB_TOKEN"]
            st.info("ℹ️ GitHub token cleared")
    
    # GitHub Token Status
    if st.session_state.github_token:
        st.success("🐙 GitHub Token: Configured")
    else:
        st.info("🐙 GitHub Token: Not configured (public repos only)")
    
    st.markdown("---")
    
    # Settings Section
    from src.ui.settings_sidebar import render_settings_sidebar
    settings = render_settings_sidebar()
    
    # Session Management
    st.markdown("---")
    render_session_management()
    
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
    <p class="header-subtitle">Systematic AI-Powered Repository Analysis with FastMCP v2 & Groq</p>
</div>
""", unsafe_allow_html=True)

# Enhanced System Status Display with Performance Monitoring
from src.utils.performance_monitor import get_performance_monitor

server_status = get_servers_status()
performance_monitor = get_performance_monitor()

# System Status Banner
if server_status['running_servers'] < server_status['total_servers']:
    st.warning(f"⚠️ {server_status['total_servers'] - server_status['running_servers']} MCP servers are offline. Some features may be limited.")

# Enhanced System Status Display
st.markdown("### 🔧 Enhanced System Status & Performance")
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

# Show individual server status with utilization
st.markdown("#### 📊 MCP Server Status & Utilization")
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
        status_color = "#10b981" if server_info['running'] else "#ef4444"
        status_text = "Running" if server_info['running'] else "Offline"
        
        # Get server utilization from performance monitor
        server_status_data = performance_monitor.get_server_status().get(server_name)
        utilization = server_status_data.utilization if server_status_data else 0.0
        
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; border: 2px solid {status_color}; border-radius: 12px; background: linear-gradient(135deg, #1f2937, #111827); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 32px; margin-bottom: 8px;">{server_icon}</div>
            <div style="font-weight: bold; margin: 8px 0; color: #f9fafb; font-size: 16px;">{server_name.replace('_', ' ').title()}</div>
            <div style="color: {status_color}; font-weight: bold; font-size: 14px; background-color: rgba(255, 255, 255, 0.1); padding: 4px 8px; border-radius: 6px; display: inline-block;">{status_icon} {status_text}</div>
            <div style="color: #9ca3af; font-size: 12px; margin-top: 8px;">Utilization: {utilization:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

# Real-time Performance Monitoring
st.markdown("### ⏱️ Real-time Performance Monitor")
current_status = performance_monitor.get_current_status()

if current_status['status'] == 'running':
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔄 Analysis Type", current_status['analysis_type'].replace('_', ' ').title())
    with col2:
        st.metric("📊 Progress", f"{current_status['progress']:.1f}%")
    with col3:
        st.metric("⏱️ Elapsed", current_status['elapsed_formatted'])
    with col4:
        st.metric("⏳ ETA", current_status['eta_formatted'])
    
    # Progress bar
    st.progress(current_status['progress'] / 100)
    
    # Tools used
    if current_status['tools_used']:
        st.markdown("**🔧 Tools Used:**")
        for tool in current_status['tools_used']:
            tool_info = performance_monitor.get_tool_explanation(tool)
            if isinstance(tool_info, dict) and 'name' in tool_info:
                st.markdown(f"• {tool_info['name']} ({tool_info['typical_duration']}s)")
else:
    st.info("💡 No analysis currently running. Start an analysis to see real-time performance data.")

st.markdown("---")

# Main Analysis Interface
if not get_current_repository():
    st.markdown("### 🎯 Getting Started")
    st.info("""
    **🚀 Welcome to the GitHub Repository Analyzer!**
    
    **To get started:**
    1. **Enter a GitHub repository URL** in the sidebar
    2. **Choose your analysis type** from the options below
    3. **Get comprehensive insights** about the repository
    
    **Available Analysis Types:**
    - **🔍 Comprehensive Analysis**: Full repository analysis with multiple dimensions
    - **⚡ Quick Overview**: Fast repository summary
    - **🔒 Security Analysis**: Security-focused analysis
    - **📊 Code Quality**: Code quality and best practices analysis
    - **💬 Q&A Chat**: Ask specific questions about the repository
    """)
    
    # Show example repositories
    st.markdown("#### 💡 Example Repositories")
    example_repos = [
        "https://github.com/microsoft/vscode",
        "https://github.com/facebook/react",
        "https://github.com/python/cpython",
        "https://github.com/tensorflow/tensorflow"
    ]
    
    cols = st.columns(len(example_repos))
    for i, repo in enumerate(example_repos):
        with cols[i]:
            if st.button(f"Try {repo.split('/')[-1]}", key=f"example_{i}", use_container_width=True):
                st.session_state.current_repo = repo
                st.rerun()
else:
    # Repository is selected - show analysis options
    st.markdown("### 🎯 Choose Your Analysis Tool")
    st.markdown("Select the analysis type you want to perform on the current repository:")
    
    # Create main analysis tabs
    analysis_tab, chat_tab, settings_tab = st.tabs([
        "🔍 Systematic Analysis",
        "💬 Q&A Chat", 
        "⚙️ Advanced Settings"
    ])
    
    with analysis_tab:
        render_analysis_interface(get_current_repository())
    
    with chat_tab:
        render_chat_interface(get_current_repository())
    
    with settings_tab:
        st.markdown("#### ⚙️ Advanced Settings")
        
        # Analysis Settings
        st.markdown("**Analysis Settings:**")
        analysis_settings = get_analysis_settings()
        
        col1, col2 = st.columns(2)
        with col1:
            max_file_size = st.number_input(
                "Max File Size (MB)",
                min_value=1,
                max_value=100,
                value=analysis_settings["max_file_size"] // (1024 * 1024),
                help="Maximum file size to analyze"
            )
            
            max_files = st.number_input(
                "Max Files per Analysis",
                min_value=10,
                max_value=500,
                value=analysis_settings["max_files_per_analysis"],
                help="Maximum number of files to analyze"
            )
        
        with col2:
            include_hidden = st.checkbox(
                "Include Hidden Files",
                value=analysis_settings["include_hidden_files"],
                help="Include hidden files in analysis"
            )
            
            enable_caching = st.checkbox(
                "Enable Caching",
                value=analysis_settings.get("enable_caching", True),
                help="Cache analysis results for faster subsequent runs"
            )
        
        # Save settings
        if st.button("💾 Save Analysis Settings", type="primary"):
            new_settings = {
                "max_file_size": max_file_size * 1024 * 1024,
                "max_files_per_analysis": max_files,
                "include_hidden_files": include_hidden,
                "enable_caching": enable_caching
            }
            save_analysis_settings(new_settings)
            st.success("✅ Analysis settings saved!")
        
        # Analysis Presets
        st.markdown("**Analysis Presets:**")
        presets = get_analysis_presets()
        for preset_id, preset in presets.items():
            with st.expander(f"📋 {preset['name']} - {preset['description']}"):
                st.markdown(f"**Max Files:** {preset['max_files']}")
                st.markdown(f"**Max Depth:** {preset['max_depth']}")
                st.markdown(f"**Include Metrics:** {'✅' if preset['include_metrics'] else '❌'}")
                st.markdown(f"**Include Security:** {'✅' if preset['include_security'] else '❌'}")
                st.markdown(f"**Timeout:** {preset['timeout']} seconds")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    🚀 GitHub Repository Analyzer | Powered by FastMCP v2 & Groq AI
</div>
""", unsafe_allow_html=True) 