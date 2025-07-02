"""
Clean Settings Sidebar UI Component
Provides streamlined interface for application settings and server management
"""

import streamlit as st
import os
from src.utils.config import get_groq_api_key, has_required_keys
from src.servers.server_manager import get_servers_status, start_mcp_servers, stop_mcp_servers, restart_mcp_servers

def render_settings_sidebar():
    """Render the enhanced settings sidebar with system status"""
    st.markdown("## ⚙️ Settings & Status")
    
    # System Health Section
    st.markdown("### 🏥 System Health")
    
    try:
        server_status = get_servers_status()
        
        # Calculate health percentage
        health_percentage = (server_status['running_servers'] / server_status['total_servers']) * 100 if server_status['total_servers'] > 0 else 0
        
        # Health indicator
        if health_percentage >= 80:
            health_color = "green"
            health_icon = "✅"
        elif health_percentage >= 50:
            health_color = "orange"
            health_icon = "⚠️"
        else:
            health_color = "red"
            health_icon = "❌"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; border: 2px solid {health_color}; border-radius: 10px; background-color: #f8f9fa;">
            <div style="font-size: 32px; margin-bottom: 10px;">{health_icon}</div>
            <div style="font-size: 24px; font-weight: bold; color: {health_color}; margin-bottom: 5px;">{health_percentage:.0f}%</div>
            <div style="font-size: 14px; color: #666;">System Health</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Server status details
        st.markdown("#### 📊 Server Details")
        for server_name, server_info in server_status['servers'].items():
            server_icon = {
                'file_content': '📄',
                'repository_structure': '📁',
                'commit_history': '📝',
                'code_search': '🔍'
            }.get(server_name, '🖥️')
            
            status_icon = "✅" if server_info['running'] else "❌"
            status_color = "green" if server_info['running'] else "red"
            
            st.markdown(f"{server_icon} **{server_name.replace('_', ' ').title()}:** {status_icon} {server_info['status']}")
        
        # Store health percentage for other components
        st.session_state.system_health = health_percentage
        
    except Exception as e:
        st.error(f"❌ Error getting server status: {str(e)}")
        st.session_state.system_health = 0
    
    st.markdown("---")
    
    # Analysis Settings
    st.markdown("### 🔍 Analysis Settings")
    
    # Analysis depth
    analysis_depth = st.slider(
        "Analysis Depth:",
        min_value=1,
        max_value=5,
        value=st.session_state.get("analysis_depth", 3),
        help="How deep to analyze the repository structure"
    )
    st.session_state.analysis_depth = analysis_depth
    
    # Model selection
    model_options = [
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-versatile",
        "mixtral-8x7b-32768",
        "gemma-7b-it"
    ]
    
    selected_model = st.selectbox(
        "AI Model:",
        model_options,
        index=0,
        help="Select the AI model for analysis"
    )
    st.session_state.selected_model = selected_model
    
    # Show tool usage toggle
    show_tool_usage = st.checkbox(
        "Show Tool Usage",
        value=st.session_state.get("show_tool_usage", True),
        help="Display which tools were used in each analysis"
    )
    st.session_state.show_tool_usage = show_tool_usage
    
    # Auto-start servers toggle
    auto_start_servers = st.checkbox(
        "Auto-start Servers",
        value=st.session_state.get("auto_start_servers", True),
        help="Automatically start MCP servers if they're offline"
    )
    st.session_state.auto_start_servers = auto_start_servers
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Status", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("🚀 Start All Servers", use_container_width=True):
            try:
                start_mcp_servers()
                st.success("✅ All servers started!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error starting servers: {str(e)}")
    
    # Return settings for use in main app
    return {
        "analysis_depth": analysis_depth,
        "selected_model": selected_model,
        "show_tool_usage": show_tool_usage,
        "auto_start_servers": auto_start_servers,
        "system_health": st.session_state.get("system_health", 0)
    }

def validate_api_keys():
    """Validate that required API keys are configured"""
    return has_required_keys() 