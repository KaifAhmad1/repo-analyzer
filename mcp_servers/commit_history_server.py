"""
Commit History MCP Server

This server provides tools for accessing commit messages, changes, and history
from GitHub repositories. Supports filtering, pagination, and detailed analysis.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from .base_server import BaseMCPServer

class CommitHistoryServer(BaseMCPServer):
    """
    MCP Server for commit history operations.
    
    Tools provided:
    - get_recent_commits: Get recent commits with details
    - get_commit_details: Get detailed information about a specific commit
    - get_commit_changes: Get files changed in a commit
    - get_commit_stats: Get commit statistics and metrics
    - search_commits: Search commits by message, author, or date
    - get_branch_commits: Get commits for a specific branch
    """
    
    def __init__(self):
        super().__init__(
            name="commit_history_server",
            description="Server for accessing commit history and changes from GitHub repositories"
        )
        
    async def initialize_tools(self) -> List[Dict[str, Any]]:
        """
        Initialize tools for commit history operations.
        """
        tools = [
            {
                "name": "get_recent_commits",
                "description": "Get recent commits from a repository with details",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "branch": "string (optional): Branch name, defaults to 'main'",
                    "limit": "integer (optional): Number of commits to return, defaults to 10",
                    "since": "string (optional): Get commits since this date (ISO format)"
                }
            },
            {
                "name": "get_commit_details",
                "description": "Get detailed information about a specific commit",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "commit_sha": "string (required): Commit SHA hash"
                }
            },
            {
                "name": "get_commit_changes",
                "description": "Get files changed in a specific commit",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "commit_sha": "string (required): Commit SHA hash"
                }
            },
            {
                "name": "get_commit_stats",
                "description": "Get commit statistics and metrics for a repository",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "branch": "string (optional): Branch name, defaults to 'main'",
                    "days": "integer (optional): Number of days to analyze, defaults to 30"
                }
            },
            {
                "name": "search_commits",
                "description": "Search commits by message, author, or date range",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "query": "string (optional): Search query for commit messages",
                    "author": "string (optional): Filter by author name or email",
                    "since": "string (optional): Start date (ISO format)",
                    "until": "string (optional): End date (ISO format)",
                    "limit": "integer (optional): Number of commits to return, defaults to 10"
                }
            },
            {
                "name": "get_branch_commits",
                "description": "Get commits for a specific branch",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "branch": "string (required): Branch name",
                    "limit": "integer (optional): Number of commits to return, defaults to 10"
                }
            }
        ]
        return tools
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Handle commit history tool calls.
        """
        try:
            if tool_name == "get_recent_commits":
                return await self._get_recent_commits(**arguments)
            elif tool_name == "get_commit_details":
                return await self._get_commit_details(**arguments)
            elif tool_name == "get_commit_changes":
                return await self._get_commit_changes(**arguments)
            elif tool_name == "get_commit_stats":
                return await self._get_commit_stats(**arguments)
            elif tool_name == "search_commits":
                return await self._search_commits(**arguments)
            elif tool_name == "get_branch_commits":
                return await self._get_branch_commits(**arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        except Exception as e:
            return await self.handle_error(e, f"Tool call failed: {tool_name}")
    
    async def _get_recent_commits(self, repository: str, branch: str = "main", 
                                 limit: int = 10, since: Optional[str] = None) -> Dict[str, Any]:
        """
        Get recent commits from repository.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Get commits for the specified branch
            commits = repo.get_commits(sha=branch, per_page=limit)
            
            commit_list = []
            for commit in commits:
                # Parse since date if provided
                if since:
                    since_date = datetime.fromisoformat(since.replace('Z', '+00:00'))
                    if commit.commit.author.date < since_date:
                        break
                
                commit_list.append({
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author": {
                        "name": commit.commit.author.name,
                        "email": commit.commit.author.email,
                        "date": commit.commit.author.date.isoformat()
                    },
                    "committer": {
                        "name": commit.commit.committer.name,
                        "email": commit.commit.committer.email,
                        "date": commit.commit.committer.date.isoformat()
                    },
                    "url": commit.html_url,
                    "parents": [parent.sha for parent in commit.parents],
                    "stats": {
                        "total": commit.stats.total,
                        "additions": commit.stats.additions,
                        "deletions": commit.stats.deletions
                    } if commit.stats else None
                })
            
            return {
                "repository": repository,
                "branch": branch,
                "total_commits": len(commit_list),
                "commits": commit_list
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_recent_commits({repository}, {branch})")
    
    async def _get_commit_details(self, repository: str, commit_sha: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific commit.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            commit = repo.get_commit(commit_sha)
            
            return {
                "repository": repository,
                "sha": commit.sha,
                "message": commit.commit.message,
                "author": {
                    "name": commit.commit.author.name,
                    "email": commit.commit.author.email,
                    "date": commit.commit.author.date.isoformat()
                },
                "committer": {
                    "name": commit.commit.committer.name,
                    "email": commit.commit.committer.email,
                    "date": commit.commit.committer.date.isoformat()
                },
                "url": commit.html_url,
                "parents": [parent.sha for parent in commit.parents],
                "stats": {
                    "total": commit.stats.total,
                    "additions": commit.stats.additions,
                    "deletions": commit.stats.deletions
                } if commit.stats else None,
                "files": [
                    {
                        "filename": file.filename,
                        "status": file.status,
                        "additions": file.additions,
                        "deletions": file.deletions,
                        "changes": file.changes,
                        "patch": file.patch
                    } for file in commit.files
                ] if commit.files else []
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_commit_details({repository}, {commit_sha})")
    
    async def _get_commit_changes(self, repository: str, commit_sha: str) -> Dict[str, Any]:
        """
        Get files changed in a specific commit.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            commit = repo.get_commit(commit_sha)
            
            changes = []
            for file in commit.files:
                change_info = {
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes
                }
                
                # Add patch information if available
                if file.patch:
                    change_info["patch"] = file.patch
                
                # Add previous filename for renamed files
                if file.status == "renamed" and hasattr(file, 'previous_filename'):
                    change_info["previous_filename"] = file.previous_filename
                
                changes.append(change_info)
            
            return {
                "repository": repository,
                "commit_sha": commit_sha,
                "total_files": len(changes),
                "total_additions": sum(f["additions"] for f in changes),
                "total_deletions": sum(f["deletions"] for f in changes),
                "changes": changes
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_commit_changes({repository}, {commit_sha})")
    
    async def _get_commit_stats(self, repository: str, branch: str = "main", 
                               days: int = 30) -> Dict[str, Any]:
        """
        Get commit statistics and metrics for a repository.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get commits in the date range
            commits = repo.get_commits(sha=branch, since=start_date, until=end_date)
            
            total_commits = 0
            total_additions = 0
            total_deletions = 0
            authors = {}
            daily_commits = {}
            
            for commit in commits:
                total_commits += 1
                
                # Track author activity
                author_name = commit.commit.author.name
                if author_name not in authors:
                    authors[author_name] = {
                        "commits": 0,
                        "additions": 0,
                        "deletions": 0
                    }
                authors[author_name]["commits"] += 1
                
                # Track daily activity
                commit_date = commit.commit.author.date.date().isoformat()
                if commit_date not in daily_commits:
                    daily_commits[commit_date] = 0
                daily_commits[commit_date] += 1
                
                # Track code changes
                if commit.stats:
                    total_additions += commit.stats.additions
                    total_deletions += commit.stats.deletions
                    authors[author_name]["additions"] += commit.stats.additions
                    authors[author_name]["deletions"] += commit.stats.deletions
            
            # Sort authors by commit count
            sorted_authors = sorted(authors.items(), key=lambda x: x[1]["commits"], reverse=True)
            
            return {
                "repository": repository,
                "branch": branch,
                "period_days": days,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_commits": total_commits,
                "total_additions": total_additions,
                "total_deletions": total_deletions,
                "net_changes": total_additions - total_deletions,
                "unique_authors": len(authors),
                "top_authors": sorted_authors[:5],
                "daily_activity": daily_commits,
                "average_commits_per_day": total_commits / days if days > 0 else 0
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_commit_stats({repository}, {branch})")
    
    async def _search_commits(self, repository: str, query: Optional[str] = None,
                             author: Optional[str] = None, since: Optional[str] = None,
                             until: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        Search commits by message, author, or date range.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Build search query
            search_query_parts = [f"repo:{repository}"]
            
            if query:
                search_query_parts.append(query)
            
            if author:
                search_query_parts.append(f"author:{author}")
            
            if since:
                search_query_parts.append(f"committer-date:>={since}")
            
            if until:
                search_query_parts.append(f"committer-date:<={until}")
            
            search_query = " ".join(search_query_parts)
            
            # Search commits
            commits = repo.search_commits(search_query, per_page=limit)
            
            commit_list = []
            for commit in commits:
                commit_list.append({
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author": {
                        "name": commit.commit.author.name,
                        "email": commit.commit.author.email,
                        "date": commit.commit.author.date.isoformat()
                    },
                    "committer": {
                        "name": commit.commit.committer.name,
                        "email": commit.commit.committer.email,
                        "date": commit.commit.committer.date.isoformat()
                    },
                    "url": commit.html_url,
                    "score": commit.score if hasattr(commit, 'score') else None
                })
            
            return {
                "repository": repository,
                "search_query": search_query,
                "total_results": len(commit_list),
                "commits": commit_list
            }
            
        except Exception as e:
            return await self.handle_error(e, f"search_commits({repository})")
    
    async def _get_branch_commits(self, repository: str, branch: str, 
                                 limit: int = 10) -> Dict[str, Any]:
        """
        Get commits for a specific branch.
        """
        return await self._get_recent_commits(repository, branch, limit) 