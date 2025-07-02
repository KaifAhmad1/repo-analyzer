"""
Settings Sidebar UI Component
Provides interface for users to configure application settings
"""

import streamlit as st
import os
from src.utils.config import get_groq_api_key, has_required_keys

def render_settings_sidebar():
    """Render the organized settings sidebar with application settings and user controls"""
    
    # Main Settings Section
    st.sidebar.markdown("## ⚙️ Settings")
    
    # API Configuration Status Section
    with st.sidebar.expander("🔑 API Configuration", expanded=True):
        st.markdown("#### 🤖 Groq API Key")
        
        # Get current API key from .env
        groq_api_key = get_groq_api_key()
        
        # Show API key status
        if groq_api_key:
            st.success("✅ Groq API key configured from .env file")
            st.info("**Status:** Ready for analysis")
        else:
            st.error("❌ Groq API key not found in .env file")
            st.markdown("""
            **To configure:**
            1. Get your key from: [Groq Console](https://console.groq.com/keys)
            2. Add to `.env` file: `GROQ_API_KEY=your_key_here`
            3. Restart the application
            """)
    
    # Model Configuration Section
    with st.sidebar.expander("🤖 AI Model Settings", expanded=False):
        st.markdown("#### Model Selection")
        
        # Available Groq models
        groq_models = [
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant", 
            "llama-3.1-405b-reasoning",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]
        
        selected_model = st.selectbox(
            "Choose AI Model:",
            groq_models,
            index=0,
            help="Select the Groq model for analysis"
        )
        
        # Store in session state
        st.session_state.selected_model = selected_model
        
        # Model info
        st.info(f"**Current Model:** {selected_model}")
    
    # Analysis Settings Section
    with st.sidebar.expander("🔍 Analysis Settings", expanded=False):
        st.markdown("#### Analysis Preferences")
        
        # Analysis depth
        analysis_depth = st.slider(
            "Analysis Depth:",
            min_value=1,
            max_value=5,
            value=3,
            help="How deep to analyze the repository structure"
        )
        st.session_state.analysis_depth = analysis_depth
        
        # Include patterns
        include_patterns = st.multiselect(
            "Include in Analysis:",
            ["Code Files", "Documentation", "Configuration", "Tests", "Dependencies"],
            default=["Code Files", "Documentation", "Configuration"],
            help="What types of files to include in analysis"
        )
        st.session_state.include_patterns = include_patterns
        
        # Response style
        response_style = st.selectbox(
            "Response Style:",
            ["Detailed", "Concise", "Technical", "Beginner-friendly"],
            help="How detailed and technical the responses should be"
        )
        st.session_state.response_style = response_style
    
    # UI Settings Section
    with st.sidebar.expander("🎨 UI Preferences", expanded=False):
        st.markdown("#### Interface Settings")
        
        # Theme preference
        theme = st.selectbox(
            "Theme:",
            ["Auto", "Light", "Dark"],
            help="Choose your preferred theme"
        )
        st.session_state.theme = theme
        
        # Sidebar state
        sidebar_expanded = st.checkbox(
            "Keep sidebar expanded",
            value=True,
            help="Keep the sidebar open by default"
        )
        st.session_state.sidebar_expanded = sidebar_expanded
        
        # Show tool usage
        show_tool_usage = st.checkbox(
            "Show tool usage",
            value=True,
            help="Display which tools were used in responses"
        )
        st.session_state.show_tool_usage = show_tool_usage
    
    # Quick Actions Section
    st.sidebar.markdown("## ⚡ Quick Actions")
    
    # Quick action buttons
    if st.sidebar.button("🔄 Refresh Analysis", use_container_width=True):
        st.session_state.refresh_analysis = True
        st.rerun()
    
    if st.sidebar.button("📊 Show Metrics", use_container_width=True):
        st.session_state.show_metrics = True
    
    if st.sidebar.button("🗂️ Export Results", use_container_width=True):
        st.session_state.export_results = True
    
    # Status Section
    st.sidebar.markdown("## 📊 Status")
    
    # Configuration status
    config_valid = bool(groq_api_key)
    if config_valid:
        st.sidebar.success("✅ Ready for analysis")
    else:
        st.sidebar.error("❌ API key required")
    
    # Return current configuration
    return {
        "groq_api_key": groq_api_key,
        "config_valid": config_valid,
        "selected_model": st.session_state.get("selected_model", "llama-3.1-70b-versatile"),
        "analysis_depth": st.session_state.get("analysis_depth", 3),
        "include_patterns": st.session_state.get("include_patterns", ["Code Files", "Documentation", "Configuration"]),
        "response_style": st.session_state.get("response_style", "Detailed")
    }

def validate_api_keys():
    """Validate that required API keys are configured"""
    return has_required_keys() 