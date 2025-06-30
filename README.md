# 🚀 GitHub Repository Analyzer - Modern AI-Powered Analysis

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **A beautiful, modern, and feature-rich interface for analyzing GitHub repositories using AI agents and Model Context Protocol (MCP) servers.**

## ✨ Features

### 🎨 **Modern UI & Animations**
- **Beautiful gradient designs** with smooth animations
- **Responsive layout** that works on all devices
- **Dark/Light theme toggle** with automatic switching
- **Floating action buttons** for quick access
- **Animated loading states** and progress indicators
- **Modern card layouts** with hover effects
- **Custom scrollbars** and smooth transitions

### 🤖 **AI-Powered Analysis**
- **Intelligent Q&A** with natural language processing
- **Multi-step reasoning** and tool chaining
- **Context-aware responses** based on repository data
- **Structured insights** with detailed explanations
- **Code analysis** and quality assessment
- **Dependency mapping** and relationship analysis

### 📊 **Rich Visualizations**
- **Interactive charts** using Plotly and Altair
- **Commit activity timelines** with trend analysis
- **Language distribution** pie charts
- **Issue tracking** and bug analysis
- **Repository statistics** with animated counters
- **File structure trees** with interactive exploration

### 🔧 **MCP Server Integration**
- **Unified MCP server** with comprehensive tools
- **Real-time data fetching** from GitHub API
- **Repository structure analysis** with file trees
- **Commit history tracking** with detailed metadata
- **Issue and PR management** with filtering
- **Code search capabilities** with pattern matching

### 💬 **Enhanced Chat Interface**
- **Modern chat bubbles** with user/AI distinction
- **Quick question buttons** for common queries
- **Conversation history** with timestamps
- **Tool usage tracking** with detailed explanations
- **Export functionality** for conversation logs
- **Auto-complete suggestions** for better UX

### 📁 **Repository Explorer**
- **Interactive file browser** with syntax highlighting
- **Code preview** with line numbers
- **Search functionality** across files
- **Directory tree navigation** with expand/collapse
- **File type icons** and metadata display
- **Quick file actions** (view, download, analyze)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- GitHub Personal Access Token
- OpenAI or Anthropic API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/repo-analyzer-4.git
   cd repo-analyzer-4
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GITHUB_TOKEN=your_github_token_here" > .env
   echo "OPENAI_API_KEY=your_openai_key_here" >> .env
   # OR
   echo "ANTHROPIC_API_KEY=your_anthropic_key_here" >> .env
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501` to see the beautiful interface!

## 🎯 Usage Guide

### 1. **Repository Selection**
- Enter any public GitHub repository URL
- Use the modern repository selector with validation
- Browse popular repositories for inspiration
- View recent repositories for quick access

### 2. **AI-Powered Analysis**
- Ask natural language questions about the repository
- Use quick question buttons for common queries
- Get detailed insights with tool usage tracking
- Export conversations for later reference

### 3. **Visual Insights**
- Explore interactive charts and visualizations
- View commit activity and trends
- Analyze language distribution and code patterns
- Track issues and pull requests

### 4. **Advanced Features**
- Navigate file structure with interactive trees
- Search for specific code patterns
- Analyze dependencies and relationships
- Generate comprehensive reports

## 🛠️ Architecture

### **Frontend (Streamlit)**
```
src/ui/
├── modern_styles.css      # Beautiful CSS with animations
├── chat_interface.py      # Modern chat UI component
├── repository_selector.py # Enhanced repo selector
└── components/           # Reusable UI components
```

### **Backend (MCP Servers)**
```
src/servers/
├── repository_analyzer_server.py  # Main MCP server
├── mcp_client_improved.py        # Enhanced MCP client
├── server_manager.py             # Server orchestration
└── tools/                        # MCP tool implementations
```

### **AI Agent**
```
src/agent/
├── ai_agent.py           # Main AI agent logic
├── prompts.py            # System prompts and templates
└── tools.py              # Tool calling and processing
```

## 🎨 UI Components

### **Modern Cards**
- Gradient backgrounds with hover effects
- Animated borders and shadows
- Responsive grid layouts
- Interactive elements

### **Chat Interface**
- Bubble-style messages with user/AI distinction
- Timestamps and tool usage tracking
- Quick question buttons with icons
- Export and clear functionality

### **Visualizations**
- Interactive Plotly charts
- Animated progress bars
- Timeline components
- Statistics cards with counters

### **Navigation**
- Sidebar with configuration options
- Tabbed interface for different views
- Floating action buttons
- Breadcrumb navigation

## 🔧 Configuration

### **Environment Variables**
```bash
# Required
GITHUB_TOKEN=your_github_token

