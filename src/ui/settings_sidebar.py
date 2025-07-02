"""
Enhanced Settings Sidebar UI Component
Provides comprehensive interface for application settings and server management
"""

import streamlit as st
import os
from src.utils.config import get_groq_api_key, has_required_keys
from src.servers.server_manager import get_servers_status, start_mcp_servers, stop_mcp_servers, restart_mcp_servers

def render_settings_sidebar():
    """Render the enhanced settings sidebar with comprehensive controls"""
    
    # Essential Settings with enhanced organization
    st.markdown("### ⚙️ Analysis Settings")
    
    # Analysis depth with enhanced slider
    st.markdown("**🔍 Analysis Depth**")
    analysis_depth = st.slider(
        "How deep to analyze:",
        min_value=1,
        max_value=5,
        value=3,
        help="Controls how deep the analysis explores the repository structure"
    )
    st.session_state.analysis_depth = analysis_depth
    
    # Model selection - Fixed to llama-3.1-70b-versatile
    st.markdown("**🤖 AI Model**")
    selected_model = "llama-3.1-70b-versatile"
    st.session_state.selected_model = selected_model
    
    # Show current model info
    st.info(f"**Current Model:** {selected_model}")
    st.markdown("*This is the default and recommended model for best performance.*")
    
    # Show tool usage with enhanced styling
    st.markdown("**🔧 Tool Usage Display**")
    show_tool_usage = st.checkbox(
        "Show which tools were used",
        value=True,
        help="Display which MCP tools were used in AI responses"
    )
    st.session_state.show_tool_usage = show_tool_usage
    
    # Server Management Section
    st.markdown("---")
    st.markdown("### 🖥️ Server Management")
    
    # Get current server status
    server_status = get_servers_status()
    
    # Server status overview
    st.markdown(f"**📊 Server Status:** {server_status['running_servers']}/{server_status['total_servers']} Active")
    
    # Individual server controls
    for server_name, server_info in server_status["servers"].items():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            status_icon = "🟢" if server_info["running"] else "🔴"
            st.write(f"{status_icon} {server_info['name']}")
        
        with col2:
            if server_info["running"]:
                if st.button("⏹️", key=f"stop_{server_name}", help=f"Stop {server_info['name']}"):
                    stop_mcp_servers([server_name])
                    st.rerun()
            else:
                if st.button("▶️", key=f"start_{server_name}", help=f"Start {server_info['name']}"):
                    start_mcp_servers([server_name])
                    st.rerun()
    
    # Bulk server controls
    st.markdown("**⚡ Quick Actions:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Start All", use_container_width=True):
            start_mcp_servers()
            st.rerun()
    
    with col2:
        if st.button("⏹️ Stop All", use_container_width=True):
            stop_mcp_servers()
            st.rerun()
    
    with col3:
        if st.button("🔄 Restart All", use_container_width=True):
            restart_mcp_servers()
            st.rerun()
    
    # Advanced Tools Section
    st.markdown("---")
    st.markdown("### 🛠️ Advanced Tools")
    
    # Repository Analysis Tools
    st.markdown("**📊 Analysis Tools:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Quick Scan", use_container_width=True):
            st.session_state.run_quick_scan = True
            st.rerun()
        
        if st.button("📈 Code Metrics", use_container_width=True):
            st.session_state.run_code_metrics = True
            st.rerun()
    
    with col2:
        if st.button("🔗 Dependency Check", use_container_width=True):
            st.session_state.run_dependency_check = True
            st.rerun()
        
        if st.button("📝 Generate Report", use_container_width=True):
            st.session_state.run_generate_report = True
            st.rerun()
    
    # AI Tools Section
    st.markdown("**🤖 AI Tools:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💬 Chat Mode", use_container_width=True):
            st.session_state.ai_mode = "chat"
            st.rerun()
        
        if st.button("📊 Summarize", use_container_width=True):
            st.session_state.ai_mode = "summarize"
            st.rerun()
    
    with col2:
        if st.button("🔍 Code Review", use_container_width=True):
            st.session_state.ai_mode = "review"
            st.rerun()
        
        if st.button("📋 Documentation", use_container_width=True):
            st.session_state.ai_mode = "documentation"
            st.rerun()
    
    # System Information
    st.markdown("---")
    st.markdown("### ℹ️ System Info")
    
    # API Key Status
    api_key_status = "✅ Configured" if has_required_keys() else "❌ Missing"
    st.markdown(f"**🔑 API Keys:** {api_key_status}")
    
    # Server Health
    total_servers = server_status['total_servers']
    running_servers = server_status['running_servers']
    health_percentage = (running_servers / total_servers) * 100 if total_servers > 0 else 0
    
    st.markdown(f"**🏥 System Health:** {health_percentage:.0f}%")
    
    if health_percentage == 100:
        st.success("✅ All systems operational")
    elif health_percentage > 50:
        st.warning("⚠️ Some servers offline")
    else:
        st.error("❌ Multiple servers offline")
    
    # Return current configuration
    return {
        "groq_api_key": get_groq_api_key(),
        "config_valid": has_required_keys(),
        "selected_model": st.session_state.get("selected_model", "llama-3.1-70b-versatile"),
        "analysis_depth": st.session_state.get("analysis_depth", 3),
        "show_tool_usage": st.session_state.get("show_tool_usage", True),
        "server_status": server_status,
        "system_health": health_percentage
    }

def validate_api_keys():
    """Validate that required API keys are configured"""
    return has_required_keys() 