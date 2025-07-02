"""
Enhanced Settings Sidebar UI Component
Provides minimal interface for essential application settings with improved visual appeal
"""

import streamlit as st
import os
from src.utils.config import get_groq_api_key, has_required_keys

def render_settings_sidebar():
    """Render the enhanced settings sidebar with only essential settings"""
    
    # API Configuration Status - Enhanced display
    st.markdown("### 🔑 API Configuration")
    groq_api_key = get_groq_api_key()
    
    if groq_api_key:
        st.success("✅ **Groq API Configured**")
        st.info("**Status:** Ready for analysis")
    else:
        st.error("❌ **Groq API Key Required**")
        st.markdown("""
        **To configure:**
        1. Get your key from: [Groq Console](https://console.groq.com/keys)
        2. Add to `.env` file: `GROQ_API_KEY=your_key_here`
        3. Restart the application
        """)
    
    st.markdown("---")
    
    # Essential Settings with enhanced organization
    st.markdown("### ⚙️ Analysis Settings")
    
    # Analysis depth with enhanced slider
    st.markdown("**🔍 Analysis Depth**")
    analysis_depth = st.slider(
        "How deep to analyze:",
        min_value=1,
        max_value=5,
        value=3,
        help="Controls how deep the analysis explores the repository structure"
    )
    st.session_state.analysis_depth = analysis_depth
    
    # Model selection with enhanced display
    st.markdown("**🤖 AI Model Selection**")
    groq_models = [
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant", 
        "llama-3.1-405b-reasoning"
    ]
    
    selected_model = st.selectbox(
        "Choose AI Model:",
        groq_models,
        index=0,
        help="Select the Groq model for analysis"
    )
    st.session_state.selected_model = selected_model
    
    # Show current model info
    st.info(f"**Current Model:** {selected_model}")
    
    # Show tool usage with enhanced styling
    st.markdown("**🔧 Tool Usage Display**")
    show_tool_usage = st.checkbox(
        "Show which tools were used",
        value=True,
        help="Display which MCP tools were used in AI responses"
    )
    st.session_state.show_tool_usage = show_tool_usage
    
    # Quick Actions with enhanced styling
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("🔄 Refresh Application", use_container_width=True):
        st.rerun()
    
    # Return current configuration
    return {
        "groq_api_key": groq_api_key,
        "config_valid": bool(groq_api_key),
        "selected_model": st.session_state.get("selected_model", "llama-3.1-70b-versatile"),
        "analysis_depth": st.session_state.get("analysis_depth", 3),
        "show_tool_usage": st.session_state.get("show_tool_usage", True)
    }

def validate_api_keys():
    """Validate that required API keys are configured"""
    return has_required_keys() 