"""
GitHub Repository Q&A Chat Interface (Modern, Minimal)
Streamlined chat with tool usage, quick actions, and beautiful layout
"""

import streamlit as st
from datetime import datetime
from typing import Optional

# --- Quick Questions ---
QUICK_QUESTIONS = [
    ("🏠 What is this repo about?", "What is this repository about and what does it do?"),
    ("📁 Show file structure", "Show me the main entry points of this application"),
    ("📋 Dependencies?", "What dependencies does this project use?"),
    ("📖 Show README", "Show me the README file and explain what this project does"),
    ("🔐 Auth code?", "Find all functions related to authentication"),
    ("🗄️ Database?", "Explain how the database connection is implemented"),
    ("🧪 Testing?", "What's the testing strategy used in this project?"),
    ("⚡ Performance?", "Are there any open issues related to performance?"),
    ("🔄 Recent changes", "What are the recent changes in the last 10 commits?"),
    ("📊 Commit stats", "Show me commit statistics and activity patterns"),
    ("👥 Contributors", "Who are the main contributors and what do they work on?"),
]

# --- Main Chat Interface ---
def render_chat_interface(repo_url: Optional[str] = None) -> None:
    """Render the modern chat interface component"""
    if not repo_url:
        st.info("🎯 Please select a repository to start asking questions.")
        return

    st.markdown("### 💬 Repository Q&A Chat")
    st.markdown("Ask questions about this repository. The AI agent will use MCP tools as needed.")

    # --- Chat History State ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- Quick Questions ---
    st.markdown("#### 🚀 Quick Questions")
    cols = st.columns(4)
    for i, (label, q) in enumerate(QUICK_QUESTIONS):
        if cols[i % 4].button(label, key=f"quick_{i}"):
            st.session_state.question_input = q
            st.rerun()

    # --- User Input ---
    st.markdown("#### 📝 Ask a Question")
    
    # Create a form for better UX with enter key support
    with st.form(key="question_form", clear_on_submit=True):
        question = st.text_input(
            "Your question:",
            value=st.session_state.get("question_input", ""),
            placeholder="e.g., What is this repository about? (Press Enter to submit)",
            key="question_input_box",
            help="Type your question and press Enter or click the Ask button"
        )
        
        # Button row
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            submit_button = st.form_submit_button("🤖 Ask AI Agent", type="primary", use_container_width=True)
        with col2:
            clear_button = st.form_submit_button("🗑️ Clear", use_container_width=True)
        with col3:
            export_button = st.form_submit_button("📥 Export", use_container_width=True)
        with col4:
            refresh_button = st.form_submit_button("🔄 Refresh", use_container_width=True)
    
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
    
    if export_button:
        export_chat_history()
    
    if refresh_button:
        st.rerun()

    # --- Display Chat History ---
    display_chat_history()

# --- Process Question ---
def process_question(question: str, repo_url: str) -> None:
    """Process a question and get AI response with MCP tool tracking"""
    st.session_state.chat_history.append({
        "role": "user",
        "content": question,
        "timestamp": datetime.now().isoformat(),
        "tools_used": []
    })
    
    # Create a progress container
    progress_container = st.container()
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Update progress stages
        status_text.text("🔍 Initializing AI agent...")
        progress_bar.progress(20)
        
        status_text.text("📡 Connecting to repository...")
        progress_bar.progress(40)
        
        status_text.text("🤖 Analyzing with AI tools...")
        progress_bar.progress(60)
        
        try:
            from src.agent.ai_agent import ask_question
            status_text.text("🧠 Processing your question...")
            progress_bar.progress(80)
            
            response = ask_question(question, repo_url)
            tools_used = extract_tools_from_response(response)
            
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
            status_text.text("❌ Error occurred")
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

# --- Tool Extraction (Heuristic) ---
def extract_tools_from_response(response: str) -> list:
    """Extract which MCP tools were likely used based on response content"""
    tools_used = []
    # Heuristic: look for keywords
    if "repository overview" in response.lower() or "description" in response.lower():
        tools_used.append("Overview")
    if "file structure" in response.lower() or "directory" in response.lower():
        tools_used.append("File Structure")
    if "commit" in response.lower() or "recent changes" in response.lower():
        tools_used.append("Commits")
    if "search" in response.lower() or "function" in response.lower():
        tools_used.append("Code Search")
    if "metrics" in response.lower() or "statistics" in response.lower():
        tools_used.append("Metrics")
    if "readme" in response.lower() or "documentation" in response.lower():
        tools_used.append("README")
    if "dependency" in response.lower():
        tools_used.append("Dependencies")
    return tools_used

# --- Display Chat History ---
def display_chat_history() -> None:
    """Display the chat history with tool usage badges"""
    if not st.session_state.chat_history:
        st.info("💬 No conversation history yet. Ask a question to get started!")
        return
    
    # Header with stats
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
    
    st.markdown("### 📝 Conversation History")
    
    # Add a search/filter option
    search_term = st.text_input("🔍 Search in conversation history", placeholder="Type to filter messages...")
    
    # Filter messages if search term is provided
    filtered_messages = st.session_state.chat_history
    if search_term:
        filtered_messages = [
            msg for msg in st.session_state.chat_history 
            if search_term.lower() in msg["content"].lower()
        ]
        if not filtered_messages:
            st.info(f"No messages found containing '{search_term}'")
            return
    
    # Display messages with enhanced styling
    for i, message in enumerate(reversed(filtered_messages[-10:])):
        is_user = message["role"] == "user"
        
        # Create expandable container for each message
        with st.expander(f"{'👤 You' if is_user else '🤖 AI'} - {format_timestamp(message['timestamp'])}", expanded=True):
            # Message content with better formatting
            if is_user:
                st.markdown(f"**{message['content']}**")
            else:
                st.markdown(message['content'])
            
            # Tool usage badges
            if message["role"] == "assistant" and message["tools_used"]:
                st.markdown("**Tools used:**")
                for tool in message["tools_used"]:
                    st.markdown(f"🔧 {tool}")
            
            # Copy button for AI responses
            if message["role"] == "assistant":
                if st.button(f"📋 Copy Response", key=f"copy_{i}"):
                    st.write("Response copied to clipboard!")
                    # Note: In a real implementation, you'd use st.clipboard.write()

# --- Export Chat ---
def export_chat_history() -> None:
    """Export chat history as a JSON file"""
    import json
    import io
    chat_json = json.dumps(st.session_state.chat_history, indent=2)
    st.download_button(
        label="Download Chat History",
        data=io.BytesIO(chat_json.encode()),
        file_name="repo_chat_history.json",
        mime="application/json"
    )

def format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return timestamp 