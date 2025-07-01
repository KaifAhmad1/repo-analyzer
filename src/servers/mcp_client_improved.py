"""
Unified MCP Client for FastMCP v2 Servers
Provides integration with all repository analysis MCP servers
"""

import asyncio
import subprocess
import json
import os
from typing import Dict, Any, Optional, List
from contextlib import asynccontextmanager
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters

class UnifiedMCPClient:
    """Unified client for all FastMCP v2 servers"""
    
    def __init__(self):
        self.servers = {
            "repository_analyzer": "src/servers/repository_analyzer_server.py",
            "file_content": "src/servers/file_content_server.py", 
            "repository_structure": "src/servers/repository_structure_server.py",
            "commit_history": "src/servers/commit_history_server.py",
            "issues": "src/servers/issues_server.py",
            "code_search": "src/servers/code_search_server.py"
        }
        self.processes = {}
        self.sessions = {}
    
    def __enter__(self):
        """Start all MCP servers and create sessions"""
        self._start_all_servers()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up all servers and sessions"""
        self._stop_all_servers()
    
    def _start_all_servers(self):
        """Start all MCP server processes"""
        for server_name, script_path in self.servers.items():
            if os.path.exists(script_path):
                try:
                    process = subprocess.Popen(
                        ["python", script_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        text=True
                    )
                    self.processes[server_name] = process
                    print(f"✅ Started {server_name} server")
                except Exception as e:
                    print(f"❌ Failed to start {server_name} server: {e}")
            else:
                print(f"⚠️ Server script not found: {script_path}")
        
        # Wait for servers to start
        import time
        time.sleep(3)
    
    def _stop_all_servers(self):
        """Stop all MCP server processes"""
        for server_name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Stopped {server_name} server")
            except:
                process.kill()
                print(f"⚠️ Force killed {server_name} server")
            finally:
                self.processes[server_name] = None
    
    def call_tool(self, server_name: str, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool from a specific server"""
        if server_name not in self.servers:
            return {"error": f"Unknown server: {server_name}", "success": False}
        
        script_path = self.servers[server_name]
        if not os.path.exists(script_path):
            return {"error": f"Server script not found: {script_path}", "success": False}
        
        try:
            server_params = StdioServerParameters(
                command="python",
                args=[script_path],
                env=os.environ.copy()
            )
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(self._call_tool_async(server_params, tool_name, parameters))
                return result
            finally:
                loop.close()
                
        except Exception as e:
            return {"error": f"Tool call failed: {str(e)}", "success": False}
    
    async def _call_tool_async(self, server_params: StdioServerParameters, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool asynchronously"""
        try:
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, parameters)
                    
                    if hasattr(result, 'content') and result.content:
                        return {
                            "result": result.content[0].text if result.content else "",
                            "success": True
                        }
                    else:
                        return {
                            "result": "No content returned",
                            "success": True
                        }
                        
        except Exception as e:
            return {"error": str(e), "success": False}
    
    # Repository Analyzer Server Tools
    def get_repository_overview(self, repo_url: str) -> Dict[str, Any]:
        """Get repository overview"""
        return self.call_tool("repository_analyzer", "get_repository_overview", {"repo_url": repo_url})
    
    def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """Perform comprehensive repository analysis"""
        return self.call_tool("repository_analyzer", "analyze_repository", {"repo_url": repo_url})
    
    def get_repository_activity(self, repo_url: str, days: int = 30) -> Dict[str, Any]:
        """Get repository activity analysis"""
        return self.call_tool("repository_analyzer", "get_repository_activity", {"repo_url": repo_url, "days": days})
    
    # File Content Server Tools
    def get_file_content(self, repo_url: str, file_path: str) -> Dict[str, Any]:
        """Get file content"""
        return self.call_tool("file_content", "get_file_content", {"repo_url": repo_url, "file_path": file_path})
    
    def list_directory(self, repo_url: str, directory_path: str = "") -> Dict[str, Any]:
        """List directory contents"""
        return self.call_tool("file_content", "list_directory", {"repo_url": repo_url, "directory_path": directory_path})
    
    # Repository Structure Server Tools
    def get_directory_tree(self, repo_url: str, max_depth: int = 3) -> Dict[str, Any]:
        """Get directory tree structure"""
        return self.call_tool("repository_structure", "get_directory_tree", {"repo_url": repo_url, "max_depth": max_depth})
    
    def get_file_structure(self, repo_url: str) -> Dict[str, Any]:
        """Get file structure analysis"""
        return self.call_tool("repository_structure", "get_file_structure", {"repo_url": repo_url})
    
    # Commit History Server Tools
    def get_recent_commits(self, repo_url: str, limit: int = 10) -> Dict[str, Any]:
        """Get recent commit history"""
        return self.call_tool("commit_history", "get_recent_commits", {"repo_url": repo_url, "limit": limit})
    
    def get_commit_statistics(self, repo_url: str, days: int = 30) -> Dict[str, Any]:
        """Get commit statistics"""
        return self.call_tool("commit_history", "get_commit_statistics", {"repo_url": repo_url, "days": days})
    
    def get_commit_details(self, repo_url: str, commit_sha: str) -> Dict[str, Any]:
        """Get detailed commit information"""
        return self.call_tool("commit_history", "get_commit_details", {"repo_url": repo_url, "commit_sha": commit_sha})
    
    # Issues Server Tools
    def get_issues(self, repo_url: str, state: str = "open", limit: int = 10) -> Dict[str, Any]:
        """Get repository issues"""
        return self.call_tool("issues", "get_issues", {"repo_url": repo_url, "state": state, "limit": limit})
    
    def get_pull_requests(self, repo_url: str, state: str = "open", limit: int = 10) -> Dict[str, Any]:
        """Get pull requests"""
        return self.call_tool("issues", "get_pull_requests", {"repo_url": repo_url, "state": state, "limit": limit})
    
    def get_issue_statistics(self, repo_url: str) -> Dict[str, Any]:
        """Get issue statistics"""
        return self.call_tool("issues", "get_issue_statistics", {"repo_url": repo_url})
    
    # Code Search Server Tools
    def search_code(self, repo_url: str, query: str, language: str = "") -> Dict[str, Any]:
        """Search for code patterns"""
        params = {"repo_url": repo_url, "query": query}
        if language:
            params["language"] = language
        return self.call_tool("code_search", "search_code", params)
    
    def search_files(self, repo_url: str, filename_pattern: str) -> Dict[str, Any]:
        """Search for files by pattern"""
        return self.call_tool("code_search", "search_files", {"repo_url": repo_url, "filename_pattern": filename_pattern})
    
    def get_code_metrics(self, repo_url: str) -> Dict[str, Any]:
        """Get code metrics and statistics"""
        return self.call_tool("code_search", "get_code_metrics", {"repo_url": repo_url})

class AsyncUnifiedMCPClient:
    """Asynchronous unified client for all FastMCP v2 servers"""
    
    def __init__(self):
        self.servers = {
            "repository_analyzer": "src/servers/repository_analyzer_server.py",
            "file_content": "src/servers/file_content_server.py", 
            "repository_structure": "src/servers/repository_structure_server.py",
            "commit_history": "src/servers/commit_history_server.py",
            "issues": "src/servers/issues_server.py",
            "code_search": "src/servers/code_search_server.py"
        }
    
    def get_server_params(self, server_name: str) -> StdioServerParameters:
        """Get server parameters for a specific server"""
        script_path = self.servers[server_name]
        return StdioServerParameters(
            command="python",
            args=[script_path],
            env=os.environ.copy()
        )
    
    @asynccontextmanager
    async def session(self, server_name: str):
        """Get an MCP session context manager for a specific server"""
        server_params = self.get_server_params(server_name)
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                yield session
    
    async def call_tool(self, server_name: str, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool asynchronously from a specific server"""
        try:
            async with self.session(server_name) as session:
                result = await session.call_tool(tool_name, parameters)
                
                if hasattr(result, 'content') and result.content:
                    return {
                        "result": result.content[0].text if result.content else "",
                        "success": True
                    }
                else:
                    return {
                        "result": "No content returned",
                        "success": True
                    }
                    
        except Exception as e:
            return {"error": str(e), "success": False}
    
    # Async versions of all tools
    async def get_repository_overview(self, repo_url: str) -> Dict[str, Any]:
        return await self.call_tool("repository_analyzer", "get_repository_overview", {"repo_url": repo_url})
    
    async def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        return await self.call_tool("repository_analyzer", "analyze_repository", {"repo_url": repo_url})
    
    async def get_file_content(self, repo_url: str, file_path: str) -> Dict[str, Any]:
        return await self.call_tool("file_content", "get_file_content", {"repo_url": repo_url, "file_path": file_path})
    
    async def get_directory_tree(self, repo_url: str, max_depth: int = 3) -> Dict[str, Any]:
        return await self.call_tool("repository_structure", "get_directory_tree", {"repo_url": repo_url, "max_depth": max_depth})
    
    async def get_recent_commits(self, repo_url: str, limit: int = 10) -> Dict[str, Any]:
        return await self.call_tool("commit_history", "get_recent_commits", {"repo_url": repo_url, "limit": limit})
    
    async def get_issues(self, repo_url: str, state: str = "open", limit: int = 10) -> Dict[str, Any]:
        return await self.call_tool("issues", "get_issues", {"repo_url": repo_url, "state": state, "limit": limit})
    
    async def search_code(self, repo_url: str, query: str, language: str = "") -> Dict[str, Any]:
        params = {"repo_url": repo_url, "query": query}
        if language:
            params["language"] = language
        return await self.call_tool("code_search", "search_code", params)

# Legacy compatibility - keep the old SyncMCPClient for backward compatibility
class SyncMCPClient(UnifiedMCPClient):
    """Legacy sync client for backward compatibility"""
    pass

# Convenience functions for direct usage
def get_repository_overview(repo_url: str) -> Dict[str, Any]:
    """Get repository overview using unified client"""
    with UnifiedMCPClient() as client:
        return client.get_repository_overview(repo_url)

def search_code(repo_url: str, query: str, language: str = "") -> Dict[str, Any]:
    """Search code using unified client"""
    with UnifiedMCPClient() as client:
        return client.search_code(repo_url, query, language)

def get_recent_commits(repo_url: str, limit: int = 10) -> Dict[str, Any]:
    """Get recent commits using unified client"""
    with UnifiedMCPClient() as client:
        return client.get_recent_commits(repo_url, limit)

def get_issues(repo_url: str, state: str = "open", limit: int = 10) -> Dict[str, Any]:
    """Get issues using unified client"""
    with UnifiedMCPClient() as client:
        return client.get_issues(repo_url, state, limit)

def analyze_repository(repo_url: str) -> Dict[str, Any]:
    """Analyze repository using unified client"""
    with UnifiedMCPClient() as client:
        return client.analyze_repository(repo_url)

# Example usage
if __name__ == "__main__":
    # Test the client
    repo_url = "https://github.com/microsoft/vscode"
    
    print("Testing MCP Client...")
    
    # Test repository overview
    result = get_repository_overview(repo_url)
    print(f"Repository Overview: {result}")
    
    # Test code search
    result = search_code(repo_url, "function main", "typescript")
    print(f"Code Search: {result}")
    
    # Test recent commits
    result = get_recent_commits(repo_url, 5)
    print(f"Recent Commits: {result}")
    
    # Test issues
    result = get_issues(repo_url, "open", 5)
    print(f"Issues: {result}")
    
    # Test analysis
    result = analyze_repository(repo_url)
    print(f"Analysis: {result}") 