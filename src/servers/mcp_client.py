"""
Simplified MCP Client for communicating with MCP servers
"""

import requests
import json
from typing import Dict, Any, Optional

class MCPClient:
    """Simple MCP client for tool calling"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"  # Default MCP server URL
        self.session = requests.Session()
    
    def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific MCP tool"""
        try:
            # Map tool names to server endpoints
            tool_mapping = {
                "get_file_content": "/file-content",
                "get_repository_structure": "/repository-structure", 
                "get_commit_history": "/commit-history",
                "search_code": "/code-search",
                "get_issues": "/issues"
            }
            
            if tool_name not in tool_mapping:
                return {"error": f"Unknown tool: {tool_name}"}
            
            endpoint = tool_mapping[tool_name]
            url = f"{self.base_url}{endpoint}"
            
            # Make request to MCP server
            response = self.session.post(
                url,
                json={"parameters": parameters},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Server error: {response.status_code}"}
        
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_file_content(self, file_path: str) -> Dict[str, Any]:
        """Get content of a specific file"""
        return self.call_tool("get_file_content", {"file_path": file_path})
    
    def get_repository_structure(self, path: str = "") -> Dict[str, Any]:
        """Get repository directory structure"""
        return self.call_tool("get_repository_structure", {"path": path})
    
    def get_commit_history(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent commit history"""
        return self.call_tool("get_commit_history", {"limit": limit})
    
    def search_code(self, query: str, file_type: str = "") -> Dict[str, Any]:
        """Search for code patterns"""
        params = {"query": query}
        if file_type:
            params["file_type"] = file_type
        return self.call_tool("search_code", params)
    
    def get_issues(self, state: str = "open", limit: int = 10) -> Dict[str, Any]:
        """Get repository issues"""
        return self.call_tool("get_issues", {"state": state, "limit": limit}) 