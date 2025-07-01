"""
File Content Server using FastMCP v2
Provides file content and directory listing from GitHub repositories
"""

import os
import base64
import requests
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP, Context

mcp = FastMCP("File Content Server 🚀")

def get_github_token() -> Optional[str]:
    import streamlit as st
    return st.session_state.get("github_token", os.getenv("GITHUB_TOKEN"))

def parse_repo_url(repo_url: str) -> tuple[str, str]:
    if "github.com" in repo_url:
        parts = repo_url.replace("https://github.com/", "").split("/")
        owner = parts[0]
        repo = parts[1].replace(".git", "")
        return owner, repo
    else:
        raise ValueError("Invalid GitHub URL")

def make_github_request(endpoint: str) -> Dict[str, Any]:
    token = get_github_token()
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    response = requests.get(f"https://api.github.com{endpoint}", headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool
async def get_file_content(repo_url: str, file_path: str, ctx: Context) -> Dict[str, Any]:
    """Get content of a specific file in a GitHub repository"""
    try:
        await ctx.info(f"Fetching file: {file_path}")
        owner, repo = parse_repo_url(repo_url)
        api_url = f"/repos/{owner}/{repo}/contents/{file_path}"
        file_data = make_github_request(api_url)
        encoding = file_data.get("encoding", "")
        if encoding == "base64":
            content = base64.b64decode(file_data["content"]).decode("utf-8")
        else:
            content = file_data["content"]
        return {
            "content": content,
            "encoding": encoding,
            "size": file_data.get("size", 0),
            "path": file_path
        }
    except Exception as e:
        await ctx.error(f"Error fetching file: {str(e)}")
        return {"error": str(e), "path": file_path}

@mcp.tool
async def list_directory(repo_url: str, path: str = "", ctx: Context = None) -> Dict[str, Any]:
    """List contents of a directory in a GitHub repository"""
    try:
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
                    "type": "file"
                })
            elif item["type"] == "dir":
                directories.append({
                    "name": item["name"],
                    "path": item["path"],
                    "type": "directory"
                })
        return {
            "path": path,
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories)
        }
    except Exception as e:
        if ctx:
            await ctx.error(f"Error listing directory: {str(e)}")
        return {"error": str(e), "path": path}

if __name__ == "__main__":
    mcp.run() 