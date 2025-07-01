"""
Commit History Server using FastMCP v2
Simple and effective commit history analysis
"""

import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from fastmcp import FastMCP, Context

# Create FastMCP server instance
mcp = FastMCP("Commit History Server 📝")

def parse_repo_url(repo_url: str) -> tuple[str, str]:
    """Parse GitHub repository URL to get owner and repo name"""
    if "github.com" in repo_url:
        parts = repo_url.replace("https://github.com/", "").split("/")
        owner = parts[0]
        repo = parts[1].replace(".git", "")
        return owner, repo
    else:
        raise ValueError("Invalid GitHub URL")

def make_github_request(endpoint: str) -> Dict[str, Any]:
    """Make a GitHub API request with proper headers"""
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(f"https://api.github.com{endpoint}", headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool
async def get_recent_commits(repo_url: str, ctx: Context, limit: int = 20) -> Dict[str, Any]:
    """Get recent commits from repository with detailed information"""
    try:
        await ctx.info(f"Fetching {limit} recent commits from {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        data = make_github_request(f"/repos/{owner}/{repo}/commits?per_page={limit}")
        
        commits = []
        for commit_data in data:
            commit = {
                "sha": commit_data["sha"][:8],
                "full_sha": commit_data["sha"],
                "message": commit_data["commit"]["message"],
                "author": {
                    "name": commit_data["commit"]["author"]["name"],
                    "email": commit_data["commit"]["author"]["email"],
                    "login": commit_data.get("author", {}).get("login", "Unknown")
                },
                "date": commit_data["commit"]["author"]["date"],
                "url": commit_data["html_url"],
                "files_changed": len(commit_data.get("files", [])),
                "additions": sum(f.get("additions", 0) for f in commit_data.get("files", [])),
                "deletions": sum(f.get("deletions", 0) for f in commit_data.get("files", [])),
                "stats": {
                    "total": commit_data.get("stats", {}).get("total", 0),
                    "additions": commit_data.get("stats", {}).get("additions", 0),
                    "deletions": commit_data.get("stats", {}).get("deletions", 0)
                }
            }
            commits.append(commit)
        
        result = {
            "repository": f"{owner}/{repo}",
            "commits": commits,
            "count": len(commits),
            "success": True
        }
        
        await ctx.info(f"Retrieved {len(commits)} commits")
        return result
        
    except Exception as e:
        await ctx.error(f"Error fetching commits: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

@mcp.tool
async def get_commit_details(repo_url: str, commit_sha: str, ctx: Context) -> Dict[str, Any]:
    """Get detailed information about a specific commit"""
    try:
        await ctx.info(f"Fetching details for commit {commit_sha[:8]} from {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        commit_data = make_github_request(f"/repos/{owner}/{repo}/commits/{commit_sha}")
        
        # Get files changed
        files_changed = []
        for file_data in commit_data.get("files", []):
            file_info = {
                "filename": file_data["filename"],
                "status": file_data["status"],
                "additions": file_data.get("additions", 0),
                "deletions": file_data.get("deletions", 0),
                "changes": file_data.get("changes", 0),
                "patch": file_data.get("patch", "")[:500] + "..." if file_data.get("patch") and len(file_data.get("patch", "")) > 500 else file_data.get("patch", "")
            }
            files_changed.append(file_info)
        
        # Get commit message and details
        commit = commit_data["commit"]
        result = {
            "sha": commit_data["sha"][:8],
            "full_sha": commit_data["sha"],
            "message": commit["message"],
            "author": {
                "name": commit["author"]["name"],
                "email": commit["author"]["email"],
                "date": commit["author"]["date"],
                "login": commit_data.get("author", {}).get("login", "Unknown")
            },
            "committer": {
                "name": commit["committer"]["name"],
                "email": commit["committer"]["email"],
                "date": commit["committer"]["date"]
            },
            "url": commit_data["html_url"],
            "files_changed": files_changed,
            "stats": commit_data.get("stats", {}),
            "parents": [p["sha"][:8] for p in commit_data.get("parents", [])],
            "success": True
        }
        
        await ctx.info(f"Retrieved details for commit {commit_sha[:8]}")
        return result
        
    except Exception as e:
        await ctx.error(f"Error fetching commit details: {str(e)}")
        return {
            "error": str(e),
            "commit_sha": commit_sha,
            "success": False
        }

@mcp.tool
async def get_commit_statistics(repo_url: str, ctx: Context, days: int = 30) -> Dict[str, Any]:
    """Get commit statistics for a repository over a time period"""
    try:
        await ctx.info(f"Calculating commit statistics for {repo_url} (last {days} days)")
        
        owner, repo = parse_repo_url(repo_url)
        
        # Get commits for the specified period
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        data = make_github_request(f"/repos/{owner}/{repo}/commits?since={since_date}&per_page=100")
        
        if not data:
            return {
                "repository": f"{owner}/{repo}",
                "period_days": days,
                "total_commits": 0,
                "statistics": {
                    "total_commits": 0,
                    "total_additions": 0,
                    "total_deletions": 0,
                    "average_commit_size": 0,
                    "most_active_day": None,
                    "most_active_author": None
                },
                "success": True
            }
        
        # Calculate statistics
        total_commits = len(data)
        total_additions = 0
        total_deletions = 0
        author_commits = {}
        daily_commits = {}
        
        for commit_data in data:
            # Count additions and deletions
            stats = commit_data.get("stats", {})
            total_additions += stats.get("additions", 0)
            total_deletions += stats.get("deletions", 0)
            
            # Count author commits
            author = commit_data.get("author", {}).get("login", "Unknown")
            author_commits[author] = author_commits.get(author, 0) + 1
            
            # Count daily commits
            commit_date = commit_data["commit"]["author"]["date"][:10]  # YYYY-MM-DD
            daily_commits[commit_date] = daily_commits.get(commit_date, 0) + 1
        
        # Find most active author and day
        most_active_author = max(author_commits.items(), key=lambda x: x[1]) if author_commits else None
        most_active_day = max(daily_commits.items(), key=lambda x: x[1]) if daily_commits else None
        
        result = {
            "repository": f"{owner}/{repo}",
            "period_days": days,
            "total_commits": total_commits,
            "statistics": {
                "total_commits": total_commits,
                "total_additions": total_additions,
                "total_deletions": total_deletions,
                "average_commit_size": (total_additions + total_deletions) / total_commits if total_commits > 0 else 0,
                "most_active_day": {
                    "date": most_active_day[0],
                    "commits": most_active_day[1]
                } if most_active_day else None,
                "most_active_author": {
                    "author": most_active_author[0],
                    "commits": most_active_author[1]
                } if most_active_author else None,
                "author_breakdown": author_commits,
                "daily_breakdown": daily_commits
            },
            "success": True
        }
        
        await ctx.info(f"Statistics calculated: {total_commits} commits, {total_additions} additions, {total_deletions} deletions")
        return result
        
    except Exception as e:
        await ctx.error(f"Error calculating commit statistics: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

@mcp.tool
async def search_commits(repo_url: str, query: str, ctx: Context, limit: int = 20) -> Dict[str, Any]:
    """Search for commits containing specific text in commit messages"""
    try:
        await ctx.info(f"Searching for commits with '{query}' in {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        # Get recent commits and filter by query
        data = make_github_request(f"/repos/{owner}/{repo}/commits?per_page=100")
        
        matching_commits = []
        query_lower = query.lower()
        
        for commit_data in data:
            message = commit_data["commit"]["message"].lower()
            if query_lower in message:
                commit = {
                    "sha": commit_data["sha"][:8],
                    "message": commit_data["commit"]["message"],
                    "author": {
                        "name": commit_data["commit"]["author"]["name"],
                        "login": commit_data.get("author", {}).get("login", "Unknown")
                    },
                    "date": commit_data["commit"]["author"]["date"],
                    "url": commit_data["html_url"]
                }
                matching_commits.append(commit)
                
                if len(matching_commits) >= limit:
                    break
        
        result = {
            "repository": f"{owner}/{repo}",
            "query": query,
            "commits": matching_commits,
            "count": len(matching_commits),
            "success": True
        }
        
        await ctx.info(f"Found {len(matching_commits)} commits matching '{query}'")
        return result
        
    except Exception as e:
        await ctx.error(f"Error searching commits: {str(e)}")
        return {
            "error": str(e),
            "query": query,
            "success": False
        }

@mcp.tool
async def get_branch_commits(repo_url: str, branch: str, ctx: Context, limit: int = 20) -> Dict[str, Any]:
    """Get commits from a specific branch"""
    try:
        await ctx.info(f"Fetching commits from branch '{branch}' in {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        data = make_github_request(f"/repos/{owner}/{repo}/commits?sha={branch}&per_page={limit}")
        
        commits = []
        for commit_data in data:
            commit = {
                "sha": commit_data["sha"][:8],
                "message": commit_data["commit"]["message"],
                "author": {
                    "name": commit_data["commit"]["author"]["name"],
                    "login": commit_data.get("author", {}).get("login", "Unknown")
                },
                "date": commit_data["commit"]["author"]["date"],
                "url": commit_data["html_url"]
            }
            commits.append(commit)
        
        result = {
            "repository": f"{owner}/{repo}",
            "branch": branch,
            "commits": commits,
            "count": len(commits),
            "success": True
        }
        
        await ctx.info(f"Retrieved {len(commits)} commits from branch '{branch}'")
        return result
        
    except Exception as e:
        await ctx.error(f"Error fetching branch commits: {str(e)}")
        return {
            "error": str(e),
            "branch": branch,
            "success": False
        }

# Resources for static data access
@mcp.resource("commits://{owner}/{repo}/recent")
def get_recent_commits_resource(owner: str, repo: str) -> Dict[str, Any]:
    """Resource endpoint for recent commits"""
    try:
        data = make_github_request(f"/repos/{owner}/{repo}/commits?per_page=10")
        commits = []
        for commit_data in data:
            commits.append({
                "sha": commit_data["sha"][:8],
                "message": commit_data["commit"]["message"],
                "author": commit_data.get("author", {}).get("login", "Unknown"),
                "date": commit_data["commit"]["author"]["date"]
            })
        return {
            "repository": f"{owner}/{repo}",
            "commits": commits
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("commits://{owner}/{repo}/stats")
def get_commit_stats_resource(owner: str, repo: str) -> Dict[str, Any]:
    """Resource endpoint for commit statistics"""
    try:
        # Get basic stats
        data = make_github_request(f"/repos/{owner}/{repo}/commits?per_page=100")
        total_commits = len(data)
        total_additions = sum(c.get("stats", {}).get("additions", 0) for c in data)
        total_deletions = sum(c.get("stats", {}).get("deletions", 0) for c in data)
        
        return {
            "repository": f"{owner}/{repo}",
            "total_commits": total_commits,
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "average_commit_size": (total_additions + total_deletions) / total_commits if total_commits > 0 else 0
        }
    except Exception as e:
        return {"error": str(e)}

# Prompts for commit analysis
@mcp.prompt
def commit_analysis_prompt(commit_data: str) -> str:
    """Generate a prompt for analyzing commit data"""
    return f"""Analyze this commit data:

{commit_data[:2000]}{'...' if len(commit_data) > 2000 else ''}

Please provide:
1. Commit purpose and impact
2. Files changed and their significance
3. Code quality indicators
4. Potential issues or improvements
5. Development patterns observed"""

@mcp.prompt
def commit_history_prompt(commits_data: str) -> str:
    """Generate a prompt for analyzing commit history"""
    return f"""Analyze this commit history:

{commits_data[:3000]}{'...' if len(commits_data) > 3000 else ''}

Please provide:
1. Development activity patterns
2. Most active contributors
3. Commit frequency and consistency
4. Project health indicators
5. Development workflow insights"""

if __name__ == "__main__":
    mcp.run() 