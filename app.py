"""
🚀 GitHub Repository Analyzer - Simplified UI
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
    initial_sidebar_state="collapsed"
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
    </div>
    """, unsafe_allow_html=True)

def create_sidebar_controls():
    """Create simplified sidebar controls"""
    
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
    
    # Show server status
    for server_name, server_info in detailed_status["servers"].items():
        status_icon = "✅" if server_info["running"] else "❌"
        server_display_name = server_info["name"].replace(" MCP Server", "")
        st.sidebar.text(f"{status_icon} {server_display_name}")
    
    # Server controls
    if st.sidebar.button("🔄 Restart All Servers"):
        with st.spinner("Restarting all MCP servers..."):
            from src.servers.server_manager import restart_mcp_servers
            results = restart_mcp_servers()
            st.sidebar.success(f"Restarted {sum(results.values())}/{len(results)} servers")
        st.rerun()
    
    return model

def create_repository_overview(repo_url: str):
    """Create repository overview section"""
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

def create_code_analysis(repo_url: str):
    """Create code analysis section"""
    if not repo_url:
        return
    
    st.markdown("### 🔍 Code Analysis")
    
    try:
        with UnifiedMCPClient() as client:
            # Get code metrics
            metrics = client.get_code_metrics(repo_url)
            if metrics.get("success"):
                st.markdown("#### 📊 Code Metrics")
                st.markdown(metrics.get("result", "No metrics available"))
            
            # Get file structure
            structure = client.get_file_structure(repo_url)
            if structure.get("success"):
                st.markdown("#### 📁 File Structure Analysis")
                st.markdown(structure.get("result", "No structure available"))
            
            # Search for common patterns
            st.markdown("#### 🔍 Code Pattern Analysis")
            
            patterns = [
                ("Authentication", "auth login password token"),
                ("Database", "database db sql connection"),
                ("Testing", "test unittest pytest"),
                ("API", "api endpoint route controller"),
                ("Security", "security encrypt hash")
            ]
            
            for pattern_name, search_terms in patterns:
                with st.expander(f"🔍 {pattern_name} Patterns"):
                    result = client.search_code(repo_url, search_terms)
                    if result.get("success") and result.get("result"):
                        st.markdown(result.get("result", "No patterns found"))
                    else:
                        st.info(f"No {pattern_name.lower()} patterns found")
    
    except Exception as e:
        st.error(f"Error in code analysis: {e}")

def create_visual_repository_map(repo_url: str):
    """Create visual repository map"""
    if not repo_url:
        return
    
    st.markdown("### 🗺️ Visual Repository Map")
    
    try:
        with UnifiedMCPClient() as client:
            # Get directory tree
            tree_result = client.get_directory_tree(repo_url, max_depth=4)
            
            if tree_result.get("success"):
                st.markdown("#### 📁 Directory Structure")
                st.markdown(tree_result.get("result", "No structure available"))
            
            # Create file type distribution chart
            st.markdown("#### 📊 File Type Distribution")
            
            # Get file structure for analysis
            structure = client.get_file_structure(repo_url)
            if structure.get("success") and structure.get("result"):
                # This would need parsing of the structure result to create charts
                st.info("File type distribution visualization would be generated here")
            
            # Activity timeline
            st.markdown("#### 📈 Activity Timeline")
            commits = client.get_recent_commits(repo_url, 20)
            
            if commits.get("success") and commits.get("result"):
                commit_data = commits["result"]
                
                if isinstance(commit_data, list) and len(commit_data) > 0:
                    df = pd.DataFrame(commit_data)
                    
                    if 'date' in df.columns:
                        df['date'] = pd.to_datetime(df['date'])
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
    
    except Exception as e:
        st.error(f"Error creating visual map: {e}")

def create_smart_summarization(repo_url: str):
    """Create smart summarization section"""
    if not repo_url:
        return
    
    st.markdown("### 🧠 Smart Summarization")
    
    # AI-powered summary
    with st.spinner("🤖 Generating smart summary..."):
        try:
            summary = analyze_repository(repo_url)
            st.markdown("#### 📋 AI-Generated Summary")
            st.markdown(summary)
        except Exception as e:
            st.error(f"Error generating summary: {e}")
    
    # Key insights
    st.markdown("#### 🔑 Key Insights")
    
    try:
        with UnifiedMCPClient() as client:
            # Get recent activity
            commits = client.get_recent_commits(repo_url, 5)
            if commits.get("success") and commits.get("result"):
                st.markdown("**Recent Activity:**")
                commit_data = commits["result"]
                if isinstance(commit_data, list):
                    for commit in commit_data[:3]:
                        st.markdown(f"- {commit.get('message', 'No message')[:100]}...")
            
            # Get issues summary
            issues = client.get_issues(repo_url, "open", 5)
            if issues.get("success") and issues.get("result"):
                st.markdown("**Open Issues:**")
                issues_data = issues["result"]
                if isinstance(issues_data, list):
                    for issue in issues_data[:3]:
                        st.markdown(f"- #{issue.get('number', 'N/A')}: {issue.get('title', 'No title')[:80]}...")
    
    except Exception as e:
        st.error(f"Error getting insights: {e}")

