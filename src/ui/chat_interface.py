"""
GitHub Repository Q&A Chat Interface
Clean, intuitive interface for repository analysis questions
"""

import streamlit as st
from datetime import datetime
from typing import Optional

def render_chat_interface(repo_url: Optional[str] = None, agent_type: str = "Single Agent") -> None:
    """Render the enhanced chat interface component"""
    
    if not repo_url:
        st.info("🎯 Please select a repository to start asking questions.")
        return
    
    st.markdown("### 💬 Repository Analysis Q&A")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Question input with better UX
    st.markdown("#### 📝 Ask a Question")
    question = st.text_area(
        "Enter your question about this repository:",
        placeholder="e.g., What is this repository about? Show me the main entry points. What are the recent changes?",
        height=80,
        key="question_input"
    )
    
    # Quick question categories
    st.markdown("#### 🚀 Quick Questions")
    
    # Repository Overview Questions
    st.markdown("**📊 Repository Overview**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 What is this repo about?", key="overview_1", use_container_width=True):
            st.session_state.question_input = "What is this repository about and what does it do?"
            st.rerun()
        if st.button("📁 Show me the file structure", key="overview_2", use_container_width=True):
            st.session_state.question_input = "Show me the main entry points of this application"
            st.rerun()
    
    with col2:
        if st.button("📋 What are the dependencies?", key="overview_3", use_container_width=True):
            st.session_state.question_input = "What dependencies does this project use?"
            st.rerun()
        if st.button("📖 Show me the README", key="overview_4", use_container_width=True):
            st.session_state.question_input = "Show me the README file and explain what this project does"
            st.rerun()
    
    # Code Analysis Questions
    st.markdown("**🔍 Code Analysis**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Find authentication code", key="code_1", use_container_width=True):
            st.session_state.question_input = "Find all functions related to authentication"
            st.rerun()
        if st.button("🗄️ Database implementation", key="code_2", use_container_width=True):
            st.session_state.question_input = "Explain how the database connection is implemented"
            st.rerun()
    
    with col2:
        if st.button("🧪 Testing strategy", key="code_3", use_container_width=True):
            st.session_state.question_input = "What's the testing strategy used in this project?"
            st.rerun()
        if st.button("⚡ Performance issues", key="code_4", use_container_width=True):
            st.session_state.question_input = "Are there any open issues related to performance?"
            st.rerun()
    
    # Activity Questions
    st.markdown("**📈 Recent Activity**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Recent changes", key="activity_1", use_container_width=True):
            st.session_state.question_input = "What are the recent changes in the last 10 commits?"
            st.rerun()
        if st.button("🐛 Open issues", key="activity_2", use_container_width=True):
            st.session_state.question_input = "Show me the open issues and their status"
            st.rerun()
    
    with col2:
        if st.button("📊 Commit statistics", key="activity_3", use_container_width=True):
            st.session_state.question_input = "Show me commit statistics and activity patterns"
            st.rerun()
        if st.button("👥 Contributors", key="activity_4", use_container_width=True):
            st.session_state.question_input = "Who are the main contributors and what do they work on?"
            st.rerun()
    
    # Ask button with better styling
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🤖 Ask AI Agent", type="primary", use_container_width=True):
            if question.strip():
                process_question(question, repo_url, agent_type)
                st.session_state.question_input = ""
                st.rerun()
            else:
                st.warning("⚠️ Please enter a question.")
    
    # Display chat history
    display_chat_history()

def process_question(question: str, repo_url: str, agent_type: str) -> None:
    """Process a question and get AI response"""
    
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": question,
        "timestamp": datetime.now().isoformat()
    })
    
    # Get AI response with progress indicator
    with st.spinner("🤖 Analyzing repository with AI agent..."):
        try:
            from src.agent.ai_agent import ask_question
            
            response = ask_question(question, repo_url)
            
            # Add AI response to history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            error_response = f"❌ Error getting AI response: {str(e)}"
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": error_response,
                "timestamp": datetime.now().isoformat()
            })

def display_chat_history() -> None:
    """Display the chat history with better formatting"""
    
    if not st.session_state.chat_history:
        return
    
    st.markdown("### 📝 Conversation History")
    
    # Chat controls
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("📥 Export Chat"):
            export_chat_history()
    
    # Display messages with better formatting
    for i, message in enumerate(reversed(st.session_state.chat_history[-10:])):  # Show last 10
        is_user = message["role"] == "user"
        
        # Create expander with better styling
        with st.expander(
            f"{'👤 You' if is_user else '🤖 AI'} - {format_timestamp(message['timestamp'])}",
            expanded=(i == 0)  # Expand the most recent message
        ):
            if is_user:
                st.markdown(f"**Question:** {message['content']}")
            else:
                st.markdown(f"**Answer:**")
                st.markdown(message['content'])

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%H:%M")
    except:
        return timestamp

def export_chat_history() -> None:
    """Export chat history to a file"""
    if not st.session_state.chat_history:
        st.warning("No chat history to export.")
        return
    
    # Create export content
    export_content = "# GitHub Repository Analysis Chat History\n\n"
    export_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for message in st.session_state.chat_history:
        role = "User" if message["role"] == "user" else "AI"
        timestamp = format_timestamp(message["timestamp"])
        export_content += f"## {role} ({timestamp})\n\n"
        export_content += f"{message['content']}\n\n"
        export_content += "---\n\n"
    
    # Create download button
    st.download_button(
        label="📥 Download Chat History",
        data=export_content,
        file_name=f"repository_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )

def render_chat_stats() -> None:
    """Render enhanced chat statistics"""
    
    if "chat_history" not in st.session_state or not st.session_state.chat_history:
        return
    
    st.markdown("### 📊 Chat Statistics")
    
    total_messages = len(st.session_state.chat_history)
    user_messages = len([m for m in st.session_state.chat_history if m["role"] == "user"])
    ai_messages = len([m for m in st.session_state.chat_history if m["role"] == "assistant"])
    
    # Create metrics with better styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💬 Total Messages", total_messages)
    
    with col2:
        st.metric("👤 Your Questions", user_messages)
    
    with col3:
        st.metric("🤖 AI Responses", ai_messages)
    
    with col4:
        if user_messages > 0:
            avg_length = sum(len(m["content"]) for m in st.session_state.chat_history if m["role"] == "user") / user_messages
            st.metric("📏 Avg Question Length", f"{avg_length:.0f} chars")
        else:
            st.metric("📏 Avg Question Length", "0 chars") 