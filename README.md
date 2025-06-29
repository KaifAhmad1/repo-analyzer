# 🔍 GitHub Repository Analyzer

> **Intelligent Q&A System for GitHub Repositories**  
> Built with modern AI, beautiful UI, and powerful analysis capabilities

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-orange.svg)]()

## ✨ Features

### 🧠 **Smart AI Analysis**
- **Natural Language Q&A** - Ask questions in plain English
- **Multi-Model Support** - OpenAI GPT-4, Claude-3, and more
- **Context-Aware Responses** - Understands repository context
- **Intelligent Reasoning** - Multi-step analysis and synthesis

### 🔧 **Powerful MCP Servers**
- **File Content Analysis** - Read and analyze any file
- **Repository Structure** - Understand project organization
- **Commit History** - Track changes and evolution
- **Code Search** - Find functions, classes, and patterns
- **Issue Tracking** - Monitor bugs and features
- **Documentation** - Extract and analyze docs

### 🎨 **Beautiful Modern UI**
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark/Light Themes** - Choose your preferred theme
- **Smooth Animations** - Delightful user experience
- **Real-time Updates** - Live analysis and results
- **Interactive Visualizations** - Charts, graphs, and maps

### 🚀 **Advanced Features**
- **Code Quality Analysis** - Complexity, patterns, and metrics
- **Visual Repository Maps** - Interactive dependency graphs
- **Smart Summaries** - Auto-generated project overviews
- **Change Detection** - Track recent updates and trends
- **Dependency Analysis** - Map project relationships
- **Documentation Generation** - Auto-create missing docs

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   AI Agent      │    │   MCP Servers   │
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
git clone https://github.com/your-username/repo-analyzer.git
cd repo-analyzer

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
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
# Start the application
streamlit run app/main.py

# Open http://localhost:8501 in your browser
```

## 🎯 Example Questions

Ask questions like:
- 🤔 *"What is this repository about?"*
- 🔍 *"Show me the main entry points"*
- 📊 *"What are the recent changes?"*
- 🔐 *"Find all authentication functions"*
- 📦 *"What dependencies does this project use?"*
- 🐛 *"Are there any open issues related to performance?"*
- 💾 *"Explain how the database connection is implemented"*
- 🧪 *"What's the testing strategy used in this project?"*

## 📁 Project Structure

```
repo-analyzer/
├── 🎨 app/                    # Main Streamlit application
│   ├── main.py               # Entry point
│   ├── components/           # UI components
│   ├── pages/                # Multi-page interface
│   ├── themes/               # Custom themes
│   └── assets/               # Static assets
│
├── 🤖 core/                   # Core functionality
│   ├── agent.py              # AI agent
│   ├── servers/              # MCP servers
│   └── utils/                # Utilities
│
├── 🎨 ui/                     # UI components
│   ├── components/           # Reusable components
│   ├── themes/               # Theme system
│   └── animations/           # Animation utilities
│
├── ⚙️ config/                 # Configuration
│   ├── settings.yaml         # App settings
│   └── themes.yaml           # Theme definitions
│
├── 🧪 tests/                  # Test suite
├── 📚 docs/                   # Documentation
└── 💡 examples/               # Examples
```

## 🎨 UI Features

### **Modern Design**
- **Clean Interface** - Minimalist, focused design
- **Responsive Layout** - Works on all devices
- **Smooth Animations** - Delightful micro-interactions
- **Accessibility** - WCAG compliant

### **Theme System**
- **Dark Mode** - Easy on the eyes
- **Light Mode** - Clean and professional
- **Custom Themes** - Create your own
- **Auto-switching** - Follows system preference

### **Interactive Elements**
- **Real-time Chat** - Instant responses
- **Live Visualizations** - Dynamic charts and graphs
- **Smooth Transitions** - Fluid page changes
- **Loading States** - Clear feedback

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

### **Custom Themes**
```yaml
# config/themes.yaml
themes:
  dark:
    primary: "#1f2937"
    secondary: "#374151"
    accent: "#3b82f6"
    text: "#f9fafb"
  
  light:
    primary: "#ffffff"
    secondary: "#f3f4f6"
    accent: "#2563eb"
    text: "#111827"
```

## 🚀 Advanced Usage

### **Custom Analysis**
```python
from core.agent import RepositoryAgent

agent = RepositoryAgent()
result = await agent.analyze_repository("owner/repo")
```

### **API Integration**
```python
from core.servers import FileContentServer

server = FileContentServer()
content = await server.get_file_content("owner/repo", "path/to/file")
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Setup**
```bash
# Fork and clone
git clone https://github.com/your-username/repo-analyzer.git

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Start development server
streamlit run app/main.py
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

- **Streamlit** - For the amazing web app framework
- **OpenAI & Anthropic** - For powerful AI models
- **GitHub** - For the comprehensive API
- **Community** - For feedback and contributions

---

<div align="center">

**Made with ❤️ by the GitHub Repository Analyzer Team**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/your-username/repo-analyzer)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/repoanalyzer)
[![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/repoanalyzer)

</div>