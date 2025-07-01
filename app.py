"""
🚀 GitHub Repository Analyzer - Streamlined UI (FastMCP v2)
A clean, modern interface for analyzing GitHub repositories using FastMCP v2 servers and AI agents
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

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 📁 Repository Selector")
    repo_url = render_repository_selector()
    st.markdown("---")
    repo_info = None
    if repo_url:
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
        # Add analysis options
        analysis_type = st.selectbox(
            "Choose analysis type:",
            ["Code Metrics", "File Structure", "Dependencies", "Code Patterns", "All Analysis"],
            help="Select what type of analysis you want to perform"
        )
        
        if st.button("🔍 Run Analysis", type="primary", use_container_width=True):
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
        # Add visualization options
        viz_type = st.selectbox(
            "Choose visualization type:",
            ["Directory Tree", "File Structure", "Project Analysis", "Interactive Tree"],
            help="Select how you want to visualize the repository structure"
        )
        
        max_depth = st.slider("Maximum depth:", min_value=1, max_value=5, value=3, help="How deep to explore the directory structure")
        
        if st.button("🗺️ Generate Visualization", type="primary", use_container_width=True):
            tools = FastMCPTools()
            
            # Progress container
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    if viz_type == "Directory Tree":
                        status_text.text("🌳 Generating directory tree...")
                        progress_bar.progress(50)
                        tree = tools.get_directory_tree(repo_url, max_depth=max_depth)
                        progress_bar.progress(100)
                        st.success("✅ Directory tree generated!")
                        
                        st.markdown("### 🌳 Directory Tree")
                        st.code(tree, language="text")
                        
                    elif viz_type == "File Structure":
                        status_text.text("📁 Analyzing file structure...")
                        progress_bar.progress(50)
                        structure = tools.get_file_structure(repo_url)
                        progress_bar.progress(100)
                        st.success("✅ File structure analysis complete!")
                        
                        st.markdown("### 📁 File Structure")
                        st.json(structure)
                        
                    elif viz_type == "Project Analysis":
                        status_text.text("🔍 Analyzing project structure...")
                        progress_bar.progress(50)
                        analysis = tools.analyze_project_structure(repo_url)
                        progress_bar.progress(100)
                        st.success("✅ Project analysis complete!")
                        
                        st.markdown("### 🔍 Project Analysis")
                        st.json(analysis)
                        
                    elif viz_type == "Interactive Tree":
                        status_text.text("🌳 Building interactive tree...")
                        progress_bar.progress(50)
                        tree = tools.get_directory_tree(repo_url, max_depth=max_depth)
                        progress_bar.progress(100)
                        st.success("✅ Interactive tree ready!")
                        
                        st.markdown("### 🌳 Interactive Directory Tree")
                        
                        # Create a simple interactive tree using expandable sections
                        tree_lines = tree.split('\n')
                        current_level = 0
                        
                        for line in tree_lines:
                            if line.strip():
                                # Count leading spaces to determine level
                                level = len(line) - len(line.lstrip())
                                indent = "  " * (level // 2)
                                
                                if level == 0:  # Root level
                                    st.markdown(f"**{line.strip()}**")
                                else:
                                    st.markdown(f"{indent}📁 {line.strip()}")
                    
                except Exception as e:
                    st.error(f"❌ Visualization failed: {str(e)}")
                finally:
                    progress_bar.empty()
                    status_text.empty()
    else:
        st.info("🎯 Please select a repository to view its structure.")

with tab4:
    st.markdown("### 📝 Smart Repository Summary")
    if repo_url:
        # Add summary options
        summary_type = st.selectbox(
            "Choose summary type:",
            ["Quick Overview", "Detailed Analysis", "Technical Summary", "Contributor Analysis", "Full Repository Report"],
            help="Select the type of summary you want to generate"
        )
        
        include_metrics = st.checkbox("Include code metrics", value=True, help="Include code metrics in the summary")
        include_structure = st.checkbox("Include project structure", value=True, help="Include project structure analysis")
        
        if st.button("📝 Generate Summary", type="primary", use_container_width=True):
            # Progress container
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("🤖 Initializing AI analysis...")
                    progress_bar.progress(20)
                    
                    status_text.text("📊 Gathering repository data...")
                    progress_bar.progress(40)
                    
                    status_text.text("🧠 Generating AI summary...")
                    progress_bar.progress(60)
                    
                    # Generate the summary based on type
                    if summary_type == "Quick Overview":
                        summary, tools_used = analyze_repository(repo_url)
                    elif summary_type == "Detailed Analysis":
                        summary, tools_used = analyze_repository(repo_url)
                        summary += "\n\n" + "Detailed analysis with additional insights..."
                    elif summary_type == "Technical Summary":
                        summary, tools_used = analyze_repository(repo_url)
                        summary += "\n\n" + "Technical architecture and implementation details..."
                    elif summary_type == "Contributor Analysis":
                        summary, tools_used = analyze_repository(repo_url)
                        summary += "\n\n" + "Contributor activity and collaboration patterns..."
                    elif summary_type == "Full Repository Report":
                        summary, tools_used = analyze_repository(repo_url)
                        summary += "\n\n" + "Comprehensive repository analysis report..."
                    
                    progress_bar.progress(80)
                    
                    status_text.text("📋 Formatting results...")
                    progress_bar.progress(100)
                    
                    st.success("✅ Summary generated successfully!")
                    
                    # Display the summary
                    st.markdown("### 📝 Generated Summary")
                    st.markdown(summary)
                    
                    # Display tools used if available
                    if tools_used:
                        st.markdown("### 🔧 MCP Tools Used")
                        tool_descriptions = {
                            "get_file_content": "📄 File Content",
                            "list_directory": "📁 Directory Listing", 
                            "get_readme_content": "📖 README Content",
                            "get_directory_tree": "🌳 Directory Tree",
                            "get_file_structure": "📋 File Structure",
                            "analyze_project_structure": "🏗️ Project Structure",
                            "get_recent_commits": "📝 Recent Commits",
                            "get_commit_details": "🔍 Commit Details",
                            "get_commit_statistics": "📊 Commit Stats",
                            "search_code": "🔍 Code Search",
                            "search_files": "📁 File Search",
                            "find_functions": "⚙️ Function Search",
                            "get_code_metrics": "📈 Code Metrics",
                            "search_dependencies": "📦 Dependency Search"
                        }
                        
                        for tool in tools_used:
                            tool_name = tool_descriptions.get(tool, f"🔧 {tool}")
                            st.markdown(f"• {tool_name}")
                        
                        st.markdown(f"*Total tools used: {len(tools_used)}*")
                    
                    # Add additional sections if requested
                    if include_metrics:
                        st.markdown("### 📊 Code Metrics")
                        tools = FastMCPTools()
                        metrics = tools.get_code_metrics(repo_url)
                        st.json(metrics)
                    
                    if include_structure:
                        st.markdown("### 📁 Project Structure")
                        tools = FastMCPTools()
                        structure = tools.analyze_project_structure(repo_url)
                        st.json(structure)
                    
                    # Add export options
                    st.markdown("### 📤 Export Options")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📄 Export as Text", use_container_width=True):
                            st.download_button(
                                label="Download Summary",
                                data=summary,
                                file_name="repository_summary.txt",
                                mime="text/plain"
                            )
                    with col2:
                        if st.button("📊 Export as JSON", use_container_width=True):
                            import json
                            summary_data = {
                                "repository": repo_url,
                                "summary_type": summary_type,
                                "summary": summary,
                                "timestamp": datetime.now().isoformat()
                            }
                            st.download_button(
                                label="Download JSON",
                                data=json.dumps(summary_data, indent=2),
                                file_name="repository_summary.json",
                                mime="application/json"
                            )
                    
                except Exception as e:
                    st.error(f"❌ Summary generation failed: {str(e)}")
                finally:
                    progress_bar.empty()
                    status_text.empty()
    else:
        st.info("🎯 Please select a repository to get a summary.") 