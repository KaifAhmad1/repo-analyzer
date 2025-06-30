"""
Repository Selector UI Component
Allows users to select and configure GitHub repositories
"""

import streamlit as st
import re
from typing import Optional

def render_repository_selector() -> Optional[str]:
    """Render repository selector and return selected repository URL"""
    
    st.subheader("📁 Select Repository")
    
    # Repository URL input
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/username/repository",
        help="Enter the full GitHub repository URL"
    )
    
    if repo_url:
        # Validate GitHub URL
        if not is_valid_github_url(repo_url):
            st.error("❌ Please enter a valid GitHub repository URL")
            return None
        
        # Extract repository info
        repo_info = extract_repo_info(repo_url)
        if repo_info:
            st.success(f"✅ Repository: {repo_info['owner']}/{repo_info['repo']}")
            
            # Display repository info
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Owner", repo_info['owner'])
            with col2:
                st.metric("Repository", repo_info['repo'])
            
            # Set environment variable for MCP servers
            st.session_state.github_repo_url = repo_url
            
            return repo_url
    
    return None

def is_valid_github_url(url: str) -> bool:
    """Validate if the URL is a valid GitHub repository URL"""
    # GitHub repository URL patterns
    patterns = [
        r'https://github\.com/[^/]+/[^/]+/?$',
        r'https://github\.com/[^/]+/[^/]+\.git$',
        r'git@github\.com:[^/]+/[^/]+\.git$'
    ]
    
    for pattern in patterns:
        if re.match(pattern, url):
            return True
    
    return False

def extract_repo_info(url: str) -> Optional[dict]:
    """Extract owner and repository name from GitHub URL"""
    # Handle HTTPS URLs
    if url.startswith('https://github.com/'):
        parts = url.replace('https://github.com/', '').split('/')
        if len(parts) >= 2:
            owner = parts[0]
            repo = parts[1].replace('.git', '')
            return {
                'owner': owner,
                'repo': repo,
                'full_name': f"{owner}/{repo}"
            }
    
    # Handle SSH URLs
    elif url.startswith('git@github.com:'):
        parts = url.replace('git@github.com:', '').split('/')
        if len(parts) >= 2:
            owner = parts[0]
            repo = parts[1].replace('.git', '')
            return {
                'owner': owner,
                'repo': repo,
                'full_name': f"{owner}/{repo}"
            }
    
    return None

def render_repository_examples():
    """Render example repositories for quick selection"""
    st.subheader("🎯 Example Repositories")
    
    examples = [
        {
            "name": "React",
            "url": "https://github.com/facebook/react",
            "description": "JavaScript library for building user interfaces"
        },
        {
            "name": "Python",
            "url": "https://github.com/python/cpython",
            "description": "Python programming language"
        },
        {
            "name": "TensorFlow",
            "url": "https://github.com/tensorflow/tensorflow",
            "description": "Machine learning framework"
        },
        {
            "name": "VS Code",
            "url": "https://github.com/microsoft/vscode",
            "description": "Visual Studio Code editor"
        }
    ]
    
    cols = st.columns(2)
    for i, example in enumerate(examples):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"**{example['name']}**")
                st.markdown(f"*{example['description']}*")
                if st.button(f"Select {example['name']}", key=f"example_{i}"):
                    st.session_state.example_repo = example['url']
                    st.rerun()
    
    # Handle example selection
    if hasattr(st.session_state, 'example_repo'):
        repo_url = st.session_state.example_repo
        del st.session_state.example_repo
        return repo_url
    
    return None 