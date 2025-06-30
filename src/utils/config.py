"""
Configuration management for the GitHub Repository Analyzer
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables"""
    
    config = {
        # Google Gemini API Configuration
        "google_api_key": os.getenv("GOOGLE_API_KEY", ""),
        "gemini_model": os.getenv("GEMINI_MODEL", "gemini-2.0-flash-001"),
        
        # GitHub Configuration
        "github_token": os.getenv("GITHUB_TOKEN", ""),
        "github_api_url": os.getenv("GITHUB_API_URL", "https://api.github.com"),
        
        # MCP Server Configuration
        "mcp_servers": {
            "repository_analyzer": {
                "port": int(os.getenv("REPO_ANALYZER_PORT", "8001")),
                "host": os.getenv("REPO_ANALYZER_HOST", "localhost")
            },
            "code_search": {
                "port": int(os.getenv("CODE_SEARCH_PORT", "8002")),
                "host": os.getenv("CODE_SEARCH_HOST", "localhost")
            },
            "commit_history": {
                "port": int(os.getenv("COMMIT_HISTORY_PORT", "8003")),
                "host": os.getenv("COMMIT_HISTORY_HOST", "localhost")
            },
            "file_content": {
                "port": int(os.getenv("FILE_CONTENT_PORT", "8004")),
                "host": os.getenv("FILE_CONTENT_HOST", "localhost")
            },
            "issues": {
                "port": int(os.getenv("ISSUES_PORT", "8005")),
                "host": os.getenv("ISSUES_HOST", "localhost")
            },
            "repository_structure": {
                "port": int(os.getenv("REPO_STRUCTURE_PORT", "8006")),
                "host": os.getenv("REPO_STRUCTURE_HOST", "localhost")
            }
        },
        
        # Application Configuration
        "app": {
            "debug": os.getenv("DEBUG", "False").lower() == "true",
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "max_file_size": int(os.getenv("MAX_FILE_SIZE", "10485760")),  # 10MB
            "cache_ttl": int(os.getenv("CACHE_TTL", "3600")),  # 1 hour
        },
        
        # Agent Configuration
        "agents": {
            "default_model": "gemini-2.0-flash-001",
            "available_models": [
                "gemini-2.0-flash-001",
                "gemini-1.5-pro", 
                "gemini-1.5-flash"
            ],
            "max_tokens": int(os.getenv("MAX_TOKENS", "8192")),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "team_mode": os.getenv("TEAM_MODE", "coordinate"),
        },
        
        # UI Configuration
        "ui": {
            "theme": os.getenv("UI_THEME", "light"),
            "page_title": "🚀 GitHub Repository Analyzer",
            "page_icon": "🚀",
            "layout": "wide",
        }
    }
    
    return config

def get_google_api_key() -> str:
    """Get Google API key from environment"""
    return os.getenv("GOOGLE_API_KEY", "")

def get_github_token() -> str:
    """Get GitHub token from environment"""
    return os.getenv("GITHUB_TOKEN", "")

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration"""
    required_keys = ["google_api_key"]
    
    for key in required_keys:
        if not config.get(key):
            print(f"Warning: Missing required configuration key: {key}")
            return False
    
    return True

def get_mcp_server_config(server_name: str) -> Dict[str, Any]:
    """Get MCP server configuration"""
    config = load_config()
    return config["mcp_servers"].get(server_name, {})

def get_agent_config() -> Dict[str, Any]:
    """Get agent configuration"""
    config = load_config()
    return config["agents"] 