# AI Provider (choose one)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Optional
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### **MCP Server Configuration**
```python
# Server settings in config.py
MCP_SERVER_HOST = "localhost"
MCP_SERVER_PORT = 8000
MCP_SERVER_TIMEOUT = 30
```

## 📊 Sample Questions

The AI can answer questions like:

- **"What is this repository about?"** - Get comprehensive overview
- **"Show me the main entry points"** - Find application entry files
- **"What are the recent changes?"** - View recent commits and updates
- **"Find authentication-related code"** - Locate security implementations
- **"What dependencies does this use?"** - Analyze project dependencies
- **"Are there any performance issues?"** - Check for performance concerns
- **"Explain the database implementation"** - Understand data storage
- **"What's the testing strategy?"** - Review testing approach

## 🎯 Advanced Features

### **Code Analysis**
- Syntax highlighting with multiple themes
- Code complexity analysis
- Security vulnerability scanning
- Performance optimization suggestions

### **Repository Insights**
- Contributor analysis and statistics
- Commit pattern analysis
- Issue trend tracking
- Dependency health assessment

### **Export & Reporting**
- Conversation export in JSON format
- Repository analysis reports
- Code quality metrics
- Performance benchmarks

## 🚀 Deployment

### **Local Development**
```bash
# Development mode with auto-reload
streamlit run app.py --server.runOnSave true
```

### **Production Deployment**
```bash
# Using Docker
docker build -t repo-analyzer .
docker run -p 8501:8501 repo-analyzer

# Using Streamlit Cloud
# Connect your GitHub repository to Streamlit Cloud
```

### **Environment Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with production settings
streamlit run app.py --server.headless true
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Setup**
```bash
# Fork and clone
git clone https://github.com/your-username/repo-analyzer-4.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black src/
flake8 src/
```

## 📈 Roadmap

### **Phase 1: Enhanced UI** ✅
- [x] Modern design with animations
- [x] Responsive layout
- [x] Dark/light theme
- [x] Interactive visualizations

### **Phase 2: Advanced Analysis** 🚧
- [ ] Code quality scoring
- [ ] Security vulnerability detection
- [ ] Performance benchmarking
- [ ] Architecture analysis

### **Phase 3: Collaboration** 📋
- [ ] Multi-user support
- [ ] Team workspaces
- [ ] Shared analysis reports
- [ ] Real-time collaboration

### **Phase 4: AI Enhancement** 📋
- [ ] Custom AI models
- [ ] Advanced code understanding
- [ ] Predictive analytics
- [ ] Automated recommendations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** for the amazing web framework
- **Anthropic** for the MCP protocol and Claude AI
- **OpenAI** for GPT models and API
- **GitHub** for the comprehensive API
- **Plotly** for beautiful visualizations

## 📞 Support

- **Documentation**: [Wiki](https://github.com/your-username/repo-analyzer-4/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-username/repo-analyzer-4/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/repo-analyzer-4/discussions)
- **Email**: support@repo-analyzer.com

---

<div align="center">

**Built with ❤️ using Streamlit, AI agents, and MCP servers**

[![GitHub stars](https://img.shields.io/github/stars/your-username/repo-analyzer-4?style=social)](https://github.com/your-username/repo-analyzer-4)
[![GitHub forks](https://img.shields.io/github/forks/your-username/repo-analyzer-4?style=social)](https://github.com/your-username/repo-analyzer-4)
[![GitHub issues](https://img.shields.io/github/issues/your-username/repo-analyzer-4)](https://github.com/your-username/repo-analyzer-4/issues)

</div>