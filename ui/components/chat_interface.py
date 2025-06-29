"""
💬 Modern Chat Interface Component

Beautiful, responsive chat interface with animations,
message history, and real-time updates.
"""

import streamlit as st
from typing import List, Dict, Any, Optional
import time
from datetime import datetime

class ChatInterface:
    """Modern chat interface with animations and responsive design."""
    
    def __init__(self, repository: str):
        self.repository = repository
        self.messages = st.session_state.get('messages', [])
    
    def render(self):
        """Render the chat interface."""
        
        # Chat container with modern styling
        with st.container():
            st.markdown(f"""
            <div class="chat-header">
                <h3>💬 Chat Analysis</h3>
                <p>Ask questions about <strong>{self.repository}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Messages area
            self._render_messages()
            
            # Input area
            self._render_input()
    
    def _render_messages(self):
        """Render chat messages with animations."""
        
        # Messages container
        messages_container = st.container()
        
        with messages_container:
            # Display existing messages
            for i, message in enumerate(self.messages):
                self._render_message(message, i)
            
            # Auto-scroll to bottom
            st.markdown("""
            <script>
                // Auto-scroll to bottom of chat
                const messagesContainer = document.querySelector('.stChatMessage');
                if (messagesContainer) {
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }
            </script>
            """, unsafe_allow_html=True)
    
    def _render_message(self, message: Dict[str, Any], index: int):
        """Render a single message with animations."""
        
        role = message.get("role", "user")
        content = message.get("content", "")
        timestamp = message.get("timestamp", datetime.now().isoformat())
        
        # Message styling based on role
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"""
                <div class="user-message">
                    <div class="message-content">{content}</div>
                    <div class="message-time">{self._format_timestamp(timestamp)}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"""
                <div class="assistant-message">
                    <div class="message-content">{content}</div>
                    <div class="message-time">{self._format_timestamp(timestamp)}</div>
                </div>
                """, unsafe_allow_html=True)
    
    def _render_input(self):
        """Render the chat input area."""
        
        # Input container
        input_container = st.container()
        
        with input_container:
            # Question input with modern styling
            question = st.chat_input(
                "Ask a question about the repository...",
                key=f"chat_input_{int(time.time())}"
            )
            
            if question:
                self._process_question(question)
    
    def _process_question(self, question: str):
        """Process a user question."""
        
        # Add user message
        user_message = {
            "role": "user",
            "content": question,
            "timestamp": datetime.now().isoformat()
        }
        
        self.messages.append(user_message)
        st.session_state.messages = self.messages
        
        # Show typing indicator
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤖 Thinking..."):
                # Process the question
                response = self._get_ai_response(question)
                
                # Add AI response
                ai_message = {
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                }
                
                self.messages.append(ai_message)
                st.session_state.messages = self.messages
        
        # Rerun to update chat
        st.rerun()
    
    def _get_ai_response(self, question: str) -> str:
        """Get AI response for a question."""
        
        # TODO: Integrate with AI agent
        # For now, return a placeholder response
        responses = [
            f"I understand you're asking about {self.repository}: {question}. Let me analyze this for you...",
            f"Great question! Looking at {self.repository}, I can see that {question.lower()}. Here's what I found...",
            f"Analyzing {self.repository} for your question about {question.lower()}. The repository shows...",
            f"Based on my analysis of {self.repository}, regarding {question.lower()}, here are the key insights..."
        ]
        
        import random
        return random.choice(responses)
    
    def _format_timestamp(self, timestamp: str) -> str:
        """Format timestamp for display."""
        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime("%H:%M")
        except:
            return "now"
    
    def clear_history(self):
        """Clear chat history."""
        self.messages = []
        st.session_state.messages = []
    
    def export_chat(self) -> str:
        """Export chat history as text."""
        export_text = f"Chat Analysis for {self.repository}\n"
        export_text += "=" * 50 + "\n\n"
        
        for message in self.messages:
            role = "User" if message["role"] == "user" else "AI"
            content = message["content"]
            timestamp = self._format_timestamp(message["timestamp"])
            
            export_text += f"[{timestamp}] {role}: {content}\n\n"
        
        return export_text 