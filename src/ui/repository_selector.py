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
    
    # Repository URL input
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/owner/repository",
        help="Enter a valid GitHub repository URL"
    )
    
    if repo_url:
        # Validate and normalize URL
        if validate_github_url(repo_url):
            normalized_url = normalize_github_url(repo_url)
            
            # Display repository info
            st.success(f"✅ Valid repository: {normalized_url}")
            
            # Extract owner and repo name
            parts = normalized_url.replace("https://github.com/", "").split("/")
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
                st.info(f"**Owner:** {owner} | **Repository:** {repo}")
            
            return normalized_url
        else:
            st.error("❌ Invalid GitHub repository URL. Please enter a valid URL.")
            return None
    
    # Quick examples
    st.markdown("#### 💡 Example Repositories")
    
    examples = [
        ("Microsoft VSCode", "https://github.com/microsoft/vscode"),
        ("React", "https://github.com/facebook/react"),
        ("Python", "https://github.com/python/cpython"),
        ("Django", "https://github.com/django/django"),
    ]
    
    cols = st.columns(2)
    for i, (name, url) in enumerate(examples):
        with cols[i % 2]:
            if st.button(f"📦 {name}", key=f"example_{i}", use_container_width=True):
                st.session_state.example_url = url
                st.rerun()
    
    # Handle example selection
    if "example_url" in st.session_state:
        st.session_state.pop("example_url")
        return st.session_state.example_url
    
    return None 