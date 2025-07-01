"""
GitHub API utilities for the Repository Analyzer
"""

import requests
from typing import Dict, Any, Optional, List
from .config import get_github_token

def make_github_request(endpoint: str, token: Optional[str] = None) -> Dict[str, Any]:
    """Make a GitHub API request"""
    if not token:
        token = get_github_token()
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    if token:
        headers["Authorization"] = f"token {token}"
    
    response = requests.get(f"https://api.github.com{endpoint}", headers=headers)
    response.raise_for_status()
    return response.json()

def parse_repo_url(repo_url: str) -> tuple[str, str]:
    """Parse GitHub repository URL to get owner and repo name"""
    if "github.com" in repo_url:
        parts = repo_url.replace("https://github.com/", "").split("/")
        owner = parts[0]
        repo = parts[1].replace(".git", "")
        return owner, repo
    else:
        raise ValueError("Invalid GitHub URL")

def get_repository_info(repo_url: str) -> Dict[str, Any]:
    """Get basic repository information"""
    try:
        owner, repo = parse_repo_url(repo_url)
        data = make_github_request(f"/repos/{owner}/{repo}")
        
        return {
            "name": data["name"],
            "full_name": data["full_name"],
            "description": data["description"] or "No description",
            "language": data["language"] or "Unknown",
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "issues": data["open_issues_count"],
            "size": data["size"],
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
            "topics": data.get("topics", [])
        }
    except Exception as e:
        raise Exception(f"Error getting repository info: {str(e)}")

def get_repository_languages(repo_url: str) -> Dict[str, int]:
    """Get repository language statistics"""
    try:
        owner, repo = parse_repo_url(repo_url)
        return make_github_request(f"/repos/{owner}/{repo}/languages")
    except Exception as e:
        raise Exception(f"Error getting repository languages: {str(e)}")

def get_repository_commits(repo_url: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent commits from repository"""
    try:
        owner, repo = parse_repo_url(repo_url)
        data = make_github_request(f"/repos/{owner}/{repo}/commits?per_page={limit}")
        
        commits = []
        for commit_data in data:
            commit = {
                "sha": commit_data["sha"][:8],
                "message": commit_data["commit"]["message"],
                "author": commit_data["commit"]["author"]["name"],
                "date": commit_data["commit"]["author"]["date"],
                "url": commit_data["html_url"]
            }
            commits.append(commit)
        
        return commits
    except Exception as e:
        raise Exception(f"Error getting repository commits: {str(e)}")

def get_repository_issues(repo_url: str, state: str = "open", limit: int = 10) -> List[Dict[str, Any]]:
    """Get repository issues"""
    try:
        owner, repo = parse_repo_url(repo_url)
        data = make_github_request(f"/repos/{owner}/{repo}/issues?state={state}&per_page={limit}")
        
        issues = []
        for issue_data in data:
            issue = {
                "number": issue_data["number"],
                "title": issue_data["title"],
                "state": issue_data["state"],
                "author": issue_data["user"]["login"],
                "created_at": issue_data["created_at"],
                "labels": [label["name"] for label in issue_data["labels"]]
            }
            issues.append(issue)
        
        return issues
    except Exception as e:
        raise Exception(f"Error getting repository issues: {str(e)}")

def search_repository_code(repo_url: str, query: str) -> List[Dict[str, Any]]:
    """Search for code in repository"""
    try:
        owner, repo = parse_repo_url(repo_url)
        data = make_github_request(f"/search/code?q={query}+repo:{owner}/{repo}")
        
        results = []
        for item in data.get("items", []):
            result = {
                "file_path": item["path"],
                "file_name": item["name"],
                "url": item["html_url"],
                "repository": item["repository"]["full_name"]
            }
            results.append(result)
        
        return results
    except Exception as e:
        raise Exception(f"Error searching repository code: {str(e)}") 