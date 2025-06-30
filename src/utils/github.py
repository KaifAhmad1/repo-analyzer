"""
GitHub utilities for repository analysis
"""

import requests
import os
from typing import Dict, Any, Optional

def validate_github_token(token: str) -> bool:
    """Validate GitHub token by making a test API call"""
    try:
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get("https://api.github.com/user", headers=headers)
        return response.status_code == 200
    except Exception:
        return False

def get_repository_info(repo_url: str, token: str) -> Optional[Dict[str, Any]]:
    """Get basic repository information"""
    try:
        # Parse repository URL
        if "github.com" in repo_url:
            parts = repo_url.replace("https://github.com/", "").split("/")
            owner = parts[0]
            repo = parts[1].replace(".git", "")
        else:
            return None
        
        # Get repository info from GitHub API
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "name": data["name"],
                "full_name": data["full_name"],
                "description": data["description"],
                "language": data["language"],
                "stars": data["stargazers_count"],
                "forks": data["forks_count"],
                "issues": data["open_issues_count"],
                "size": data["size"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
                "url": data["html_url"]
            }
        
        return None
    
    except Exception:
        return None

def check_repository_access(repo_url: str, token: str) -> Dict[str, Any]:
    """Check if we have access to the repository and what permissions we have"""
    try:
        repo_info = get_repository_info(repo_url, token)
        
        if not repo_info:
            return {
                "accessible": False,
                "error": "Repository not found or no access"
            }
        
        # Check if repository is private
        if repo_info.get("private", False):
            return {
                "accessible": True,
                "private": True,
                "info": repo_info
            }
        else:
            return {
                "accessible": True,
                "private": False,
                "info": repo_info
            }
    
    except Exception as e:
        return {
            "accessible": False,
            "error": str(e)
        }

def get_repository_languages(repo_url: str, token: str) -> Dict[str, int]:
    """Get programming languages used in the repository"""
    try:
        # Parse repository URL
        if "github.com" in repo_url:
            parts = repo_url.replace("https://github.com/", "").split("/")
            owner = parts[0]
            repo = parts[1].replace(".git", "")
        else:
            return {}
        
        # Get languages from GitHub API
        api_url = f"https://api.github.com/repos/{owner}/{repo}/languages"
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        
        return {}
    
    except Exception:
        return {}

def get_repository_topics(repo_url: str, token: str) -> list:
    """Get topics/tags for the repository"""
    try:
        # Parse repository URL
        if "github.com" in repo_url:
            parts = repo_url.replace("https://github.com/", "").split("/")
            owner = parts[0]
            repo = parts[1].replace(".git", "")
        else:
            return []
        
        # Get topics from GitHub API
        api_url = f"https://api.github.com/repos/{owner}/{repo}/topics"
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.mercy-preview+json"
        }
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            return response.json().get("names", [])
        
        return []
    
    except Exception:
        return [] 