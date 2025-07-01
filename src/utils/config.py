"""
Configuration utilities for the GitHub Repository Analyzer
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_config() -> Dict[str, Any]:
    """Get application configuration"""
    return {
        "github_token": os.getenv("GITHUB_TOKEN"),
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "default_model": os.getenv("GEMINI_MODEL", "gemini-2.0-flash-001"),
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO")
    }

def validate_config() -> bool:
    """Validate that required configuration is present"""
    config = get_config()
    
    if not config["google_api_key"]:
        print("❌ GOOGLE_API_KEY is required")
        return False
    
    if not config["github_token"]:
        print("⚠️ GITHUB_TOKEN not found - some features may be limited")
    
    return True

def get_github_token() -> Optional[str]:
    """Get GitHub token from environment"""
    return os.getenv("GITHUB_TOKEN")

def get_google_api_key() -> Optional[str]:
    """Get Google API key from environment"""
    return os.getenv("GOOGLE_API_KEY")

def is_debug_mode() -> bool:
    """Check if debug mode is enabled"""
    return os.getenv("DEBUG", "False").lower() == "true" 