"""
GitHub Repository Q&A Chat Interface (Enhanced)
Clean chat interface with enhanced visual appeal and better UX
"""

import streamlit as st
from datetime import datetime
from typing import Optional
import time

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

# --- Processing States ---
PROCESSING_STATES = [
    "🔗 Connecting to repository...",
    "🔍 Initializing analysis tools...",
    "🤖 AI agent is thinking...",
    "📊 Gathering repository data...",
    "🔧 Using MCP servers...",
    "🧠 Generating response...",
    "✅ Finalizing results..."
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
    
    if "processing" not in st.session_state:
        st.session_state.processing = False

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
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            submit_button = st.form_submit_button("🤖 Ask AI Agent", type="primary", use_container_width=True)
        with col2:
            summarize_button = st.form_submit_button("📊 Summarize", use_container_width=True)
        with col3:
            clear_button = st.form_submit_button("🗑️ Clear", use_container_width=True)
    
    # Handle form submissions
    if submit_button and question.strip():
        process_question(question, repo_url, "chat")
        st.session_state.question_input = ""
        st.rerun()
    elif submit_button and not question.strip():
        st.warning("⚠️ Please enter a question.")
    
    if summarize_button and question.strip():
        process_question(question, repo_url, "summarize")
        st.session_state.question_input = ""
        st.rerun()
    elif summarize_button and not question.strip():
        st.warning("⚠️ Please enter a question for summarization.")
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()

    # --- Display Chat History ---
    display_chat_history()

# --- Process Question with enhanced spinners ---
def process_question(question: str, repo_url: str, mode: str = "chat") -> None:
    """Process a question and get AI response with enhanced progress tracking and tool status updates"""
    st.session_state.chat_history.append({
        "role": "user",
        "content": question,
        "timestamp": datetime.now().isoformat(),
        "mode": mode
    })
    
    # Set processing state
    st.session_state.processing = True
    
    # Enhanced progress display with multiple stages
    progress_container = st.container()
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            from src.agent.ai_agent import ask_repository_question
            from src.servers.server_manager import get_servers_status
            
            # Get server status for tracking
            server_status = get_servers_status()
            active_servers = [name for name, info in server_status["servers"].items() if info["running"]]
            
            # Stage 1: Repository connection
            status_text.text("🔗 Connecting to repository...")
            progress_bar.progress(10)
            time.sleep(0.5)
            
            # Stage 2: Analysis preparation
            status_text.text("🔍 Preparing analysis tools...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            # Stage 3: Server status check
            status_text.text(f"🔧 Checking MCP servers ({len(active_servers)} active)...")
            progress_bar.progress(30)
            time.sleep(0.5)
            
            # Stage 4: AI processing
            status_text.text("🤖 AI agent is analyzing your question...")
            progress_bar.progress(50)
            
            # Stage 5: Generating response
            status_text.text("🧠 Generating comprehensive response...")
            progress_bar.progress(70)
            
            def status_callback(msg):
                status_text.text(f"🛠️ {msg}")
            
            with st.spinner("🤖 AI is thinking..."):
                response, tools_used = ask_repository_question(question, repo_url, status_callback=status_callback)
            
            # Stage 6: Completion
            status_text.text("✅ Response ready!")
            progress_bar.progress(100)
            time.sleep(0.5)
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat(),
                "tools_used": tools_used,
                "mode": mode,
                "servers_used": active_servers
            })
            
        except Exception as e:
            status_text.text("❌ Error occurred during analysis")
            progress_bar.progress(100)
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "tools_used": [],
                "mode": mode,
                "servers_used": []
            })
        
        finally:
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            st.session_state.processing = False

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
    all_servers_used = []
    for message in st.session_state.chat_history:
        if message["role"] == "assistant":
            if message.get("tools_used"):
                all_tools_used.extend(message["tools_used"])
            if message.get("servers_used"):
                all_servers_used.extend(message["servers_used"])
    
    unique_tools_used = len(set(all_tools_used))
    unique_servers_used = len(set(all_servers_used))
    
    # Enhanced metrics display
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("💬 Total Messages", total_messages)
    with col2:
        st.metric("👤 Your Questions", user_messages)
    with col3:
        st.metric("🤖 AI Responses", ai_messages)
    with col4:
        st.metric("🔧 Tools Used", f"{unique_tools_used} unique")
    with col5:
        st.metric("🖥️ Servers Used", f"{unique_servers_used} active")
    
    st.markdown("---")
    
    # Enhanced message display
    st.markdown("#### 💭 Conversation History")
    
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(f"**{message['content']}**")
                st.caption(f"📅 {format_timestamp(message['timestamp'])}")
                if message.get("mode") == "summarize":
                    st.info("📊 Summarization request")
        else:
            with st.chat_message("assistant"):
                # Enhanced response with green highlights
                response_content = message["content"]
                if message.get("mode") == "summarize":
                    response_content = f"📊 **Summary:**\n\n{response_content}"
                
                # Apply green highlighting for better visibility
                st.markdown(f"""
                <div style="background-color: #f0f9ff; border-left: 4px solid #10b981; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                    {response_content}
                </div>
                """, unsafe_allow_html=True)
                
                st.caption(f"📅 {format_timestamp(message['timestamp'])}")
                
                # Enhanced tool and server usage display
                if message.get("tools_used") and st.session_state.get("show_tool_usage", True):
                    st.markdown("**🔧 Analysis Tools Used:**")
                    # Group tools by server
                    server_tools = {}
                    for tool in message["tools_used"]:
                        if '.' in tool:
                            server, tool_name = tool.split('.', 1)
                            if server not in server_tools:
                                server_tools[server] = []
                            server_tools[server].append(tool_name)
                        else:
                            if 'unknown' not in server_tools:
                                server_tools['unknown'] = []
                            server_tools['unknown'].append(tool)
                    
                    # Display grouped by server
                    for server, tools in server_tools.items():
                        server_icon = {
                            'file_content': '📄',
                            'repository_structure': '📁',
                            'commit_history': '📝',
                            'code_search': '🔍',
                            'unknown': '❓'
                        }.get(server, '🔧')
                        
                        st.markdown(f"**{server_icon} {server.replace('_', ' ').title()} Server:**")
                        for tool in tools:
                            st.write(f"  - {tool}")
                        st.markdown("")
                
                if message.get("servers_used"):
                    st.markdown("**🖥️ Active MCP Servers:**")
                    for server in message["servers_used"]:
                        server_icon = {
                            'file_content': '📄',
                            'repository_structure': '📁',
                            'commit_history': '📝',
                            'code_search': '🔍'
                        }.get(server, '🖥️')
                        st.write(f"• {server_icon} {server.replace('_', ' ').title()}")

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%H:%M:%S")
    except:
        return timestamp 