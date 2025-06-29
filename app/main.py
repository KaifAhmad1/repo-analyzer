"""
🎨 Main Streamlit Application

Modern, responsive GitHub Repository Analyzer with beautiful UI,
themes, animations, and AI-powered analysis.
"""

import streamlit as st
import asyncio
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import custom modules
from ui.themes import ThemeManager
from ui.components import ChatInterface, RepositorySelector, AnalyticsDashboard
from ui.animations import LoadingAnimation, SuccessAnimation
from core.agent import RepositoryAgent
from config.settings import load_settings

# Configure page
st.set_page_config(
    page_title="🔍 GitHub Repository Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-username/repo-analyzer',
        'Report a bug': 'https://github.com/your-username/repo-analyzer/issues',
        'About': 'GitHub Repository Analyzer - AI-powered repository analysis'
    }
)

# Initialize theme manager
theme_manager = ThemeManager()

def main():
    """Main application function with modern UI and animations."""
    
    # Apply custom CSS and theme
    theme_manager.apply_theme()
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'selected_repo' not in st.session_state:
        st.session_state.selected_repo = None
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    
    # Header with animations
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="header-container">
                <h1 class="main-title">
                    🔍 GitHub Repository Analyzer
                </h1>
                <p class="subtitle">
                    AI-powered analysis with beautiful insights
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Sidebar with modern design
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h3>⚙️ Settings</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Repository selector
        repo_selector = RepositorySelector()
        selected_repo = repo_selector.render()
        
        if selected_repo:
            st.session_state.selected_repo = selected_repo
            st.success(f"✅ Selected: {selected_repo}")
        
        # Theme selector
        st.markdown("### 🎨 Theme")
        theme = st.selectbox(
            "Choose theme",
            ["Auto", "Light", "Dark"],
            key="theme_selector"
        )
        theme_manager.set_theme(theme)
        
        # AI Model selector
        st.markdown("### 🤖 AI Model")
        model = st.selectbox(
            "Select AI model",
            ["GPT-4", "Claude-3", "GPT-3.5"],
            key="model_selector"
        )
        
        # Settings
        st.markdown("### ⚙️ Settings")
        response_length = st.slider(
            "Response Length",
            min_value=100,
            max_value=1000,
            value=300,
            step=50
        )
        
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📊 Generate Report", use_container_width=True):
            if st.session_state.selected_repo:
                generate_report(st.session_state.selected_repo)
    
    # Main content area
    if st.session_state.selected_repo:
        show_main_interface()
    else:
        show_welcome_screen()

def show_main_interface():
    """Show the main analysis interface."""
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Chat Analysis", 
        "📊 Analytics", 
        "🗺️ Repository Map", 
        "📈 Insights"
    ])
    
    with tab1:
        show_chat_interface()
    
    with tab2:
        show_analytics_dashboard()
    
    with tab3:
        show_repository_map()
    
    with tab4:
        show_insights()

def show_chat_interface():
    """Show the chat interface with modern design."""
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Messages display
        messages_container = st.container()
        
        with messages_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Input area
        input_container = st.container()
        
        with input_container:
            # Question input with modern styling
            question = st.chat_input(
                "Ask a question about the repository...",
                key="chat_input"
            )
            
            if question:
                # Add user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": question
                })
                
                # Show loading animation
                with st.spinner("🤖 Analyzing..."):
                    # Process question
                    response = process_question(question)
                    
                    # Add AI response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                
                # Show success animation
                SuccessAnimation.show()
                
                # Rerun to update chat
                st.rerun()

def show_analytics_dashboard():
    """Show analytics dashboard with charts and metrics."""
    
    if not st.session_state.selected_repo:
        st.info("Please select a repository first.")
        return
    
    # Dashboard header
    st.markdown("""
    <div class="dashboard-header">
        <h2>📊 Repository Analytics</h2>
        <p>Comprehensive analysis of {}</p>
    </div>
    """.format(st.session_state.selected_repo), unsafe_allow_html=True)
    
    # Metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📁 Files",
            value="1,234",
            delta="+12%"
        )
    
    with col2:
        st.metric(
            label="👥 Contributors",
            value="45",
            delta="+3"
        )
    
    with col3:
        st.metric(
            label="🔄 Commits",
            value="2,567",
            delta="+89"
        )
    
    with col4:
        st.metric(
            label="⭐ Stars",
            value="12.5k",
            delta="+234"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Activity Over Time")
        # TODO: Add activity chart
        st.info("Activity chart coming soon...")
    
    with col2:
        st.markdown("### 🗂️ File Types")
        # TODO: Add file type chart
        st.info("File type chart coming soon...")

def show_repository_map():
    """Show interactive repository map."""
    
    st.markdown("""
    <div class="map-header">
        <h2>🗺️ Repository Structure</h2>
        <p>Interactive visualization of the repository structure</p>
    </div>
    """, unsafe_allow_html=True)
    
    # TODO: Add interactive repository map
    st.info("Interactive repository map coming soon...")

def show_insights():
    """Show AI-generated insights."""
    
    st.markdown("""
    <div class="insights-header">
        <h2>📈 AI Insights</h2>
        <p>Intelligent analysis and recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # TODO: Add AI insights
    st.info("AI insights coming soon...")

def show_welcome_screen():
    """Show welcome screen with modern design."""
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Welcome to GitHub Repository Analyzer</h1>
        <p class="hero-subtitle">
            Discover the power of AI-driven repository analysis with beautiful visualizations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 Smart AI Analysis</h3>
            <p>Ask questions in natural language and get intelligent answers</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🎨 Beautiful UI</h3>
            <p>Modern, responsive design with smooth animations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Rich Visualizations</h3>
            <p>Interactive charts, graphs, and repository maps</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Real-time Analysis</h3>
            <p>Get instant insights and live updates</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Example questions
    st.markdown("### 💡 Example Questions")
    
    example_questions = [
        "What is this repository about?",
        "Show me the main entry points",
        "What are the recent changes?",
        "Find all authentication functions",
        "What dependencies does this project use?",
        "Are there any open issues related to performance?",
        "Explain how the database connection is implemented",
        "What's the testing strategy used in this project?"
    ]
    
    for i, question in enumerate(example_questions, 1):
        st.markdown(f"**{i}.** {question}")

def process_question(question: str) -> str:
    """Process a question using the AI agent."""
    
    # Initialize agent if not exists
    if st.session_state.agent is None:
        st.session_state.agent = RepositoryAgent()
    
    # TODO: Implement actual question processing
    # For now, return a placeholder response
    return f"I understand you're asking about {st.session_state.selected_repo}: {question}. This feature is coming soon!"

def generate_report(repository: str):
    """Generate a comprehensive repository report."""
    
    with st.spinner("📊 Generating comprehensive report..."):
        # TODO: Implement report generation
        st.success("Report generation feature coming soon!")

if __name__ == "__main__":
    main() 