"""
Commit History Server using FastMCP v2
Provides commit history and statistics for GitHub repositories
"""

import os
import requests
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP, Context
from datetime import datetime

mcp = FastMCP("Commit History Server 🚀")

def get_github_token() -> Optional[str]:
    import streamlit as st
    return st.session_state.get("github_token", os.getenv("GITHUB_TOKEN"))

def parse_repo_url(repo_url: str) -> tuple[str, str]:
    if "github.com" in repo_url:
        parts = repo_url.replace("https://github.com/", "").split("/")
        owner = parts[0]
        repo = parts[1].replace(".git", "")
        return owner, repo
    else:
        raise ValueError("Invalid GitHub URL")

def make_github_request(endpoint: str, params: dict = None) -> Any:
    token = get_github_token()
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    response = requests.get(f"https://api.github.com{endpoint}", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

@mcp.tool
async def get_commit_history(repo_url: str, limit: int = 10, ctx: Context = None) -> Dict[str, Any]:
    """Get recent commit history for a repository"""
    try:
        owner, repo = parse_repo_url(repo_url)
        params = {"per_page": min(limit, 100), "page": 1}
        data = make_github_request(f"/repos/{owner}/{repo}/commits", params)
        commits = []
        for commit_data in data[:limit]:
            commit = {
                "sha": commit_data["sha"][:8],
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
                "url": commit_data["html_url"]
            }
            commits.append(commit)
        return {"commits": commits, "total_count": len(commits), "repository": f"{owner}/{repo}"}
    except Exception as e:
        if ctx:
            await ctx.error(f"Error fetching commit history: {str(e)}")
        return {"error": str(e)}

@mcp.tool
async def get_commit_statistics(repo_url: str, limit: int = 50, ctx: Context = None) -> Dict[str, Any]:
    """Get commit statistics and patterns for a repository"""
    try:
        owner, repo = parse_repo_url(repo_url)
        params = {"per_page": min(limit, 100), "page": 1}
        data = make_github_request(f"/repos/{owner}/{repo}/commits", params)
        commits = []
        for commit_data in data[:limit]:
            commit = {
                "sha": commit_data["sha"][:8],
                "message": commit_data["commit"]["message"],
                "author": commit_data["commit"]["author"]["name"],
                "date": commit_data["commit"]["author"]["date"]
            }
            commits.append(commit)
        stats = calculate_commit_statistics(commits)
        return {"statistics": stats, "commits_analyzed": len(commits)}
    except Exception as e:
        if ctx:
            await ctx.error(f"Error fetching commit statistics: {str(e)}")
        return {"error": str(e)}

def calculate_commit_statistics(commits: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not commits:
        return {}
    stats = {
        "total_commits": len(commits),
        "authors": {},
        "commit_frequency": {},
        "commit_types": {}
    }
    for commit in commits:
        author = commit["author"]
        stats["authors"][author] = stats["authors"].get(author, 0) + 1
        date = commit["date"][:10]
        stats["commit_frequency"][date] = stats["commit_frequency"].get(date, 0) + 1
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
    stats["top_contributors"] = sorted(
        stats["authors"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    return stats

if __name__ == "__main__":
    mcp.run() 