"""
Settings Sidebar UI Component
Provides interface for users to configure API keys and tokens
"""

import streamlit as st
import os
from src.utils.config import get_github_token, get_google_api_key, has_required_keys, save_keys_to_env

def render_settings_sidebar():
    """Render the settings sidebar with API key configuration"""
    
    st.sidebar.markdown("### 🔑 API Configuration")
    
    # GitHub Token Section
    st.sidebar.markdown("#### 🔐 GitHub Access Token")
    st.sidebar.markdown("""
    **Required for:** Repository access, private repos, higher rate limits
    
    Get your token from: [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
    """)
    
    # Get current token
    current_github_token = get_github_token() or ""
    
    github_token = st.sidebar.text_input(
        "GitHub Access Token",
        value=current_github_token,
        type="password",
        placeholder="ghp_xxxxxxxxxxxxxxxxxxxx",
        help="Enter your GitHub personal access token"
    )
    
    if github_token != current_github_token:
        st.session_state.github_token = github_token
        os.environ["GITHUB_TOKEN"] = github_token
    
    # Show token status
    if github_token:
        st.sidebar.success("✅ GitHub token configured")
    else:
        st.sidebar.warning("⚠️ GitHub token not set")
    
    # Google API Key Section
    st.sidebar.markdown("#### 🤖 Google API Key")
    st.sidebar.markdown("""
    **Required for:** AI analysis and Q&A features
    
    Get your key from: [Google AI Studio](https://aistudio.google.com/app/apikey)
    """)
    
    # Get current API key
    current_google_api_key = get_google_api_key() or ""
    
    google_api_key = st.sidebar.text_input(
        "Google API Key",
        value=current_google_api_key,
        type="password",
        placeholder="AIzaSyC...",
        help="Enter your Google AI API key"
    )
    
    if google_api_key != current_google_api_key:
        st.session_state.google_api_key = google_api_key
        os.environ["GOOGLE_API_KEY"] = google_api_key
    
    # Show API key status
    if google_api_key:
        st.sidebar.success("✅ Google API key configured")
    else:
        st.sidebar.error("❌ Google API key required")
    
    # Configuration validation
    st.sidebar.markdown("### ✅ Configuration Status")
    
    config_valid = bool(google_api_key)
    if not google_api_key:
        st.sidebar.error("❌ Google API key is required")
    else:
        st.sidebar.success("✅ Google API key is set")
    
    if not github_token:
        st.sidebar.warning("⚠️ GitHub token not set (some features may be limited)")
    else:
        st.sidebar.success("✅ GitHub token is set")
    
    # Save configuration button
    if st.sidebar.button("💾 Save Configuration", type="primary"):
        if config_valid:
            st.session_state.github_token = github_token
            st.session_state.google_api_key = google_api_key
            os.environ["GITHUB_TOKEN"] = github_token
            os.environ["GOOGLE_API_KEY"] = google_api_key
            
            if save_keys_to_env(github_token, google_api_key):
                st.sidebar.success("✅ Configuration saved!")
            else:
                st.sidebar.warning("⚠️ Saved to session but couldn't write to .env file")
            st.rerun()
        else:
            st.sidebar.error("❌ Please fix configuration errors before saving")
    
    # Clear configuration button
    if st.sidebar.button("🗑️ Clear Configuration"):
        if "github_token" in st.session_state:
            del st.session_state.github_token
        if "google_api_key" in st.session_state:
            del st.session_state.google_api_key
        if "GITHUB_TOKEN" in os.environ:
            del os.environ["GITHUB_TOKEN"]
        if "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]
        
        st.sidebar.success("✅ Configuration cleared!")
        st.rerun()
    
    # Return current configuration
    return {
        "github_token": github_token,
        "google_api_key": google_api_key,
        "config_valid": config_valid
    }

def validate_api_keys():
    """Validate that required API keys are configured"""
    return has_required_keys() 