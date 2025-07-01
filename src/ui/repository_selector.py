"""
Streamlined Repository Selector UI Component
Provides a clean interface for selecting and analyzing GitHub repositories
"""

import streamlit as st
import re
from typing import Optional

def validate_github_url(url: str) -> bool:
    """Validate if the URL is a valid GitHub repository URL"""
    if not url:
        return False
    
    # Basic GitHub URL patterns
    patterns = [
        r'^https://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/?$',
        r'^https://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+\.git$',
        r'^github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/?$'
    ]
    
    for pattern in patterns:
        if re.match(pattern, url):
            return True
    
    return False

def normalize_github_url(url: str) -> str:
    """Normalize GitHub URL to standard format"""
    if not url:
        return ""
    
    # Remove .git suffix if present
    if url.endswith('.git'):
        url = url[:-4]
    
    # Add https:// if not present
    if not url.startswith('http'):
        url = 'https://' + url
    
    # Ensure no trailing slash
    if url.endswith('/'):
        url = url[:-1]
    
    return url

def render_repository_selector() -> Optional[str]:
    """Render the repository selector component"""
    
    st.markdown("### 📁 Select Repository")
    
    # Add recent repositories feature
    if "recent_repos" not in st.session_state:
        st.session_state.recent_repos = []
    
    # Show recent repositories if available
    if st.session_state.recent_repos:
        st.markdown("#### 🕒 Recent Repositories")
        for i, recent_repo in enumerate(st.session_state.recent_repos[-3:]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"📦 {recent_repo}")
            with col2:
                if st.button("Use", key=f"use_recent_{i}"):
                    st.session_state.current_repo = recent_repo
                    st.rerun()
    
    # Repository URL input with form for better UX
    with st.form(key="repo_selector_form"):
        repo_url = st.text_input(
            "GitHub Repository URL",
            value=st.session_state.get("current_repo", ""),
            placeholder="https://github.com/owner/repository",
            help="Enter a valid GitHub repository URL (press Enter to submit)"
        )
        
        col1, col2 = st.columns([2, 1])
        with col1:
            submit_button = st.form_submit_button("🔍 Analyze Repository", type="primary", use_container_width=True)
        with col2:
            clear_button = st.form_submit_button("🗑️ Clear", use_container_width=True)
    
    # Handle form submissions
    if clear_button:
        st.session_state.current_repo = ""
        st.rerun()
    
    if submit_button and repo_url:
        # Validate and normalize URL
        if validate_github_url(repo_url):
            normalized_url = normalize_github_url(repo_url)
            
            # Add to recent repositories
            if normalized_url not in st.session_state.recent_repos:
                st.session_state.recent_repos.append(normalized_url)
                # Keep only last 5 repositories
                if len(st.session_state.recent_repos) > 5:
                    st.session_state.recent_repos = st.session_state.recent_repos[-5:]
            
            # Display repository info with enhanced styling
            st.success(f"✅ **Valid repository selected!**")
            
            # Extract owner and repo name
            parts = normalized_url.replace("https://github.com/", "").split("/")
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
                
                # Create a nice info box
                st.info(f"""
                **Repository Details:**
                - **Owner:** {owner}
                - **Repository:** {repo}
                - **Full URL:** {normalized_url}
                """)
            
            # Add quick actions
            st.markdown("#### ⚡ Quick Actions")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Quick Overview", key="quick_overview"):
                    st.session_state.quick_action = "overview"
                    st.rerun()
            with col2:
                if st.button("📁 File Structure", key="quick_structure"):
                    st.session_state.quick_action = "structure"
                    st.rerun()
            with col3:
                if st.button("🔍 Code Search", key="quick_search"):
                    st.session_state.quick_action = "search"
                    st.rerun()
            
            return normalized_url
        else:
            st.error("❌ **Invalid GitHub repository URL.** Please enter a valid URL in the format: `https://github.com/owner/repository`")
            
            # Show examples
            st.markdown("#### 💡 Example URLs:")
            st.code("""
https://github.com/microsoft/vscode
https://github.com/facebook/react
https://github.com/python/cpython
            """)
            return None
    
    # Instructions for users
    if not repo_url:
        st.markdown("#### 📝 Instructions")
        st.info("""
        **How to use:**
        1. Enter a valid GitHub repository URL
        2. Press Enter or click "Analyze Repository"
        3. Start exploring the repository with AI-powered tools!
        
        **Example format:** `https://github.com/owner/repository`
        """)
    
    return None 