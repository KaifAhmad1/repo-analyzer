"""
Main Streamlit Application

This is the main entry point for the GitHub Repository Analyzer Streamlit application.
Provides a chat-like interface for asking questions about GitHub repositories using Agno.
"""

import streamlit as st
import os
import json
import asyncio
from typing import Dict, List, Any
from datetime import datetime

# Import our components
from ui.components.repository_selector import RepositorySelector
from ai_agent.agent import GitHubRepositoryAgent

def main():
    """
    Main Streamlit application function.
    """
    # Configure page
    st.set_page_config(
        page_title="GitHub Repository Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Load configuration
    config = load_config()
    
    # Main layout
    st.title("🔍 GitHub Repository Analyzer")
    st.markdown("Ask questions about any GitHub repository and get intelligent answers powered by Agno!")
    
    # Sidebar for repository selection and settings
    with st.sidebar:
        st.header("Repository Settings")
        
        # Repository selector
        repository_selector = RepositorySelector()
        selected_repo = repository_selector.render()
        
        if selected_repo:
            st.success(f"Selected: {selected_repo}")
            
            # Repository statistics
            st.header("Repository Stats")
            display_repository_stats(selected_repo)
        
        # AI Model Settings
        st.header("AI Settings")
        model_provider = st.selectbox(
            "AI Provider",
            ["openai", "anthropic"],
            key="model_provider"
        )
        
        model_name = st.selectbox(
            "Model",
            ["gpt-4", "gpt-3.5-turbo"] if model_provider == "openai" else ["claude-3-sonnet", "claude-3-haiku"],
            key="model_name"
        )
        
        # Initialize AI agent
        if st.button("Initialize AI Agent"):
            try:
                agent = GitHubRepositoryAgent(model_provider, model_name)
                st.session_state.agent = agent
                st.success("AI Agent initialized successfully!")
            except Exception as e:
                st.error(f"Failed to initialize AI agent: {e}")
    
    # Main content area
    if selected_repo:
        # Chat interface
        st.header("Ask Questions")
        
        # Initialize agent if not already done
        if "agent" not in st.session_state:
            st.warning("Please initialize the AI agent in the sidebar first.")
        else:
            render_chat_interface(selected_repo, st.session_state.agent)
        
        # Tool usage display
        st.header("Tool Usage")
        display_tool_usage()
        
        # Advanced features
        st.header("Advanced Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Code Analysis"):
                if "agent" in st.session_state:
                    run_code_analysis(selected_repo, st.session_state.agent)
                else:
                    st.warning("Please initialize the AI agent first.")
        
        with col2:
            if st.button("🗺️ Visual Map"):
                if "agent" in st.session_state:
                    generate_repository_visualization(selected_repo, st.session_state.agent)
                else:
                    st.warning("Please initialize the AI agent first.")
        
        with col3:
            if st.button("📝 Smart Summary"):
                if "agent" in st.session_state:
                    generate_repository_summary(selected_repo, st.session_state.agent)
                else:
                    st.warning("Please initialize the AI agent first.")
    
    else:
        # Welcome screen
        st.markdown("""
        ## Welcome to GitHub Repository Analyzer!
        
        This intelligent Q&A system can help you understand any GitHub repository by:
        
        - **Analyzing code structure** and organization
        - **Exploring commit history** and changes
        - **Searching through code** and documentation
        - **Understanding dependencies** and relationships
        - **Identifying patterns** and best practices
        
        ### How to get started:
        1. Select a repository from the sidebar
        2. Initialize the AI agent with your preferred model
        3. Ask questions about the codebase
        4. Explore advanced features for deeper analysis
        
        ### Example questions you can ask:
        - "What is this repository about?"
        - "Show me the main entry points"
        - "What are the recent changes?"
        - "Find all authentication functions"
        - "What dependencies does this project use?"
        """)
        
        # Quick start examples
        st.header("Quick Start Examples")
        
        example_questions = [
            "What is this repository about and what does it do?",
            "Show me the main entry points of this application",
            "What are the recent changes in the last 10 commits?",
            "Find all functions related to authentication",
            "What dependencies does this project use?",
            "Are there any open issues related to performance?",
            "Explain how the database connection is implemented",
            "What's the testing strategy used in this project?"
        ]
        
        for i, question in enumerate(example_questions, 1):
            st.write(f"{i}. {question}")

def init_session_state():
    """
    Initialize Streamlit session state variables.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "selected_repository" not in st.session_state:
        st.session_state.selected_repository = None
    
    if "tool_usage" not in st.session_state:
        st.session_state.tool_usage = []
    
    if "repository_stats" not in st.session_state:
        st.session_state.repository_stats = {}

def load_config() -> Dict[str, Any]:
    """
    Load application configuration.
    """
    return {
        "mcp_servers": {
            "host": os.getenv("MCP_SERVER_HOST", "localhost"),
            "port": int(os.getenv("MCP_SERVER_PORT", "8000"))
        },
        "ai_model": {
            "provider": os.getenv("AI_PROVIDER", "openai"),
            "model": os.getenv("AI_MODEL", "gpt-4")
        }
    }

def render_chat_interface(repository: str, agent: GitHubRepositoryAgent):
    """
    Render the chat interface for asking questions.
    """
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about the repository..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                # Process question with AI agent
                with st.spinner("Analyzing repository..."):
                    # Run async function in sync context
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        response = loop.run_until_complete(
                            agent.process_question(prompt, repository)
                        )
                    finally:
                        loop.close()
                
                # Display response
                message_placeholder.markdown(response["answer"])
                
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response["answer"]
                })
                
                # Track tool usage
                if response.get("tool_usage"):
                    st.session_state.tool_usage.extend(response["tool_usage"])
                
                # Display tool usage info
                if response.get("tool_usage"):
                    with st.expander("🔧 Tools Used"):
                        for tool in response["tool_usage"]:
                            st.write(f"**{tool.get('tool', 'Unknown')}**: {tool.get('result', 'No result')}")
                
            except Exception as e:
                message_placeholder.error(f"Error processing question: {e}")

def display_repository_stats(repository: str):
    """
    Display repository statistics.
    """
    try:
        # Placeholder for repository stats
        st.metric("Repository", repository)
        st.metric("Status", "Active")
        st.metric("Last Updated", "Today")
        
        # Add more stats as needed
        st.info("Repository statistics will be displayed here")
        
    except Exception as e:
        st.error(f"Error loading repository stats: {e}")

def display_tool_usage():
    """
    Display tool usage history.
    """
    if st.session_state.tool_usage:
        for i, tool_usage in enumerate(st.session_state.tool_usage[-5:]):  # Show last 5
            with st.expander(f"Tool Usage {i+1}"):
                st.json(tool_usage)
    else:
        st.info("No tool usage recorded yet.")

def run_code_analysis(repository: str, agent: GitHubRepositoryAgent):
    """
    Run code analysis on the repository.
    """
    try:
        with st.spinner("Running code analysis..."):
            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    agent.analyze_code_quality(repository)
                )
            finally:
                loop.close()
        
        st.success("Code analysis completed!")
        st.json(result)
        
    except Exception as e:
        st.error(f"Error running code analysis: {e}")

def generate_repository_visualization(repository: str, agent: GitHubRepositoryAgent):
    """
    Generate repository visualization.
    """
    try:
        with st.spinner("Generating repository visualization..."):
            # Placeholder for visualization
            st.info("Repository visualization feature coming soon!")
            
            # This would integrate with the repository structure server
            # to generate visual maps of the codebase
        
    except Exception as e:
        st.error(f"Error generating visualization: {e}")

def generate_repository_summary(repository: str, agent: GitHubRepositoryAgent):
    """
    Generate repository summary.
    """
    try:
        with st.spinner("Generating repository summary..."):
            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    agent.analyze_repository_overview(repository)
                )
            finally:
                loop.close()
        
        st.success("Repository summary generated!")
        st.markdown(result["answer"])
        
    except Exception as e:
        st.error(f"Error generating repository summary: {e}")

if __name__ == "__main__":
    main() 