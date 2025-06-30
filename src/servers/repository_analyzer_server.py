"""
Repository Analyzer MCP Server
A comprehensive MCP server for analyzing GitHub repositories using the official Anthropic MCP SDK
"""

import os
import base64
import requests
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path

from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field

# Create the MCP server
mcp = FastMCP("Repository Analyzer", dependencies=["requests", "PyGithub"])

# Data models
class RepositoryInfo(BaseModel):
    """Repository information"""
    name: str = Field(description="Repository name")
    full_name: str = Field(description="Full repository name (owner/repo)")
    description: str = Field(description="Repository description")
    language: str = Field(description="Primary programming language")
    stars: int = Field(description="Number of stars")
    forks: int = Field(description="Number of forks")
    issues: int = Field(description="Number of open issues")
    size: int = Field(description="Repository size in KB")
    created_at: str = Field(description="Creation date")
    updated_at: str = Field(description="Last update date")
    topics: List[str] = Field(description="Repository topics")

class FileInfo(BaseModel):
    """File information"""
    name: str = Field(description="File name")
    path: str = Field(description="File path")
    size: int = Field(description="File size in bytes")
    type: str = Field(description="File type (file/directory)")
    content: Optional[str] = Field(description="File content (if applicable)")

class CommitInfo(BaseModel):
    """Commit information"""
    sha: str = Field(description="Commit SHA")
    message: str = Field(description="Commit message")
    author: str = Field(description="Author name")
    date: str = Field(description="Commit date")
    files_changed: int = Field(description="Number of files changed")

class IssueInfo(BaseModel):
    """Issue information"""
    number: int = Field(description="Issue number")
    title: str = Field(description="Issue title")
    state: str = Field(description="Issue state (open/closed)")
    author: str = Field(description="Issue author")
    created_at: str = Field(description="Creation date")
    labels: List[str] = Field(description="Issue labels")

class CodeSearchResult(BaseModel):
    """Code search result"""
    file_path: str = Field(description="File path")
    line_number: int = Field(description="Line number")
    content: str = Field(description="Code content")
    match_type: str = Field(description="Type of match")

# Helper functions
def get_github_token() -> str:
    """Get GitHub token from environment"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GitHub token not found in environment variables")
    return token

def parse_repo_url(repo_url: str) -> tuple[str, str]:
    """Parse GitHub repository URL to get owner and repo name"""
    if "github.com" in repo_url:
        parts = repo_url.replace("https://github.com/", "").split("/")
        owner = parts[0]
        repo = parts[1].replace(".git", "")
        return owner, repo
    else:
        raise ValueError("Invalid GitHub URL")

def make_github_request(endpoint: str, token: str) -> Dict[str, Any]:
    """Make a GitHub API request"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(f"https://api.github.com{endpoint}", headers=headers)
    response.raise_for_status()
    return response.json()

