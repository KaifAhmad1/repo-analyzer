"""
GitHub Repository Analyzer - Main Application
A simplified Q&A system for GitHub repositories using MCP servers and AI agents.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.agent.ai_agent import create_ai_agent
from src.servers.server_manager import start_mcp_servers, stop_mcp_servers
from src.ui.chat_interface import render_chat_interface
from src.ui.repository_selector import render_repository_selector
from src.utils.config import load_config
from src.utils.github import validate_github_token

# Inject custom CSS for modern styling and animations
with open(Path(__file__).parent / "src" / "ui" / "styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="GitHub Repository Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load configuration
    config = load_config()
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'repository_url' not in st.session_state:
        st.session_state.repository_url = ""
    if 'ai_agent' not in st.session_state:
        st.session_state.ai_agent = None
    if 'servers_started' not in st.session_state:
        st.session_state.servers_started = False
    
    # Sidebar for configuration
    with st.sidebar:
        st.title("🔍 Repository Analyzer")
        st.markdown("---")
        
        # GitHub Token Input
        github_token = st.text_input(
            "GitHub Token",
            type="password",
            help="Enter your GitHub personal access token"
        )
        
        if github_token:
            if validate_github_token(github_token):
                st.success("✅ GitHub token validated")
                os.environ['GITHUB_TOKEN'] = github_token
            else:
                st.error("❌ Invalid GitHub token")
                return
        
        # AI Model Selection
        ai_model = st.selectbox(
            "AI Model",
            ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"],
            help="Choose the AI model for analysis"
        )
        
        # Start/Stop Servers
        if st.button("🚀 Start MCP Servers"):
            if not st.session_state.servers_started:
                try:
                    start_mcp_servers()
                    st.session_state.servers_started = True
                    st.success("✅ MCP Servers started successfully")
                except Exception as e:
                    st.error(f"❌ Failed to start servers: {e}")
        
        if st.button("🛑 Stop MCP Servers"):
            if st.session_state.servers_started:
                try:
                    stop_mcp_servers()
                    st.session_state.servers_started = False
                    st.success("✅ MCP Servers stopped")
                except Exception as e:
                    st.error(f"❌ Failed to stop servers: {e}")
        
        # Repository Information
        if st.session_state.repository_url:
            st.markdown("---")
            st.subheader("📁 Current Repository")
            st.write(st.session_state.repository_url)
    
    # Main content area
    st.title("🔍 GitHub Repository Analyzer")
    st.markdown("Ask questions about any GitHub repository and get intelligent answers!")
    
    # Repository selector
    repository_url = render_repository_selector()
    
    if repository_url and repository_url != st.session_state.repository_url:
        st.session_state.repository_url = repository_url
        st.session_state.messages = []  # Clear previous conversation
        st.session_state.ai_agent = None  # Reset AI agent
    
    # Chat interface
    if st.session_state.repository_url and st.session_state.servers_started:
        if st.session_state.ai_agent is None:
            st.session_state.ai_agent = create_ai_agent(ai_model, config)
        
        render_chat_interface(st.session_state.ai_agent)
    elif st.session_state.repository_url and not st.session_state.servers_started:
        st.warning("⚠️ Please start the MCP servers to begin analysis")
    else:
        st.info("👆 Please select a GitHub repository to get started")

if __name__ == "__main__":
    main() 