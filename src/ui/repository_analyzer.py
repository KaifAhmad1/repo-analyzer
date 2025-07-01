"""
Enhanced Repository Analyzer UI Component
Provides advanced analysis features with modern UI
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

def render_repository_dashboard(repo_url: str, repo_data: Dict[str, Any]):
    """Render comprehensive repository dashboard"""
    
    st.markdown("""
    <div class="modern-card">
        <h3>📊 Repository Dashboard</h3>
        <p>Comprehensive analysis and insights for your repository</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different analysis sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Activity", "🔍 Code Analysis", "🐛 Issues & PRs", "👥 Contributors", "📊 Metrics"
    ])
    
    with tab1:
        render_activity_analysis(repo_url, repo_data)
    
    with tab2:
        render_code_analysis(repo_url, repo_data)
    
    with tab3:
        render_issues_analysis(repo_url, repo_data)
    
    with tab4:
        render_contributors_analysis(repo_url, repo_data)
    
    with tab5:
        render_metrics_analysis(repo_url, repo_data)

def render_activity_analysis(repo_url: str, repo_data: Dict[str, Any]):
    """Render activity analysis charts"""
    
    # Commit activity over time
    st.markdown("### 📈 Commit Activity")
    
    # Sample data - replace with actual data from MCP servers
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    commits = np.random.poisson(3, len(dates))  # Random commit data
    
    df_commits = pd.DataFrame({
        'date': dates,
        'commits': commits
    })
    
    fig = px.line(df_commits, x='date', y='commits',
                  title="Daily Commit Activity",
                  labels={'date': 'Date', 'commits': 'Number of Commits'})
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Activity heatmap
    st.markdown("### 🌡️ Activity Heatmap")
    
    # Create weekly activity data
    weeks = pd.date_range(start='2024-01-01', end='2024-12-31', freq='W')
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Generate random activity data
    activity_data = np.random.randint(0, 10, (len(weeks), 7))
    
    fig = go.Figure(data=go.Heatmap(
        z=activity_data,
        x=days,
        y=[w.strftime('%Y-%m-%d') for w in weeks],
        colorscale='Viridis',
        showscale=True
    ))
    
    fig.update_layout(
        title="Weekly Activity Heatmap",
        xaxis_title="Day of Week",
        yaxis_title="Week",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_code_analysis(repo_url: str, repo_data: Dict[str, Any]):
    """Render code analysis charts"""
    
    # Language distribution
    st.markdown("### 🔤 Language Distribution")
    
    languages = ['Python', 'JavaScript', 'TypeScript', 'HTML', 'CSS', 'Java', 'Go']
    percentages = [35, 25, 15, 10, 8, 5, 2]
    
    fig = px.pie(values=percentages, names=languages,
                 title="Code Language Distribution")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # File size distribution
    st.markdown("### 📁 File Size Analysis")
    
    file_types = ['Python', 'JavaScript', 'TypeScript', 'HTML', 'CSS']
    avg_sizes = [150, 80, 120, 45, 35]
    
    fig = px.bar(x=file_types, y=avg_sizes,
                 title="Average File Size by Type (KB)",
                 labels={'x': 'File Type', 'y': 'Average Size (KB)'})
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Code complexity analysis
    st.markdown("### 🧮 Code Complexity")
    
    files = ['main.py', 'utils.py', 'config.py', 'models.py', 'api.py', 'tests.py']
    complexity = [15, 8, 3, 12, 20, 6]
    lines = [200, 150, 80, 300, 400, 120]
    
    fig = px.scatter(x=lines, y=complexity, size=complexity,
                     title="Code Complexity vs Lines of Code",
                     labels={'x': 'Lines of Code', 'y': 'Cyclomatic Complexity'},
                     hover_data=[files])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)

