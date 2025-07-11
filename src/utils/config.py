"""
Enhanced configuration utilities for the GitHub Repository Analyzer
Comprehensive settings management for systematic repository analysis
"""

import os
import json
import streamlit as st
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List
from pathlib import Path

# Load environment variables silently
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        load_dotenv(verbose=False)
    except Exception:
        # .env file doesn't exist or can't be loaded, which is fine
        pass

# Create necessary directories
def ensure_directories():
    """Ensure all necessary directories exist"""
    directories = [
        "tmp",
        "cache",
        "logs",
        "data",
        "sessions"
    ]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

ensure_directories()

def get_groq_api_key():
    """Get Groq API key from session state, environment, or fallback"""
    # Try to get from Streamlit session state first
    try:
        import streamlit as st
        if hasattr(st, 'session_state') and 'groq_api_key' in st.session_state:
            session_key = st.session_state.groq_api_key
            if session_key and session_key.strip():
                return session_key.strip()
    except:
        pass  # Streamlit not available or session state not accessible
    
    # Try to load from environment
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return api_key
    
    # Try to load from .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            return api_key
    except ImportError:
        pass  # python-dotenv not installed
    
    # Fallback to hardcoded key (for company assignment)
    fallback_key = "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"
    return fallback_key

def get_github_token():
    """Get GitHub token from session state, environment, or None"""
    # Try to get from Streamlit session state first
    try:
        import streamlit as st
        if hasattr(st, 'session_state') and 'github_token' in st.session_state:
            session_token = st.session_state.github_token
            if session_token and session_token.strip():
                return session_token.strip()
    except:
        pass  # Streamlit not available or session state not accessible
    
    # Try to load from environment
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token
    
    # Try to load from .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        token = os.getenv("GITHUB_TOKEN")
        if token:
            return token
    except ImportError:
        pass  # python-dotenv not installed
    
    return None  # No token configured

def has_required_keys():
    """Check if required API keys are configured - always True for company assignment"""
    return True

def save_keys_to_env(groq_api_key: str, github_token: str = ""):
    """Save API keys to .env file - disabled for company assignment"""
    return True  # Always return True since we don't need to save keys

def get_available_models():
    """Get list of available models based on configured APIs"""
    models = []
    if get_groq_api_key():
        models.extend([
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile",
            "llama-3.1-405b-reasoning",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ])
    return models

def get_default_model():
    """Get the default model to use"""
    if get_groq_api_key():
        return "llama-3.1-70b-versatile"
    return None

def get_ui_settings():
    """Get UI settings from session state or defaults"""
    defaults = {
        "theme": "light",
        "sidebar_width": "medium", 
        "auto_analyze": False,
        "show_advanced_options": False,
        "max_results": 10,
        "analysis_depth": "medium",
        "enable_caching": True,
        "cache_duration": 3600,  # 1 hour
        "auto_save_sessions": True,
        "show_tool_usage": True,
        "enable_progress_tracking": True
    }
    
    return {key: st.session_state.get(key, default) for key, default in defaults.items()}

def save_ui_settings(settings: Dict[str, Any]):
    """Save UI settings to session state"""
    for key, value in settings.items():
        st.session_state[key] = value

def get_analysis_settings():
    """Get analysis-specific settings"""
    defaults = {
        "max_file_size": 1024 * 1024,  # 1MB
        "max_files_per_analysis": 100,
        "include_hidden_files": False,
        "analysis_timeout": 300,  # 5 minutes
        "enable_code_metrics": True,
        "enable_security_analysis": True,
        "enable_dependency_analysis": True,
        "enable_commit_analysis": True,
        "enable_structure_analysis": True
    }
    
    return {key: st.session_state.get(key, default) for key, default in defaults.items()}

def save_analysis_settings(settings: Dict[str, Any]):
    """Save analysis settings to session state"""
    for key, value in settings.items():
        st.session_state[key] = value

def get_session_data(session_id: str) -> Dict[str, Any]:
    """Get session data from file"""
    session_file = Path(f"sessions/{session_id}.json")
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_session_data(session_id: str, data: Dict[str, Any]):
    """Save session data to file"""
    try:
        session_file = Path(f"sessions/{session_id}.json")
        with open(session_file, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

def get_cache_key(repo_url: str, operation: str, params: Dict[str, Any] = None) -> str:
    """Generate cache key for repository operations"""
    import hashlib
    key_data = f"{repo_url}:{operation}"
    if params:
        key_data += f":{json.dumps(params, sort_keys=True)}"
    return hashlib.md5(key_data.encode()).hexdigest()

def get_cache_path(cache_key: str) -> Path:
    """Get cache file path"""
    return Path(f"cache/{cache_key}.json")

def is_cache_valid(cache_key: str, max_age: int = 3600) -> bool:
    """Check if cache is still valid"""
    cache_file = get_cache_path(cache_key)
    if not cache_file.exists():
        return False
    
    import time
    file_age = time.time() - cache_file.stat().st_mtime
    return file_age < max_age

def save_to_cache(cache_key: str, data: Any):
    """Save data to cache"""
    try:
        cache_file = get_cache_path(cache_key)
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

def load_from_cache(cache_key: str) -> Optional[Any]:
    """Load data from cache"""
    try:
        cache_file = get_cache_path(cache_key)
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return None

def clear_cache():
    """Clear all cache files"""
    cache_dir = Path("cache")
    if cache_dir.exists():
        for cache_file in cache_dir.glob("*.json"):
            cache_file.unlink()

def get_system_info() -> Dict[str, Any]:
    """Get system information for debugging"""
    import platform
    import sys
    
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "streamlit_version": st.__version__,
        "cache_directory": str(Path("cache").absolute()),
        "sessions_directory": str(Path("sessions").absolute()),
        "temp_directory": str(Path("tmp").absolute())
    }

def get_analysis_presets() -> Dict[str, Dict[str, Any]]:
    """Get predefined analysis presets"""
    return {
        "quick": {
            "name": "Quick Overview",
            "description": "Fast analysis with basic insights",
            "max_files": 20,
            "max_depth": 2,
            "include_metrics": False,
            "include_security": False,
            "timeout": 60
        },
        "standard": {
            "name": "Standard Analysis",
            "description": "Comprehensive analysis with metrics",
            "max_files": 50,
            "max_depth": 3,
            "include_metrics": True,
            "include_security": True,
            "timeout": 180
        },
        "deep": {
            "name": "Deep Analysis",
            "description": "In-depth analysis with all features",
            "max_files": 100,
            "max_depth": 5,
            "include_metrics": True,
            "include_security": True,
            "timeout": 300
        },
        "security": {
            "name": "Security Focus",
            "description": "Security-focused analysis",
            "max_files": 75,
            "max_depth": 4,
            "include_metrics": True,
            "include_security": True,
            "timeout": 240
        }
    } 