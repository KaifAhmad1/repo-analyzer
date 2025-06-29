"""
Issues and Pull Requests MCP Server

This server provides tools for querying and analyzing GitHub issues and pull requests.
Supports filtering, searching, and detailed analysis of project issues.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from .base_server import BaseMCPServer

class IssuesServer(BaseMCPServer):
    """
    MCP Server for issues and pull requests operations.
    
    Tools provided:
    - get_issues: Get issues and pull requests
    - get_issue_details: Get detailed information about an issue
    - search_issues: Search issues by labels, state, or content
    - get_issue_comments: Get comments for an issue
    - analyze_issues: Analyze issue patterns and trends
    - get_pull_requests: Get pull requests with details
    """
    
    def __init__(self):
        super().__init__(
            name="issues_server",
            description="Server for querying and analyzing GitHub issues and pull requests"
        )
        
    async def initialize_tools(self) -> List[Dict[str, Any]]:
        """
        Initialize tools for issues and pull requests operations.
        """
        tools = [
            {
                "name": "get_issues",
                "description": "Get issues and pull requests from the repository",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "state": "string (optional): Issue state ('open', 'closed'), defaults to 'open'",
                    "labels": "array (optional): Filter by labels",
                    "assignee": "string (optional): Filter by assignee",
                    "creator": "string (optional): Filter by creator",
                    "limit": "integer (optional): Number of issues to return, defaults to 10"
                }
            },
            {
                "name": "get_issue_details",
                "description": "Get detailed information about a specific issue",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "issue_number": "integer (required): Issue number"
                }
            },
            {
                "name": "search_issues",
                "description": "Search issues by content, labels, or other criteria",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "query": "string (optional): Search query",
                    "state": "string (optional): Issue state ('open', 'closed')",
                    "labels": "array (optional): Filter by labels",
                    "limit": "integer (optional): Number of results to return, defaults to 10"
                }
            },
            {
                "name": "get_issue_comments",
                "description": "Get comments for a specific issue",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "issue_number": "integer (required): Issue number",
                    "limit": "integer (optional): Number of comments to return, defaults to 10"
                }
            },
            {
                "name": "analyze_issues",
                "description": "Analyze issue patterns and trends",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "days": "integer (optional): Number of days to analyze, defaults to 30"
                }
            },
            {
                "name": "get_pull_requests",
                "description": "Get pull requests with details",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "state": "string (optional): PR state ('open', 'closed', 'all'), defaults to 'open'",
                    "base": "string (optional): Filter by base branch",
                    "head": "string (optional): Filter by head branch",
                    "limit": "integer (optional): Number of PRs to return, defaults to 10"
                }
            }
        ]
        return tools
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Handle issues and pull requests tool calls.
        """
        try:
            if tool_name == "get_issues":
                return await self._get_issues(**arguments)
            elif tool_name == "get_issue_details":
                return await self._get_issue_details(**arguments)
            elif tool_name == "search_issues":
                return await self._search_issues(**arguments)
            elif tool_name == "get_issue_comments":
                return await self._get_issue_comments(**arguments)
            elif tool_name == "analyze_issues":
                return await self._analyze_issues(**arguments)
            elif tool_name == "get_pull_requests":
                return await self._get_pull_requests(**arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        except Exception as e:
            return await self.handle_error(e, f"Tool call failed: {tool_name}")
    
    async def _get_issues(self, repository: str, state: str = "open", 
                         labels: Optional[List[str]] = None, assignee: Optional[str] = None,
                         creator: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        Get issues and pull requests from repository.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Build filter parameters
            filters = {"state": state}
            if labels:
                filters["labels"] = labels
            if assignee:
                filters["assignee"] = assignee
            if creator:
                filters["creator"] = creator
            
            issues = repo.get_issues(**filters)
            
            issue_list = []
            for issue in issues:
                if len(issue_list) >= limit:
                    break
                
                issue_data = {
                    "number": issue.number,
                    "title": issue.title,
                    "body": issue.body,
                    "state": issue.state,
                    "created_at": issue.created_at.isoformat(),
                    "updated_at": issue.updated_at.isoformat(),
                    "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                    "user": {
                        "login": issue.user.login,
                        "avatar_url": issue.user.avatar_url
                    },
                    "labels": [label.name for label in issue.labels],
                    "assignees": [assignee.login for assignee in issue.assignees],
                    "comments": issue.comments,
                    "url": issue.html_url,
                    "is_pull_request": issue.pull_request is not None
                }
                
                issue_list.append(issue_data)
            
            return {
                "repository": repository,
                "state": state,
                "filters": filters,
                "total_issues": len(issue_list),
                "issues": issue_list
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_issues({repository}, {state})")
    
    async def _get_issue_details(self, repository: str, issue_number: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific issue.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            issue = repo.get_issue(issue_number)
            
            return {
                "repository": repository,
                "number": issue.number,
                "title": issue.title,
                "body": issue.body,
                "state": issue.state,
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat(),
                "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                "user": {
                    "login": issue.user.login,
                    "avatar_url": issue.user.avatar_url,
                    "type": issue.user.type
                },
                "labels": [
                    {
                        "name": label.name,
                        "color": label.color,
                        "description": label.description
                    } for label in issue.labels
                ],
                "assignees": [
                    {
                        "login": assignee.login,
                        "avatar_url": assignee.avatar_url
                    } for assignee in issue.assignees
                ],
                "comments": issue.comments,
                "url": issue.html_url,
                "is_pull_request": issue.pull_request is not None,
                "milestone": {
                    "title": issue.milestone.title,
                    "description": issue.milestone.description,
                    "state": issue.milestone.state
                } if issue.milestone else None
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_issue_details({repository}, {issue_number})")
    
    async def _search_issues(self, repository: str, query: Optional[str] = None,
                            state: Optional[str] = None, labels: Optional[List[str]] = None,
                            limit: int = 10) -> Dict[str, Any]:
        """
        Search issues by content, labels, or other criteria.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Build search query
            search_parts = [f"repo:{repository}"]
            
            if query:
                search_parts.append(query)
            
            if state:
                search_parts.append(f"state:{state}")
            
            if labels:
                for label in labels:
                    search_parts.append(f"label:\"{label}\"")
            
            search_query = " ".join(search_parts)
            
            # Search issues
            issues = repo.search_issues(search_query)
            
            issue_list = []
            for issue in issues:
                if len(issue_list) >= limit:
                    break
                
                issue_list.append({
                    "number": issue.number,
                    "title": issue.title,
                    "body": issue.body[:200] + "..." if issue.body and len(issue.body) > 200 else issue.body,
                    "state": issue.state,
                    "created_at": issue.created_at.isoformat(),
                    "updated_at": issue.updated_at.isoformat(),
                    "user": {
                        "login": issue.user.login,
                        "avatar_url": issue.user.avatar_url
                    },
                    "labels": [label.name for label in issue.labels],
                    "comments": issue.comments,
                    "url": issue.html_url,
                    "score": issue.score if hasattr(issue, 'score') else None
                })
            
            return {
                "repository": repository,
                "search_query": search_query,
                "total_results": len(issue_list),
                "issues": issue_list
            }
            
        except Exception as e:
            return await self.handle_error(e, f"search_issues({repository})")
    
    async def _get_issue_comments(self, repository: str, issue_number: int, 
                                 limit: int = 10) -> Dict[str, Any]:
        """
        Get comments for a specific issue.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            issue = repo.get_issue(issue_number)
            comments = issue.get_comments()
            
            comment_list = []
            for comment in comments:
                if len(comment_list) >= limit:
                    break
                
                comment_list.append({
                    "id": comment.id,
                    "body": comment.body,
                    "created_at": comment.created_at.isoformat(),
                    "updated_at": comment.updated_at.isoformat(),
                    "user": {
                        "login": comment.user.login,
                        "avatar_url": comment.user.avatar_url
                    },
                    "url": comment.html_url
                })
            
            return {
                "repository": repository,
                "issue_number": issue_number,
                "total_comments": len(comment_list),
                "comments": comment_list
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_issue_comments({repository}, {issue_number})")
    
    async def _analyze_issues(self, repository: str, days: int = 30) -> Dict[str, Any]:
        """
        Analyze issue patterns and trends.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get all issues in the date range
            issues = repo.get_issues(state="all")
            
            total_issues = 0
            open_issues = 0
            closed_issues = 0
            labels_usage = {}
            authors = {}
            daily_activity = {}
            
            for issue in issues:
                # Check if issue is in the date range
                if issue.created_at < start_date:
                    continue
                
                total_issues += 1
                
                if issue.state == "open":
                    open_issues += 1
                else:
                    closed_issues += 1
                
                # Track label usage
                for label in issue.labels:
                    labels_usage[label.name] = labels_usage.get(label.name, 0) + 1
                
                # Track author activity
                author = issue.user.login
                if author not in authors:
                    authors[author] = {
                        "issues_created": 0,
                        "issues_closed": 0
                    }
                authors[author]["issues_created"] += 1
                if issue.state == "closed":
                    authors[author]["issues_closed"] += 1
                
                # Track daily activity
                issue_date = issue.created_at.date().isoformat()
                if issue_date not in daily_activity:
                    daily_activity[issue_date] = {"created": 0, "closed": 0}
                daily_activity[issue_date]["created"] += 1
                
                if issue.closed_at and issue.closed_at >= start_date:
                    closed_date = issue.closed_at.date().isoformat()
                    if closed_date not in daily_activity:
                        daily_activity[closed_date] = {"created": 0, "closed": 0}
                    daily_activity[closed_date]["closed"] += 1
            
            # Sort authors by activity
            sorted_authors = sorted(authors.items(), key=lambda x: x[1]["issues_created"], reverse=True)
            
            # Sort labels by usage
            sorted_labels = sorted(labels_usage.items(), key=lambda x: x[1], reverse=True)
            
            return {
                "repository": repository,
                "period_days": days,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_issues": total_issues,
                "open_issues": open_issues,
                "closed_issues": closed_issues,
                "closure_rate": closed_issues / total_issues if total_issues > 0 else 0,
                "unique_authors": len(authors),
                "top_authors": sorted_authors[:5],
                "top_labels": sorted_labels[:10],
                "daily_activity": daily_activity,
                "average_issues_per_day": total_issues / days if days > 0 else 0
            }
            
        except Exception as e:
            return await self.handle_error(e, f"analyze_issues({repository}, {days})")
    
    async def _get_pull_requests(self, repository: str, state: str = "open",
                                base: Optional[str] = None, head: Optional[str] = None,
                                limit: int = 10) -> Dict[str, Any]:
        """
        Get pull requests with details.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Build filter parameters
            filters = {"state": state}
            if base:
                filters["base"] = base
            if head:
                filters["head"] = head
            
            pull_requests = repo.get_pulls(**filters)
            
            pr_list = []
            for pr in pull_requests:
                if len(pr_list) >= limit:
                    break
                
                pr_data = {
                    "number": pr.number,
                    "title": pr.title,
                    "body": pr.body,
                    "state": pr.state,
                    "created_at": pr.created_at.isoformat(),
                    "updated_at": pr.updated_at.isoformat(),
                    "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                    "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                    "user": {
                        "login": pr.user.login,
                        "avatar_url": pr.user.avatar_url
                    },
                    "base": {
                        "ref": pr.base.ref,
                        "sha": pr.base.sha
                    },
                    "head": {
                        "ref": pr.head.ref,
                        "sha": pr.head.sha
                    },
                    "labels": [label.name for label in pr.labels],
                    "assignees": [assignee.login for assignee in pr.assignees],
                    "comments": pr.comments,
                    "review_comments": pr.review_comments,
                    "commits": pr.commits,
                    "additions": pr.additions,
                    "deletions": pr.deletions,
                    "changed_files": pr.changed_files,
                    "url": pr.html_url,
                    "is_merged": pr.merged
                }
                
                pr_list.append(pr_data)
            
            return {
                "repository": repository,
                "state": state,
                "filters": filters,
                "total_pull_requests": len(pr_list),
                "pull_requests": pr_list
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_pull_requests({repository}, {state})") 