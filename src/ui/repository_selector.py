"""
Modern Repository Selector UI Component
Provides a beautiful interface for selecting and analyzing GitHub repositories
"""

import streamlit as st
from typing import Optional, Dict, Any
import re
from urllib.parse import urlparse
import requests
import json
from datetime import datetime

def render_repository_selector() -> Optional[str]:
    """Render the modern repository selector interface"""
    
    # Header with modern styling
    st.markdown("""
    <div class="modern-card">
        <h3>🔍 Repository Selector</h3>
        <p>Enter a GitHub repository URL to start analyzing it with AI-powered insights.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Repository input section
    repo_url = render_repository_input()
    
    if repo_url:
        # Validate and display repository info
        repo_info = validate_and_get_repo_info(repo_url)
        if repo_info:
            render_repository_info(repo_info)
            return repo_url
    
    # Show popular repositories
    render_popular_repositories()
    
    return None

def render_repository_input() -> Optional[str]:
    """Render the repository input with modern styling"""
    
    st.markdown("### 📝 Enter Repository URL")
    
    # Input container with modern styling
    col1, col2 = st.columns([3, 1])
    
    with col1:
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repository",
            key="repo_url_input",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("🔍 Analyze", type="primary", use_container_width=True):
            if repo_url:
                return repo_url
            else:
                st.error("Please enter a repository URL")
    
    # Auto-detect from clipboard or recent
    if st.button("📋 Paste from Clipboard", help="Paste repository URL from clipboard"):
        # This would need JavaScript integration for clipboard access
        st.info("Clipboard access requires browser permissions")
    
    return repo_url

def validate_and_get_repo_info(repo_url: str) -> Optional[Dict[str, Any]]:
    """Validate repository URL and get basic information"""
    
    # Validate URL format
    if not is_valid_github_url(repo_url):
        st.error("❌ Invalid GitHub repository URL. Please enter a valid URL like: https://github.com/username/repository")
        return None
    
    # Extract repository details
    repo_details = extract_repo_details(repo_url)
    if not repo_details:
        st.error("❌ Could not extract repository details from URL")
        return None
    
    # Get repository information from GitHub API
    repo_info = fetch_repository_info(repo_details['owner'], repo_details['repo'])
    if not repo_info:
        st.error("❌ Could not fetch repository information. Please check the URL and try again.")
        return None
    
    return repo_info

def is_valid_github_url(url: str) -> bool:
    """Check if the URL is a valid GitHub repository URL"""
    github_pattern = r'^https?://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/?$'
    return bool(re.match(github_pattern, url))

def extract_repo_details(url: str) -> Optional[Dict[str, str]]:
    """Extract owner and repository name from GitHub URL"""
    try:
        parsed = urlparse(url)
        if parsed.netloc == 'github.com':
            path_parts = parsed.path.strip('/').split('/')
            if len(path_parts) >= 2:
                return {
                    'owner': path_parts[0],
                    'repo': path_parts[1]
                }
    except Exception:
        pass
    return None

def fetch_repository_info(owner: str, repo: str) -> Optional[Dict[str, Any]]:
    """Fetch repository information from GitHub API"""
    try:
        # Get GitHub token from environment
        import os
        github_token = os.getenv("GITHUB_TOKEN")
        
        headers = {}
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        
        # Fetch repository info
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            repo_data = response.json()
            
            # Get additional stats
            stats = fetch_repository_stats(owner, repo, headers)
            
            return {
                'name': repo_data['name'],
                'full_name': repo_data['full_name'],
                'description': repo_data['description'] or "No description available",
                'url': repo_data['html_url'],
                'stars': repo_data['stargazers_count'],
                'forks': repo_data['forks_count'],
                'language': repo_data['language'],
                'created_at': repo_data['created_at'],
                'updated_at': repo_data['updated_at'],
                'size': repo_data['size'],
                'open_issues': repo_data['open_issues_count'],
                'license': repo_data.get('license', {}).get('name', 'No license'),
                'topics': repo_data.get('topics', []),
                'stats': stats
            }
        else:
            st.error(f"❌ Repository not found or access denied (Status: {response.status_code})")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Error fetching repository info: {str(e)}")
        return None

def fetch_repository_stats(owner: str, repo: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """Fetch additional repository statistics"""
    stats = {
        'languages': {},
        'contributors': 0,
        'commits': 0,
        'branches': 0
    }
    
    try:
        # Get languages
        lang_url = f"https://api.github.com/repos/{owner}/{repo}/languages"
        lang_response = requests.get(lang_url, headers=headers, timeout=10)
        if lang_response.status_code == 200:
            stats['languages'] = lang_response.json()
        
        # Get contributors count
        contrib_url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
        contrib_response = requests.get(contrib_url, headers=headers, timeout=10)
        if contrib_response.status_code == 200:
            stats['contributors'] = len(contrib_response.json())
        
        # Get branches count
        branch_url = f"https://api.github.com/repos/{owner}/{repo}/branches"
        branch_response = requests.get(branch_url, headers=headers, timeout=10)
        if branch_response.status_code == 200:
            stats['branches'] = len(branch_response.json())
            
    except Exception:
        # Silently fail for additional stats
        pass
    
    return stats

def render_repository_info(repo_info: Dict[str, Any]):
    """Render repository information with modern cards"""
    
    st.markdown("### 📊 Repository Information")
    
    # Main repository card
    st.markdown(f"""
    <div class="modern-card success-card">
        <div style="display: flex; align-items: center; margin-bottom: 16px;">
            <h3 style="margin: 0;">{repo_info['name']}</h3>
            <span style="margin-left: auto; font-size: 1.2rem;">⭐ {repo_info['stars']:,}</span>
        </div>
        <p style="margin-bottom: 16px; opacity: 0.9;">{repo_info['description']}</p>
        <div style="display: flex; gap: 16px; flex-wrap: wrap;">
            <span>🔤 {repo_info['language'] or 'Unknown'}</span>
            <span>🍴 {repo_info['forks']:,} forks</span>
            <span>🐛 {repo_info['open_issues']} issues</span>
            <span>📅 {format_date(repo_info['updated_at'])}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats grid
    render_repository_stats_grid(repo_info)
    
    # Topics and metadata
    render_repository_metadata(repo_info)
    
    # Action buttons
    render_repository_actions(repo_info)

def render_repository_stats_grid(repo_info: Dict[str, Any]):
    """Render repository statistics in a grid"""
    
    stats = [
        {
            "label": "Repository Size",
            "value": f"{repo_info['size']:,} KB",
            "icon": "📦",
            "color": "primary"
        },
        {
            "label": "Contributors",
            "value": f"{repo_info['stats']['contributors']:,}",
            "icon": "👥",
            "color": "secondary"
        },
        {
            "label": "Branches",
            "value": f"{repo_info['stats']['branches']}",
            "icon": "🌿",
            "color": "success"
        },
        {
            "label": "License",
            "value": repo_info['license'],
            "icon": "📄",
            "color": "warning"
        }
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

def render_repository_metadata(repo_info: Dict[str, Any]):
    """Render repository metadata and topics"""
    
    # Languages breakdown
    if repo_info['stats']['languages']:
        st.markdown("### 🔤 Languages")
        
        # Create language chart
        languages = list(repo_info['stats']['languages'].keys())[:5]  # Top 5
        values = list(repo_info['stats']['languages'].values())[:5]
        
        # Display as progress bars
        for lang, bytes_count in zip(languages, values):
            percentage = (bytes_count / sum(values)) * 100
            st.markdown(f"""
            <div style="margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>{lang}</span>
                    <span>{percentage:.1f}%</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {percentage}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Topics
    if repo_info['topics']:
        st.markdown("### 🏷️ Topics")
        topics_html = " ".join([f'<span style="background: var(--primary-color); color: white; padding: 4px 8px; border-radius: 12px; margin: 2px; display: inline-block;">{topic}</span>' for topic in repo_info['topics']])
        st.markdown(f'<div style="margin-bottom: 16px;">{topics_html}</div>', unsafe_allow_html=True)

def render_repository_actions(repo_info: Dict[str, Any]):
    """Render action buttons for the repository"""
    
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Analyze Repository", use_container_width=True):
            st.session_state.auto_analyze = True
            st.rerun()
    
    with col2:
        if st.button("📊 View Insights", use_container_width=True):
            st.session_state.show_insights = True
            st.rerun()
    
    with col3:
        if st.button("📁 Explore Files", use_container_width=True):
            st.session_state.show_files = True
            st.rerun()
    
    with col4:
        if st.button("🕒 View History", use_container_width=True):
            st.session_state.show_history = True
            st.rerun()

def render_popular_repositories():
    """Render popular repository suggestions"""
    
    st.markdown("### 🌟 Popular Repositories")
    
    popular_repos = [
        {
            "name": "streamlit/streamlit",
            "description": "The fastest way to build and share data apps",
            "stars": "30k+",
            "language": "Python"
        },
        {
            "name": "microsoft/vscode",
            "description": "Visual Studio Code",
            "stars": "150k+",
            "language": "TypeScript"
        },
        {
            "name": "facebook/react",
            "description": "The library for web and native user interfaces",
            "stars": "200k+",
            "language": "JavaScript"
        },
        {
            "name": "tensorflow/tensorflow",
            "description": "An Open Source Machine Learning Framework",
            "stars": "175k+",
            "language": "Python"
        }
    ]
    
    cols = st.columns(2)
    for i, repo in enumerate(popular_repos):
        with cols[i % 2]:
            if st.button(
                f"📦 {repo['name']}\n{repo['description']}\n⭐ {repo['stars']} • 🔤 {repo['language']}",
                key=f"popular_{i}",
                use_container_width=True,
                help=f"Click to analyze {repo['name']}"
            ):
                st.session_state.repo_url_input = f"https://github.com/{repo['name']}"
                st.rerun()

def format_date(date_string: str) -> str:
    """Format date string to human readable format"""
    try:
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date_obj.strftime("%b %d, %Y")
    except:
        return date_string

def render_recent_repositories():
    """Render recently analyzed repositories"""
    
    if 'recent_repositories' in st.session_state and st.session_state.recent_repositories:
        st.markdown("### 🕒 Recently Analyzed")
        
        for repo in st.session_state.recent_repositories[-5:]:  # Show last 5
            if st.button(
                f"📦 {repo['name']} • {repo['language']} • ⭐ {repo['stars']}",
                key=f"recent_{repo['name']}",
                use_container_width=True
            ):
                st.session_state.repo_url_input = repo['url']
                st.rerun()

def add_to_recent_repositories(repo_info: Dict[str, Any]):
    """Add repository to recent list"""
    if 'recent_repositories' not in st.session_state:
        st.session_state.recent_repositories = []
    
    # Check if already exists
    existing = [r for r in st.session_state.recent_repositories if r['name'] == repo_info['full_name']]
    if existing:
        # Remove existing and add to front
        st.session_state.recent_repositories = [r for r in st.session_state.recent_repositories if r['name'] != repo_info['full_name']]
    
    # Add to front
    st.session_state.recent_repositories.insert(0, {
        'name': repo_info['full_name'],
        'url': repo_info['url'],
        'language': repo_info['language'],
        'stars': repo_info['stars']
    })
    
    # Keep only last 10
    st.session_state.recent_repositories = st.session_state.recent_repositories[:10] 