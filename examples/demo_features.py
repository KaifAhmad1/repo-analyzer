"""
🚀 GitHub Repository Analyzer - Feature Demo
Comprehensive demonstration of all modern features and capabilities
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def demo_header():
    """Demo the beautiful animated header"""
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🚀 GitHub Repository Analyzer</h1>
        <p class="header-subtitle">Modern AI-Powered Repository Analysis with Beautiful UI</p>
    </div>
    """, unsafe_allow_html=True)

def demo_stats_cards():
    """Demo animated stats cards"""
    st.markdown("### 📊 Animated Statistics Cards")
    
    # Sample data
    stats = [
        {"label": "Files Analyzed", "value": "1,247", "icon": "📁"},
        {"label": "Lines of Code", "value": "45,892", "icon": "💻"},
        {"label": "Languages", "value": "8", "icon": "🔤"},
        {"label": "Issues Found", "value": "23", "icon": "🐛"},
    ]
    
    cols = st.columns(4)
    for i, stat in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stat['icon']} {stat['value']}</div>
                <div class="stat-label">{stat['label']}</div>
            </div>
            """, unsafe_allow_html=True)

def demo_modern_cards():
    """Demo modern card designs"""
    st.markdown("### 🎨 Modern Card Designs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="modern-card insight-card">
            <h3>💡 Repository Insights</h3>
            <p>This is a modern Python web application built with Streamlit and FastAPI. 
            It provides comprehensive repository analysis using AI agents and MCP servers.</p>
            <div style="margin-top: 16px;">
                <strong>Key Features:</strong>
                <ul>
                    <li>Modern UI with animations</li>
                    <li>AI-powered analysis</li>
                    <li>Interactive visualizations</li>
                    <li>Real-time data fetching</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card success-card">
            <h3>✅ Analysis Complete</h3>
            <p>Repository analysis completed successfully! All components have been analyzed 
            and insights have been generated.</p>
            <div style="margin-top: 16px;">
                <strong>Results:</strong>
                <ul>
                    <li>Code quality: Excellent</li>
                    <li>Security: No vulnerabilities found</li>
                    <li>Performance: Optimized</li>
                    <li>Documentation: Comprehensive</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

def demo_chat_interface():
    """Demo modern chat interface"""
    st.markdown("### 💬 Modern Chat Interface")
    
    st.markdown("""
    <div class="chat-container">
        <div class="chat-message user">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.2rem; margin-right: 8px;">👤</span>
                <strong>You</strong>
                <small style="margin-left: auto; opacity: 0.7;">14:32</small>
            </div>
            <div>What is this repository about?</div>
        </div>
        
        <div class="chat-message assistant">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.2rem; margin-right: 8px;">🤖</span>
                <strong>AI Assistant</strong>
                <small style="margin-left: auto; opacity: 0.7;">14:33</small>
            </div>
            <div>This is a GitHub Repository Analyzer built with modern technologies. It uses AI agents and MCP servers to provide comprehensive analysis of GitHub repositories. The application features a beautiful UI with animations, interactive visualizations, and real-time data fetching.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def demo_visualizations():
    """Demo interactive visualizations"""
    st.markdown("### 📊 Interactive Visualizations")
    
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    
    # Sample data
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    commits = np.random.poisson(5, 30)
    issues = np.random.poisson(2, 30)
    
    df = pd.DataFrame({
        'date': dates,
        'commits': commits,
        'issues': issues
    })
    
    # Activity chart
    fig = px.line(df, x='date', y=['commits', 'issues'], 
                  title="Repository Activity Over Time",
                  labels={'value': 'Count', 'variable': 'Activity Type'})
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Language distribution
    languages = ['Python', 'JavaScript', 'TypeScript', 'HTML', 'CSS', 'Docker']
    values = [45, 25, 15, 8, 5, 2]
    
    fig2 = px.pie(values=values, names=languages, 
                  title="Language Distribution",
                  color_discrete_sequence=px.colors.qualitative.Set3)
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig2, use_container_width=True)

