# 🚀 GitHub Repository Analyzer - Multi-Server Ecosystem

> A comprehensive AI-powered GitHub repository analysis tool built with **FastMCP v2**, **Google Gemini AI**, **Agno**, and **Streamlit**. This application provides deep insights into code repositories using a multi-server ecosystem of specialized MCP servers.

## ✨ Features

### 🤖 AI-Powered Analysis
- **Single Agent Mode**: Comprehensive analysis using a single AI agent
- **Multi-Agent Team**: Specialized agents for different aspects of analysis
- **Google Gemini AI**: Powered by the latest Gemini models
- **Natural Language Q&A**: Ask questions about repositories in plain English

### 🔍 Multi-Server MCP Ecosystem
- **Repository Analyzer Server**: Overview, analysis, and activity data
- **File Content Server**: File contents and directory listings
- **Repository Structure Server**: Directory trees and structure analysis
- **Commit History Server**: Commit data and statistics
- **Issues Server**: Issues and pull requests data
- **Code Search Server**: Code search and metrics

### 📊 Comprehensive Analytics
- Repository overview and metadata
- Directory structure visualization
- Commit activity charts
- Issues and pull requests tracking
- Code metrics and statistics
- File content analysis

### 🎨 Modern UI
- Clean, responsive Streamlit interface
- Tabbed organization for different data types
- Real-time server status monitoring
- Interactive charts and visualizations
- Chat history and Q&A interface

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   AI Agents      │    │  FastMCP v2     │
│                 │    │                  │    │   Servers       │
│ • Repository    │◄──►│ • Single Agent   │◄──►│ • Repository    │
│   Selector      │    │ • Multi-Agent    │    │   Analyzer      │
│ • Q&A Interface │    │   Team           │    │ • File Content  │
│ • Analytics     │    │ • Google Gemini  │    │ • Structure     │
│ • Server Status │    │   Integration    │    │ • Commit History│
└─────────────────┘    └──────────────────┘    │ • Issues        │
                                               │ • Code Search   │
                                               └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- GitHub Personal Access Token
- Google API Key (for Gemini AI)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd repo-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**
   - Set `GITHUB_TOKEN` environment variable
   - Set `GOOGLE_API_KEY` environment variable
   - Or use the settings sidebar in the app

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Testing the Ecosystem

Run the test script to verify all components are working:

```bash
python test_multi_server_ecosystem.py
```

## 🔧 Configuration

### Environment Variables
```bash
export GITHUB_TOKEN="your_github_token"
export GOOGLE_API_KEY="your_google_api_key"
```

### API Keys Setup
1. **GitHub Token**: Create a personal access token with `repo` scope
2. **Google API Key**: Get an API key from Google AI Studio for Gemini

## 📖 Usage

### 1. Repository Selection
- Enter a GitHub repository URL
- The app will automatically fetch repository data

### 2. Explore Data
Use the tabbed interface to explore different aspects:
- **📊 Overview**: Repository metadata and basic information
- **📁 Structure**: Directory tree and file structure analysis
- **📈 Activity**: Commit activity charts and statistics
- **🐛 Issues**: Open issues and pull requests
- **📊 Metrics**: Code metrics and statistics

### 3. Ask Questions
- Use the Q&A interface to ask natural language questions
- Choose between single agent or multi-agent team mode
- Get comprehensive AI-powered analysis

### 4. Server Management
- Monitor server status in the sidebar
- Restart servers if needed
- View detailed server information

## 🛠️ Development

### Project Structure
```
repo-analyzer/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── test_multi_server_ecosystem.py # Test script
├── src/
│   ├── agent/
│   │   └── ai_agent.py            # AI agent system
│   ├── servers/
│   │   ├── repository_analyzer_server.py
│   │   ├── file_content_server.py
│   │   ├── repository_structure_server.py
│   │   ├── commit_history_server.py
│   │   ├── issues_server.py
│   │   ├── code_search_server.py
│   │   ├── mcp_client_improved.py # Unified MCP client
│   │   └── server_manager.py      # Multi-server manager
│   ├── ui/
│   │   ├── repository_selector.py
│   │   ├── chat_interface.py
│   │   ├── settings_sidebar.py
│   │   └── modern_styles.css
│   └── utils/
│       ├── config.py              # Configuration utilities
│       └── github.py              # GitHub API utilities
```

### Adding New Servers
1. Create a new FastMCP v2 server in `src/servers/`
2. Add server configuration to `server_manager.py`
3. Add tools to `mcp_client_improved.py`
4. Update AI agent tools in `ai_agent.py`

### Testing
```bash
# Test the entire ecosystem
python test_multi_server_ecosystem.py

# Test individual components
python -m pytest tests/
```

## 🔍 MCP Server Details

### Repository Analyzer Server
- **Tools**: Repository overview, analysis, activity data
- **Purpose**: High-level repository insights and metadata

### File Content Server
- **Tools**: File content retrieval, directory listing
- **Purpose**: Access to specific files and directories

### Repository Structure Server
- **Tools**: Directory tree, file structure analysis
- **Purpose**: Understanding repository organization

### Commit History Server
- **Tools**: Recent commits, commit statistics, commit details
- **Purpose**: Development activity and history analysis

### Issues Server
- **Tools**: Issues, pull requests, issue statistics
- **Purpose**: Community and development workflow analysis

### Code Search Server
- **Tools**: Code search, file search, code metrics
- **Purpose**: Code analysis and quality assessment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastMCP**: For the excellent MCP framework
- **Google Gemini**: For powerful AI capabilities
- **Streamlit**: For the beautiful web interface
- **GitHub API**: For repository data access

## 🆘 Support

If you encounter any issues:
1. Check the test script output
2. Verify API keys are configured
3. Ensure all dependencies are installed
4. Check server status in the sidebar

For more help, please open an issue on GitHub.
