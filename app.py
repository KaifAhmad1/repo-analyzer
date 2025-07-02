"""
🚀 GitHub Repository Analyzer - Streamlined UI (FastMCP v2)
A clean, modern interface for analyzing GitHub repositories using FastMCP v2 servers and Groq AI
"""

import streamlit as st
import os
from datetime import datetime
from src.ui.repository_selector import render_repository_selector
from src.ui.chat_interface import render_chat_interface
from src.ui.settings_sidebar import render_settings_sidebar
from src.agent.ai_agent import get_repository_overview, analyze_repository, FastMCPTools
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

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_repo' not in st.session_state:
    st.session_state.current_repo = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}

# --- SIDEBAR ---
with st.sidebar:
    # Repository Selector Section
    st.markdown("## 📁 Repository")
    repo_url = render_repository_selector()
    
    # Repository Info
    if repo_url and repo_url != st.session_state.get('current_repo'):
        st.session_state.current_repo = repo_url
        try:
            repo_info = get_repository_overview(repo_url)
            # Handle both old string format and new tuple format
            if isinstance(repo_info, tuple):
                repo_info_text, tools_used = repo_info
                if isinstance(repo_info_text, str):
                    import json
                    try:
                        repo_info = json.loads(repo_info_text)
                    except:
                        repo_info = {"name": "Repository", "description": repo_info_text}
            elif isinstance(repo_info, str):
                import json
                try:
                    repo_info = json.loads(repo_info)
                except:
                    repo_info = {"name": "Repository", "description": repo_info}
            
            if repo_info and isinstance(repo_info, dict):
                st.markdown("### 📋 Repository Info")
                st.markdown(f"**{repo_info.get('name', 'Repository')}**")
                st.caption(repo_info.get('description', 'No description'))
                st.write(f"⭐ {repo_info.get('stars', 0)} | 🍴 {repo_info.get('forks', 0)} | 🕒 Updated: {repo_info.get('last_updated', repo_info.get('updated_at', ''))}")
        except Exception as e:
            st.error(f"❌ Error loading repository: {str(e)}")
    
    st.markdown("---")
    
    # Settings Section
    settings = render_settings_sidebar()
    
    st.markdown("---")
    
    # Server Status Section
    st.markdown("### 🖥️ Server Status")
    status = get_servers_status()
    for server_name, server in status["servers"].items():
        icon = "✅" if server["running"] else "❌"
        st.write(f"{icon} {server['name']}")

# --- MAIN AREA ---
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🚀 GitHub Repository Analyzer</h1>
    <p class="header-subtitle">AI-Powered Repository Analysis with FastMCP v2 & Groq</p>