def demo_timeline():
    """Demo timeline component"""
    st.markdown("### 🕒 Timeline Component")
    
    st.markdown("""
    <div class="timeline">
        <div class="timeline-item">
            <strong>a1b2c3d</strong><br>
            <em>Add modern UI components and animations</em><br>
            <small>By John Doe on Jan 15, 2024</small>
        </div>
        <div class="timeline-item">
            <strong>e4f5g6h</strong><br>
            <em>Implement MCP server integration</em><br>
            <small>By Jane Smith on Jan 14, 2024</small>
        </div>
        <div class="timeline-item">
            <strong>i7j8k9l</strong><br>
            <em>Add AI agent with tool calling</em><br>
            <small>By Bob Johnson on Jan 13, 2024</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

def demo_progress_bars():
    """Demo animated progress bars"""
    st.markdown("### 📈 Animated Progress Bars")
    
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span>Python</span>
            <span>45.2%</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: 45.2%;"></div>
        </div>
    </div>
    
    <div style="margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span>JavaScript</span>
            <span>25.8%</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: 25.8%;"></div>
        </div>
    </div>
    
    <div style="margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span>TypeScript</span>
            <span>15.3%</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: 15.3%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def demo_buttons():
    """Demo modern button styles"""
    st.markdown("### 🔘 Modern Button Styles")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <button class="modern-button">Primary Button</button>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <button class="modern-button secondary">Secondary</button>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <button class="modern-button success">Success</button>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <button class="modern-button warning">Warning</button>
        """, unsafe_allow_html=True)

def demo_loading_animations():
    """Demo loading animations"""
    st.markdown("### ⏳ Loading Animations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div class="loading-spinner"></div>
            <p>Loading data...</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div class="loading-pulse" style="width: 40px; height: 40px; background: var(--primary-color); border-radius: 50%; margin: 0 auto;"></div>
            <p>Processing...</p>
        </div>
        """, unsafe_allow_html=True)

def demo_notifications():
    """Demo notification system"""
    st.markdown("### 🔔 Notification System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="notification success">
            ✅ Success! Analysis completed.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="notification error">
            ❌ Error: Could not fetch data.
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="notification warning">
            ⚠️ Warning: Rate limit approaching.
        </div>
        """, unsafe_allow_html=True)

def demo_code_blocks():
    """Demo code block styling"""
    st.markdown("### 💻 Code Block Styling")
    
    st.markdown("""
    <div class="code-block">
import streamlit as st
import plotly.express as px

def create_chart():
    data = {
        'x': [1, 2, 3, 4, 5],
        'y': [10, 20, 30, 40, 50]
    }
    fig = px.line(data, x='x', y='y')
    st.plotly_chart(fig)

if __name__ == "__main__":
    create_chart()
    </div>
    """, unsafe_allow_html=True)

def demo_file_tree():
    """Demo file tree component"""
    st.markdown("### 📁 File Tree Component")
    
    st.markdown("""
    <div class="file-tree">
        <div class="file-item">
            <span class="file-icon">📁</span>
            <span>src/</span>
        </div>
        <div class="file-item" style="margin-left: 20px;">
            <span class="file-icon">📁</span>
            <span>ui/</span>
        </div>
        <div class="file-item" style="margin-left: 40px;">
            <span class="file-icon">📄</span>
            <span>chat_interface.py</span>
        </div>
        <div class="file-item" style="margin-left: 40px;">
            <span class="file-icon">📄</span>
            <span>repository_selector.py</span>
        </div>
        <div class="file-item" style="margin-left: 20px;">
            <span class="file-icon">📁</span>
            <span>servers/</span>
        </div>
        <div class="file-item" style="margin-left: 40px;">
            <span class="file-icon">📄</span>
            <span>mcp_client.py</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def demo_floating_actions():
    """Demo floating action buttons"""
    st.markdown("### 🎯 Floating Action Buttons")
    
    st.markdown("""
    <div class="fab" onclick="alert('Clear chat clicked!')">🗑️</div>
    <div class="fab" style="bottom: 100px;" onclick="alert('Export clicked!')">📥</div>
    <div class="fab" style="bottom: 170px;" onclick="alert('Settings clicked!')">⚙️</div>
    """, unsafe_allow_html=True)

def main():
    """Main demo function"""
    
    # Load CSS
    with open("src/ui/modern_styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Page config
    st.set_page_config(
        page_title="🚀 Feature Demo",
        page_icon="🚀",
        layout="wide"
    )
    
    # Demo sections
    demo_header()
    
    st.markdown("---")
    demo_stats_cards()
    
    st.markdown("---")
    demo_modern_cards()
    
    st.markdown("---")
    demo_chat_interface()
    
    st.markdown("---")
    demo_visualizations()
    
    st.markdown("---")
    demo_timeline()
    
    st.markdown("---")
    demo_progress_bars()
    
    st.markdown("---")
    demo_buttons()
    
    st.markdown("---")
    demo_loading_animations()
    
    st.markdown("---")
    demo_notifications()
    
    st.markdown("---")
    demo_code_blocks()
    
    st.markdown("---")
    demo_file_tree()
    
    st.markdown("---")
    demo_floating_actions()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6c757d; padding: 20px;'>
        <p>🚀 Modern UI • 🤖 AI-Powered • 📊 Rich Insights</p>
        <p>Built with ❤️ using Streamlit, AI agents, and MCP servers</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 