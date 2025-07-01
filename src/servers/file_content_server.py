"""
File Content Server using FastMCP v2
Simple and effective file content retrieval from GitHub repositories
"""

import base64
import requests
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP, Context

# Create FastMCP server instance
mcp = FastMCP("File Content Server 📁")

def parse_repo_url(repo_url: str) -> tuple[str, str]:
    """Parse GitHub repository URL to get owner and repo name"""
    if "github.com" in repo_url:
        parts = repo_url.replace("https://github.com/", "").split("/")
        owner = parts[0]
        repo = parts[1].replace(".git", "")
        return owner, repo
    else:
        raise ValueError("Invalid GitHub URL")

def make_github_request(endpoint: str) -> Dict[str, Any]:
    """Make a GitHub API request with proper headers"""
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(f"https://api.github.com{endpoint}", headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool
async def get_file_content(repo_url: str, file_path: str, ctx: Context) -> Dict[str, Any]:
    """Get content of a specific file in a GitHub repository"""
    try:
        await ctx.info(f"Fetching file: {file_path} from {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        api_url = f"/repos/{owner}/{repo}/contents/{file_path}"
        file_data = make_github_request(api_url)
        
        # Handle different content encodings
        encoding = file_data.get("encoding", "")
        if encoding == "base64":
            content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
        else:
            content = file_data["content"]
        
        result = {
            "content": content,
            "encoding": encoding,
            "size": file_data.get("size", 0),
            "path": file_path,
            "sha": file_data.get("sha", ""),
            "url": file_data.get("html_url", ""),
            "success": True
        }
        
        await ctx.info(f"Successfully retrieved {file_path} ({len(content)} characters)")
        return result
        
    except Exception as e:
        await ctx.error(f"Error fetching file {file_path}: {str(e)}")
        return {
            "error": str(e),
            "path": file_path,
            "success": False
        }

@mcp.tool
async def list_directory(repo_url: str, path: str = "", ctx: Context = None) -> Dict[str, Any]:
    """List contents of a directory in a GitHub repository"""
    try:
        if ctx:
            await ctx.info(f"Listing directory: {path or 'root'} from {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        api_url = f"/repos/{owner}/{repo}/contents/{path}"
        contents = make_github_request(api_url)
        
        files = []
        directories = []
        
        for item in contents:
            if item["type"] == "file":
                files.append({
                    "name": item["name"],
                    "path": item["path"],
                    "size": item["size"],
                    "type": "file",
                    "url": item.get("html_url", "")
                })
            elif item["type"] == "dir":
                directories.append({
                    "name": item["name"],
                    "path": item["path"],
                    "type": "directory",
                    "url": item.get("html_url", "")
                })
        
        result = {
            "path": path or "root",
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories),
            "success": True
        }
        
        if ctx:
            await ctx.info(f"Found {len(files)} files and {len(directories)} directories")
        
        return result
        
    except Exception as e:
        error_msg = f"Error listing directory {path}: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        return {
            "error": str(e),
            "path": path,
            "success": False
        }

@mcp.tool
async def get_readme_content(repo_url: str, ctx: Context) -> Dict[str, Any]:
    """Get README content from a GitHub repository"""
    try:
        await ctx.info(f"Fetching README from {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        # Try different README file names
        readme_files = ["README.md", "README.txt", "README.rst", "readme.md"]
        
        for readme_file in readme_files:
            try:
                api_url = f"/repos/{owner}/{repo}/contents/{readme_file}"
                file_data = make_github_request(api_url)
                
                encoding = file_data.get("encoding", "")
                if encoding == "base64":
                    content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
                else:
                    content = file_data["content"]
                
                result = {
                    "content": content,
                    "filename": readme_file,
                    "size": file_data.get("size", 0),
                    "url": file_data.get("html_url", ""),
                    "success": True
                }
                
                await ctx.info(f"Found README: {readme_file}")
                return result
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    continue  # Try next README file
                else:
                    raise
        
        # No README found
        await ctx.info("No README file found")
        return {
            "error": "No README file found",
            "success": False
        }
        
    except Exception as e:
        await ctx.error(f"Error fetching README: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

@mcp.tool
async def get_file_info(repo_url: str, file_path: str, ctx: Context) -> Dict[str, Any]:
    """Get detailed information about a file without downloading content"""
    try:
        await ctx.info(f"Getting file info: {file_path}")
        
        owner, repo = parse_repo_url(repo_url)
        api_url = f"/repos/{owner}/{repo}/contents/{file_path}"
        file_data = make_github_request(api_url)
        
        result = {
            "name": file_data["name"],
            "path": file_data["path"],
            "size": file_data.get("size", 0),
            "type": file_data["type"],
            "sha": file_data.get("sha", ""),
            "url": file_data.get("html_url", ""),
            "download_url": file_data.get("download_url", ""),
            "encoding": file_data.get("encoding", ""),
            "success": True
        }
        
        await ctx.info(f"File info retrieved: {file_path} ({file_data.get('size', 0)} bytes)")
        return result
        
    except Exception as e:
        await ctx.error(f"Error getting file info: {str(e)}")
        return {
            "error": str(e),
            "path": file_path,
            "success": False
        }

# Resources for static data access
@mcp.resource("file://{owner}/{repo}/{path}")
def get_file_resource(owner: str, repo: str, path: str) -> Dict[str, Any]:
    """Resource endpoint for file content"""
    try:
        api_url = f"/repos/{owner}/{repo}/contents/{path}"
        file_data = make_github_request(api_url)
        
        encoding = file_data.get("encoding", "")
        if encoding == "base64":
            content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
        else:
            content = file_data["content"]
        
        return {
            "content": content,
            "path": path,
            "size": file_data.get("size", 0)
        }
    except Exception as e:
        return {"error": str(e), "path": path}

@mcp.resource("directory://{owner}/{repo}/{path}")
def get_directory_resource(owner: str, repo: str, path: str) -> Dict[str, Any]:
    """Resource endpoint for directory listing"""
    try:
        api_url = f"/repos/{owner}/{repo}/contents/{path}"
        contents = make_github_request(api_url)
        
        files = [item for item in contents if item["type"] == "file"]
        directories = [item for item in contents if item["type"] == "dir"]
        
        return {
            "path": path,
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories)
        }
    except Exception as e:
        return {"error": str(e), "path": path}

# Prompts for common file operations
@mcp.prompt
def file_analysis_prompt(file_path: str, content: str) -> str:
    """Generate a prompt for analyzing file content"""
    return f"""Analyze the following file: {file_path}

Content:
{content[:2000]}{'...' if len(content) > 2000 else ''}

Please provide:
1. File type and purpose
2. Key components or functions
3. Dependencies or imports
4. Any notable patterns or issues"""

@mcp.prompt
def readme_analysis_prompt(content: str) -> str:
    """Generate a prompt for analyzing README content"""
    return f"""Analyze this README file:

{content[:3000]}{'...' if len(content) > 3000 else ''}

Please provide:
1. Project overview and purpose
2. Installation instructions
3. Usage examples
4. Key features
5. Dependencies or requirements"""

if __name__ == "__main__":
    mcp.run() 