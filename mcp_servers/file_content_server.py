"""
File Content MCP Server

This server provides tools for retrieving and reading file contents from GitHub repositories.
Supports various file types, encoding detection, and content filtering.
"""

import base64
import mimetypes
import re
from typing import Dict, List, Optional, Any
from pathlib import Path

from .base_server import BaseMCPServer

class FileContentServer(BaseMCPServer):
    """
    MCP Server for file content operations.
    
    Tools provided:
    - get_file_content: Retrieve raw file content
    - get_file_metadata: Get file information (size, type, etc.)
    - search_file_content: Search within file content
    - get_file_history: Get file change history
    - list_directory_files: List files in a directory
    """
    
    def __init__(self):
        super().__init__(
            name="file_content_server",
            description="Server for retrieving and analyzing file contents from GitHub repositories"
        )
        
    async def initialize_tools(self) -> List[Dict[str, Any]]:
        """
        Initialize tools for file content operations.
        """
        tools = [
            {
                "name": "get_file_content",
                "description": "Retrieve the content of a specific file from a GitHub repository",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "file_path": "string (required): Path to the file within the repository",
                    "branch": "string (optional): Branch name, defaults to 'main'",
                    "encoding": "string (optional): File encoding, auto-detected if not specified"
                }
            },
            {
                "name": "get_file_metadata",
                "description": "Get metadata about a file (size, type, last modified, etc.)",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "file_path": "string (required): Path to the file within the repository",
                    "branch": "string (optional): Branch name, defaults to 'main'"
                }
            },
            {
                "name": "search_file_content",
                "description": "Search for specific text patterns within file content",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "file_path": "string (required): Path to the file within the repository",
                    "search_pattern": "string (required): Text pattern to search for",
                    "case_sensitive": "boolean (optional): Case sensitive search, defaults to false",
                    "regex": "boolean (optional): Use regex pattern, defaults to false"
                }
            },
            {
                "name": "get_file_history",
                "description": "Get the commit history for a specific file",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "file_path": "string (required): Path to the file within the repository",
                    "limit": "integer (optional): Number of commits to return, defaults to 10"
                }
            },
            {
                "name": "list_directory_files",
                "description": "List all files in a directory with their metadata",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "directory_path": "string (required): Path to the directory within the repository",
                    "branch": "string (optional): Branch name, defaults to 'main'",
                    "recursive": "boolean (optional): Include subdirectories, defaults to false"
                }
            }
        ]
        return tools
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Handle file content tool calls.
        """
        try:
            if tool_name == "get_file_content":
                return await self._get_file_content(**arguments)
            elif tool_name == "get_file_metadata":
                return await self._get_file_metadata(**arguments)
            elif tool_name == "search_file_content":
                return await self._search_file_content(**arguments)
            elif tool_name == "get_file_history":
                return await self._get_file_history(**arguments)
            elif tool_name == "list_directory_files":
                return await self._list_directory_files(**arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        except Exception as e:
            return await self.handle_error(e, f"Tool call failed: {tool_name}")
    
    async def _get_file_content(self, repository: str, file_path: str, 
                               branch: str = "main", encoding: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve file content from GitHub repository.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            contents = repo.get_contents(file_path, ref=branch)
            
            if contents.type != "file":
                return {"error": f"Path {file_path} is not a file"}
            
            # Get file content
            content = contents.decoded_content
            
            # Detect file type and encoding
            file_info = self._detect_file_type(file_path, content)
            
            # Decode content if it's text
            if file_info["type"] == "text":
                if encoding:
                    text_content = content.decode(encoding)
                else:
                    text_content = content.decode(file_info["encoding"])
            else:
                text_content = None
            
            return {
                "file_path": file_path,
                "repository": repository,
                "branch": branch,
                "content": text_content,
                "binary_content": base64.b64encode(content).decode() if file_info["type"] == "binary" else None,
                "file_info": file_info,
                "size": len(content),
                "sha": contents.sha,
                "url": contents.url
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_file_content({repository}, {file_path})")
    
    async def _get_file_metadata(self, repository: str, file_path: str, 
                                branch: str = "main") -> Dict[str, Any]:
        """
        Get file metadata information.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            contents = repo.get_contents(file_path, ref=branch)
            
            return {
                "file_path": file_path,
                "repository": repository,
                "branch": branch,
                "name": contents.name,
                "path": contents.path,
                "sha": contents.sha,
                "size": contents.size,
                "type": contents.type,
                "url": contents.url,
                "html_url": contents.html_url,
                "git_url": contents.git_url,
                "download_url": contents.download_url,
                "encoding": contents.encoding
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_file_metadata({repository}, {file_path})")
    
    async def _search_file_content(self, repository: str, file_path: str, 
                                  search_pattern: str, case_sensitive: bool = False,
                                  regex: bool = False) -> Dict[str, Any]:
        """
        Search for patterns within file content.
        """
        # First get the file content
        content_result = await self._get_file_content(repository, file_path)
        
        if "error" in content_result:
            return content_result
        
        content = content_result["content"]
        if not content:
            return {"error": "Cannot search in binary files"}
        
        try:
            matches = []
            lines = content.split('\n')
            
            if regex:
                pattern = re.compile(search_pattern, flags=0 if case_sensitive else re.IGNORECASE)
            else:
                if case_sensitive:
                    pattern = search_pattern
                else:
                    pattern = search_pattern.lower()
                    lines = [line.lower() for line in lines]
            
            for line_num, line in enumerate(lines, 1):
                if regex:
                    if pattern.search(line):
                        matches.append({
                            "line_number": line_num,
                            "line_content": line,
                            "match": pattern.search(line).group()
                        })
                else:
                    if pattern in line:
                        start_pos = line.find(pattern)
                        matches.append({
                            "line_number": line_num,
                            "line_content": line,
                            "match_start": start_pos,
                            "match_end": start_pos + len(pattern)
                        })
            
            return {
                "file_path": file_path,
                "repository": repository,
                "search_pattern": search_pattern,
                "case_sensitive": case_sensitive,
                "regex": regex,
                "total_matches": len(matches),
                "matches": matches
            }
            
        except Exception as e:
            return await self.handle_error(e, f"search_file_content({repository}, {file_path})")
    
    async def _get_file_history(self, repository: str, file_path: str, 
                               limit: int = 10) -> Dict[str, Any]:
        """
        Get file commit history.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            commits = repo.get_commits(path=file_path, per_page=limit)
            
            history = []
            for commit in commits:
                history.append({
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
                    "url": commit.html_url
                })
            
            return {
                "file_path": file_path,
                "repository": repository,
                "total_commits": len(history),
                "commits": history
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_file_history({repository}, {file_path})")
    
    async def _list_directory_files(self, repository: str, directory_path: str,
                                   branch: str = "main", recursive: bool = False) -> Dict[str, Any]:
        """
        List files in a directory.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            contents = repo.get_contents(directory_path, ref=branch)
            
            files = []
            directories = []
            
            for item in contents:
                if item.type == "file":
                    files.append({
                        "name": item.name,
                        "path": item.path,
                        "size": item.size,
                        "sha": item.sha,
                        "url": item.url,
                        "html_url": item.html_url,
                        "download_url": item.download_url
                    })
                elif item.type == "dir":
                    directories.append({
                        "name": item.name,
                        "path": item.path,
                        "sha": item.sha,
                        "url": item.url,
                        "html_url": item.html_url
                    })
            
            result = {
                "directory_path": directory_path,
                "repository": repository,
                "branch": branch,
                "files": files,
                "directories": directories,
                "total_files": len(files),
                "total_directories": len(directories)
            }
            
            # If recursive is True, also get contents of subdirectories
            if recursive and directories:
                for directory in directories:
                    sub_result = await self._list_directory_files(
                        repository, directory["path"], branch, recursive=True
                    )
                    if "error" not in sub_result:
                        directory["contents"] = sub_result
            
            return result
            
        except Exception as e:
            return await self.handle_error(e, f"list_directory_files({repository}, {directory_path})")
    
    def _detect_file_type(self, file_path: str, content: bytes) -> Dict[str, str]:
        """
        Detect file type and encoding.
        """
        # Get MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # Check if it's binary
        is_binary = self._is_binary_file(content)
        
        if is_binary:
            return {
                "type": "binary",
                "mime_type": mime_type or "application/octet-stream",
                "encoding": "binary"
            }
        else:
            # Try to detect text encoding
            try:
                content.decode('utf-8')
                encoding = 'utf-8'
            except UnicodeDecodeError:
                try:
                    content.decode('latin-1')
                    encoding = 'latin-1'
                except UnicodeDecodeError:
                    encoding = 'unknown'
            
            return {
                "type": "text",
                "mime_type": mime_type or "text/plain",
                "encoding": encoding
            }
    
    def _is_binary_file(self, content: bytes) -> bool:
        """
        Check if file content is binary.
        """
        # Check for null bytes (common in binary files)
        if b'\x00' in content:
            return True
        
        # Check if more than 30% of bytes are non-printable
        non_printable = sum(1 for byte in content if byte < 32 and byte not in [9, 10, 13])
        if len(content) > 0 and non_printable / len(content) > 0.3:
            return True
        
        return False 