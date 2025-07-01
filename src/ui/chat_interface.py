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
    question = st.text_input(
        "Your question:",
        value=st.session_state.get("question_input", ""),
        placeholder="e.g., What is this repository about?",
        key="question_input_box"
    )
    ask_col, clear_col, export_col = st.columns([2,1,1])
    with ask_col:
        if st.button("🤖 Ask AI Agent", type="primary"):
            if question.strip():
                process_question(question, repo_url)
                st.session_state.question_input = ""
                st.rerun()
            else:
                st.warning("⚠️ Please enter a question.")
    with clear_col:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    with export_col:
        if st.button("📥 Export Chat"):
            export_chat_history()

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
    with st.spinner("🤖 Analyzing repository with AI agent..."):
        try:
            from src.agent.ai_agent import ask_question
            response = ask_question(question, repo_url)
            tools_used = extract_tools_from_response(response)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat(),
                "tools_used": tools_used
            })
        except Exception as e:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "tools_used": []
            })

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
        return
    st.markdown("### 📝 Conversation History")
    for i, message in enumerate(reversed(st.session_state.chat_history[-10:])):
        is_user = message["role"] == "user"
        with st.container():
            bubble_class = "chat-message user" if is_user else "chat-message ai"
            st.markdown(f"<div class='{bubble_class}'>", unsafe_allow_html=True)
            icon = "👤" if is_user else "🤖"
            st.markdown(f"<b>{icon} {'You' if is_user else 'AI'}:</b> {message['content']}", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:0.8em;color:#888;'>{format_timestamp(message['timestamp'])}</span>", unsafe_allow_html=True)
            if message["role"] == "assistant" and message["tools_used"]:
                st.markdown(
                    "<div style='margin-top:0.5em;'>" +
                    " ".join([f"<span class='tool-usage'>{tool}</span>" for tool in message["tools_used"]]) +
                    "</div>",
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

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