def create_documentation_generation(repo_url: str):
    """Create documentation generation section"""
    if not repo_url:
        return
    
    st.markdown("### 📚 Documentation Generation")
    
    try:
        with UnifiedMCPClient() as client:
            # Check for existing documentation
            st.markdown("#### 📖 Existing Documentation")
            
            # Try to get README
            readme_result = client.get_file_content(repo_url, "README.md")
            if readme_result.get("success"):
                st.markdown("**README.md found:**")
                st.markdown(readme_result.get("result", "No content")[:500] + "...")
            else:
                st.warning("No README.md found")
            
            # Check for other docs
            docs_files = ["docs/", "documentation/", "DOCS.md", "CONTRIBUTING.md"]
            st.markdown("**Other Documentation:**")
            for doc_path in docs_files:
                try:
                    result = client.get_file_content(repo_url, doc_path)
                    if result.get("success"):
                        st.markdown(f"✅ {doc_path}")
                    else:
                        st.markdown(f"❌ {doc_path}")
                except:
                    st.markdown(f"❌ {doc_path}")
            
            # Generate missing documentation suggestions
            st.markdown("#### 🔧 Documentation Suggestions")
            
            # Analyze what's missing
            suggestions = []
            
            # Check for API documentation
            api_search = client.search_code(repo_url, "def class api endpoint")
            if api_search.get("success") and api_search.get("result"):
                suggestions.append("📋 API Documentation - Found API endpoints that need documentation")
            
            # Check for setup instructions
            setup_files = ["requirements.txt", "package.json", "setup.py", "install.sh"]
            for setup_file in setup_files:
                try:
                    result = client.get_file_content(repo_url, setup_file)
                    if result.get("success"):
                        suggestions.append(f"📋 Setup Instructions - Found {setup_file}")
                        break
                except:
                    continue
            
            if suggestions:
                for suggestion in suggestions:
                    st.markdown(f"- {suggestion}")
            else:
                st.info("No specific documentation suggestions at this time")
    
    except Exception as e:
        st.error(f"Error in documentation generation: {e}")

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
        return
    
    # Start MCP servers if not running
    server_status = check_servers_status()
    if not any(server_status.values()):
        with st.spinner("Starting MCP servers..."):
            results = start_mcp_servers()
            st.success(f"Started {sum(results.values())}/{len(results)} servers")
    
    # Repository selector
    repo_url = render_repository_selector()
    if repo_url:
        st.session_state.selected_repo = repo_url
        
        # Create large, prominent tabs
        st.markdown("---")
        st.markdown("## 🎯 Analysis Tools")
        
        # Use columns to make tabs more prominent
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            qa_tab = st.button("💬 Q&A Interface", use_container_width=True, type="primary")
        
        with col2:
            code_tab = st.button("🔍 Code Analysis", use_container_width=True, type="primary")
        
        with col3:
            visual_tab = st.button("🗺️ Visual Map", use_container_width=True, type="primary")
        
        with col4:
            summary_tab = st.button("🧠 Smart Summary", use_container_width=True, type="primary")
        
        with col5:
            docs_tab = st.button("📚 Documentation", use_container_width=True, type="primary")
        
        # Show content based on button clicks
        if qa_tab:
            st.markdown("---")
            render_chat_interface(repo_url)
            render_chat_stats()
        
        elif code_tab:
            st.markdown("---")
            create_code_analysis(repo_url)
        
        elif visual_tab:
            st.markdown("---")
            create_visual_repository_map(repo_url)
        
        elif summary_tab:
            st.markdown("---")
            create_smart_summarization(repo_url)
        
        elif docs_tab:
            st.markdown("---")
            create_documentation_generation(repo_url)
        
        else:
            # Default view - show overview
            st.markdown("---")
            st.markdown("## 📊 Repository Overview")
            create_repository_overview(repo_url)
            
            st.markdown("---")
            st.markdown("### 🎯 Choose an Analysis Tool Above")
            st.markdown("""
            - **💬 Q&A Interface**: Ask questions about the repository
            - **🔍 Code Analysis**: Analyze code quality and patterns
            - **🗺️ Visual Map**: Interactive repository visualization
            - **🧠 Smart Summary**: AI-generated repository summary
            - **📚 Documentation**: Generate and analyze documentation
            """)
    
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