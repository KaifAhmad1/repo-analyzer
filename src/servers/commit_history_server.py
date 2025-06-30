"""
Simplified Commit History MCP Server
Provides commit history and change analysis
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from typing import Dict, Any, List
from datetime import datetime

app = FastAPI(title="Commit History MCP Server")

class CommitRequest(BaseModel):
    parameters: Dict[str, Any]

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "commit_history_server"}

@app.post("/commit-history")
def get_commit_history(request: CommitRequest):
    """Get recent commit history"""
    try:
        limit = request.parameters.get("limit", 10)
        
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise HTTPException(status_code=500, detail="GitHub token not configured")
        
        repo_url = os.getenv("GITHUB_REPO_URL")
        if not repo_url:
            raise HTTPException(status_code=500, detail="Repository URL not configured")
        
        # Parse repository URL
        if "github.com" in repo_url:
            parts = repo_url.replace("https://github.com/", "").split("/")
            owner = parts[0]
            repo = parts[1].replace(".git", "")
        else:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")
        
        # Get commits
        commits = get_commits(owner, repo, limit, github_token)
        
        return {
            "commits": commits,
            "total_count": len(commits),
            "repository": f"{owner}/{repo}"
        }
    
    except Exception as e:
        return {"error": str(e)}

def get_commits(owner: str, repo: str, limit: int, token: str) -> List[Dict[str, Any]]:
    """Get commit history from GitHub API"""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    params = {
        "per_page": min(limit, 100),  # GitHub API limit
        "page": 1
    }
    
    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="GitHub API error")
    
    commits_data = response.json()
    
    commits = []
    for commit_data in commits_data[:limit]:
        commit = {
            "sha": commit_data["sha"][:8],  # Short SHA
            "message": commit_data["commit"]["message"],
            "author": {
                "name": commit_data["commit"]["author"]["name"],
                "email": commit_data["commit"]["author"]["email"],
                "date": commit_data["commit"]["author"]["date"]
            },
            "committer": {
                "name": commit_data["commit"]["committer"]["name"],
                "email": commit_data["commit"]["committer"]["email"],
                "date": commit_data["commit"]["committer"]["date"]
            },
            "url": commit_data["html_url"],
            "files_changed": len(commit_data.get("files", [])),
            "additions": sum(f.get("additions", 0) for f in commit_data.get("files", [])),
            "deletions": sum(f.get("deletions", 0) for f in commit_data.get("files", [])),
            "files": [f["filename"] for f in commit_data.get("files", [])]
        }
        commits.append(commit)
    
    return commits

@app.post("/commit-stats")
def get_commit_statistics(request: CommitRequest):
    """Get commit statistics and patterns"""
    try:
        limit = request.parameters.get("limit", 50)
        
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise HTTPException(status_code=500, detail="GitHub token not configured")
        
        repo_url = os.getenv("GITHUB_REPO_URL")
        if not repo_url:
            raise HTTPException(status_code=500, detail="Repository URL not configured")
        
        # Parse repository URL
        if "github.com" in repo_url:
            parts = repo_url.replace("https://github.com/", "").split("/")
            owner = parts[0]
            repo = parts[1].replace(".git", "")
        else:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")
        
        # Get commits for analysis
        commits = get_commits(owner, repo, limit, github_token)
        
        # Calculate statistics
        stats = calculate_commit_statistics(commits)
        
        return {
            "statistics": stats,
            "commits_analyzed": len(commits)
        }
    
    except Exception as e:
        return {"error": str(e)}

def calculate_commit_statistics(commits: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate commit statistics and patterns"""
    if not commits:
        return {}
    
    stats = {
        "total_commits": len(commits),
        "total_additions": 0,
        "total_deletions": 0,
        "total_files_changed": 0,
        "authors": {},
        "commit_frequency": {},
        "file_changes": {},
        "commit_types": {}
    }
    
    for commit in commits:
        # Count additions and deletions
        stats["total_additions"] += commit.get("additions", 0)
        stats["total_deletions"] += commit.get("deletions", 0)
        stats["total_files_changed"] += commit.get("files_changed", 0)
        
        # Count authors
        author = commit["author"]["name"]
        stats["authors"][author] = stats["authors"].get(author, 0) + 1
        
        # Count commit frequency by date
        date = commit["author"]["date"][:10]  # YYYY-MM-DD
        stats["commit_frequency"][date] = stats["commit_frequency"].get(date, 0) + 1
        
        # Count file changes
        for file in commit.get("files", []):
            stats["file_changes"][file] = stats["file_changes"].get(file, 0) + 1
        
        # Analyze commit types
        message = commit["message"].lower()
        if message.startswith("feat"):
            stats["commit_types"]["feature"] = stats["commit_types"].get("feature", 0) + 1
        elif message.startswith("fix"):
            stats["commit_types"]["bugfix"] = stats["commit_types"].get("bugfix", 0) + 1
        elif message.startswith("docs"):
            stats["commit_types"]["documentation"] = stats["commit_types"].get("documentation", 0) + 1
        elif message.startswith("style"):
            stats["commit_types"]["style"] = stats["commit_types"].get("style", 0) + 1
        elif message.startswith("refactor"):
            stats["commit_types"]["refactor"] = stats["commit_types"].get("refactor", 0) + 1
        elif message.startswith("test"):
            stats["commit_types"]["test"] = stats["commit_types"].get("test", 0) + 1
        else:
            stats["commit_types"]["other"] = stats["commit_types"].get("other", 0) + 1
    
    # Calculate averages
    stats["avg_additions"] = stats["total_additions"] / len(commits)
    stats["avg_deletions"] = stats["total_deletions"] / len(commits)
    stats["avg_files_changed"] = stats["total_files_changed"] / len(commits)
    
    # Get top contributors
    stats["top_contributors"] = sorted(
        stats["authors"].items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:5]
    
    # Get most changed files
    stats["most_changed_files"] = sorted(
        stats["file_changes"].items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:10]
    
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 