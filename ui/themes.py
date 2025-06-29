"""
🎨 Theme Management System

Modern theme system with dark/light modes, custom CSS,
animations, and responsive design.
"""

import streamlit as st
from typing import Dict, Any
import yaml
from pathlib import Path

class ThemeManager:
    """Manages application themes and styling."""
    
    def __init__(self):
        self.themes = self._load_themes()
        self.current_theme = "auto"
    
    def _load_themes(self) -> Dict[str, Any]:
        """Load theme definitions from config."""
        themes_path = Path(__file__).parent.parent / "config" / "themes.yaml"
        
        if themes_path.exists():
            with open(themes_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            return self._get_default_themes()
    
    def _get_default_themes(self) -> Dict[str, Any]:
        """Get default theme definitions."""
        return {
            "themes": {
                "light": {
                    "primary": "#ffffff",
                    "secondary": "#f8fafc",
                    "accent": "#3b82f6",
                    "text": "#1e293b",
                    "text_secondary": "#64748b",
                    "border": "#e2e8f0",
                    "success": "#10b981",
                    "warning": "#f59e0b",
                    "error": "#ef4444",
                    "background": "#ffffff",
                    "surface": "#f8fafc"
                },
                "dark": {
                    "primary": "#0f172a",
                    "secondary": "#1e293b",
                    "accent": "#3b82f6",
                    "text": "#f1f5f9",
                    "text_secondary": "#94a3b8",
                    "border": "#334155",
                    "success": "#10b981",
                    "warning": "#f59e0b",
                    "error": "#ef4444",
                    "background": "#0f172a",
                    "surface": "#1e293b"
                }
            }
        }
    
    def set_theme(self, theme: str):
        """Set the current theme."""
        self.current_theme = theme
    
    def get_current_theme_colors(self) -> Dict[str, str]:
        """Get colors for the current theme."""
        if self.current_theme == "auto":
            # TODO: Detect system theme
            theme_name = "light"
        else:
            theme_name = self.current_theme.lower()
        
        return self.themes["themes"].get(theme_name, self.themes["themes"]["light"])
    
    def apply_theme(self):
        """Apply the current theme to the application."""
        colors = self.get_current_theme_colors()
        
        # Custom CSS with modern design and animations
        css = f"""
        <style>
        /* Modern CSS Reset */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        /* Global Styles */
        .main {{
            background-color: {colors['background']};
            color: {colors['text']};
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        /* Header Styles */
        .header-container {{
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            border-radius: 1rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            animation: fadeInUp 0.8s ease-out;
        }}
        
        .main-title {{
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, {colors['accent']}, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            animation: slideInDown 1s ease-out;
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            color: {colors['text_secondary']};
            font-weight: 400;
            animation: slideInUp 1s ease-out 0.2s both;
        }}
        
        /* Sidebar Styles */
        .sidebar .sidebar-content {{
            background-color: {colors['surface']};
            border-right: 1px solid {colors['border']};
        }}
        
        .sidebar-header {{
            padding: 1rem;
            border-bottom: 1px solid {colors['border']};
            margin-bottom: 1rem;
        }}
        
        .sidebar-header h3 {{
            color: {colors['text']};
            font-weight: 600;
        }}
        
        /* Feature Cards */
        .feature-card {{
            background: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 1rem;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
            animation: fadeInUp 0.6s ease-out;
        }}
        
        .feature-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border-color: {colors['accent']};
        }}
        
        .feature-card h3 {{
            color: {colors['text']};
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        
        .feature-card p {{
            color: {colors['text_secondary']};
            line-height: 1.6;
        }}
        
        /* Dashboard Styles */
        .dashboard-header {{
            background: {colors['surface']};
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid {colors['border']};
            animation: fadeInUp 0.6s ease-out;
        }}
        
        .dashboard-header h2 {{
            color: {colors['text']};
            margin-bottom: 0.5rem;
        }}
        
        .dashboard-header p {{
            color: {colors['text_secondary']};
        }}
        
        /* Hero Section */
        .hero-section {{
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            border-radius: 2rem;
            margin: 2rem 0;
            animation: fadeInUp 1s ease-out;
        }}
        
        .hero-title {{
            font-size: 3.5rem;
            font-weight: 800;
            color: {colors['text']};
            margin-bottom: 1rem;
            animation: slideInDown 1s ease-out;
        }}
        
        .hero-subtitle {{
            font-size: 1.3rem;
            color: {colors['text_secondary']};
            max-width: 600px;
            margin: 0 auto;
            animation: slideInUp 1s ease-out 0.2s both;
        }}
        
        /* Map and Insights Headers */
        .map-header, .insights-header {{
            background: {colors['surface']};
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid {colors['border']};
            animation: fadeInUp 0.6s ease-out;
        }}
        
        .map-header h2, .insights-header h2 {{
            color: {colors['text']};
            margin-bottom: 0.5rem;
        }}
        
        .map-header p, .insights-header p {{
            color: {colors['text_secondary']};
        }}
        
        /* Button Styles */
        .stButton > button {{
            background: linear-gradient(135deg, {colors['accent']}, #8b5cf6);
            border: none;
            border-radius: 0.75rem;
            padding: 0.75rem 1.5rem;
            color: white;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        }}
        
        /* Input Styles */
        .stTextInput > div > div > input {{
            border: 2px solid {colors['border']};
            border-radius: 0.75rem;
            padding: 0.75rem 1rem;
            background: {colors['surface']};
            color: {colors['text']};
            transition: all 0.3s ease;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {colors['accent']};
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}
        
        /* Chat Styles */
        .stChatMessage {{
            background: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 1rem;
            margin: 1rem 0;
            animation: fadeInUp 0.4s ease-out;
        }}
        
        /* Metric Cards */
        .metric-container {{
            background: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 1rem;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }}
        
        .metric-container:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }}
        
        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes slideInDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes slideInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{
                opacity: 1;
            }}
            50% {{
                opacity: 0.5;
            }}
        }}
        
        @keyframes bounce {{
            0%, 20%, 53%, 80%, 100% {{
                transform: translate3d(0,0,0);
            }}
            40%, 43% {{
                transform: translate3d(0, -30px, 0);
            }}
            70% {{
                transform: translate3d(0, -15px, 0);
            }}
            90% {{
                transform: translate3d(0, -4px, 0);
            }}
        }}
        
        /* Loading Animation */
        .loading-spinner {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid {colors['border']};
            border-radius: 50%;
            border-top-color: {colors['accent']};
            animation: spin 1s ease-in-out infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        /* Success Animation */
        .success-checkmark {{
            color: {colors['success']};
            animation: bounce 0.6s ease-out;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .main-title {{
                font-size: 2rem;
            }}
            
            .hero-title {{
                font-size: 2.5rem;
            }}
            
            .feature-card {{
                margin: 0.5rem 0;
            }}
        }}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {colors['surface']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {colors['border']};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {colors['accent']};
        }}
        
        /* Focus States */
        *:focus {{
            outline: 2px solid {colors['accent']};
            outline-offset: 2px;
        }}
        
        /* Selection */
        ::selection {{
            background: {colors['accent']};
            color: white;
        }}
        
        /* Print Styles */
        @media print {{
            .sidebar, .stButton {{
                display: none !important;
            }}
        }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)
    
    def get_theme_info(self) -> Dict[str, Any]:
        """Get information about the current theme."""
        colors = self.get_current_theme_colors()
        return {
            "name": self.current_theme,
            "colors": colors,
            "is_dark": self.current_theme.lower() == "dark"
        } 