# MCP Resources
@mcp.resource("repo://{owner}/{repo}/info")
def get_repository_info(owner: str, repo: str) -> str:
    """Get basic repository information"""
    try:
        token = get_github_token()
        data = make_github_request(f"/repos/{owner}/{repo}", token)
        
        info = RepositoryInfo(
            name=data["name"],
            full_name=data["full_name"],
            description=data["description"] or "No description",
            language=data["language"] or "Unknown",
            stars=data["stargazers_count"],
            forks=data["forks_count"],
            issues=data["open_issues_count"],
            size=data["size"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            topics=data.get("topics", [])
        )
        
        return f"""
# Repository Information: {info.full_name}

**Description:** {info.description}
**Language:** {info.language}
**Stars:** {info.stars} | **Forks:** {info.forks} | **Issues:** {info.issues}
**Size:** {info.size} KB
**Created:** {info.created_at}
**Updated:** {info.updated_at}
**Topics:** {', '.join(info.topics) if info.topics else 'None'}
        """.strip()
    
    except Exception as e:
        return f"Error getting repository info: {str(e)}"

@mcp.resource("repo://{owner}/{repo}/structure/{path:path}")
def get_repository_structure(owner: str, repo: str, path: str = "") -> str:
    """Get repository directory structure"""
    try:
        token = get_github_token()
        data = make_github_request(f"/repos/{owner}/{repo}/contents/{path}", token)
        
        if isinstance(data, dict):
            # Single file
            file_info = FileInfo(
                name=data["name"],
                path=data["path"],
                size=data["size"],
                type="file",
                content=None
            )
            return f"File: {file_info.path} ({file_info.size} bytes)"
        
        # Directory listing
        files = []
        directories = []
        
        for item in data:
            if item["type"] == "file":
                files.append(FileInfo(
                    name=item["name"],
                    path=item["path"],
                    size=item["size"],
                    type="file"
                ))
            elif item["type"] == "dir":
                directories.append(FileInfo(
                    name=item["name"],
                    path=item["path"],
                    size=0,
                    type="directory"
                ))
        
        result = f"# Repository Structure: {path or 'root'}\n\n"
        
        if directories:
            result += "## 📁 Directories\n"
            for dir_info in directories:
                result += f"- `{dir_info.name}/`\n"
            result += "\n"
        
        if files:
            result += "## 📄 Files\n"
            for file_info in files:
                result += f"- `{file_info.name}` ({file_info.size} bytes)\n"
        
        return result
    
    except Exception as e:
        return f"Error getting repository structure: {str(e)}"

@mcp.resource("repo://{owner}/{repo}/file/{path:path}")
def get_file_content(owner: str, repo: str, path: str) -> str:
    """Get content of a specific file"""
    try:
        token = get_github_token()
        data = make_github_request(f"/repos/{owner}/{repo}/contents/{path}", token)
        
        if data["type"] != "file":
            return f"Error: {path} is not a file"
        
        # Decode content
        content = base64.b64decode(data["content"]).decode("utf-8")
        
        return f"""
# File: {path}

```{Path(path).suffix[1:] if Path(path).suffix else 'text'}
{content}
```
        """.strip()
    
    except Exception as e:
        return f"Error getting file content: {str(e)}"

# MCP Tools
@mcp.tool(title="Repository Overview")
def get_repository_overview(repo_url: str) -> RepositoryInfo:
    """Get comprehensive repository overview"""
    try:
        owner, repo = parse_repo_url(repo_url)
        token = get_github_token()
        data = make_github_request(f"/repos/{owner}/{repo}", token)
        
        return RepositoryInfo(
            name=data["name"],
            full_name=data["full_name"],
            description=data["description"] or "No description",
            language=data["language"] or "Unknown",
            stars=data["stargazers_count"],
            forks=data["forks_count"],
            issues=data["open_issues_count"],
            size=data["size"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            topics=data.get("topics", [])
        )
    
    except Exception as e:
        raise ValueError(f"Error getting repository overview: {str(e)}")

@mcp.tool(title="Search Code")
def search_code(repo_url: str, query: str, language: str = "") -> List[CodeSearchResult]:
    """Search for code patterns in the repository"""
    try:
        owner, repo = parse_repo_url(repo_url)
        token = get_github_token()
        
        # Build search query
        search_query = f"{query} repo:{owner}/{repo}"
        if language:
            search_query += f" language:{language}"
        
        data = make_github_request(f"/search/code?q={search_query}", token)
        
        results = []
        for item in data["items"]:
            # Get file content for the matched file
            file_data = make_github_request(f"/repos/{owner}/{repo}/contents/{item['path']}", token)
            content = base64.b64decode(file_data["content"]).decode("utf-8")
            
            # Find the line with the match (simplified)
            lines = content.split('\n')
            line_number = 1  # Default to first line
            
            for i, line in enumerate(lines, 1):
                if query.lower() in line.lower():
                    line_number = i
                    break
            
            results.append(CodeSearchResult(
                file_path=item["path"],
                line_number=line_number,
                content=lines[line_number-1] if line_number <= len(lines) else "",
                match_type="text_match"
            ))
        
        return results
    
    except Exception as e:
        raise ValueError(f"Error searching code: {str(e)}")

@mcp.tool(title="Get Recent Commits")
def get_recent_commits(repo_url: str, limit: int = 10) -> List[CommitInfo]:
    """Get recent commit history"""
    try:
        owner, repo = parse_repo_url(repo_url)
        token = get_github_token()
        data = make_github_request(f"/repos/{owner}/{repo}/commits?per_page={limit}", token)
        
        commits = []
        for commit_data in data:
            commits.append(CommitInfo(
                sha=commit_data["sha"][:8],
                message=commit_data["commit"]["message"],
                author=commit_data["commit"]["author"]["name"],
                date=commit_data["commit"]["author"]["date"],
                files_changed=0  # Would need additional API call to get this
            ))
        
        return commits
    
    except Exception as e:
        raise ValueError(f"Error getting commits: {str(e)}")

@mcp.tool(title="Get Issues")
def get_issues(repo_url: str, state: str = "open", limit: int = 10) -> List[IssueInfo]:
    """Get repository issues"""
    try:
        owner, repo = parse_repo_url(repo_url)
        token = get_github_token()
        data = make_github_request(f"/repos/{owner}/{repo}/issues?state={state}&per_page={limit}", token)
        
        issues = []
        for issue_data in data:
            issues.append(IssueInfo(
                number=issue_data["number"],
                title=issue_data["title"],
                state=issue_data["state"],
                author=issue_data["user"]["login"],
                created_at=issue_data["created_at"],
                labels=[label["name"] for label in issue_data["labels"]]
            ))
        
        return issues
    
    except Exception as e:
        raise ValueError(f"Error getting issues: {str(e)}")

@mcp.tool(title="Analyze Repository")
async def analyze_repository(repo_url: str, ctx: Context) -> str:
    """Perform comprehensive repository analysis"""
    try:
        owner, repo = parse_repo_url(repo_url)
        token = get_github_token()
        
        # Get repository info
        repo_data = make_github_request(f"/repos/{owner}/{repo}", token)
        
        # Get recent commits
        commits_data = make_github_request(f"/repos/{owner}/{repo}/commits?per_page=5", token)
        
        # Get open issues
        issues_data = make_github_request(f"/repos/{owner}/{repo}/issues?state=open&per_page=5", token)
        
        # Get repository structure (root level)
        try:
            structure_data = make_github_request(f"/repos/{owner}/{repo}/contents", token)
            file_count = len([item for item in structure_data if item["type"] == "file"])
            dir_count = len([item for item in structure_data if item["type"] == "dir"])
        except:
            file_count = 0
            dir_count = 0
        
        analysis = f"""
# Repository Analysis: {repo_data['full_name']}

## 📊 Overview
- **Description:** {repo_data['description'] or 'No description'}
- **Language:** {repo_data['language'] or 'Unknown'}
- **Stars:** {repo_data['stargazers_count']} | **Forks:** {repo_data['forks_count']}
- **Issues:** {repo_data['open_issues_count']} open
- **Size:** {repo_data['size']} KB
- **Created:** {repo_data['created_at']}
- **Last Updated:** {repo_data['updated_at']}

## 📁 Structure
- **Files:** {file_count} | **Directories:** {dir_count}

## 🔄 Recent Activity
**Latest Commits:**
"""
        
        for commit in commits_data[:3]:
            analysis += f"- {commit['sha'][:8]}: {commit['commit']['message'][:50]}...\n"
        
        analysis += "\n**Recent Issues:**\n"
        for issue in issues_data[:3]:
            analysis += f"- #{issue['number']}: {issue['title'][:50]}...\n"
        
        return analysis
    
    except Exception as e:
        raise ValueError(f"Error analyzing repository: {str(e)}")

# MCP Prompts
@mcp.prompt(title="Code Review Assistant")
def code_review_prompt(code: str, file_path: str = "") -> str:
    """Generate a code review prompt"""
    return f"""
Please review this code{f" from {file_path}" if file_path else ""}:

```python
{code}
```

Please provide:
1. Code quality assessment
2. Potential issues or bugs
3. Security concerns
4. Performance improvements
5. Best practices suggestions
"""

@mcp.prompt(title="Repository Analysis")
def repository_analysis_prompt(repo_url: str) -> str:
    """Generate a repository analysis prompt"""
    return f"""
Please analyze the repository at {repo_url} and provide:

1. **Project Overview**
   - What is this project about?
   - What are its main features?
   - What technologies does it use?

2. **Code Quality Assessment**
   - Overall code structure
   - Documentation quality
   - Testing coverage

3. **Architecture Analysis**
   - Design patterns used
   - Dependencies and their purposes
   - Scalability considerations

4. **Security & Best Practices**
   - Security vulnerabilities
   - Code quality issues
   - Recommendations for improvement

5. **Maintenance & Development**
   - Recent activity level
   - Community health
   - Future development potential
"""

if __name__ == "__main__":
    mcp.run() 