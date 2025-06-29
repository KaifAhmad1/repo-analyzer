"""
📁 Repository Selector Component

Modern repository selector with search, suggestions,
and beautiful UI design.
"""

import streamlit as st
from typing import List, Dict, Any, Optional
import re

class RepositorySelector:
    """Modern repository selector with search and suggestions."""
    
    def __init__(self):
        self.suggested_repos = self._get_suggested_repos()
        self.recent_repos = st.session_state.get('recent_repos', [])
    
    def render(self) -> Optional[str]:
        """Render the repository selector and return selected repository."""
        
        # Repository input section
        st.markdown("### 📁 Repository")
        
        # Search input with validation
        repo_input = st.text_input(
            "Enter repository (owner/repo)",
            placeholder="e.g., microsoft/vscode",
            help="Enter repository in format: owner/repository-name",
            key="repo_input"
        )
        
        # Validate repository format
        if repo_input and not self._is_valid_repo_format(repo_input):
            st.error("❌ Invalid repository format. Use: owner/repository-name")
            return None
        
        # Quick suggestions
        if not repo_input:
            st.markdown("#### 💡 Popular Repositories")
            self._render_suggestions()
        
        # Recent repositories
        if self.recent_repos:
            st.markdown("#### ⏰ Recent Repositories")
            self._render_recent_repos()
        
        # Return selected repository
        if repo_input and self._is_valid_repo_format(repo_input):
            # Add to recent repos
            self._add_to_recent(repo_input)
            return repo_input
        
        return None
    
    def _is_valid_repo_format(self, repo: str) -> bool:
        """Validate repository format."""
        pattern = r'^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$'
        return bool(re.match(pattern, repo))
    
    def _get_suggested_repos(self) -> List[Dict[str, str]]:
        """Get suggested popular repositories."""
        return [
            {
                "name": "microsoft/vscode",
                "description": "Visual Studio Code - Open source code editor",
                "stars": "150k+",
                "language": "TypeScript"
            },
            {
                "name": "facebook/react",
                "description": "React - JavaScript library for building user interfaces",
                "stars": "210k+",
                "language": "JavaScript"
            },
            {
                "name": "tensorflow/tensorflow",
                "description": "TensorFlow - Open source machine learning framework",
                "stars": "180k+",
                "language": "Python"
            },
            {
                "name": "kubernetes/kubernetes",
                "description": "Kubernetes - Container orchestration platform",
                "stars": "100k+",
                "language": "Go"
            },
            {
                "name": "microsoft/PowerToys",
                "description": "PowerToys - Windows system utilities",
                "stars": "95k+",
                "language": "C#"
            },
            {
                "name": "flutter/flutter",
                "description": "Flutter - UI toolkit for cross-platform apps",
                "stars": "160k+",
                "language": "Dart"
            }
        ]
    
    def _render_suggestions(self):
        """Render repository suggestions."""
        
        # Create columns for suggestions
        cols = st.columns(2)
        
        for i, repo in enumerate(self.suggested_repos):
            col = cols[i % 2]
            
            with col:
                # Repository card
                st.markdown(f"""
                <div class="repo-suggestion-card" onclick="selectRepo('{repo['name']}')">
                    <div class="repo-header">
                        <strong>{repo['name']}</strong>
                        <span class="repo-stars">⭐ {repo['stars']}</span>
                    </div>
                    <div class="repo-description">{repo['description']}</div>
                    <div class="repo-language">{repo['language']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Click handler
                if st.button(f"Select {repo['name']}", key=f"suggest_{i}"):
                    st.session_state.repo_input = repo['name']
                    st.rerun()
    
    def _render_recent_repos(self):
        """Render recent repositories."""
        
        for repo in self.recent_repos[:5]:  # Show last 5
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.text(repo)
            
            with col2:
                if st.button("Select", key=f"recent_{repo}"):
                    st.session_state.repo_input = repo
                    st.rerun()
    
    def _add_to_recent(self, repo: str):
        """Add repository to recent list."""
        if repo not in self.recent_repos:
            self.recent_repos.insert(0, repo)
            # Keep only last 10
            self.recent_repos = self.recent_repos[:10]
            st.session_state.recent_repos = self.recent_repos
    
    def search_repositories(self, query: str) -> List[Dict[str, Any]]:
        """Search for repositories (placeholder for GitHub API integration)."""
        
        # TODO: Integrate with GitHub API for real search
        # For now, return filtered suggestions
        results = []
        query_lower = query.lower()
        
        for repo in self.suggested_repos:
            if (query_lower in repo['name'].lower() or 
                query_lower in repo['description'].lower()):
                results.append(repo)
        
        return results
    
    def get_repo_info(self, repo: str) -> Optional[Dict[str, Any]]:
        """Get repository information (placeholder for GitHub API integration)."""
        
        # TODO: Integrate with GitHub API
        # For now, return placeholder info
        return {
            "name": repo,
            "description": "Repository description",
            "stars": "1k+",
            "forks": "100+",
            "language": "Python",
            "last_updated": "2024-01-01",
            "size": "1MB",
            "topics": ["python", "analysis", "ai"]
        } 