def render_issues_analysis(repo_url: str, repo_data: Dict[str, Any]):
    """Render issues and PRs analysis"""
    
    # Issues over time
    st.markdown("### 🐛 Issues Timeline")
    
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    opened_issues = np.random.randint(5, 25, len(dates))
    closed_issues = np.random.randint(3, 20, len(dates))
    
    df_issues = pd.DataFrame({
        'date': dates,
        'opened': opened_issues,
        'closed': closed_issues
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_issues['date'], y=df_issues['opened'],
                             mode='lines+markers', name='Opened Issues',
                             line=dict(color='#ff6b6b')))
    fig.add_trace(go.Scatter(x=df_issues['date'], y=df_issues['closed'],
                             mode='lines+markers', name='Closed Issues',
                             line=dict(color='#51cf66')))
    
    fig.update_layout(
        title="Issues Opened vs Closed",
        xaxis_title="Month",
        yaxis_title="Number of Issues",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Issue types distribution
    st.markdown("### 🏷️ Issue Types")
    
    issue_types = ['Bug', 'Feature', 'Documentation', 'Enhancement', 'Question']
    counts = [45, 30, 15, 8, 2]
    
    fig = px.bar(x=issue_types, y=counts,
                 title="Issue Types Distribution",
                 labels={'x': 'Issue Type', 'y': 'Count'})
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Pull request analysis
    st.markdown("### 🔄 Pull Request Analysis")
    
    pr_status = ['Open', 'Merged', 'Closed', 'Draft']
    pr_counts = [12, 85, 8, 5]
    
    fig = px.pie(values=pr_counts, names=pr_status,
                 title="Pull Request Status")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)

def render_contributors_analysis(repo_url: str, repo_data: Dict[str, Any]):
    """Render contributors analysis"""
    
    # Top contributors
    st.markdown("### 👥 Top Contributors")
    
    contributors = ['alice', 'bob', 'charlie', 'diana', 'eve', 'frank']
    contributions = [150, 120, 95, 80, 65, 45]
    
    fig = px.bar(x=contributors, y=contributions,
                 title="Contributions by User",
                 labels={'x': 'Contributor', 'y': 'Contributions'})
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Contribution timeline
    st.markdown("### 📅 Contribution Timeline")
    
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='W')
    contributors_data = []
    
    for contributor in contributors[:3]:  # Top 3 contributors
        contributions = np.random.poisson(5, len(dates))
        for date, count in zip(dates, contributions):
            contributors_data.append({
                'date': date,
                'contributor': contributor,
                'contributions': count
            })
    
    df_contrib = pd.DataFrame(contributors_data)
    
    fig = px.line(df_contrib, x='date', y='contributions', color='contributor',
                  title="Contributions Over Time",
                  labels={'date': 'Date', 'contributions': 'Contributions'})
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)

def render_metrics_analysis(repo_url: str, repo_data: Dict[str, Any]):
    """Render repository metrics"""
    
    # Key metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card stat-card-primary">
            <div class="stat-icon">⭐</div>
            <div class="stat-number">1,234</div>
            <div class="stat-label">Stars</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card stat-card-success">
            <div class="stat-icon">🍴</div>
            <div class="stat-number">567</div>
            <div class="stat-label">Forks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card stat-card-warning">
            <div class="stat-icon">👀</div>
            <div class="stat-number">89</div>
            <div class="stat-label">Watchers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card stat-card-error">
            <div class="stat-icon">🐛</div>
            <div class="stat-number">23</div>
            <div class="stat-label">Open Issues</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Repository health score
    st.markdown("### 🏥 Repository Health Score")
    
    metrics = {
        'Documentation': 85,
        'Test Coverage': 78,
        'Code Quality': 92,
        'Security': 88,
        'Performance': 76,
        'Maintainability': 84
    }
    
    fig = go.Figure(data=go.Scatterpolar(
        r=list(metrics.values()),
        theta=list(metrics.keys()),
        fill='toself',
        name='Health Score'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Repository Health Radar Chart"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Growth metrics
    st.markdown("### 📈 Growth Metrics")
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    stars = [100, 150, 200, 280, 400, 600]
    forks = [20, 35, 50, 75, 120, 180]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=stars, mode='lines+markers',
                             name='Stars', line=dict(color='#ffd700')))
    fig.add_trace(go.Scatter(x=months, y=forks, mode='lines+markers',
                             name='Forks', line=dict(color='#ff6b6b')))
    
    fig.update_layout(
        title="Repository Growth",
        xaxis_title="Month",
        yaxis_title="Count",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)

