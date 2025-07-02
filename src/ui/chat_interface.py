"""
GitHub Repository Q&A Chat Interface (Enhanced)
Clean chat interface with enhanced visual appeal and better UX
"""

import streamlit as st
from datetime import datetime
from typing import Optional

# --- Quick Questions - Enhanced set ---
QUICK_QUESTIONS = [
    ("🏠 What is this repo about?", "What is this repository about and what does it do?"),
    ("📁 Show file structure", "Show me the main entry points of this application"),
    ("📋 Dependencies?", "What dependencies does this project use?"),
    ("📖 Show README", "Show me the README file and explain what this project does"),
    ("🔐 Auth code?", "Find all functions related to authentication"),
    ("🧪 Testing?", "What's the testing strategy used in this project?"),
    ("⚡ Performance?", "Are there any performance considerations in this codebase?"),
    ("🔄 Recent changes", "What are the recent changes in the last 10 commits?"),
]

# --- Main Chat Interface ---
def render_chat_interface(repo_url: Optional[str] = None) -> None:
    """Render the enhanced chat interface component"""
    if not repo_url:
        st.info("🎯 Please select a repository to start asking questions.")
        return

    st.markdown("### 💬 Repository Q&A Chat")
    st.markdown("Ask questions about this repository. The AI agent will analyze it for you with enhanced tools.")

    # --- Chat History State ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- Quick Questions with enhanced layout ---
    st.markdown("#### 🚀 Quick Questions")
    st.markdown("Click on any question to get instant insights:")
    
    # Create a grid layout for quick questions
    cols = st.columns(4)
    for i, (label, q) in enumerate(QUICK_QUESTIONS):
        if cols[i % 4].button(label, key=f"quick_{i}", use_container_width=True):
            st.session_state.question_input = q
            st.rerun()

    # --- User Input with enhanced styling ---
    st.markdown("#### 📝 Ask a Custom Question")
    
    # Create a form for better UX with enter key support
    with st.form(key="question_form", clear_on_submit=True):
        question = st.text_input(
            "Your question:",
            value=st.session_state.get("question_input", ""),
            placeholder="e.g., What is this repository about? (Press Enter to submit)",
            key="question_input_box",
            help="Type your question and press Enter or click the Ask button"
        )
        
        # Button row with enhanced styling
        col1, col2 = st.columns([3, 1])
        with col1:
            submit_button = st.form_submit_button("🤖 Ask AI Agent", type="primary", use_container_width=True)
        with col2:
            clear_button = st.form_submit_button("🗑️ Clear", use_container_width=True)
    
    # Handle form submissions
    if submit_button and question.strip():
        process_question(question, repo_url)
        st.session_state.question_input = ""
        st.rerun()
    elif submit_button and not question.strip():
        st.warning("⚠️ Please enter a question.")
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()

    # --- Display Chat History ---
    display_chat_history()

# --- Process Question with enhanced spinners ---
def process_question(question: str, repo_url: str) -> None:
    """Process a question and get AI response with enhanced progress tracking"""
    st.session_state.chat_history.append({
        "role": "user",
        "content": question,
        "timestamp": datetime.now().isoformat()
    })
    
    # Enhanced progress display with multiple stages
    with st.spinner("🔄 Initializing AI analysis..."):
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Stage 1: Repository connection
            status_text.text("🔗 Connecting to repository...")
            progress_bar.progress(20)
            
            # Stage 2: Analysis preparation
            status_text.text("🔍 Preparing analysis tools...")
            progress_bar.progress(40)
            
            try:
                from src.agent.ai_agent import ask_question
                
                # Stage 3: AI processing
                status_text.text("🤖 AI is analyzing your question...")
                progress_bar.progress(60)
                
                # Stage 4: Generating response
                status_text.text("🧠 Generating comprehensive response...")
                progress_bar.progress(80)
                
                with st.spinner("🤖 AI is thinking..."):
                    response, tools_used = ask_question(question, repo_url)
                
                # Stage 5: Completion
                status_text.text("✅ Response ready!")
                progress_bar.progress(100)
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().isoformat(),
                    "tools_used": tools_used
                })
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                status_text.text("❌ Error occurred during analysis")
                progress_bar.progress(100)
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"❌ Error: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                    "tools_used": []
                })
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()

# --- Display Chat History with enhanced styling ---
def display_chat_history() -> None:
    """Display the chat history with enhanced visual appeal"""
    if not st.session_state.chat_history:
        st.info("💬 No conversation history yet. Ask a question to get started!")
        return
    
    # Enhanced header with stats
    st.markdown("#### 📊 Conversation Statistics")
    
    total_messages = len(st.session_state.chat_history)
    user_messages = len([m for m in st.session_state.chat_history if m["role"] == "user"])
    ai_messages = len([m for m in st.session_state.chat_history if m["role"] == "assistant"])
    
    # Calculate total tools used
    all_tools_used = []
    for message in st.session_state.chat_history:
        if message["role"] == "assistant" and message.get("tools_used"):
            all_tools_used.extend(message["tools_used"])
    unique_tools_used = len(set(all_tools_used))
    
    # Enhanced metrics display
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💬 Total Messages", total_messages)
    with col2:
        st.metric("👤 Your Questions", user_messages)
    with col3:
        st.metric("🤖 AI Responses", ai_messages)
    with col4:
        st.metric("🔧 Tools Used", f"{unique_tools_used} unique")
    
    st.markdown("---")
    
    # Enhanced message display
    st.markdown("#### 💭 Conversation History")
    
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(f"**{message['content']}**")
                st.caption(f"📅 {format_timestamp(message['timestamp'])}")
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])
                st.caption(f"📅 {format_timestamp(message['timestamp'])}")
                
                # Enhanced tool usage display
                if message.get("tools_used") and st.session_state.get("show_tool_usage", True):
                    st.markdown("**🔧 Tools Used:**")
                    for tool in message["tools_used"]:
                        st.write(f"• {tool}")

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%H:%M:%S")
    except:
        return timestamp 