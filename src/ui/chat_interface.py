"""
Chat Interface UI Component
Provides a chat-like interface for interacting with the AI agent
"""

import streamlit as st
from typing import Dict, Any, List
import time

def render_chat_interface(ai_agent: Dict[str, Any]):
    """Render the main chat interface"""
    st.subheader("💬 Ask Questions About the Repository")

    # Floating action buttons
    render_fab_buttons()

    # Display conversation history in card
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        display_conversation_history()
        st.markdown('</div>', unsafe_allow_html=True)

    # Question input in card
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        question = st.text_input(
            "Ask a question about the repository:",
            placeholder="e.g., What is this repository about? Show me the main entry points...",
            key="question_input"
        )
        render_quick_questions()
        if st.button("🚀 Ask AI", type="primary") or (question and st.session_state.get("auto_submit", False)):
            if question:
                process_question(ai_agent, question)
                st.session_state.question_input = ""
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def display_conversation_history():
    """Display the conversation history with chat bubbles and animation"""
    if 'messages' in st.session_state and st.session_state.messages:
        for i, message in enumerate(st.session_state.messages):
            is_user = message["role"] == "user"
            bubble_class = "user-bubble" if is_user else "ai-bubble"
            icon = "👤" if is_user else "🤖"
            with st.container():
                st.markdown(f'<div class="chat-bubble {bubble_class}">{icon} {message["content"]}</div>', unsafe_allow_html=True)
                # Show tools used if any
                if message.get("tools_used"):
                    with st.expander("🔧 Tools Used"):
                        for tool in message["tools_used"]:
                            st.markdown(f"- {tool}")

def render_quick_questions():
    """Render quick question buttons"""
    st.markdown("**💡 Quick Questions:**")
    
    quick_questions = [
        "What is this repository about?",
        "Show me the main entry points",
        "What are the recent changes?",
        "Find authentication-related code",
        "What dependencies does this use?",
        "Are there any performance issues?",
        "Explain the database implementation",
        "What's the testing strategy?"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(quick_questions):
        with cols[i % 2]:
            if st.button(question, key=f"quick_{i}"):
                st.session_state.quick_question = question
                st.rerun()
    
    # Handle quick question selection
    if hasattr(st.session_state, 'quick_question'):
        question = st.session_state.quick_question
        del st.session_state.quick_question
        process_question(ai_agent, question)
        st.rerun()

def process_question(ai_agent: Dict[str, Any], question: str):
    """Process a question and get AI response with animated loader"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    st.session_state.messages.append({
        "role": "user",
        "content": question,
        "timestamp": time.time()
    })
    # Show animated loader
    st.markdown('<div class="loader"></div>', unsafe_allow_html=True)
    with st.spinner("🤖 AI is analyzing the repository..."):
        try:
            repo_url = st.session_state.get("repository_url", "")
            if not repo_url:
                st.error("❌ No repository selected. Please select a repository first.")
                return
            import os
            os.environ['GITHUB_REPO_URL'] = repo_url
            from src.agent.ai_agent import ask_question
            response = ask_question(ai_agent, question, repo_url)
            if response["success"]:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["response"],
                    "tools_used": response.get("tools_used", []),
                    "timestamp": time.time()
                })
                show_toast("✅ Response generated successfully!", success=True)
            else:
                show_toast(f"❌ Error: {response['response']}", success=False)
        except Exception as e:
            show_toast(f"❌ Error processing question: {str(e)}", success=False)

def render_analysis_options():
    """Render additional analysis options"""
    st.markdown("---")
    st.subheader("🔍 Advanced Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Repository Overview"):
            generate_repository_overview()
    
    with col2:
        if st.button("📈 Code Analysis"):
            generate_code_analysis()
    
    with col3:
        if st.button("🐛 Issue Analysis"):
            generate_issue_analysis()

def generate_repository_overview():
    """Generate a comprehensive repository overview"""
    st.info("🔄 Generating repository overview...")
    # This would call the AI agent with a specific prompt for overview
    pass

def generate_code_analysis():
    """Generate code quality analysis"""
    st.info("🔄 Analyzing code quality...")
    # This would call the AI agent with a specific prompt for code analysis
    pass

def generate_issue_analysis():
    """Generate issue and bug analysis"""
    st.info("🔄 Analyzing issues and bugs...")
    # This would call the AI agent with a specific prompt for issue analysis
    pass

def render_response_with_formatting(response: str):
    """Render AI response with proper formatting"""
    # Split response into paragraphs
    paragraphs = response.split('\n\n')
    
    for paragraph in paragraphs:
        if paragraph.strip():
            # Check if it's a code block
            if paragraph.startswith('```') and paragraph.endswith('```'):
                # Extract code content
                code_content = paragraph[3:-3]
                st.code(code_content, language='python')
            elif paragraph.startswith('**') and paragraph.endswith('**'):
                # Bold text
                st.markdown(paragraph)
            elif paragraph.startswith('- '):
                # List item
                st.markdown(paragraph)
            else:
                # Regular paragraph
                st.markdown(paragraph)
            
            st.markdown("")  # Add spacing

def clear_conversation():
    """Clear the conversation history"""
    if 'messages' in st.session_state:
        st.session_state.messages = []
        st.success("🗑️ Conversation history cleared!")

def export_conversation():
    """Export conversation to file"""
    if 'messages' in st.session_state and st.session_state.messages:
        import json
        from datetime import datetime
        
        # Create export data
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "repository": st.session_state.get("repository_url", ""),
            "messages": st.session_state.messages
        }
        
        # Convert to JSON
        json_str = json.dumps(export_data, indent=2)
        
        # Create download button
        st.download_button(
            label="📥 Export Conversation",
            data=json_str,
            file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def render_fab_buttons():
    """Render floating action buttons for clear and export"""
    st.markdown('''
    <div class="fab" onclick="window.dispatchEvent(new CustomEvent('clearChat'))" title="Clear Chat">🗑️</div>
    <div class="fab" style="right: 100px; background: #10b981;" onclick="window.dispatchEvent(new CustomEvent('exportChat'))" title="Export Conversation">⬇️</div>
    <script>
    window.addEventListener('clearChat', function() {
        window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', key: 'clear_chat', value: true}, '*');
    });
    window.addEventListener('exportChat', function() {
        window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', key: 'export_chat', value: true}, '*');
    });
    </script>
    ''', unsafe_allow_html=True)
    # Handle clear/export in Streamlit
    if st.session_state.get('clear_chat', False):
        clear_conversation()
        st.session_state['clear_chat'] = False
        st.rerun()
    if st.session_state.get('export_chat', False):
        export_conversation()
        st.session_state['export_chat'] = False

def show_toast(message: str, success: bool = True):
    """Show a toast notification with animation"""
    color = '#10b981' if success else '#ef4444'
    st.markdown(f'<div class="toast" style="border-left: 6px solid {color};">{message}</div>', unsafe_allow_html=True) 