</div>
""", unsafe_allow_html=True)

# Tabs for main features
TABS = ["💬 Q&A Chat", "🔍 Code Analysis", "🗺️ Visual Repo Map", "📊 Smart Summary"]
tab1, tab2, tab3, tab4 = st.tabs(TABS)

with tab1:
    render_chat_interface(repo_url)

with tab2:
    st.markdown("### 🔍 Code Analysis")
    if repo_url:
        # Analysis Controls
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            analysis_type = st.selectbox(
                "Analysis Type:",
                ["Code Metrics", "File Structure", "Dependencies", "Code Patterns", "All Analysis"],
                help="Select what type of analysis you want to perform"
            )
        
        with col2:
            analysis_depth = st.slider(
                "Analysis Depth:",
                min_value=1,
                max_value=5,
                value=settings.get("analysis_depth", 3),
                help="How deep to analyze the repository"
            )
        
        with col3:
            if st.button("🔍 Run Analysis", type="primary", use_container_width=True):
                st.session_state.run_analysis = True
        
        # Run analysis if requested
        if st.session_state.get("run_analysis", False):
            st.session_state.run_analysis = False
            tools = FastMCPTools()
            
            # Progress container
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    if analysis_type == "Code Metrics":
                        status_text.text("📊 Analyzing code metrics...")
                        progress_bar.progress(25)
                        metrics = tools.get_code_metrics(repo_url)
                        progress_bar.progress(100)
                        st.success("✅ Code metrics analysis complete!")
                        
                        # Display metrics in a nice format
                        st.markdown("### 📊 Code Metrics")
                        st.json(metrics)
                        
                    elif analysis_type == "File Structure":
                        status_text.text("📁 Analyzing file structure...")
                        progress_bar.progress(25)
                        structure = tools.get_file_structure(repo_url)
                        progress_bar.progress(100)
                        st.success("✅ File structure analysis complete!")
                        
                        st.markdown("### 📁 File Structure")
                        st.json(structure)
                        
                    elif analysis_type == "Dependencies":
                        status_text.text("📦 Analyzing dependencies...")
                        progress_bar.progress(25)
                        deps = tools.search_dependencies(repo_url)
                        progress_bar.progress(100)
                        st.success("✅ Dependency analysis complete!")
                        
                        st.markdown("### 📦 Dependencies")
                        st.json(deps)
                        
                    elif analysis_type == "Code Patterns":
                        status_text.text("🔍 Analyzing code patterns...")
                        progress_bar.progress(25)
                        patterns = tools.search_code(repo_url, "function class def")
                        progress_bar.progress(100)
                        st.success("✅ Code pattern analysis complete!")
                        
                        st.markdown("### 🔍 Code Patterns")
                        st.json(patterns)
                        
                    elif analysis_type == "All Analysis":
                        status_text.text("🔍 Starting comprehensive analysis...")
                        progress_bar.progress(20)
                        
                        status_text.text("📊 Analyzing code metrics...")
                        metrics = tools.get_code_metrics(repo_url)
                        progress_bar.progress(40)
                        
                        status_text.text("📁 Analyzing file structure...")
                        structure = tools.get_file_structure(repo_url)
                        progress_bar.progress(60)
                        
                        status_text.text("📦 Analyzing dependencies...")
                        deps = tools.search_dependencies(repo_url)
                        progress_bar.progress(80)
                        
                        status_text.text("🔍 Analyzing code patterns...")
                        patterns = tools.search_code(repo_url, "function class def")
                        progress_bar.progress(100)
                        
                        st.success("✅ Comprehensive analysis complete!")
                        
                        # Display all results in tabs
                        tab1, tab2, tab3, tab4 = st.tabs(["📊 Metrics", "📁 Structure", "📦 Dependencies", "🔍 Patterns"])
                        with tab1:
                            st.json(metrics)
                        with tab2:
                            st.json(structure)
                        with tab3:
                            st.json(deps)
                        with tab4:
                            st.json(patterns)
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                finally:
                    progress_bar.empty()
                    status_text.empty()
    else:
        st.info("🎯 Please select a repository to analyze code.")

with tab3:
    st.markdown("### 🗺️ Visual Repository Map")
    if repo_url:
        # Visualization Controls
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            viz_type = st.selectbox(
                "Visualization Type:",
                ["Directory Tree", "File Structure", "Project Analysis", "Interactive Tree"],
                help="Select how you want to visualize the repository structure"
            )
        
        with col2:
            max_depth = st.slider("Maximum depth:", min_value=1, max_value=5, value=3, help="How deep to explore the directory structure")
        
        with col3:
            if st.button("🗺️ Generate", type="primary", use_container_width=True):
                st.session_state.generate_viz = True
        
        # Generate visualization if requested
        if st.session_state.get("generate_viz", False):
            st.session_state.generate_viz = False
            tools = FastMCPTools()
            
            # Progress container
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("🗺️ Generating visualization...")
                    progress_bar.progress(50)
                    
                    if viz_type == "Directory Tree":
                        tree_data = tools.get_directory_tree(repo_url, max_depth)
                        progress_bar.progress(100)
                        st.success("✅ Directory tree generated!")
                        
                        st.markdown("### 📁 Directory Tree")
                        st.code(tree_data, language="text")
                        
                    elif viz_type == "File Structure":
                        structure_data = tools.get_file_structure(repo_url)
                        progress_bar.progress(100)
                        st.success("✅ File structure generated!")
                        
                        st.markdown("### 📁 File Structure")
                        st.json(structure_data)
                        
                    elif viz_type == "Project Analysis":
                        analysis_data = tools.analyze_project_structure(repo_url)
                        progress_bar.progress(100)
                        st.success("✅ Project analysis generated!")
                        
                        st.markdown("### 🏗️ Project Analysis")
                        st.json(analysis_data)
                        
                    elif viz_type == "Interactive Tree":
                        tree_data = tools.get_directory_tree(repo_url, max_depth)
                        progress_bar.progress(100)
                        st.success("✅ Interactive tree generated!")
                        
                        st.markdown("### 🌳 Interactive Directory Tree")
                        st.code(tree_data, language="text")
                        
                        # Add interactive features
                        st.markdown("#### 🔍 Explore Specific Paths")
                        path_to_explore = st.text_input("Enter path to explore:", placeholder="src/")
                        if path_to_explore and st.button("🔍 Explore Path"):
                            path_content = tools.list_directory(repo_url, path_to_explore)
                            st.json(path_content)
                    
                except Exception as e:
                    st.error(f"❌ Visualization failed: {str(e)}")
                finally:
                    progress_bar.empty()
                    status_text.empty()
    else:
        st.info("🎯 Please select a repository to generate visualizations.")

with tab4:
    st.markdown("### 📊 Smart Summary")
    if repo_url:
        # Summary Controls
        col1, col2 = st.columns([3, 1])
        
        with col1:
            summary_type = st.selectbox(
                "Summary Type:",
                ["Repository Overview", "Code Quality Analysis", "Architecture Review", "Development Insights", "Comprehensive Report"],
                help="Select the type of summary you want"
            )
        
        with col2:
            if st.button("📊 Generate", type="primary", use_container_width=True):
                st.session_state.generate_summary = True
        
        # Generate summary if requested
        if st.session_state.get("generate_summary", False):
            st.session_state.generate_summary = False
            
            # Progress container
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("📊 Generating smart summary...")
                    progress_bar.progress(30)
                    
                    # Use AI agent to generate summary
                    from src.agent.ai_agent import ask_question
                    
                    if summary_type == "Repository Overview":
                        question = "Provide a comprehensive overview of this repository including its purpose, main features, and key components."
                    elif summary_type == "Code Quality Analysis":
                        question = "Analyze the code quality of this repository, including code structure, patterns, and potential improvements."
                    elif summary_type == "Architecture Review":
                        question = "Review the architecture of this repository, including design patterns, structure, and scalability considerations."
                    elif summary_type == "Development Insights":
                        question = "Provide insights about the development process, commit patterns, and project health."
                    else:  # Comprehensive Report
                        question = "Generate a comprehensive report covering all aspects of this repository including overview, architecture, code quality, and development insights."
                    
                    progress_bar.progress(60)
                    response, tools_used = ask_question(question, repo_url)
                    progress_bar.progress(100)
                    
                    st.success("✅ Smart summary generated!")
                    
                    # Display summary
                    st.markdown(f"### 📊 {summary_type}")
                    st.markdown(response)
                    
                    # Show tools used if enabled
                    if settings.get("show_tool_usage", True) and tools_used:
                        st.markdown("#### 🔧 Tools Used")
                        for tool in tools_used:
                            st.write(f"• {tool}")
                    
                except Exception as e:
                    st.error(f"❌ Summary generation failed: {str(e)}")
                finally:
                    progress_bar.empty()
                    status_text.empty()
    else:
        st.info("🎯 Please select a repository to generate summaries.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    🚀 Powered by FastMCP v2 & Groq AI | Built with Streamlit
</div>
""", unsafe_allow_html=True) 