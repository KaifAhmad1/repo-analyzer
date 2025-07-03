"""
Repository Manager for GitHub Repository Analyzer
Handles repository persistence, session management, and systematic data collection
"""

import os
import json
import time
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import requests
from urllib.parse import urlparse

from .config import (
    save_session_data, 
    get_session_data, 
    save_to_cache, 
    load_from_cache,
    get_cache_key,
    is_cache_valid
)

class RepositoryManager:
    """Manages repository data, sessions, and caching for systematic analysis"""
    
    def __init__(self):
        self.session_id = None
        self.current_repo = None
        self.repo_data = {}
        self.analysis_history = []
        self.cache_enabled = True
        
    def set_session_id(self, session_id: str):
        """Set the current session ID"""
        self.session_id = session_id
        
    def get_session_id(self) -> str:
        """Get current session ID or generate new one"""
        if not self.session_id:
            self.session_id = f"session_{int(time.time())}"
        return self.session_id
    
    def set_repository(self, repo_url: str) -> bool:
        """Set the current repository and initialize data collection"""
        try:
            # Normalize repository URL
            normalized_url = self._normalize_repo_url(repo_url)
            
            # Validate repository exists
            if not self._validate_repository(normalized_url):
                return False
            
            self.current_repo = normalized_url
            self.repo_data = self._initialize_repo_data(normalized_url)
            
            # Save to session
            self._save_session_state()
            
            return True
            
        except Exception as e:
            print(f"Error setting repository: {e}")
            return False
    
    def get_repository(self) -> Optional[str]:
        """Get current repository URL"""
        return self.current_repo
    
    def get_repo_data(self) -> Dict[str, Any]:
        """Get current repository data"""
        return self.repo_data.copy()
    
    def update_repo_data(self, key: str, value: Any):
        """Update repository data"""
        self.repo_data[key] = value
        self._save_session_state()
    
    def add_analysis_result(self, analysis_type: str, result: Dict[str, Any], tools_used: List[str] = None):
        """Add analysis result to history"""
        analysis_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": analysis_type,
            "result": result,
            "tools_used": tools_used or [],
            "session_id": self.get_session_id()
        }
        
        self.analysis_history.append(analysis_entry)
        self._save_session_state()
    
    def get_analysis_history(self, analysis_type: str = None) -> List[Dict[str, Any]]:
        """Get analysis history, optionally filtered by type"""
        if analysis_type:
            return [entry for entry in self.analysis_history if entry["type"] == analysis_type]
        return self.analysis_history.copy()
    
    def get_cached_data(self, operation: str, params: Dict[str, Any] = None) -> Optional[Any]:
        """Get cached data for operation"""
        if not self.cache_enabled or not self.current_repo:
            return None
        
        cache_key = get_cache_key(self.current_repo, operation, params)
        if is_cache_valid(cache_key):
            return load_from_cache(cache_key)
        return None
    
    def cache_data(self, operation: str, data: Any, params: Dict[str, Any] = None):
        """Cache data for operation"""
        if not self.cache_enabled or not self.current_repo:
            return
        
        cache_key = get_cache_key(self.current_repo, operation, params)
        save_to_cache(cache_key, data)
    
    def get_repository_info(self) -> Dict[str, Any]:
        """Get basic repository information"""
        if not self.current_repo:
            return {}
        
        # Try to get from cache first
        cached_info = self.get_cached_data("repo_info")
        if cached_info:
            return cached_info
        
        try:
            # Parse repository URL
            parsed = urlparse(self.current_repo)
            owner, repo = parsed.path.strip('/').split('/')[:2]
            
            # Get repository info from GitHub API
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                repo_info = response.json()
                info = {
                    "name": repo_info.get("name"),
                    "full_name": repo_info.get("full_name"),
                    "description": repo_info.get("description"),
                    "language": repo_info.get("language"),
                    "stars": repo_info.get("stargazers_count", 0),
                    "forks": repo_info.get("forks_count", 0),
                    "watchers": repo_info.get("watchers_count", 0),
                    "open_issues": repo_info.get("open_issues_count", 0),
                    "size": repo_info.get("size", 0),
                    "created_at": repo_info.get("created_at"),
                    "updated_at": repo_info.get("updated_at"),
                    "pushed_at": repo_info.get("pushed_at"),
                    "default_branch": repo_info.get("default_branch"),
                    "topics": repo_info.get("topics", []),
                    "license": repo_info.get("license", {}).get("name") if repo_info.get("license") else None,
                    "archived": repo_info.get("archived", False),
                    "private": repo_info.get("private", False)
                }
                
                # Cache the result
                self.cache_data("repo_info", info)
                return info
            else:
                return {"error": f"Failed to fetch repository info: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Error fetching repository info: {str(e)}"}
    
    def get_repository_stats(self) -> Dict[str, Any]:
        """Get repository statistics"""
        if not self.current_repo:
            return {}
        
        # Try to get from cache first
        cached_stats = self.get_cached_data("repo_stats")
        if cached_stats:
            return cached_stats
        
        try:
            # Parse repository URL
            parsed = urlparse(self.current_repo)
            owner, repo = parsed.path.strip('/').split('/')[:2]
            
            # Get repository statistics
            stats = {
                "total_analyses": len(self.analysis_history),
                "last_analysis": self.analysis_history[-1]["timestamp"] if self.analysis_history else None,
                "analysis_types": list(set(entry["type"] for entry in self.analysis_history)),
                "total_tools_used": len(set(tool for entry in self.analysis_history for tool in entry.get("tools_used", []))),
                "session_duration": self._calculate_session_duration(),
                "cache_hits": self._get_cache_stats()
            }
            
            # Cache the result
            self.cache_data("repo_stats", stats)
            return stats
            
        except Exception as e:
            return {"error": f"Error calculating repository stats: {str(e)}"}
    
    def export_session_data(self) -> Dict[str, Any]:
        """Export complete session data"""
        return {
            "session_id": self.get_session_id(),
            "repository": self.current_repo,
            "repository_data": self.repo_data,
            "analysis_history": self.analysis_history,
            "export_timestamp": datetime.now().isoformat(),
            "session_stats": self.get_repository_stats()
        }
    
    def import_session_data(self, data: Dict[str, Any]) -> bool:
        """Import session data"""
        try:
            self.session_id = data.get("session_id")
            self.current_repo = data.get("repository")
            self.repo_data = data.get("repository_data", {})
            self.analysis_history = data.get("analysis_history", [])
            
            self._save_session_state()
            return True
            
        except Exception as e:
            print(f"Error importing session data: {e}")
            return False
    
    def clear_session(self):
        """Clear current session data"""
        self.current_repo = None
        self.repo_data = {}
        self.analysis_history = []
        self._save_session_state()
    
    def _normalize_repo_url(self, repo_url: str) -> str:
        """Normalize repository URL"""
        if not repo_url:
            return ""
        
        # Remove .git suffix if present
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]
        
        # Add https:// if not present
        if not repo_url.startswith('http'):
            repo_url = 'https://' + repo_url
        
        # Ensure no trailing slash
        if repo_url.endswith('/'):
            repo_url = repo_url[:-1]
        
        return repo_url
    
    def _validate_repository(self, repo_url: str) -> bool:
        """Validate that repository exists and is accessible"""
        try:
            parsed = urlparse(repo_url)
            owner, repo = parsed.path.strip('/').split('/')[:2]
            
            # Check if repository exists via GitHub API
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            response = requests.get(api_url, timeout=10)
            
            return response.status_code == 200
            
        except Exception:
            return False
    
    def _initialize_repo_data(self, repo_url: str) -> Dict[str, Any]:
        """Initialize repository data structure"""
        return {
            "url": repo_url,
            "added_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "analysis_count": 0,
            "file_structure": None,
            "readme_content": None,
            "dependencies": None,
            "code_metrics": None,
            "commit_history": None,
            "security_analysis": None
        }
    
    def _save_session_state(self):
        """Save current session state to file"""
        if self.session_id:
            session_data = {
                "session_id": self.session_id,
                "current_repo": self.current_repo,
                "repo_data": self.repo_data,
                "analysis_history": self.analysis_history,
                "last_updated": datetime.now().isoformat()
            }
            save_session_data(self.session_id, session_data)
    
    def _calculate_session_duration(self) -> Optional[str]:
        """Calculate session duration"""
        if not self.analysis_history:
            return None
        
        first_analysis = datetime.fromisoformat(self.analysis_history[0]["timestamp"])
        last_analysis = datetime.fromisoformat(self.analysis_history[-1]["timestamp"])
        duration = last_analysis - first_analysis
        
        return str(duration)
    
    def _get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        # This is a simplified version - in a real implementation,
        # you'd track cache hits/misses more systematically
        return {
            "cache_hits": 0,
            "cache_misses": 0
        }

