"""
🚀 GitHub Repository Analyzer - Streamlined Version
A focused, efficient interface for analyzing GitHub repositories using MCP servers and AI agents
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
from src.ui.chat_interface import render_chat_interface
from src.agent.ai_agent import create_advanced_agent, ask_question_advanced
from src.servers.server_manager import start_mcp_servers, check_servers_status
from src.servers.mcp_client_improved import SyncMCPClient

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
        <p class="header-subtitle">AI-Powered Repository Analysis with MCP Servers</p>
        <div class="header-features">
            <span class="feature-badge">🤖 AI Agents</span>
            <span class="feature-badge">🔍 MCP Servers</span>
            <span class="feature-badge">📊 Analytics</span>
            <span class="feature-badge">💬 Q&A Interface</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar_controls():
    """Create sidebar controls"""
    st.sidebar.markdown("### ⚙️ Configuration")
    
    # Agent selection
    agent_type = st.sidebar.selectbox(
        "Agent Type",
        ["Single Agent", "Multi-Agent Team"],
        help="Choose the AI agent system"
    )
    
    model = st.sidebar.selectbox(
        "AI Model",
        ["gemini-2.0-flash-001", "gemini-1.5-pro"],
        help="Choose the Google Gemini AI model"
    )
    
    # Server status
    st.sidebar.markdown("### 🔧 Server Status")
    server_status = check_servers_status()
    
    for server, status in server_status.items():
        status_icon = "✅" if status else "❌"
        st.sidebar.markdown(f"{status_icon} {server.replace('_', ' ').title()}")
    
    # Server controls
    if st.sidebar.button("🔄 Restart Servers"):
        with st.spinner("Restarting MCP servers..."):
            from src.servers.server_manager import restart_mcp_servers
            restart_mcp_servers()
        st.rerun()
    
    return agent_type, model

def create_repository_overview(repo_url: str):
    """Create repository overview section"""
    if not repo_url:
        return
    
    try:
        with SyncMCPClient() as client:
            overview = client.get_repository_overview(repo_url)
            
            if overview.get("success"):
                st.markdown("### 📊 Repository Overview")
                st.markdown(overview.get("result", "No overview available"))
            else:
                st.error("Failed to get repository overview")
    
    except Exception as e:
        st.error(f"Error getting repository overview: {e}")

def create_activity_charts(repo_url: str):
    """Create activity visualization charts"""
    if not repo_url:
        return
    
    try:
        with SyncMCPClient() as client:
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
    
    except Exception as e:
        st.error(f"Error creating activity charts: {e}")

def create_issues_table(repo_url: str):
    """Create issues table"""
    if not repo_url:
        return
    
    try:
        with SyncMCPClient() as client:
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
    
    except Exception as e:
        st.error(f"Error getting issues: {e}")

def create_qa_interface(repo_url: str, agent_type: str, model: str):
    """Create Q&A interface"""
    if not repo_url:
        st.info("Please select a repository to start asking questions.")
        return
    
    st.markdown("### 💬 Ask Questions About This Repository")
    
    # Question input
    question = st.text_area(
        "Enter your question:",
        placeholder="e.g., What is this repository about? Show me the main entry points. What are the recent changes?",
        height=100
    )
    
    if st.button("🤖 Ask AI Agent", type="primary"):
        if question.strip():
            with st.spinner("🤖 Analyzing with AI agent..."):
                try:
                    response = ask_question_advanced(
                        question, 
                        repo_url, 
                        use_team=(agent_type == "Multi-Agent Team")
                    )
                    
                    st.markdown("#### 🤖 AI Response")
                    st.markdown(response)
                    
                    # Store in session state for chat history
                    if "chat_history" not in st.session_state:
                        st.session_state.chat_history = []
                    
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": response,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    st.error(f"Error getting AI response: {e}")
        else:
            st.warning("Please enter a question.")
    
    # Show chat history
    if "chat_history" in st.session_state and st.session_state.chat_history:
        st.markdown("### 📝 Chat History")
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
            with st.expander(f"Q: {chat['question'][:50]}..."):
                st.markdown(f"**Question:** {chat['question']}")
                st.markdown(f"**Answer:** {chat['answer']}")
                st.caption(f"Asked at: {chat['timestamp']}")

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
    agent_type, model = create_sidebar_controls()
    
    # Start MCP servers if not running
    server_status = check_servers_status()
    if not any(server_status.values()):
        with st.spinner("Starting MCP servers..."):
            start_mcp_servers()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Repository selector
        repo_url = render_repository_selector()
        if repo_url:
            st.session_state.selected_repo = repo_url
            
            # Repository overview
            create_repository_overview(repo_url)
            
            # Activity charts
            create_activity_charts(repo_url)
            
            # Issues table
            create_issues_table(repo_url)
    
    with col2:
        # Q&A Interface
        create_qa_interface(st.session_state.selected_repo, agent_type, model)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 0.8em;">
            Built with ❤️ using Streamlit, MCP Servers, and Google Gemini AI
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 