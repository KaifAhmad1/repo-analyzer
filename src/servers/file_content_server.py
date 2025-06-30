"""
Simplified File Content MCP Server
Provides file content and metadata from GitHub repositories
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import base64
import os
from typing import Dict, Any, Optional

app = FastAPI(title="File Content MCP Server")

class FileRequest(BaseModel):
    parameters: Dict[str, Any]

class FileResponse(BaseModel):
    content: str
    encoding: str
    size: int
    path: str
    error: Optional[str] = None

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "file_content_server"}

@app.post("/file-content")
def get_file_content(request: FileRequest):
    """Get content of a specific file"""
    try:
        file_path = request.parameters.get("file_path")
        if not file_path:
            raise HTTPException(status_code=400, detail="file_path is required")
        
        # Get GitHub token from environment
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise HTTPException(status_code=500, detail="GitHub token not configured")
        
        # Get repository URL from environment or request
        repo_url = os.getenv("GITHUB_REPO_URL")
        if not repo_url:
            raise HTTPException(status_code=500, detail="Repository URL not configured")
        
        # Parse repository URL
        if "github.com" in repo_url:
            parts = repo_url.replace("https://github.com/", "").split("/")
            owner = parts[0]
            repo = parts[1].replace(".git", "")
        else:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")
        
        # GitHub API endpoint
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
        
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 404:
            return FileResponse(
                content="",
                encoding="",
                size=0,
                path=file_path,
                error="File not found"
            )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="GitHub API error")
        
        file_data = response.json()
        
        # Decode content if it's base64 encoded
        content = ""
        encoding = file_data.get("encoding", "")
        
        if encoding == "base64":
            content = base64.b64decode(file_data["content"]).decode("utf-8")
        else:
            content = file_data["content"]
        
        return FileResponse(
            content=content,
            encoding=encoding,
            size=file_data.get("size", 0),
            path=file_path
        )
    
    except Exception as e:
        return FileResponse(
            content="",
            encoding="",
            size=0,
            path=file_path if 'file_path' in locals() else "",
            error=str(e)
        )

@app.post("/list-directory")
def list_directory(request: FileRequest):
    """List contents of a directory"""
    try:
        path = request.parameters.get("path", "")
        
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise HTTPException(status_code=500, detail="GitHub token not configured")
        
        repo_url = os.getenv("GITHUB_REPO_URL")
        if not repo_url:
            raise HTTPException(status_code=500, detail="Repository URL not configured")
        
        # Parse repository URL
        if "github.com" in repo_url:
            parts = repo_url.replace("https://github.com/", "").split("/")
            owner = parts[0]
            repo = parts[1].replace(".git", "")
        else:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")
        
        # GitHub API endpoint
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 404:
            return {"error": "Directory not found"}
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="GitHub API error")
        
        contents = response.json()
        
        # Format directory listing
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
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 