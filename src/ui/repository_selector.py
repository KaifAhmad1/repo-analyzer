"""
Enhanced Repository Selector UI Component
Clean interface for selecting GitHub repositories with improved visual appeal
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
    """Render the enhanced repository selector component"""
    
    st.markdown("### 📁 Repository Selection")
    st.markdown("Enter a GitHub repository URL to start analyzing:")
    
    # Repository URL input with enhanced form styling
    with st.form(key="repo_selector_form"):
        repo_url = st.text_input(
            "🔗 GitHub Repository URL",
            value=st.session_state.get("current_repo", ""),
            placeholder="https://github.com/owner/repository",
            help="Enter a valid GitHub repository URL to analyze"
        )
        
        # Enhanced button layout
        col1, col2 = st.columns([2, 1])
        with col1:
            submit_button = st.form_submit_button("🔍 Analyze Repository", type="primary", use_container_width=True)
        with col2:
            clear_button = st.form_submit_button("🗑️ Clear", use_container_width=True)
    
    # Handle form submissions with enhanced feedback
    if clear_button:
        st.session_state.current_repo = ""
        st.rerun()
    
    if submit_button and repo_url:
        # Validate and normalize URL with enhanced progress
        with st.spinner("🔍 Validating repository URL..."):
            if validate_github_url(repo_url):
                normalized_url = normalize_github_url(repo_url)
                
                # Enhanced success display
                st.success(f"✅ **Repository selected successfully!**")
                
                # Extract and display repository info
                parts = normalized_url.replace("https://github.com/", "").split("/")
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                    
                    # Enhanced info display
                    st.info(f"""
                    **📋 Repository Details:**
                    - **👤 Owner:** `{owner}`
                    - **📦 Repository:** `{repo}`
                    - **🔗 Full URL:** `{normalized_url}`
                    """)
                
                return normalized_url
            else:
                # Enhanced error display
                st.error("❌ **Invalid GitHub repository URL**")
                st.markdown("""
                **Please enter a valid URL in one of these formats:**
                - `https://github.com/owner/repository`
                - `https://github.com/owner/repository.git`
                - `github.com/owner/repository`
                """)
                
                # Show examples
                st.markdown("**💡 Example URLs:**")
                st.code("""
https://github.com/microsoft/vscode
https://github.com/facebook/react
https://github.com/python/cpython
                """)
                return None
    
    # Enhanced instructions for users
    if not repo_url:
        st.markdown("#### 📝 How to Use")
        st.info("""
        **🚀 Getting Started:**
        1. **Enter** a valid GitHub repository URL above
        2. **Click** "Analyze Repository" or press Enter
        3. **Start** exploring with AI-powered tools!
        
        **💡 Tip:** You can analyze any public GitHub repository
        """)
    
    return None 