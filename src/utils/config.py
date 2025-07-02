"""
Simple configuration utilities for the GitHub Repository Analyzer
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_groq_api_key():
    """Get Groq API key from environment"""
    return os.getenv("GROQ_API_KEY")

def has_required_keys():
    """Check if required API keys are configured"""
    return bool(get_groq_api_key())

def save_keys_to_env(groq_api_key):
    """Save API keys to .env file"""
    try:
        env_content = f"""# GitHub Repository Analyzer Configuration
GROQ_API_KEY={groq_api_key}
"""
        with open(".env", "w") as f:
            f.write(env_content)
        return True
    except Exception:
        return False

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
    return {
        "theme": st.session_state.get("theme", "light"),
        "sidebar_width": st.session_state.get("sidebar_width", "medium"),
        "auto_analyze": st.session_state.get("auto_analyze", False),
        "show_advanced_options": st.session_state.get("show_advanced_options", False),
        "max_results": st.session_state.get("max_results", 10),
        "analysis_depth": st.session_state.get("analysis_depth", "medium")
    }

def save_ui_settings(settings):
    """Save UI settings to session state"""
    for key, value in settings.items():
        st.session_state[key] = value 