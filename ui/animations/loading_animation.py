"""
⏳ Loading Animation Component

Beautiful loading animations with modern design,
smooth transitions, and customizable states.
"""

import streamlit as st
import time
from typing import Optional, Dict, Any

class LoadingAnimation:
    """Modern loading animation with customizable states."""
    
    @staticmethod
    def show_spinner(text: str = "Loading...", type: str = "default"):
        """Show a loading spinner with custom text and type."""
        
        spinner_configs = {
            "default": "⏳",
            "thinking": "🤔",
            "analyzing": "🔍",
            "processing": "⚙️",
            "searching": "🔎",
            "generating": "✨",
            "connecting": "🔗",
            "downloading": "📥",
            "uploading": "📤"
        }
        
        icon = spinner_configs.get(type, "⏳")
        
        with st.spinner(f"{icon} {text}"):
            time.sleep(0.1)  # Small delay for smooth animation
    
    @staticmethod
    def show_progress_bar(text: str = "Processing...", progress: float = 0.0):
        """Show a progress bar with custom text and progress."""
        
        progress_bar = st.progress(progress, text=text)
        return progress_bar
    
    @staticmethod
    def show_typing_indicator(text: str = "AI is thinking..."):
        """Show a typing indicator for AI responses."""
        
        # Create typing animation
        st.markdown(f"""
        <div class="typing-indicator">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <div class="typing-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_pulse_animation(text: str = "Processing"):
        """Show a pulse animation."""
        
        st.markdown(f"""
        <div class="pulse-animation">
            <div class="pulse-dot"></div>
            <span>{text}</span>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_bounce_animation(text: str = "Loading"):
        """Show a bounce animation."""
        
        st.markdown(f"""
        <div class="bounce-animation">
            <div class="bounce-dot"></div>
            <span>{text}</span>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_wave_animation(text: str = "Analyzing"):
        """Show a wave animation."""
        
        st.markdown(f"""
        <div class="wave-animation">
            <div class="wave-dots">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
            <span>{text}</span>
        </div>
        """, unsafe_allow_html=True)

class SuccessAnimation:
    """Success state animations."""
    
    @staticmethod
    def show():
        """Show a success animation."""
        
        st.markdown("""
        <div class="success-animation">
            <div class="success-checkmark">✓</div>
            <span>Success!</span>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_with_message(message: str):
        """Show a success animation with custom message."""
        
        st.markdown(f"""
        <div class="success-animation">
            <div class="success-checkmark">✓</div>
            <span>{message}</span>
        </div>
        """, unsafe_allow_html=True)

class ErrorAnimation:
    """Error state animations."""
    
    @staticmethod
    def show():
        """Show an error animation."""
        
        st.markdown("""
        <div class="error-animation">
            <div class="error-icon">✗</div>
            <span>Error occurred</span>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_with_message(message: str):
        """Show an error animation with custom message."""
        
        st.markdown(f"""
        <div class="error-animation">
            <div class="error-icon">✗</div>
            <span>{message}</span>
        </div>
        """, unsafe_allow_html=True)

class TransitionAnimation:
    """Page transition animations."""
    
    @staticmethod
    def fade_in():
        """Apply fade-in transition."""
        
        st.markdown("""
        <style>
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def slide_in(direction: str = "left"):
        """Apply slide-in transition."""
        
        directions = {
            "left": "translateX(-100%)",
            "right": "translateX(100%)",
            "up": "translateY(-100%)",
            "down": "translateY(100%)"
        }
        
        transform = directions.get(direction, "translateX(-100%)")
        
        st.markdown(f"""
        <style>
        .slide-in-{direction} {{
            animation: slideIn{direction.capitalize()} 0.5s ease-out;
        }}
        
        @keyframes slideIn{direction.capitalize()} {{
            from {{ 
                opacity: 0; 
                transform: {transform}; 
            }}
            to {{ 
                opacity: 1; 
                transform: translate(0, 0); 
            }}
        }}
        </style>
        """, unsafe_allow_html=True) 