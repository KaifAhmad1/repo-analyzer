"""
Modern Chat Interface UI Component
Provides a beautiful, animated chat-like interface for interacting with the AI agent
"""

import streamlit as st
from typing import Dict, Any, List
import time
import json
from datetime import datetime

def render_chat_interface(ai_agent: Dict[str, Any]):
    """Render the modern chat interface"""
    
    # Chat header
    st.markdown("""
    <div class="modern-card">
        <h3>💬 AI Repository Assistant</h3>
        <p>Ask questions about the repository and get intelligent insights powered by AI.</p>
    </div>
    """, unsafe_allow_html=True)

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display conversation history
    display_conversation_history()
    
    # Quick questions
    render_quick_questions(ai_agent)
    
    # Chat input
    render_chat_input(ai_agent)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_conversation_history():
    """Display the conversation history with modern chat bubbles"""
    if 'messages' in st.session_state and st.session_state.messages:
        st.markdown("### 💭 Conversation History")
        
        for i, message in enumerate(st.session_state.messages):
            is_user = message["role"] == "user"
            bubble_class = "user" if is_user else "assistant"
            icon = "👤" if is_user else "🤖"
            
            # Create chat bubble
            st.markdown(f"""
            <div class="chat-message {bubble_class}">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 1.2rem; margin-right: 8px;">{icon}</span>
                    <strong>{'You' if is_user else 'AI Assistant'}</strong>
                    <small style="margin-left: auto; opacity: 0.7;">
                        {message.get('timestamp', 'Unknown')}
                    </small>
                </div>
                <div>{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show tools used if any
            if message.get("tools_used"):
                with st.expander(f"🔧 Tools Used ({len(message['tools_used'])})"):
                    for tool in message["tools_used"]:
                        st.markdown(f"• **{tool}**")
                        st.markdown(f"  - {get_tool_description(tool)}")
    else:
        # Empty state with animation
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #6c757d;">
            <div style="font-size: 4rem; margin-bottom: 16px;">💬</div>
            <h4>Start a conversation!</h4>
            <p>Ask questions about the repository to get started.</p>
        </div>
        """, unsafe_allow_html=True)

def get_tool_description(tool_name: str) -> str:
    """Get description for a tool"""
    tool_descriptions = {
        "get_repository_overview": "Retrieved comprehensive repository information",
        "search_code": "Searched for code patterns and functions",
        "get_recent_commits": "Fetched recent commit history",
        "get_issues": "Retrieved repository issues and pull requests",
        "analyze_repository": "Performed comprehensive repository analysis"
    }
    return tool_descriptions.get(tool_name, "Analyzed repository data")

def render_quick_questions(ai_agent: Dict[str, Any]):
    """Render quick question buttons with modern styling"""
    st.markdown("### 💡 Quick Questions")
    
    quick_questions = [
        {
            "question": "What is this repository about?",
            "icon": "🏠",
            "description": "Get an overview of the project"
        },
        {
            "question": "Show me the main entry points",
            "icon": "🚪",
            "description": "Find the main application files"
        },
        {
            "question": "What are the recent changes?",
            "icon": "🔄",
            "description": "See recent commits and updates"
        },
        {
            "question": "Find authentication-related code",
            "icon": "🔐",
            "description": "Locate security and auth code"
        },
        {
            "question": "What dependencies does this use?",
            "icon": "📦",
            "description": "Analyze project dependencies"
        },
        {
            "question": "Are there any performance issues?",
            "icon": "⚡",
            "description": "Check for performance concerns"
        },
        {
            "question": "Explain the database implementation",
            "icon": "🗄️",
            "description": "Understand data storage"
        },
        {
            "question": "What's the testing strategy?",
            "icon": "🧪",
            "description": "Review testing approach"
        }
    ]
    
    # Create a grid of quick question buttons
    cols = st.columns(2)
    for i, q in enumerate(quick_questions):
        with cols[i % 2]:
            if st.button(
                f"{q['icon']} {q['question']}",
                key=f"quick_{i}",
                help=q['description']
            ):
                process_question(ai_agent, q['question'])
                st.rerun()

def render_chat_input(ai_agent: Dict[str, Any]):
    """Render the chat input with modern styling"""
    st.markdown("### 💭 Ask a Question")
    
    # Chat input container
    col1, col2 = st.columns([4, 1])
    
    with col1:
        question = st.text_input(
            "Type your question here...",
            placeholder="e.g., What is this repository about? Show me the main entry points...",
            key="question_input",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("🚀 Ask AI", type="primary", use_container_width=True):
            if question:
                process_question(ai_agent, question)
                st.session_state.question_input = ""
                st.rerun()
    
    # Auto-submit on Enter
    if question and st.session_state.get("auto_submit", False):
        process_question(ai_agent, question)
        st.session_state.question_input = ""
        st.rerun()

def process_question(ai_agent: Dict[str, Any], question: str):
    """Process a question and get AI response with modern loading animation"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": question,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    
    # Show loading animation
    with st.spinner("🤖 AI is analyzing the repository..."):
        try:
            repo_url = st.session_state.get("repository_url", "")
            if not repo_url:
                st.error("❌ No repository selected. Please select a repository first.")
                return
            
            # Set environment variable for MCP servers
            import os
            os.environ['GITHUB_REPO_URL'] = repo_url
            
            # Import and call AI agent
            from src.agent.ai_agent import ask_question
            response = ask_question(ai_agent, question, repo_url)
            
            if response["success"]:
                # Add AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["response"],
                    "tools_used": response.get("tools_used", []),
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
                # Show success notification
                show_notification("✅ Response generated successfully!", "success")
            else:
                show_notification(f"❌ Error: {response['response']}", "error")
                
        except Exception as e:
            show_notification(f"❌ Error processing question: {str(e)}", "error")

def show_notification(message: str, type: str = "info"):
    """Show a modern notification"""
    notification_class = {
        "success": "notification success",
        "error": "notification error",
        "warning": "notification warning",
        "info": "notification"
    }.get(type, "notification")
    
    st.markdown(f"""
    <div class="{notification_class}">
        {message}
    </div>
    """, unsafe_allow_html=True)

def render_analysis_options():
    """Render additional analysis options with modern cards"""
    st.markdown("### 🔍 Advanced Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Repository Overview", use_container_width=True):
            generate_repository_overview()
    
    with col2:
        if st.button("📈 Code Analysis", use_container_width=True):
            generate_code_analysis()
    
    with col3:
        if st.button("🐛 Issue Analysis", use_container_width=True):
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
    """Render AI response with proper formatting and syntax highlighting"""
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
    """Clear the conversation history with confirmation"""
    if 'messages' in st.session_state:
        st.session_state.messages = []
        show_notification("🗑️ Conversation history cleared!", "success")

def export_conversation():
    """Export conversation to file with modern formatting"""
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
            label="📥 Download Conversation",
            data=json_str,
            file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def render_fab_buttons():
    """Render floating action buttons"""
    st.markdown("""
    <div class="fab" onclick="clearChat()">🗑️</div>
    <div class="fab" style="bottom: 100px;" onclick="exportChat()">📥</div>
    <script>
    function clearChat() {
        // Clear chat functionality
        console.log('Clear chat clicked');
    }
    function exportChat() {
        // Export chat functionality
        console.log('Export chat clicked');
    }
    </script>
    """, unsafe_allow_html=True)

def show_toast(message: str, success: bool = True):
    """Show a toast notification"""
    notification_type = "success" if success else "error"
    show_notification(message, notification_type) 