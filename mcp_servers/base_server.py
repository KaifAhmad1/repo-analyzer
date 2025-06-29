"""
Base MCP Server Implementation

This module provides a base class for all MCP servers with common functionality
including error handling, rate limiting, and logging.
"""

import asyncio
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import time

from github import Github
from github.GithubException import GithubException

# TODO: Import MCP protocol libraries
# from mcp import Server, Tool, TextContent
# from mcp.server import ServerSession

class BaseMCPServer(ABC):
    """
    Base class for all MCP servers in the GitHub Repository Analyzer.
    
    Provides common functionality:
    - Error handling and logging
    - Rate limiting for GitHub API calls
    - Authentication management
    - Tool registration and management
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"mcp.{name}")
        
        # Initialize GitHub client
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        self.github_client = Github(github_token)
        
        # Rate limiting configuration
        self.rate_limit_remaining = 5000
        self.rate_limit_reset_time = None
        self.last_request_time = None
        
        # Initialize rate limits
        self._update_rate_limits()
        
        # TODO: Initialize MCP server
        # self.server = Server(name, description)
        
    @abstractmethod
    async def initialize_tools(self) -> List[Dict[str, Any]]:
        """
        Initialize and register tools for this MCP server.
        
        Returns:
            List of tool definitions
        """
        pass
    
    @abstractmethod
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Handle a tool call from the AI agent.
        
        Args:
            tool_name: Name of the tool being called
            arguments: Arguments passed to the tool
            
        Returns:
            Tool execution result
        """
        pass
    
    def _update_rate_limits(self):
        """Update rate limit information from GitHub API."""
        try:
            rate_limit = self.github_client.get_rate_limit()
            self.rate_limit_remaining = rate_limit.core.remaining
            self.rate_limit_reset_time = rate_limit.core.reset
            self.logger.debug(f"Rate limit: {self.rate_limit_remaining} remaining")
        except Exception as e:
            self.logger.warning(f"Could not update rate limits: {e}")
    
    async def check_rate_limit(self) -> bool:
        """
        Check if we can make a GitHub API request based on rate limits.
        
        Returns:
            True if request can be made, False otherwise
        """
        # Update rate limits
        self._update_rate_limits()
        
        # Check if we have remaining requests
        if self.rate_limit_remaining <= 0:
            if self.rate_limit_reset_time:
                reset_time = datetime.fromtimestamp(self.rate_limit_reset_time)
                wait_time = (reset_time - datetime.now()).total_seconds()
                if wait_time > 0:
                    self.logger.warning(f"Rate limit exceeded. Reset in {wait_time:.0f} seconds")
                    return False
        
        # Implement basic rate limiting (1 request per second)
        if self.last_request_time:
            time_since_last = time.time() - self.last_request_time
            if time_since_last < 1.0:
                await asyncio.sleep(1.0 - time_since_last)
        
        self.last_request_time = time.time()
        return True
    
    def _parse_repository(self, repository: str) -> tuple:
        """
        Parse repository string into owner and repo name.
        
        Args:
            repository: Repository string in format 'owner/repo'
            
        Returns:
            Tuple of (owner, repo_name)
        """
        if '/' not in repository:
            raise ValueError(f"Invalid repository format: {repository}. Expected 'owner/repo'")
        
        parts = repository.split('/', 1)
        return parts[0], parts[1]
    
    def _get_repository(self, repository: str):
        """
        Get GitHub repository object.
        
        Args:
            repository: Repository string in format 'owner/repo'
            
        Returns:
            GitHub repository object
        """
        owner, repo_name = self._parse_repository(repository)
        return self.github_client.get_repo(f"{owner}/{repo_name}")
    
    async def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Handle errors and return appropriate error response.
        
        Args:
            error: The exception that occurred
            context: Additional context about the error
            
        Returns:
            Error response dictionary
        """
        error_msg = str(error)
        self.logger.error(f"Error in {context}: {error_msg}")
        
        if isinstance(error, GithubException):
            if error.status == 404:
                return {
                    "error": "Repository or resource not found",
                    "details": error_msg,
                    "status_code": 404
                }
            elif error.status == 403:
                return {
                    "error": "Access denied or rate limit exceeded",
                    "details": error_msg,
                    "status_code": 403
                }
            elif error.status == 401:
                return {
                    "error": "Authentication failed",
                    "details": "Invalid or missing GitHub token",
                    "status_code": 401
                }
            else:
                return {
                    "error": "GitHub API error",
                    "details": error_msg,
                    "status_code": error.status
                }
        else:
            return {
                "error": "Internal server error",
                "details": error_msg,
                "status_code": 500
            }
    
    async def start_server(self, host: str = "localhost", port: int = 8000):
        """
        Start the MCP server.
        
        Args:
            host: Server host address
            port: Server port number
        """
        self.logger.info(f"Starting {self.name} server on {host}:{port}")
        
        # Initialize tools
        tools = await self.initialize_tools()
        self.logger.info(f"Initialized {len(tools)} tools")
        
        # TODO: Implement actual MCP server startup
        # For now, just log that the server is ready
        self.logger.info(f"{self.name} server is ready to handle requests")
    
    async def stop_server(self):
        """
        Stop the MCP server gracefully.
        """
        self.logger.info(f"Stopping {self.name} server")
        # TODO: Implement graceful shutdown
        self.logger.info(f"{self.name} server stopped") 