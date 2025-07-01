"""
Streamlined Chat Interface UI Component
Provides a clean Q&A interface for repository analysis
"""

import streamlit as st
from datetime import datetime
from typing import Optional

def render_chat_interface(repo_url: Optional[str] = None, agent_type: str = "Single Agent") -> None:
    """Render the chat interface component"""
    
    if not repo_url:
        st.info("Please select a repository to start asking questions.")
        return
    
    st.markdown("### 💬 Ask Questions About This Repository")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Question input
    question = st.text_area(
        "Enter your question:",
        placeholder="e.g., What is this repository about? Show me the main entry points. What are the recent changes?",
        height=100,
        key="question_input"
    )
    
    # Quick questions
    st.markdown("#### 💡 Quick Questions")
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
    for i, q in enumerate(quick_questions):
        with cols[i % 2]:
            if st.button(f"❓ {q[:30]}...", key=f"quick_{i}", use_container_width=True):
                st.session_state.question_input = q
                st.rerun()
    
    # Ask button
    if st.button("🤖 Ask AI Agent", type="primary"):
        if question.strip():
            process_question(question, repo_url, agent_type)
            st.session_state.question_input = ""
            st.rerun()
        else:
            st.warning("Please enter a question.")
    
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
    
    # Get AI response
    with st.spinner("🤖 Analyzing with AI agent..."):
        try:
            from src.agent.ai_agent import ask_question_advanced
            
            response = ask_question_advanced(
                question, 
                repo_url, 
                use_team=(agent_type == "Multi-Agent Team")
            )
            
            # Add AI response to history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            error_response = f"Error getting AI response: {str(e)}"
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": error_response,
                "timestamp": datetime.now().isoformat()
            })

def display_chat_history() -> None:
    """Display the chat history"""
    
    if not st.session_state.chat_history:
        return
    
    st.markdown("### 📝 Chat History")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Display messages
    for i, message in enumerate(reversed(st.session_state.chat_history[-10:])):  # Show last 10
        is_user = message["role"] == "user"
        
        with st.expander(
            f"{'👤 You' if is_user else '🤖 AI'} - {format_timestamp(message['timestamp'])}",
            expanded=(i == 0)  # Expand the most recent message
        ):
            if is_user:
                st.markdown(f"**Question:** {message['content']}")
            else:
                st.markdown(f"**Answer:** {message['content']}")

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%H:%M")
    except:
        return timestamp

def render_chat_stats() -> None:
    """Render chat statistics"""
    
    if "chat_history" not in st.session_state or not st.session_state.chat_history:
        return
    
    st.markdown("### 📊 Chat Statistics")
    
    total_messages = len(st.session_state.chat_history)
    user_messages = len([m for m in st.session_state.chat_history if m["role"] == "user"])
    ai_messages = len([m for m in st.session_state.chat_history if m["role"] == "assistant"])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Messages", total_messages)
    
    with col2:
        st.metric("Your Questions", user_messages)
    
    with col3:
        st.metric("AI Responses", ai_messages) 