def render_advanced_search(repo_url: str):
    """Render advanced search interface"""
    
    st.markdown("""
    <div class="modern-card">
        <h3>🔍 Advanced Search</h3>
        <p>Search for specific patterns, functions, or code structures</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search options
    col1, col2 = st.columns(2)
    
    with col1:
        search_type = st.selectbox(
            "Search Type",
            ["Code Pattern", "Function Name", "Class Name", "Variable", "Comment", "Import"]
        )
        
        search_query = st.text_input(
            "Search Query",
            placeholder="Enter your search term..."
        )
    
    with col2:
        file_type = st.selectbox(
            "File Type",
            ["All", "Python", "JavaScript", "TypeScript", "Java", "Go"]
        )
        
        case_sensitive = st.checkbox("Case Sensitive")
    
    # Search filters
    st.markdown("### 🔧 Search Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_lines = st.number_input("Minimum Lines", min_value=1, value=1)
    
    with col2:
        max_lines = st.number_input("Maximum Lines", min_value=1, value=1000)
    
    with col3:
        exclude_patterns = st.text_input(
            "Exclude Patterns",
            placeholder="node_modules, .git, __pycache__"
        )
    
    # Search button
    if st.button("🔍 Search", type="primary", use_container_width=True):
        if search_query:
            perform_advanced_search(repo_url, search_type, search_query, file_type, case_sensitive)
        else:
            st.warning("Please enter a search query")

def perform_advanced_search(repo_url: str, search_type: str, query: str, file_type: str, case_sensitive: bool):
    """Perform advanced search and display results"""
    
    st.markdown("### 🔍 Search Results")
    
    # Simulate search results
    results = [
        {
            "file": "src/main.py",
            "line": 45,
            "content": "def authenticate_user(username, password):",
            "context": "This function handles user authentication..."
        },
        {
            "file": "src/auth.py",
            "line": 23,
            "content": "class AuthenticationManager:",
            "context": "Manages authentication state and tokens..."
        },
        {
            "file": "tests/test_auth.py",
            "line": 12,
            "content": "def test_authenticate_user():",
            "context": "Test cases for user authentication..."
        }
    ]
    
    for result in results:
        with st.expander(f"📄 {result['file']}:{result['line']}"):
            st.markdown(f"**Line {result['line']}:**")
            st.code(result['content'], language='python')
            st.markdown(f"*{result['context']}*")

def render_code_quality_report(repo_url: str):
    """Render code quality analysis report"""
    
    st.markdown("""
    <div class="modern-card">
        <h3>📊 Code Quality Report</h3>
        <p>Comprehensive analysis of code quality, complexity, and maintainability</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quality metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card stat-card-success">
            <div class="stat-icon">📈</div>
            <div class="stat-number">92%</div>
            <div class="stat-label">Code Quality</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card stat-card-warning">
            <div class="stat-icon">🧮</div>
            <div class="stat-number">7.2</div>
            <div class="stat-label">Avg Complexity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card stat-card-primary">
            <div class="stat-icon">🧪</div>
            <div class="stat-number">78%</div>
            <div class="stat-label">Test Coverage</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card stat-card-error">
            <div class="stat-icon">⚠️</div>
            <div class="stat-number">5</div>
            <div class="stat-label">Issues Found</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Issues breakdown
    st.markdown("### ⚠️ Code Issues")
    
    issues = [
        {"type": "Complexity", "count": 2, "severity": "Medium"},
        {"type": "Duplication", "count": 1, "severity": "Low"},
        {"type": "Security", "count": 1, "severity": "High"},
        {"type": "Style", "count": 1, "severity": "Low"}
    ]
    
    for issue in issues:
        severity_color = {
            "High": "#ff6b6b",
            "Medium": "#ffa726",
            "Low": "#66bb6a"
        }.get(issue["severity"], "#ff6b6b")
        
        st.markdown(f"""
        <div class="modern-card" style="border-left: 4px solid {severity_color};">
            <strong>{issue['type']}</strong> - {issue['count']} issues ({issue['severity']} severity)
        </div>
        """, unsafe_allow_html=True) 