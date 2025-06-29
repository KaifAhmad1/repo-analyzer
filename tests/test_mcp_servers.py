"""
Tests for MCP Servers

This module contains tests for the MCP server implementations.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from typing import Dict, Any

from mcp_servers.file_content_server import FileContentServer
from mcp_servers.repository_structure_server import RepositoryStructureServer
from mcp_servers.commit_history_server import CommitHistoryServer
from mcp_servers.issues_server import IssuesServer
from mcp_servers.code_search_server import CodeSearchServer

class TestFileContentServer:
    """Test File Content Server functionality."""
    
    @pytest.fixture
    def server(self):
        """Create a FileContentServer instance."""
        return FileContentServer()
    
    @pytest.mark.asyncio
    async def test_server_initialization(self, server):
        """Test server initialization."""
        assert server.name == "file_content_server"
        assert "file content" in server.description.lower()
    
    @pytest.mark.asyncio
    async def test_get_file_content(self, server):
        """Test getting file content."""
        with patch('mcp_servers.base_server.Github') as mock_github:
            # Mock GitHub API response
            mock_repo = Mock()
            mock_content = Mock()
            mock_content.decoded_content = b"# Test File\nThis is test content"
            mock_content.path = "test.md"
            mock_content.name = "test.md"
            mock_content.size = 25
            mock_repo.get_contents.return_value = mock_content
            mock_github.return_value.get_repo.return_value = mock_repo
            
            # Test the function
            result = await server._get_file_content("test/repo", "test.md")
            
            assert result["content"] == "# Test File\nThis is test content"
            assert result["file_path"] == "test.md"
            assert result["file_size"] == 25

class TestRepositoryStructureServer:
    """Test Repository Structure Server functionality."""
    
    @pytest.fixture
    def server(self):
        """Create a RepositoryStructureServer instance."""
        return RepositoryStructureServer()
    
    @pytest.mark.asyncio
    async def test_server_initialization(self, server):
        """Test server initialization."""
        assert server.name == "repository_structure_server"
        assert "repository structure" in server.description.lower()
    
    @pytest.mark.asyncio
    async def test_get_repository_tree(self, server):
        """Test getting repository tree."""
        with patch('mcp_servers.base_server.Github') as mock_github:
            # Mock GitHub API response
            mock_repo = Mock()
            mock_tree = Mock()
            mock_tree.tree = [
                Mock(path="file1.py", type="blob", size=100),
                Mock(path="dir1/file2.py", type="blob", size=200),
                Mock(path="dir1", type="tree", size=0)
            ]
            mock_repo.get_git_tree.return_value = mock_tree
            mock_github.return_value.get_repo.return_value = mock_repo
            
            # Test the function
            result = await server._get_repository_tree("test/repo")
            
            assert "tree" in result
            assert len(result["tree"]) == 3

class TestCommitHistoryServer:
    """Test Commit History Server functionality."""
    
    @pytest.fixture
    def server(self):
        """Create a CommitHistoryServer instance."""
        return CommitHistoryServer()
    
    @pytest.mark.asyncio
    async def test_server_initialization(self, server):
        """Test server initialization."""
        assert server.name == "commit_history_server"
        assert "commit history" in server.description.lower()
    
    @pytest.mark.asyncio
    async def test_get_recent_commits(self, server):
        """Test getting recent commits."""
        with patch('mcp_servers.base_server.Github') as mock_github:
            # Mock GitHub API response
            mock_repo = Mock()
            mock_commit = Mock()
            mock_commit.sha = "abc123"
            mock_commit.commit.message = "Test commit"
            mock_commit.commit.author.name = "Test Author"
            mock_commit.commit.author.date = "2023-01-01T00:00:00Z"
            mock_repo.get_commits.return_value = [mock_commit]
            mock_github.return_value.get_repo.return_value = mock_repo
            
            # Test the function
            result = await server._get_recent_commits("test/repo", limit=5)
            
            assert "commits" in result
            assert len(result["commits"]) == 1
            assert result["commits"][0]["sha"] == "abc123"

class TestIssuesServer:
    """Test Issues Server functionality."""
    
    @pytest.fixture
    def server(self):
        """Create an IssuesServer instance."""
        return IssuesServer()
    
    @pytest.mark.asyncio
    async def test_server_initialization(self, server):
        """Test server initialization."""
        assert server.name == "issues_server"
        assert "issues" in server.description.lower()
    
    @pytest.mark.asyncio
    async def test_get_issues(self, server):
        """Test getting issues."""
        with patch('mcp_servers.base_server.Github') as mock_github:
            # Mock GitHub API response
            mock_repo = Mock()
            mock_issue = Mock()
            mock_issue.number = 1
            mock_issue.title = "Test Issue"
            mock_issue.state = "open"
            mock_issue.user.login = "testuser"
            mock_issue.created_at = "2023-01-01T00:00:00Z"
            mock_repo.get_issues.return_value = [mock_issue]
            mock_github.return_value.get_repo.return_value = mock_repo
            
            # Test the function
            result = await server._get_issues("test/repo", state="open", limit=10)
            
            assert "issues" in result
            assert len(result["issues"]) == 1
            assert result["issues"][0]["number"] == 1

class TestCodeSearchServer:
    """Test Code Search Server functionality."""
    
    @pytest.fixture
    def server(self):
        """Create a CodeSearchServer instance."""
        return CodeSearchServer()
    
    @pytest.mark.asyncio
    async def test_server_initialization(self, server):
        """Test server initialization."""
        assert server.name == "code_search_server"
        assert "code search" in server.description.lower()
    
    @pytest.mark.asyncio
    async def test_search_code(self, server):
        """Test searching code."""
        with patch('mcp_servers.base_server.Github') as mock_github:
            # Mock GitHub API response
            mock_repo = Mock()
            mock_result = Mock()
            mock_result.path = "test.py"
            mock_result.name = "test.py"
            mock_result.html_url = "https://github.com/test/repo/blob/main/test.py"
            mock_result.decoded_content = b"def test_function():\n    pass"
            mock_repo.search_code.return_value = [mock_result]
            mock_github.return_value.get_repo.return_value = mock_repo
            
            # Test the function
            result = await server._search_code("test/repo", "test_function")
            
            assert "matches" in result
            assert len(result["matches"]) == 1
            assert result["matches"][0]["file_path"] == "test.py"

class TestBaseServer:
    """Test Base Server functionality."""
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test rate limiting functionality."""
        from mcp_servers.base_server import BaseMCPServer
        
        server = BaseMCPServer("test_server", "Test server")
        
        # Test rate limit check
        result = await server.check_rate_limit()
        assert isinstance(result, bool)

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__]) 