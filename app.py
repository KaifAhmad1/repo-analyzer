"""
🚀 GitHub Repository Analyzer - Streamlined UI (FastMCP v2)
A clean, modern interface for analyzing GitHub repositories using FastMCP v2 servers and AI agents
"""

import streamlit as st
import os
from src.ui.repository_selector import render_repository_selector
from src.ui.chat_interface import render_chat_interface
from src.ui.settings_sidebar import render_settings_sidebar
from src.agent.ai_agent import get_repository_overview, analyze_repository
from src.servers.server_manager import get_servers_status

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

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 📁 Repository Selector")
    repo_url = render_repository_selector()
    st.markdown("---")
    repo_info = None
    if repo_url:
        try:
            repo_info = get_repository_overview(repo_url)
            if isinstance(repo_info, str):
                import json
                repo_info = json.loads(repo_info)
        except Exception:
            repo_info = None
    if repo_info and isinstance(repo_info, dict):
        st.markdown(f"**{repo_info.get('name', 'Repository')}**")
        st.caption(repo_info.get('description', 'No description'))
        st.write(f"⭐ {repo_info.get('stars', 0)} | 🍴 {repo_info.get('forks', 0)} | 🕒 Updated: {repo_info.get('last_updated', repo_info.get('updated_at', ''))}")
    st.markdown("---")
    render_settings_sidebar()
    st.markdown("---")
    st.markdown("### 🖥️ Server Status")
    status = get_servers_status()
    for server_name, server in status["servers"].items():
        icon = "✅" if server["running"] else "❌"
        st.write(f"{icon} {server['name']}")

# --- MAIN AREA ---
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🚀 GitHub Repository Analyzer</h1>
    <p class="header-subtitle">AI-Powered Repository Analysis with FastMCP v2</p>
</div>
""", unsafe_allow_html=True)

# Tabs for main features
TABS = ["Q&A Chat", "Code Analysis", "Visual Repo Map", "Smart Summary"]
tab1, tab2, tab3, tab4 = st.tabs(TABS)

with tab1:
    render_chat_interface(repo_url)

with tab2:
    st.markdown("### 🧑‍💻 Code Analysis")
    if repo_url:
        from src.agent.ai_agent import get_code_metrics
        metrics = get_code_metrics(repo_url)
        st.write(metrics)
        # Add more code analysis features as needed
    else:
        st.info("Select a repository to analyze code.")

with tab3:
    st.markdown("### 🗺️ Visual Repository Map")
    if repo_url:
        from src.agent.ai_agent import get_directory_tree
        tree = get_directory_tree(repo_url)
        st.write(tree)
        # Optionally, add a Plotly or Graphviz visualization here
    else:
        st.info("Select a repository to view its structure.")

with tab4:
    st.markdown("### 📝 Smart Repository Summary")
    if repo_url:
        summary = analyze_repository(repo_url)
        st.write(summary)
    else:
        st.info("Select a repository to get a summary.") 