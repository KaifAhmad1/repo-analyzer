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
                <div class="chat-message-header">
                    <span class="chat-icon">{icon}</span>
                    <strong>{'You' if is_user else 'AI Assistant'}</strong>
                    <small>{message.get('timestamp', 'Unknown')}</small>
                </div>
                <div class="chat-content">{message["content"]}</div>
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
        "analyze_repository": "Performed comprehensive repository analysis",
        "file_content_server": "Read file contents and structure",
        "repository_structure_server": "Analyzed directory structure",
        "commit_history_server": "Examined commit history and changes",
        "issues_server": "Queried issues and pull requests",
        "code_search_server": "Searched for specific code patterns"
    }
    return tool_descriptions.get(tool_name, "Analyzed repository data")

def render_quick_questions(ai_agent: Dict[str, Any]):
    """Render quick question buttons with modern styling"""
    st.markdown("### 💡 Quick Questions")
    
    quick_questions = [
        {
            "question": "What is this repository about?",
            "icon": "🏠",
            "description": "Get an overview of the project",
            "category": "Overview"
        },
        {
            "question": "Show me the main entry points",
            "icon": "🚪",
            "description": "Find the main application files",
            "category": "Structure"
        },
        {
            "question": "What are the recent changes?",
            "icon": "🔄",
            "description": "See recent commits and updates",
            "category": "Activity"
        },
        {
            "question": "Find authentication-related code",
            "icon": "🔐",
            "description": "Locate security and auth code",
            "category": "Security"
        },
        {
            "question": "What dependencies does this use?",
            "icon": "📦",
            "description": "Analyze project dependencies",
            "category": "Dependencies"
        },
        {
            "question": "Are there any performance issues?",
            "icon": "⚡",
            "description": "Check for performance concerns",
            "category": "Performance"
        },
        {
            "question": "Explain the database implementation",
            "icon": "🗄️",
            "description": "Understand data storage",
            "category": "Data"
        },
        {
            "question": "What's the testing strategy?",
            "icon": "🧪",
            "description": "Review testing approach",
            "category": "Testing"
        }
    ]
    
    # Group questions by category
    categories = {}
    for q in quick_questions:
        if q["category"] not in categories:
            categories[q["category"]] = []
        categories[q["category"]].append(q)
    
    # Create tabs for different categories
    if len(categories) > 1:
        tab_names = list(categories.keys())
        tabs = st.tabs([f"📂 {cat}" for cat in tab_names])
        
        for i, (category, questions) in enumerate(categories.items()):
            with tabs[i]:
                render_question_grid(questions, ai_agent)
    else:
        # Single category - no tabs needed
        render_question_grid(quick_questions, ai_agent)

def render_question_grid(questions: List[Dict], ai_agent: Dict[str, Any]):
    """Render a grid of quick question buttons"""
    cols = st.columns(2)
    for i, q in enumerate(questions):
        with cols[i % 2]:
            if st.button(
                f"{q['icon']} {q['question']}",
                key=f"quick_{i}_{q['category']}",
                help=q['description'],
                use_container_width=True
            ):
                process_question(ai_agent, q['question'])
                st.rerun()

def render_chat_input(ai_agent: Dict[str, Any]):
    """Render the chat input with modern styling"""
    st.markdown("### 💭 Ask a Question")
    
    # Chat input container
    col1, col2, col3 = st.columns([3, 1, 1])
    
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
    
    with col3:
        if st.button("🎯 Smart", help="Get AI-suggested questions", use_container_width=True):
            show_smart_suggestions(ai_agent)
    
    # Auto-submit on Enter
    if question and st.session_state.get("auto_submit", False):
        process_question(ai_agent, question)
        st.session_state.question_input = ""
        st.rerun()

def show_smart_suggestions(ai_agent: Dict[str, Any]):
    """Show AI-suggested questions based on repository context"""
    st.markdown("### 🎯 Smart Suggestions")
    
    suggestions = [
        "Analyze the code quality and complexity",
        "Find potential security vulnerabilities",
        "Identify performance bottlenecks",
        "Check for code duplication",
        "Review error handling patterns",
        "Analyze the API design",
        "Check for proper documentation",
        "Identify testing gaps"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(
                f"💡 {suggestion}",
                key=f"suggestion_{i}",
                use_container_width=True
            ):
                process_question(ai_agent, suggestion)
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
    """Generate repository overview analysis"""
    st.info("Repository overview analysis coming soon!")

def generate_code_analysis():
    """Generate code analysis"""
    st.info("Code analysis feature coming soon!")

def generate_issue_analysis():
    """Generate issue analysis"""
    st.info("Issue analysis feature coming soon!")

def render_response_with_formatting(response: str):
    """Render AI response with proper formatting"""
    # Split response into sections
    sections = response.split('\n\n')
    
    for section in sections:
        if section.strip().startswith('#'):
            # Headers
            level = section.count('#')
            text = section.strip('#').strip()
            st.markdown(f"{'#' * level} {text}")
        elif section.strip().startswith('```'):
            # Code blocks
            st.code(section.strip('```'), language='python')
        elif section.strip().startswith('- ') or section.strip().startswith('* '):
            # Lists
            items = [item.strip('- ').strip('* ').strip() for item in section.split('\n') if item.strip()]
            for item in items:
                st.markdown(f"• {item}")
        else:
            # Regular text
            st.markdown(section)

def clear_conversation():
    """Clear the conversation history"""
    if 'messages' in st.session_state:
        st.session_state.messages = []
    st.success("💬 Conversation cleared!")

def export_conversation():
    """Export conversation to JSON"""
    if 'messages' in st.session_state and st.session_state.messages:
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "repository": st.session_state.get("repository_url", ""),
            "messages": st.session_state.messages
        }
        
        # Create download button
        st.download_button(
            label="📥 Download Conversation",
            data=json.dumps(conversation_data, indent=2),
            file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    else:
        st.warning("No conversation to export")

def render_fab_buttons():
    """Render floating action buttons"""
    st.markdown("""
    <div class="fab-container">
        <div class="fab fab-primary" onclick="clearChat()" title="Clear Chat">🗑️</div>
        <div class="fab fab-secondary" onclick="exportChat()" title="Export Chat">📤</div>
        <div class="fab fab-success" onclick="shareChat()" title="Share Chat">📤</div>
    </div>
    <script>
    function clearChat() {
        // Clear chat functionality
        console.log('Clear chat clicked');
    }
    function exportChat() {
        // Export chat functionality
        console.log('Export chat clicked');
    }
    function shareChat() {
        // Share chat functionality
        console.log('Share chat clicked');
    }
    </script>
    """, unsafe_allow_html=True)

def show_toast(message: str, success: bool = True):
    """Show a toast notification"""
    toast_type = "success" if success else "error"
    st.markdown(f"""
    <div class="toast toast-{toast_type}">
        {message}
    </div>
    """, unsafe_allow_html=True) 