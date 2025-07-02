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

3. **Start MCP Servers** (Required):
   ```bash
   # Option 1: Use the startup script
   python start_servers.py
   
   # Option 2: Start servers manually
   python src/servers/server_manager.py start
   ```

4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

5. **Start Analyzing**:
   - Enter a GitHub repository URL (e.g., `https://github.com/microsoft/vscode`)
   - Use the Q&A chat or quick analysis features
   - Monitor server status in the sidebar

## 🎯 How to Use

### Repository Selection
- Enter any valid GitHub repository URL
- The app will validate and load repository information
- Repository details will appear in the sidebar

### Server Management
- **Server Status**: Monitor all 4 MCP servers in the sidebar
- **Auto-Start**: Servers can be started automatically if offline
- **Individual Control**: Start/stop individual servers as needed
- **Health Monitoring**: Real-time system health percentage
- **Quick Actions**: Start all, stop all, or restart all servers

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
- **Server Management**: Automated MCP server lifecycle management

## 📁 Project Structure

```
repo-analyzer/
├── app.py                 # Main Streamlit application
├── start_servers.py       # MCP server startup script
├── debug_servers.py       # Server testing and debugging
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
- **Server Status**: Monitor FastMCP server connections in real-time

### Server Management
- **Individual Server Control**: Start/stop each of the 4 MCP servers independently
- **Bulk Operations**: Start all, stop all, or restart all servers with one click
- **Health Monitoring**: Real-time system health percentage and status indicators
- **Auto-Start**: Automatic server startup when the application detects offline servers

## 🖥️ Server Management

### MCP Servers Overview
The application uses 4 core FastMCP v2 servers for repository analysis:

1. **File Content Server 📁** - Retrieves and reads file contents
2. **Repository Structure Server 🌳** - Gets directory trees and file listings  
3. **Commit History Server 📝** - Accesses commit messages and changes
4. **Code Search Server 🔍** - Searches for specific code patterns

### Starting Servers
```bash
# Quick start (recommended)
python start_servers.py

# Manual start
python src/servers/server_manager.py start
```

### Server Status Monitoring
- **Sidebar Display**: Real-time status of all servers in the application sidebar
- **Health Indicators**: Green (🟢) for running, Red (🔴) for stopped
- **System Health**: Overall health percentage based on running servers
- **Quick Actions**: Buttons to start/stop/restart servers directly from the UI

### Troubleshooting
```bash
# Test server connections
python debug_servers.py

# Check server status
python src/servers/server_manager.py status

# Restart all servers
python src/servers/server_manager.py restart
```

## 🚀 Powered By

- **FastMCP v2**: Model Context Protocol for repository access
- **Groq AI**: High-performance AI models
- **Streamlit**: Modern web app framework
- **GitHub API**: Repository data and analysis

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
