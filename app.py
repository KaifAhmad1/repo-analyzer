"""
🚀 GitHub Repository Analyzer - Modern UI with Advanced Multi-Agent System
A beautiful, animated, and feature-rich interface for analyzing GitHub repositories
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
from plotly.subplots import make_subplots
import pandas as pd

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.ui.repository_selector import render_repository_selector
from src.ui.chat_interface import render_chat_interface
from src.agent.ai_agent import (
    create_ai_agent, 
    create_advanced_agent, 
    create_agent_team,
    ask_question_advanced,
    analyze_repository_advanced
)
from src.utils.config import load_config
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
    """Create beautiful animated header"""
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🚀 GitHub Repository Analyzer</h1>
        <p class="header-subtitle">AI-Powered Repository Analysis with Advanced Multi-Agent System</p>
    </div>
    """, unsafe_allow_html=True)

def create_agent_selector():
    """Create agent selection interface"""
    st.sidebar.markdown("### 🤖 Agent System")
    
    agent_type = st.sidebar.selectbox(
        "Choose Agent Type",
        ["Single Agent", "Multi-Agent Team", "Legacy System"],
        help="Select the agent system to use for analysis"
    )
    
    if agent_type == "Single Agent":
        model = st.sidebar.selectbox(
            "Model",
            ["gemini-2.0-flash-001", "gemini-1.5-pro", "gemini-1.5-flash"],
            help="Choose the Google Gemini AI model for the agent"
        )
    elif agent_type == "Multi-Agent Team":
        st.sidebar.info("🤝 Using specialized team of agents for comprehensive analysis")
        model = "gemini-2.0-flash-001"
    else:
        st.sidebar.info("🔄 Using legacy agent system")
        model = "gemini-2.0-flash-001"
    
    return agent_type, model

def create_stats_cards(repo_data=None):
    """Create animated stats cards"""
    if not repo_data:
        # Placeholder stats
        stats = [
            {"label": "Files Analyzed", "value": "0", "icon": "📁"},
            {"label": "Lines of Code", "value": "0", "icon": "💻"},
            {"label": "Languages", "value": "0", "icon": "🔤"},
            {"label": "Issues Found", "value": "0", "icon": "🐛"},
        ]
    else:
        stats = [
            {"label": "Files Analyzed", "value": str(repo_data.get("files", 0)), "icon": "📁"},
            {"label": "Lines of Code", "value": str(repo_data.get("lines", 0)), "icon": "💻"},
            {"label": "Languages", "value": str(repo_data.get("languages", 0)), "icon": "🔤"},
            {"label": "Issues Found", "value": str(repo_data.get("issues", 0)), "icon": "🐛"},
        ]
    
    cols = st.columns(4)
    for i, stat in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stat['icon']} {stat['value']}</div>
                <div class="stat-label">{stat['label']}</div>
            </div>
            """, unsafe_allow_html=True)

def create_insights_panel(repo_url=None, agent_type="Single Agent"):
    """Create insights panel with repository analysis using advanced agents"""
    if not repo_url:
        st.markdown("""
        <div class="modern-card insight-card">
            <h3>💡 Repository Insights</h3>
            <p>Select a repository to see detailed insights and analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Get repository insights using advanced agents
    try:
        with st.spinner("🤖 Analyzing repository with AI agents..."):
            if agent_type == "Multi-Agent Team":
                # Use team for comprehensive analysis
                analysis = analyze_repository_advanced(repo_url)
            else:
                # Use single agent
                analysis = ask_question_advanced(
                    "Provide a comprehensive overview of this repository including its purpose, structure, and key features",
                    repo_url,
                    use_team=(agent_type == "Multi-Agent Team")
                )
            
            st.markdown("""
            <div class="modern-card insight-card">
                <h3>💡 Repository Insights</h3>
                <div style="margin-top: 16px;">
            """, unsafe_allow_html=True)
            
            st.markdown(analysis)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error getting insights: {e}")

def create_visualizations(repo_url=None):
    """Create beautiful visualizations"""
    if not repo_url:
        return
    
    try:
        with SyncMCPClient() as client:
            # Get repository data for visualizations
            overview = client.get_repository_overview(repo_url)
            commits = client.get_recent_commits(repo_url, 20)
            issues = client.get_issues(repo_url, "open", 10)
            
            # Create tabs for different visualizations
            tab1, tab2, tab3 = st.tabs(["📊 Activity", "🔤 Languages", "📈 Trends"])
            
            with tab1:
                if commits.get("success"):
                    # Create commit activity chart
                    commit_data = commits.get("result", [])
                    if commit_data:
                        df = pd.DataFrame(commit_data)
                        df['date'] = pd.to_datetime(df['date'])
                        
                        fig = px.line(df, x='date', y='sha', 
                                    title="Recent Commit Activity",
                                    labels={'date': 'Date', 'sha': 'Commits'})
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#2c3e50')
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Language distribution pie chart
                if overview.get("success"):
                    # This would need to be enhanced to get actual language data
                    languages = ['Python', 'JavaScript', 'TypeScript', 'HTML', 'CSS']
                    values = [40, 25, 20, 10, 5]
                    
                    fig = px.pie(values=values, names=languages, 
                               title="Language Distribution")
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#2c3e50')
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                # Create a trend analysis
                if issues.get("success"):
                    issue_data = issues.get("result", [])
                    if issue_data:
                        df = pd.DataFrame(issue_data)
                        df['created_at'] = pd.to_datetime(df['created_at'])
                        
                        fig = px.histogram(df, x='created_at', 
                                         title="Issue Creation Trends",
                                         labels={'created_at': 'Date', 'count': 'Issues'})
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#2c3e50')
                        )
                        st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error creating visualizations: {e}")

