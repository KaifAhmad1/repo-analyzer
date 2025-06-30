"""
Improved MCP Client using Official Anthropic MCP SDK
Provides better integration with the repository analyzer MCP server
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

class SyncMCPClient:
    """Synchronous wrapper for MCP client operations"""
    
    def __init__(self, server_script: str = "src/servers/repository_analyzer_server.py"):
        self.server_script = server_script
        self.process = None
        self.session = None
    
    def __enter__(self):
        """Start the MCP server and create session"""
        self._start_server()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up server and session"""
        self._stop_server()
    
    def _start_server(self):
        """Start the MCP server process"""
        try:
            # Start the server process
            self.process = subprocess.Popen(
                ["python", self.server_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True
            )
            
            # Wait a moment for server to start
            import time
            time.sleep(2)
            
        except Exception as e:
            raise RuntimeError(f"Failed to start MCP server: {e}")
    
    def _stop_server(self):
        """Stop the MCP server process"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            finally:
                self.process = None
    
    def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool synchronously"""
        try:
            # Create server parameters
            server_params = StdioServerParameters(
                command="python",
                args=[self.server_script],
                env=os.environ.copy()
            )
            
            # Run async operation in sync context
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
                    # Initialize the session
                    await session.initialize()
                    
                    # Call the tool
                    result = await session.call_tool(tool_name, parameters)
                    
                    # Return structured result
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
    
    def get_repository_overview(self, repo_url: str) -> Dict[str, Any]:
        """Get repository overview"""
        return self.call_tool("get_repository_overview", {"repo_url": repo_url})
    
    def search_code(self, repo_url: str, query: str, language: str = "") -> Dict[str, Any]:
        """Search for code patterns"""
        params = {"repo_url": repo_url, "query": query}
        if language:
            params["language"] = language
        return self.call_tool("search_code", params)
    
    def get_recent_commits(self, repo_url: str, limit: int = 10) -> Dict[str, Any]:
        """Get recent commit history"""
        return self.call_tool("get_recent_commits", {"repo_url": repo_url, "limit": limit})
    
    def get_issues(self, repo_url: str, state: str = "open", limit: int = 10) -> Dict[str, Any]:
        """Get repository issues"""
        return self.call_tool("get_issues", {"repo_url": repo_url, "state": state, "limit": limit})
    
    def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """Perform comprehensive repository analysis"""
        return self.call_tool("analyze_repository", {"repo_url": repo_url})

class AsyncMCPClient:
    """Asynchronous MCP client for advanced usage"""
    
    def __init__(self, server_script: str = "src/servers/repository_analyzer_server.py"):
        self.server_script = server_script
        self.server_params = StdioServerParameters(
            command="python",
            args=[server_script],
            env=os.environ.copy()
        )
    
    @asynccontextmanager
    async def session(self):
        """Get an MCP session context manager"""
        async with stdio_client(self.server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                yield session
    
    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool asynchronously"""
        try:
            async with self.session() as session:
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
    
    async def get_repository_overview(self, repo_url: str) -> Dict[str, Any]:
        """Get repository overview"""
        return await self.call_tool("get_repository_overview", {"repo_url": repo_url})
    
    async def search_code(self, repo_url: str, query: str, language: str = "") -> Dict[str, Any]:
        """Search for code patterns"""
        params = {"repo_url": repo_url, "query": query}
        if language:
            params["language"] = language
        return await self.call_tool("search_code", params)
    
    async def get_recent_commits(self, repo_url: str, limit: int = 10) -> Dict[str, Any]:
        """Get recent commit history"""
        return await self.call_tool("get_recent_commits", {"repo_url": repo_url, "limit": limit})
    
    async def get_issues(self, repo_url: str, state: str = "open", limit: int = 10) -> Dict[str, Any]:
        """Get repository issues"""
        return await self.call_tool("get_issues", {"repo_url": repo_url, "state": state, "limit": limit})
    
    async def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """Perform comprehensive repository analysis"""
        return await self.call_tool("analyze_repository", {"repo_url": repo_url})

# Convenience functions for direct usage
def get_repository_overview(repo_url: str) -> Dict[str, Any]:
    """Get repository overview using sync client"""
    with SyncMCPClient() as client:
        return client.get_repository_overview(repo_url)

def search_code(repo_url: str, query: str, language: str = "") -> Dict[str, Any]:
    """Search for code patterns using sync client"""
    with SyncMCPClient() as client:
        return client.search_code(repo_url, query, language)

def get_recent_commits(repo_url: str, limit: int = 10) -> Dict[str, Any]:
    """Get recent commit history using sync client"""
    with SyncMCPClient() as client:
        return client.get_recent_commits(repo_url, limit)

def get_issues(repo_url: str, state: str = "open", limit: int = 10) -> Dict[str, Any]:
    """Get repository issues using sync client"""
    with SyncMCPClient() as client:
        return client.get_issues(repo_url, state, limit)

def analyze_repository(repo_url: str) -> Dict[str, Any]:
    """Perform comprehensive repository analysis using sync client"""
    with SyncMCPClient() as client:
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