# Global repository manager instance
_repo_manager = None

def get_repository_manager() -> RepositoryManager:
    """Get the global repository manager instance"""
    global _repo_manager
    if _repo_manager is None:
        _repo_manager = RepositoryManager()
    return _repo_manager

def set_current_repository(repo_url: str) -> bool:
    """Set the current repository for analysis"""
    manager = get_repository_manager()
    return manager.set_repository(repo_url)

def get_current_repository() -> Optional[str]:
    """Get the current repository URL"""
    manager = get_repository_manager()
    return manager.get_repository()

def get_repository_info() -> Dict[str, Any]:
    """Get information about the current repository"""
    manager = get_repository_manager()
    return manager.get_repository_info()

def add_analysis_result(analysis_type: str, result: Dict[str, Any], tools_used: List[str] = None):
    """Add analysis result to the current session"""
    manager = get_repository_manager()
    manager.add_analysis_result(analysis_type, result, tools_used)

def get_analysis_history(analysis_type: str = None) -> List[Dict[str, Any]]:
    """Get analysis history for the current session"""
    manager = get_repository_manager()
    return manager.get_analysis_history(analysis_type)

def export_session_data() -> Dict[str, Any]:
    """Export current session data"""
    manager = get_repository_manager()
    return manager.export_session_data()

def clear_current_session():
    """Clear the current session"""
    manager = get_repository_manager()
    manager.clear_session() 