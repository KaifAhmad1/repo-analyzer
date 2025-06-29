# 🔍 GitHub Repository Analyzer

> **Intelligent Q&A System for GitHub Repositories**  
> Built with Agno AI framework, MCP servers, and beautiful Streamlit UI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Agno](https://img.shields.io/badge/Agno-0.1.0+-green.svg)](https://github.com/agno-ai/agno)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

### 🧠 **Smart AI Analysis with Agno**
- **Natural Language Q&A** - Ask questions in plain English
- **Multi-Model Support** - OpenAI GPT-4, Claude-3, and more
- **Context-Aware Responses** - Understands repository context
- **Intelligent Reasoning** - Multi-step analysis and synthesis
- **Tool Calling** - Automatic selection of appropriate MCP tools

### 🔧 **Powerful MCP Servers**
- **File Content Analysis** - Read and analyze any file with encoding detection
- **Repository Structure** - Complete directory trees and file organization
- **Commit History** - Track changes, authors, and evolution patterns
- **Code Search** - Find functions, classes, and patterns with regex support
- **Issue Tracking** - Monitor bugs, features, and pull requests
- **Code Quality Analysis** - Complexity metrics and pattern detection

### 🎨 **Beautiful Modern UI**
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Chat Interface** - Natural conversation with the AI agent
- **Real-time Updates** - Live analysis and results
- **Tool Usage Tracking** - See which tools were used for each response
- **Advanced Features** - Code analysis, visualizations, and summaries

### 🚀 **Advanced Features**
- **Code Quality Analysis** - Complexity, patterns, and metrics
- **Visual Repository Maps** - Interactive dependency graphs
- **Smart Summaries** - Auto-generated project overviews
- **Change Detection** - Track recent updates and trends
- **Dependency Analysis** - Map project relationships
- **Pattern Recognition** - Identify coding patterns and conventions

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   Agno Agent    │    │   MCP Servers   │
│                 │◄──►│                 │◄──►│                 │
│ • Chat Interface│    │ • LLM Integration│    │ • File Content  │
│ • Visualizations│    │ • Tool Calling  │    │ • Repository    │
│ • Themes        │    │ • Reasoning     │    │ • Commits       │
│ • Responsive    │    │ • Context       │    │ • Issues        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. **Installation**
```bash
# Clone the repository
git clone https://github.com/your-username/repo-analyzer-2.git
cd repo-analyzer-2

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
streamlit run streamlit_app/main.py

# Open http://localhost:8501 in your browser
```

### 4. **Basic Usage Example**
```bash
# Run the basic usage example
python examples/basic_usage.py
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
repo-analyzer-2/
├── 🤖 ai_agent/                 # Agno-based AI agent
│   ├── agent.py                # Main AI agent implementation
│   └── __init__.py
│
├── 🔧 mcp_servers/              # MCP server implementations
│   ├── base_server.py          # Base server with common functionality
│   ├── file_content_server.py  # File content and metadata
│   ├── repository_structure_server.py  # Directory trees and structure
│   ├── commit_history_server.py # Commit history and changes
│   ├── issues_server.py        # Issues and pull requests
│   ├── code_search_server.py   # Code search and patterns
│   ├── start_servers.py        # Server management
│   └── __init__.py
│
├── 🎨 streamlit_app/            # Streamlit web application
│   ├── main.py                 # Main application entry point
│   └── __init__.py
│
├── 🎨 ui/                       # UI components
│   ├── components/             # Reusable UI components
│   │   ├── repository_selector.py  # Repository selection
│   │   └── chat_interface.py   # Chat interface
│   ├── themes/                 # Theme system
│   └── animations/             # Animation utilities
│
├── ⚙️ config/                   # Configuration files
│   ├── settings.yaml           # App settings
│   └── themes.yaml             # Theme definitions
│
├── 💡 examples/                 # Usage examples
│   └── basic_usage.py          # Basic usage demonstration
│
├── 🧪 tests/                    # Test suite
├── 📚 docs/                     # Documentation
└── 📄 README.md                 # This file
```

## 🔧 MCP Servers

### **File Content Server**
- Retrieve file contents with encoding detection
- Get file metadata (size, type, last modified)
- Search within file content (text and regex)
- Get file change history
- List directory contents

### **Repository Structure Server**
- Get complete directory tree structure
- Analyze repository organization patterns
- Find files by type or extension
- Identify project type based on structure
- Get directory statistics

### **Commit History Server**
- Get recent commits with details
- Analyze commit patterns and trends
- Search commits by message or author
- Get commit statistics and metrics
- Track file change history

### **Issues Server**
- Get issues and pull requests
- Search issues by content or labels
- Analyze issue patterns and trends
- Get issue comments and details
- Track issue statistics

### **Code Search Server**
- Search for code patterns and functions
- Find function and class definitions
- Search import statements and dependencies
- Analyze code patterns and structure
- Find dependency relationships

## 🎨 UI Features

### **Modern Design**
- **Clean Interface** - Minimalist, focused design
- **Responsive Layout** - Works on all devices
- **Smooth Animations** - Delightful micro-interactions
- **Accessibility** - WCAG compliant

### **Chat Interface**
- **Real-time Chat** - Instant responses with typing indicators
- **Message History** - Persistent conversation history
- **Tool Usage Display** - See which tools were used
- **Error Handling** - Graceful error messages

### **Advanced Features**
- **Code Analysis** - One-click code quality analysis
- **Repository Visualization** - Interactive dependency graphs
- **Smart Summaries** - Auto-generated project overviews
- **Export Results** - Save analysis results

## 🔧 Configuration

### **Environment Variables**
```bash
# GitHub API
GITHUB_TOKEN=your_token

# AI Provider (choose one)
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# App Settings
THEME=dark  # or light
LANGUAGE=en
DEBUG=false
```

### **MCP Server Configuration**
```bash
# MCP Server Settings
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
```

## 🚀 Advanced Usage

### **Programmatic Usage**
```python
from ai_agent.agent import GitHubRepositoryAgent

# Initialize agent
agent = GitHubRepositoryAgent("openai", "gpt-4")

# Process questions
response = await agent.process_question(
    "What is this repository about?", 
    "microsoft/vscode"
)

# Get repository overview
overview = await agent.analyze_repository_overview("microsoft/vscode")

# Find code patterns
patterns = await agent.find_code_patterns("microsoft/vscode", "functions")
```

### **MCP Server Integration**
```python
from mcp_servers.start_servers import start_servers, handle_tool_call

# Start servers
await start_servers("localhost", 8000)

# Handle tool calls
result = await handle_tool_call(
    "file_content", 
    "get_file_content",
    {"repository": "microsoft/vscode", "file_path": "README.md"}
)
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Setup**
```bash
# Fork and clone
git clone https://github.com/your-username/repo-analyzer-2.git

# Install dev dependencies
pip install -r requirements.txt

# Run tests
pytest

# Start development server
streamlit run streamlit_app/main.py
```

## 📊 Roadmap

- [ ] **Enhanced Visualizations** - 3D repository maps
- [ ] **Multi-language Support** - Internationalization
- [ ] **Plugin System** - Extensible architecture
- [ ] **Collaborative Features** - Team analysis
- [ ] **Performance Optimization** - Faster analysis
- [ ] **Mobile App** - Native mobile experience

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Agno** - For the powerful AI agent framework
- **Streamlit** - For the amazing web app framework
- **OpenAI & Anthropic** - For powerful AI models
- **GitHub** - For the comprehensive API
- **Community** - For feedback and contributions

---

<div align="center">

**Made with ❤️ by the GitHub Repository Analyzer Team**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/your-username/repo-analyzer-2)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/repoanalyzer)
[![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/repoanalyzer)

</div>