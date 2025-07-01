"""
Repository Analyzer Server using FastMCP v2
Provides comprehensive repository analysis tools and resources
"""

import os
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import requests
from fastmcp import FastMCP, Context

# Create FastMCP server instance
mcp = FastMCP("Repository Analyzer 🚀")

def get_github_token() -> Optional[str]:
    """Get GitHub token from environment or session state"""
    import streamlit as st
    return st.session_state.get("github_token", os.getenv("GITHUB_TOKEN"))

def make_github_request(endpoint: str) -> Dict[str, Any]:
    """Make a GitHub API request"""
    token = get_github_token()
    
    headers = {"Accept": "application/vnd.github.v3+json"}
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

# ============================================================================
# TOOLS - Actions that can be performed
# ============================================================================

@mcp.tool
def get_repository_overview(repo_url: str, ctx: Context) -> Dict[str, Any]:
    """Get comprehensive overview of a GitHub repository"""
    try:
        await ctx.info(f"Analyzing repository: {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        data = make_github_request(f"/repos/{owner}/{repo}")
        
        # Get additional data
        languages = make_github_request(f"/repos/{owner}/{repo}/languages")
        contributors = make_github_request(f"/repos/{owner}/{repo}/contributors?per_page=5")
        topics = make_github_request(f"/repos/{owner}/{repo}/topics")
        
        # Calculate repository health metrics
        health_score = 0
        health_factors = []
        
        if data["has_issues"]:
            health_score += 20
            health_factors.append("Has issue tracking")
        
        if data["has_wiki"]:
            health_score += 10
            health_factors.append("Has documentation")
        
        if data["has_projects"]:
            health_score += 10
            health_factors.append("Has project management")
        
        if data["archived"]:
            health_score -= 30
            health_factors.append("Repository is archived")
        
        if data["fork"]:
            health_score += 5
            health_factors.append("Fork of another repository")
        
        # Recent activity check
        recent_commits = make_github_request(f"/repos/{owner}/{repo}/commits?per_page=1")
        if recent_commits:
            last_commit_date = datetime.fromisoformat(recent_commits[0]["commit"]["author"]["date"].replace("Z", "+00:00"))
            days_since_last_commit = (datetime.now(last_commit_date.tzinfo) - last_commit_date).days
            
            if days_since_last_commit <= 30:
                health_score += 25
                health_factors.append("Active development (last 30 days)")
            elif days_since_last_commit <= 90:
                health_score += 10
                health_factors.append("Recent activity (last 90 days)")
            else:
                health_score -= 20
                health_factors.append("No recent activity")
        
        overview = {
            "basic_info": {
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
                "archived": data["archived"],
                "fork": data["fork"]
            },
            "languages": languages,
            "topics": topics.get("names", []),
            "contributors": [{"login": c["login"], "contributions": c["contributions"]} for c in contributors],
            "health": {
                "score": max(0, min(100, health_score)),
                "factors": health_factors,
                "status": "Healthy" if health_score >= 70 else "Good" if health_score >= 50 else "Needs Attention"
            }
        }
        
        await ctx.info(f"Analysis complete. Health score: {overview['health']['score']}/100")
        return overview
        
    except Exception as e:
        await ctx.error(f"Error analyzing repository: {str(e)}")
        raise

@mcp.tool
def get_repository_commits(repo_url: str, limit: int = 20, ctx: Context) -> List[Dict[str, Any]]:
    """Get recent commits from repository with detailed information"""
    try:
        await ctx.info(f"Fetching {limit} recent commits from {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        data = make_github_request(f"/repos/{owner}/{repo}/commits?per_page={limit}")
        
        commits = []
        for commit_data in data:
            commit = {
                "sha": commit_data["sha"][:8],
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
                "deletions": sum(f.get("deletions", 0) for f in commit_data.get("files", []))
            }
            commits.append(commit)
        
        await ctx.info(f"Retrieved {len(commits)} commits")
        return commits
        
    except Exception as e:
        await ctx.error(f"Error fetching commits: {str(e)}")
        raise

@mcp.tool
def get_repository_issues(repo_url: str, state: str = "open", limit: int = 20, ctx: Context) -> List[Dict[str, Any]]:
    """Get repository issues with filtering options"""
    try:
        await ctx.info(f"Fetching {state} issues from {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        data = make_github_request(f"/repos/{owner}/{repo}/issues?state={state}&per_page={limit}&sort=updated")
        
        issues = []
        for issue_data in data:
            issue = {
                "number": issue_data["number"],
                "title": issue_data["title"],
                "state": issue_data["state"],
                "author": issue_data["user"]["login"],
                "created_at": issue_data["created_at"],
                "updated_at": issue_data["updated_at"],
                "labels": [label["name"] for label in issue_data["labels"]],
                "comments": issue_data["comments"],
                "body": issue_data["body"][:200] + "..." if issue_data["body"] and len(issue_data["body"]) > 200 else issue_data["body"]
            }
            issues.append(issue)
        
        await ctx.info(f"Retrieved {len(issues)} {state} issues")
        return issues
        
    except Exception as e:
        await ctx.error(f"Error fetching issues: {str(e)}")
        raise

@mcp.tool
def search_repository_code(repo_url: str, query: str, ctx: Context) -> List[Dict[str, Any]]:
    """Search for code patterns in repository"""
    try:
        await ctx.info(f"Searching for '{query}' in {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        data = make_github_request(f"/search/code?q={query}+repo:{owner}/{repo}")
        
        results = []
        for item in data.get("items", []):
            result = {
                "file_path": item["path"],
                "file_name": item["name"],
                "url": item["html_url"],
                "repository": item["repository"]["full_name"],
                "language": item.get("language", "Unknown"),
                "size": item["size"],
                "score": item["score"]
            }
            results.append(result)
        
        await ctx.info(f"Found {len(results)} code matches")
        return results
        
    except Exception as e:
        await ctx.error(f"Error searching code: {str(e)}")
        raise

@mcp.tool
def analyze_repository_activity(repo_url: str, days: int = 30, ctx: Context) -> Dict[str, Any]:
    """Analyze repository activity over a specified period"""
    try:
        await ctx.info(f"Analyzing {days} days of activity for {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        # Get commits
        commits = make_github_request(f"/repos/{owner}/{repo}/commits?since={since_date}")
        
        # Get issues
        issues = make_github_request(f"/repos/{owner}/{repo}/issues?since={since_date}&state=all")
        
        # Get pull requests
        pulls = make_github_request(f"/repos/{owner}/{repo}/pulls?state=all&per_page=100")
        
        # Analyze activity patterns
        commit_authors = {}
        issue_creators = {}
        pull_creators = {}
        
        for commit in commits:
            author = commit["commit"]["author"]["name"]
            commit_authors[author] = commit_authors.get(author, 0) + 1
        
        for issue in issues:
            creator = issue["user"]["login"]
            issue_creators[creator] = issue_creators.get(creator, 0) + 1
        
        for pull in pulls:
            creator = pull["user"]["login"]
            pull_creators[creator] = pull_creators.get(creator, 0) + 1
        
        activity = {
            "period": f"Last {days} days",
            "commits": {
                "total": len(commits),
                "unique_authors": len(commit_authors),
                "top_contributors": sorted(commit_authors.items(), key=lambda x: x[1], reverse=True)[:5]
            },
            "issues": {
                "total": len(issues),
                "unique_creators": len(issue_creators),
                "top_creators": sorted(issue_creators.items(), key=lambda x: x[1], reverse=True)[:5]
            },
            "pull_requests": {
                "total": len(pulls),
                "unique_creators": len(pull_creators),
                "top_creators": sorted(pull_creators.items(), key=lambda x: x[1], reverse=True)[:5]
            },
            "activity_score": min(100, (len(commits) * 2 + len(issues) + len(pulls) * 3) // 10)
        }
        
        await ctx.info(f"Activity analysis complete. Score: {activity['activity_score']}/100")
        return activity
        
    except Exception as e:
        await ctx.error(f"Error analyzing activity: {str(e)}")
        raise

# ============================================================================
# RESOURCES - Read-only data sources
# ============================================================================

@mcp.resource("repo://{owner}/{repo}/info")
def get_repo_info(owner: str, repo: str) -> Dict[str, Any]:
    """Get basic repository information"""
    try:
        data = make_github_request(f"/repos/{owner}/{repo}")
        return {
            "name": data["name"],
            "full_name": data["full_name"],
            "description": data["description"],
            "language": data["language"],
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "issues": data["open_issues_count"],
            "created_at": data["created_at"],
            "updated_at": data["updated_at"]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("repo://{owner}/{repo}/languages")
def get_repo_languages(owner: str, repo: str) -> Dict[str, int]:
    """Get repository language statistics"""
    try:
        return make_github_request(f"/repos/{owner}/{repo}/languages")
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("repo://{owner}/{repo}/topics")
def get_repo_topics(owner: str, repo: str) -> List[str]:
    """Get repository topics/tags"""
    try:
        data = make_github_request(f"/repos/{owner}/{repo}/topics")
        return data.get("names", [])
    except Exception as e:
        return []

# ============================================================================
# PROMPTS - Reusable message templates
# ============================================================================

@mcp.prompt
def repository_analysis_prompt(repo_url: str, analysis_type: str = "general") -> str:
    """Generate a prompt for repository analysis"""
    prompts = {
        "general": f"""Analyze the GitHub repository at {repo_url} and provide a comprehensive overview including:
1. Purpose and main functionality
2. Technology stack and architecture
3. Development activity and health
4. Key features and capabilities
5. Community engagement metrics
6. Recommendations for improvement""",
        
        "technical": f"""Perform a technical analysis of {repo_url} focusing on:
1. Code quality and structure
2. Dependencies and technology choices
3. Architecture patterns used
4. Testing and documentation coverage
5. Performance considerations
6. Security practices""",
        
        "business": f"""Evaluate {repo_url} from a business perspective:
1. Market positioning and value proposition
2. User adoption and community growth
3. Maintenance and sustainability
4. Competitive advantages
5. Potential risks and challenges
6. Strategic recommendations"""
    }
    
    return prompts.get(analysis_type, prompts["general"])

@mcp.prompt
def code_review_prompt(file_path: str, code_content: str) -> str:
    """Generate a prompt for code review"""
    return f"""Please review the following code from {file_path}:

```{file_path.split('.')[-1] if '.' in file_path else 'text'}
{code_content}
```

Provide a comprehensive code review including:
1. Code quality and readability
2. Potential bugs or issues
3. Performance considerations
4. Security concerns
5. Best practices adherence
6. Suggestions for improvement"""

if __name__ == "__main__":
    mcp.run() 