def create_file_explorer(repo_url=None):
    """Create interactive file explorer"""
    if not repo_url:
        st.markdown("""
        <div class="modern-card">
            <h3>📁 File Explorer</h3>
            <p>Select a repository to explore its file structure.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div class="modern-card">
        <h3>📁 File Explorer</h3>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with SyncMCPClient() as client:
            # Get repository structure
            # This would need to be implemented in the MCP server
            st.info("File explorer feature coming soon!")
    except Exception as e:
        st.error(f"Error loading file explorer: {e}")

def create_commit_timeline(repo_url=None):
    """Create commit timeline"""
    if not repo_url:
        st.markdown("""
        <div class="modern-card">
            <h3>🕒 Commit Timeline</h3>
            <p>Select a repository to view commit history.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div class="modern-card">
        <h3>🕒 Recent Commits</h3>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with SyncMCPClient() as client:
            commits = client.get_recent_commits(repo_url, 10)
            if commits.get("success"):
                commit_data = commits.get("result", [])
                
                st.markdown('<div class="timeline">', unsafe_allow_html=True)
                for commit in commit_data:
                    st.markdown(f"""
                    <div class="timeline-item">
                        <strong>{commit.get('sha', 'N/A')}</strong><br>
                        <em>{commit.get('message', 'No message')}</em><br>
                        <small>By {commit.get('author', 'Unknown')} on {commit.get('date', 'Unknown')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Failed to load commits")
    except Exception as e:
        st.error(f"Error loading commits: {e}")

def create_issues_table(repo_url=None):
    """Create issues table"""
    if not repo_url:
        st.markdown("""
        <div class="modern-card">
            <h3>🐛 Issues & PRs</h3>
            <p>Select a repository to view issues and pull requests.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div class="modern-card">
        <h3>🐛 Issues & Pull Requests</h3>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with SyncMCPClient() as client:
            issues = client.get_issues(repo_url, "open", 10)
            if issues.get("success"):
                issue_data = issues.get("result", [])
                
                if issue_data:
                    # Create a simple table
                    for issue in issue_data:
                        st.markdown(f"""
                        <div class="modern-card" style="margin-bottom: 12px;">
                            <strong>#{issue.get('number', 'N/A')} - {issue.get('title', 'No title')}</strong><br>
                            <small>By {issue.get('author', 'Unknown')} • {issue.get('state', 'Unknown')} • {issue.get('created_at', 'Unknown')}</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No issues found")
            else:
                st.error("Failed to load issues")
    except Exception as e:
        st.error(f"Error loading issues: {e}")

def create_floating_actions():
    """Create floating action buttons"""
    st.markdown("""
    <div class="fab" onclick="clearChat()">🗑️</div>
    <script>
    function clearChat() {
        // Clear chat functionality
        console.log('Clear chat clicked');
    }
    </script>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Load CSS
    load_css()
    
    # Load configuration
    try:
        config = load_config()
        st.session_state.config = config
    except Exception as e:
        st.error(f"Failed to load configuration: {e}")
        return
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'repository_url' not in st.session_state:
        st.session_state.repository_url = ""
    
    if 'ai_agent' not in st.session_state:
        st.session_state.ai_agent = None
    
    if 'theme' not in st.session_state:
        st.session_state.theme = "light"
    
    if 'agent_type' not in st.session_state:
        st.session_state.agent_type = "Single Agent"
    
    # Create header
    create_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Theme toggle
        if st.button("🌙 Toggle Theme"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()
        
        # GitHub Token
        github_token = st.text_input(
            "GitHub Token",
            type="password",
            help="Enter your GitHub personal access token",
            value=os.getenv("GITHUB_TOKEN", "")
        )
        
        if github_token:
            os.environ["GITHUB_TOKEN"] = github_token
        
        # AI API Key
        ai_provider = st.selectbox(
            "AI Provider",
            ["OpenAI", "Anthropic"],
            help="Choose your AI provider"
        )
        
        if ai_provider == "OpenAI":
            openai_key = st.text_input(
                "OpenAI API Key",
                type="password",
                help="Enter your OpenAI API key",
                value=os.getenv("OPENAI_API_KEY", "")
            )
            if openai_key:
                os.environ["OPENAI_API_KEY"] = openai_key
        else:
            anthropic_key = st.text_input(
                "Anthropic API Key",
                type="password",
                help="Enter your Anthropic API key",
                value=os.getenv("ANTHROPIC_API_KEY", "")
            )
            if anthropic_key:
                os.environ["ANTHROPIC_API_KEY"] = anthropic_key
        
        # Agent System Selection
        agent_type, model = create_agent_selector()
        st.session_state.agent_type = agent_type
        
        # MCP Server Status
        st.markdown("### 🔧 MCP Servers")
        
        if st.button("🚀 Start MCP Servers"):
            with st.spinner("Starting MCP servers..."):
                if start_mcp_servers():
                    st.success("✅ MCP servers started successfully!")
                else:
                    st.error("❌ Failed to start MCP servers")
        
        # Check server status
        server_status = check_servers_status()
        for server_name, status in server_status.items():
            status_icon = "✅" if status else "❌"
            st.text(f"{status_icon} {server_name.replace('_', ' ').title()}")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📊 Export Data"):
            # Export functionality
            st.info("Export feature coming soon!")
    
    # Main content
    if not github_token:
        st.warning("⚠️ Please enter your GitHub token in the sidebar to continue.")
        return
    
    # Repository selector
    repo_url = render_repository_selector()
    
    if repo_url:
        st.session_state.repository_url = repo_url
        
        # Create AI agent if not exists or if agent type changed
        if (st.session_state.ai_agent is None or 
            hasattr(st.session_state, 'last_agent_type') and 
            st.session_state.last_agent_type != agent_type):
            
            try:
                if agent_type == "Legacy System":
                    # Use legacy agent system
                    model = "gpt-4" if os.getenv("OPENAI_API_KEY") else "claude-3-sonnet"
                    st.session_state.ai_agent = create_ai_agent(model, config)
                else:
                    # Use advanced-based system
                    st.session_state.ai_agent = {
                        "type": agent_type,
                        "model": model,
                        "config": config
                    }
                
                st.session_state.last_agent_type = agent_type
                
            except Exception as e:
                st.error(f"Failed to create AI agent: {e}")
                return
        
        # Stats cards
        create_stats_cards()
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏠 Overview", "📁 Files", "🕒 Commits", "🐛 Issues", "💬 Chat", "📊 Analytics"
        ])
        
        with tab1:
            # Overview tab
            create_insights_panel(repo_url, agent_type)
            create_visualizations(repo_url)
        
        with tab2:
            # Files tab
            create_file_explorer(repo_url)
        
        with tab3:
            # Commits tab
            create_commit_timeline(repo_url)
        
        with tab4:
            # Issues tab
            create_issues_table(repo_url)
        
        with tab5:
            # Chat tab
            if agent_type == "Legacy System":
                render_chat_interface(st.session_state.ai_agent)
            else:
                # advanced-based chat interface
                st.markdown("### 💬 AI Chat with advanced Agents")
                
                # Chat input
                user_question = st.text_input(
                    "Ask a question about the repository:",
                    placeholder="e.g., What is this repository about? Find authentication code..."
                )
                
                if st.button("🤖 Ask AI Agent"):
                    if user_question:
                        with st.spinner("🤖 AI agent is thinking..."):
                            try:
                                if agent_type == "Multi-Agent Team":
                                    response = ask_question_advanced(
                                        user_question, 
                                        repo_url, 
                                        use_team=True
                                    )
                                else:
                                    response = ask_question_advanced(
                                        user_question, 
                                        repo_url, 
                                        use_team=False
                                    )
                                
                                st.markdown("### 🤖 AI Response")
                                st.markdown(response)
                                
                                # Add to chat history
                                st.session_state.messages.append({
                                    "role": "user",
                                    "content": user_question
                                })
                                st.session_state.messages.append({
                                    "role": "assistant", 
                                    "content": response
                                })
                                
                            except Exception as e:
                                st.error(f"Error getting AI response: {e}")
                
                # Chat history
                if st.session_state.messages:
                    st.markdown("### 💬 Chat History")
                    for message in st.session_state.messages[-6:]:  # Show last 6 messages
                        if message["role"] == "user":
                            st.markdown(f"**You:** {message['content']}")
                        else:
                            st.markdown(f"**AI:** {message['content']}")
                        st.divider()
        
        with tab6:
            # Analytics tab
            st.markdown("""
            <div class="modern-card">
                <h3>📊 Advanced Analytics</h3>
                <p>Advanced analytics and insights coming soon!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Floating actions
    create_floating_actions()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #6c757d; padding: 20px;'>
            <p>Built with ❤️ using Streamlit, AI agents, and MCP servers</p>
            <p>🚀 Modern UI • 🤖 AI-Powered • 📊 Rich Insights</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 