"""
Simple configuration utilities for the GitHub Repository Analyzer
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_google_api_key():
    """Get Google API key from environment"""
    return os.getenv("GOOGLE_API_KEY")

def get_groq_api_key():
    """Get Groq API key from environment"""
    return os.getenv("GROQ_API_KEY")

def has_required_keys():
    """Check if required API keys are configured"""
    return bool(get_google_api_key())

def save_keys_to_env(google_api_key):
    """Save API keys to .env file"""
    try:
        env_content = f"""# GitHub Repository Analyzer Configuration
GOOGLE_API_KEY={google_api_key}
"""
        with open(".env", "w") as f:
            f.write(env_content)
        return True
    except Exception:
        return False 