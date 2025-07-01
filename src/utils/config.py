"""
Simple configuration utilities for the GitHub Repository Analyzer
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_github_token():
    """Get GitHub token from session state or environment"""
    return st.session_state.get("github_token", os.getenv("GITHUB_TOKEN"))

def get_google_api_key():
    """Get Google API key from session state or environment"""
    return st.session_state.get("google_api_key", os.getenv("GOOGLE_API_KEY"))

def has_required_keys():
    """Check if required API keys are configured"""
    return bool(get_google_api_key())

def save_keys_to_env(github_token, google_api_key):
    """Save API keys to .env file"""
    try:
        env_content = f"""# GitHub Repository Analyzer Configuration
GITHUB_TOKEN={github_token}
GOOGLE_API_KEY={google_api_key}
"""
        with open(".env", "w") as f:
            f.write(env_content)
        return True
    except Exception:
        return False 