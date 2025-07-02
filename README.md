# 🚀 GitHub Repository Analyzer - Simplified UI

A clean, modern interface for analyzing GitHub repositories using FastMCP v2 servers and Groq AI.

## ✨ Features

- **💬 Q&A Chat**: Ask questions about any GitHub repository with tool usage tracking
- **🔍 Quick Analysis**: Get repository overview, file structure, dependencies, and code patterns
- **🗺️ Visual Repository Map**: Interactive directory trees and project structure visualization
- **📊 Smart Summary**: AI-powered comprehensive reports and insights
- **🤖 AI-Powered**: Uses Groq AI models for intelligent analysis
- **📁 FastMCP v2**: Leverages Model Context Protocol for repository access
- **🎨 Clean UI**: Simplified, focused interface with clear typography

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   - Get your Groq API key from [Groq Console](https://console.groq.com/keys)
   - Create a `.env` file in the project root:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

4. **Start Analyzing**:
   - Enter a GitHub repository URL (e.g., `https://github.com/microsoft/vscode`)
   - Use the Q&A chat or quick analysis features

## 🎯 How to Use

### Repository Selection
- Enter any valid GitHub repository URL
- The app will validate and load repository information
- Repository details will appear in the sidebar

### Q&A Chat
- Ask natural language questions about the repository
- Use quick question buttons for common queries
- Get AI-powered responses with repository context

### Quick Analysis
- Choose analysis type: Repository Overview, File Structure, Dependencies, or Code Patterns
- Adjust analysis depth as needed
- View results in a clean, organized format

### Visual Repository Map
- Generate directory trees and file structure visualizations
- Explore project architecture with interactive features
- Analyze repository structure at different depths

### Smart Summary
- Generate comprehensive AI-powered reports
- Choose from different summary types: Overview, Code Quality, Architecture, Development Insights
- Get detailed analysis with tool usage tracking

## 🛠️ Architecture

- **Frontend**: Streamlit with custom CSS styling
- **AI Backend**: Groq API with multiple model options
- **Repository Access**: FastMCP v2 servers for GitHub integration
- **Analysis Tools**: Custom tools for code analysis and metrics

## 📁 Project Structure

```
repo-analyzer/
├── app.py                 # Main Streamlit application
├── src/
│   ├── agent/            # AI agent and tools
│   ├── servers/          # FastMCP v2 servers
│   ├── ui/              # UI components
│   └── utils/           # Configuration utilities
├── requirements.txt      # Python dependencies
└── README.md           # This file
```

## 🎨 UI Design

The interface has been simplified for better usability:

- **Clean Typography**: Modern, readable fonts throughout
- **Focused Layout**: Essential features only, no unnecessary complexity
- **Clear Navigation**: Simple tabs for main features
- **Responsive Design**: Works well on different screen sizes
- **Consistent Styling**: Unified color scheme and spacing

## 🔧 Configuration

### AI Models
Choose from available Groq models:
- `llama-3.1-70b-versatile` (default)
- `llama-3.1-8b-instant`
- `llama-3.1-405b-reasoning`

### Analysis Settings
- **Analysis Depth**: Control how deep to explore repository structure (1-5)
- **Tool Usage Display**: Toggle visibility of which tools were used in responses
- **Server Status**: Monitor FastMCP server connections

## 🚀 Powered By

- **FastMCP v2**: Model Context Protocol for repository access
- **Groq AI**: High-performance AI models
- **Streamlit**: Modern web app framework
- **GitHub API**: Repository data and analysis

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
