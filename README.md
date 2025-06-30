# 🔍 GitHub Repository Analyzer

> **Intelligent Q&A System for GitHub Repositories**  
> Built with AI agents, MCP servers, and Streamlit UI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

### 🧠 **Smart AI Analysis**
- **Natural Language Q&A** - Ask questions in plain English
- **Multi-Model Support** - OpenAI GPT-4, Claude-3, and more
- **Context-Aware Responses** - Understands repository context
- **Intelligent Reasoning** - Multi-step analysis and synthesis

### 🔧 **Powerful MCP Servers**
- **File Content Analysis** - Read and analyze any file
- **Repository Structure** - Complete directory trees and organization
- **Commit History** - Track changes, authors, and evolution
- **Code Search** - Find functions, classes, and patterns
- **Issue Tracking** - Monitor bugs, features, and pull requests

### 🎨 **Beautiful Modern UI**
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Chat Interface** - Natural conversation with the AI agent
- **Real-time Updates** - Live analysis and results
- **Tool Usage Tracking** - See which tools were used for each response

## 🚀 Quick Start

### 1. **Installation**
```bash
# Clone the repository
git clone https://github.com/your-username/repo-analyzer-3.git
cd repo-analyzer-3

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp env.example .env
# Edit .env with your API keys
```

### 2. **Configuration**
```bash
# Required API Keys
GITHUB_TOKEN=your_github_token
OPENAI_API_KEY=your_openai_key
# or
ANTHROPIC_API_KEY=your_anthropic_key
```

### 3. **Run the Application**
```bash
# Start the Streamlit application
streamlit run app.py

# Open http://localhost:8501 in your browser
```

## 🎯 Example Questions

Ask questions like:
- 🤔 *"What is this repository about and what does it do?"*
- 🔍 *"Show me the main entry points of this application"*
- 📊 *"What are the recent changes in the last 10 commits?"*
- 🔐 *"Find all functions related to authentication"*
- 📦 *"What dependencies does this project use?"*
- 🐛 *"Are there any open issues related to performance?"*
- 💾 *"Explain how the database connection is implemented"*
- 🧪 *"What's the testing strategy used in this project?"*

## 📁 Project Structure

```
repo-analyzer-3/
├── app.py                    # Main application entry point
├── src/
│   ├── agent/
│   │   └── ai_agent.py      # AI agent implementation
│   ├── servers/
│   │   ├── mcp_client.py    # MCP client for tool calling
│   │   ├── server_manager.py # Server management
│   │   ├── file_content_server.py      # File content server
│   │   ├── repository_structure_server.py  # Structure server
│   │   ├── commit_history_server.py   # Commit history server
│   │   ├── code_search_server.py      # Code search server
│   │   └── issues_server.py           # Issues server
│   ├── ui/
│   │   ├── chat_interface.py          # Chat UI component
│   │   └── repository_selector.py     # Repository selector
│   └── utils/
│       ├── config.py        # Configuration utilities
│       └── github.py        # GitHub API utilities
├── config/
│   └── settings.yaml        # Application settings
├── examples/
│   └── basic_usage.py       # Usage examples
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 MCP Servers

### **File Content Server**
- Retrieve file contents with encoding detection
- Get file metadata (size, type, last modified)
- Search within file content

### **Repository Structure Server**
- Get complete directory tree structure
- Analyze repository organization patterns
- Find files by type or extension

### **Commit History Server**
- Get recent commits with details
- Analyze commit patterns and trends
- Search commits by message or author

### **Issues Server**
- Get issues and pull requests
- Search issues by content or labels
- Analyze issue patterns and trends

### **Code Search Server**
- Search for code patterns and functions
- Find function and class definitions
- Search import statements and dependencies

## 🎨 UI Features

### **Modern Design**
- **Clean Interface** - Minimalist, focused design
- **Responsive Layout** - Works on all devices
- **Smooth Animations** - Delightful micro-interactions

### **Chat Interface**
- **Real-time Chat** - Instant responses with typing indicators
- **Message History** - Persistent conversation history
- **Tool Usage Display** - See which tools were used
- **Error Handling** - Graceful error messages

## 🚀 Advanced Features

- **Code Analysis** - One-click code quality analysis
- **Visual Repository Maps** - Interactive dependency graphs
- **Smart Summaries** - Auto-generated project overviews
- **Change Detection** - Track recent updates and trends
- **Dependency Analysis** - Map project relationships

## 🔧 Development

### **Running Servers Individually**
```bash
# File Content Server
python src/servers/file_content_server.py

# Repository Structure Server
python src/servers/repository_structure_server.py

# Commit History Server
python src/servers/commit_history_server.py

# Code Search Server
python src/servers/code_search_server.py

# Issues Server
python src/servers/issues_server.py
```

### **Testing**
```bash
# Run basic usage example
python examples/basic_usage.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.