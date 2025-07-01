"""
🚀 GitHub Repository Analyzer - Multi-Server Ecosystem
A comprehensive interface for analyzing GitHub repositories using FastMCP v2 servers and AI agents
"""

import streamlit as st
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List, Optional

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.ui.repository_selector import render_repository_selector
from src.ui.chat_interface import render_chat_interface, render_chat_stats
from src.ui.settings_sidebar import render_settings_sidebar, validate_api_keys
from src.agent.ai_agent import ask_question, analyze_repository
from src.servers.server_manager import start_mcp_servers, check_servers_status, get_detailed_server_status
from src.servers.mcp_client_improved import UnifiedMCPClient

# Page configuration
st.set_page_config(
    page_title="🚀 GitHub Repository Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    """Load custom CSS for modern styling"""
    with open("src/ui/modern_styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def create_header():
    """Create clean header"""
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🚀 GitHub Repository Analyzer</h1>
        <p class="header-subtitle">AI-Powered Repository Analysis with FastMCP v2 Multi-Server Ecosystem</p>
        <div class="header-features">
            <span class="feature-badge">🤖 AI Agents</span>
            <span class="feature-badge">🔍 FastMCP v2</span>
            <span class="feature-badge">📊 Analytics</span>
            <span class="feature-badge">💬 Q&A Interface</span>
            <span class="feature-badge">🔄 Multi-Server</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar_controls():
    """Create sidebar controls"""
    
    # API Configuration Section
    config = render_settings_sidebar()
    
    # Check if API keys are configured
    if not config["config_valid"]:
        st.sidebar.error("⚠️ Please configure your API keys to use AI features")
        return None
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ AI Configuration")
    
    # Model selection
    model = st.sidebar.selectbox(
        "AI Model",
        ["gemini-2.0-flash-001", "gemini-1.5-pro"],
        help="Choose the Google Gemini AI model"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Server Status")
    
    # Get detailed server status
    detailed_status = get_detailed_server_status()
    
    # Show server status with more details
    for server_name, server_info in detailed_status["servers"].items():
        status_icon = "✅" if server_info["running"] else "❌"
        server_display_name = server_info["name"].replace(" MCP Server", "")
        
        if st.sidebar.button(f"{status_icon} {server_display_name}", key=f"server_{server_name}"):
            st.sidebar.info(f"**{server_display_name}**\n{server_info['description']}")
    
    # Server controls
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🔄 Restart All"):
            with st.spinner("Restarting all MCP servers..."):
                from src.servers.server_manager import restart_mcp_servers
                results = restart_mcp_servers()
                st.sidebar.success(f"Restarted {sum(results.values())}/{len(results)} servers")
            st.rerun()
    
    with col2:
        if st.button("📊 Status"):
            st.sidebar.json(detailed_status)
    
    return model

def create_repository_overview(repo_url: str):
    """Create repository overview section using unified MCP client"""
    if not repo_url:
        return
    
    try:
        with UnifiedMCPClient() as client:
            overview = client.get_repository_overview(repo_url)
            
            if overview.get("success"):
                st.markdown("### 📊 Repository Overview")
                st.markdown(overview.get("result", "No overview available"))
            else:
                st.error("Failed to get repository overview")
    
    except Exception as e:
        st.error(f"Error getting repository overview: {e}")

def create_repository_structure(repo_url: str):
    """Create repository structure section"""
    if not repo_url:
        return
    
    try:
        with UnifiedMCPClient() as client:
            # Get directory tree
            tree_result = client.get_directory_tree(repo_url, max_depth=3)
            
            if tree_result.get("success"):
                st.markdown("### 📁 Repository Structure")
                st.markdown(tree_result.get("result", "No structure available"))
            
            # Get file structure analysis
            structure_result = client.get_file_structure(repo_url)
            
            if structure_result.get("success"):
                st.markdown("### 📋 File Structure Analysis")
                st.markdown(structure_result.get("result", "No analysis available"))
    
    except Exception as e:
        st.error(f"Error getting repository structure: {e}")

def create_activity_charts(repo_url: str):
    """Create activity visualization charts using unified MCP client"""
    if not repo_url:
        return
    
    try:
        with UnifiedMCPClient() as client:
            # Get recent commits
            commits = client.get_recent_commits(repo_url, 20)
            
            if commits.get("success") and commits.get("result"):
                commit_data = commits["result"]
                
                # Create commit activity chart
                if isinstance(commit_data, list) and len(commit_data) > 0:
                    df = pd.DataFrame(commit_data)
                    
                    # Convert date strings to datetime
                    if 'date' in df.columns:
                        df['date'] = pd.to_datetime(df['date'])
                        
                        # Group by date and count commits
                        daily_commits = df.groupby(df['date'].dt.date).size().reset_index(name='commits')
                        daily_commits['date'] = pd.to_datetime(daily_commits['date'])
                        
                        fig = px.line(daily_commits, x='date', y='commits',
                                    title="Recent Commit Activity",
                                    labels={'date': 'Date', 'commits': 'Number of Commits'})
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#2c3e50')
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            # Get commit statistics
            stats = client.get_commit_statistics(repo_url, days=30)
            if stats.get("success") and stats.get("result"):
                st.markdown("### 📈 Commit Statistics")
                st.markdown(stats.get("result", "No statistics available"))
    
    except Exception as e:
        st.error(f"Error creating activity charts: {e}")

def create_issues_table(repo_url: str):
    """Create issues and pull requests table"""
    if not repo_url:
        return
    
    try:
        with UnifiedMCPClient() as client:
            # Get issues
            issues = client.get_issues(repo_url, "open", 10)
            if issues.get("success") and issues.get("result"):
                issues_data = issues["result"]
                
                if isinstance(issues_data, list) and len(issues_data) > 0:
                    st.markdown("### 🐛 Recent Issues")
                    
                    # Create a simple table
                    for issue in issues_data[:5]:  # Show top 5 issues
                        with st.expander(f"#{issue.get('number', 'N/A')} - {issue.get('title', 'No title')}"):
                            st.write(f"**Author:** {issue.get('author', 'Unknown')}")
                            st.write(f"**Created:** {issue.get('created_at', 'Unknown')}")
                            st.write(f"**Labels:** {', '.join(issue.get('labels', []))}")
            
            # Get pull requests
            prs = client.get_pull_requests(repo_url, "open", 5)
            if prs.get("success") and prs.get("result"):
                prs_data = prs["result"]
                
                if isinstance(prs_data, list) and len(prs_data) > 0:
                    st.markdown("### 🔄 Recent Pull Requests")
                    
                    for pr in prs_data[:3]:  # Show top 3 PRs
                        with st.expander(f"#{pr.get('number', 'N/A')} - {pr.get('title', 'No title')}"):
                            st.write(f"**Author:** {pr.get('author', 'Unknown')}")
                            st.write(f"**Created:** {pr.get('created_at', 'Unknown')}")
                            st.write(f"**Status:** {pr.get('state', 'Unknown')}")
    
    except Exception as e:
        st.error(f"Error getting issues: {e}")

def create_code_metrics(repo_url: str):
    """Create code metrics section"""
    if not repo_url:
        return
    
    try:
        with UnifiedMCPClient() as client:
            metrics = client.get_code_metrics(repo_url)
            
            if metrics.get("success"):
                st.markdown("### 📊 Code Metrics")
                st.markdown(metrics.get("result", "No metrics available"))
    
    except Exception as e:
        st.error(f"Error getting code metrics: {e}")

def main():
    """Main application function"""
    # Load CSS
    load_css()
    
    # Create header
    create_header()
    
    # Initialize session state
    if "selected_repo" not in st.session_state:
        st.session_state.selected_repo = None
    
    # Create sidebar controls
    model = create_sidebar_controls()
    
    # Check if API keys are configured
    if not validate_api_keys():
        st.warning("⚠️ Please configure your API keys in the sidebar to use AI features")
        st.info("You can still browse repositories and view basic information without API keys")
        
        # Show repository selector only
        repo_url = render_repository_selector()
        if repo_url:
            st.session_state.selected_repo = repo_url
            create_repository_overview(repo_url)
            create_repository_structure(repo_url)
            create_activity_charts(repo_url)
            create_issues_table(repo_url)
            create_code_metrics(repo_url)
        return
    
    # Start MCP servers if not running
    server_status = check_servers_status()
    if not any(server_status.values()):
        with st.spinner("Starting MCP servers..."):
            results = start_mcp_servers()
            st.success(f"Started {sum(results.values())}/{len(results)} servers")
    
    # Main content area
    repo_url = render_repository_selector()
    if repo_url:
        st.session_state.selected_repo = repo_url
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Overview", "📁 Structure", "📈 Activity", "🐛 Issues", "📊 Metrics", "💬 Q&A"
        ])
        
        with tab1:
            create_repository_overview(repo_url)
        
        with tab2:
            create_repository_structure(repo_url)
        
        with tab3:
            create_activity_charts(repo_url)
        
        with tab4:
            create_issues_table(repo_url)
        
        with tab5:
            create_code_metrics(repo_url)
        
        with tab6:
            render_chat_interface(repo_url)
            render_chat_stats()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 0.8em;">
            Built with ❤️ using Streamlit, FastMCP v2 Multi-Server Ecosystem, and Google Gemini AI
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 