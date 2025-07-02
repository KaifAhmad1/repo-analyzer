# 🚀 GitHub Repository Analyzer - Clean & Simple

A streamlined, AI-powered GitHub repository analysis tool with a clean, modern interface. Built with FastMCP v2 servers and Groq AI for comprehensive repository insights.

## ✨ Features

### 🎯 Core Functionality
- **💬 Q&A Chat Interface** - Ask natural language questions about any GitHub repository with enhanced AI agents
- **🔍 Quick Analysis** - Get structured insights about repository structure, dependencies, and code patterns
- **📊 Smart Summary** - Generate comprehensive AI-powered reports with memory and reasoning
- **🧠 Enhanced AI Agents** - Advanced agents with memory, storage, and reasoning capabilities

### 🛠️ Technical Capabilities
- **File Content Analysis** - Read and analyze repository files
- **Repository Structure** - Explore directory trees and file organization
- **Commit History** - Track recent changes and development activity
- **Code Search** - Find specific code patterns and functions
- **Dependency Analysis** - Identify project dependencies and requirements
- **AI Memory & Storage** - Persistent conversation history and user preferences
- **Reasoning Tools** - Advanced reasoning capabilities for better analysis
- **Multi-Server Integration** - Seamless use of all available MCP servers

### 🎨 Clean UI
- **Modern Design** - Clean, responsive interface with excellent UX
- **Real-time Progress** - See which tools and servers are being used
- **Server Management** - Easy control over MCP server status
- **Tool Tracking** - Visual feedback on backend operations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API key

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

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

4. **Start the application**
   ```bash
   python start_servers.py
   ```

   Or start manually:
   ```bash
   streamlit run app.py
   ```

## 🎯 How to Use

### 1. Select a Repository
- Enter a GitHub repository URL in the sidebar
- The system will automatically load repository information

### 2. Choose Your Analysis Tool
- **Q&A Chat**: Ask questions about the repository
- **Quick Analysis**: Get structured insights
- **Smart Summary**: Generate comprehensive reports

### 3. View Results
- See real-time progress and tool usage
- Get detailed analysis with visual formatting
- Track which MCP servers were used

## 🏗️ Architecture

### Core Components
- **FastMCP v2 Servers**: 4 specialized servers for different analysis tasks
- **Groq AI Integration**: Powerful AI model for natural language processing
- **Streamlit UI**: Clean, responsive web interface
- **Tool Tracking**: Real-time monitoring of backend operations

### MCP Servers
1. **File Content Server** - Read and analyze repository files
2. **Repository Structure Server** - Explore directory organization
3. **Commit History Server** - Track development activity
4. **Code Search Server** - Find code patterns and functions

---

> **Note:**  
> Never share your API key publicly or commit it to version control.

## 🔧 Configuration

### Analysis Settings
- **Analysis Depth**: Control how deep the analysis explores (1-5 levels)
- **AI Model**: Fixed to `llama-3.1-70b-versatile` for optimal performance
- **Tool Usage Display**: Toggle visibility of backend tool usage

### Server Management
- **Auto-start**: Automatically start servers when needed
- **Manual Control**: Start/stop individual servers
- **Health Monitoring**: Real-time server status tracking

## 📁 Project Structure

```
repo-analyzer/
├── app.py                 # Main Streamlit application
├── start_servers.py       # Server startup script
├── requirements.txt       # Python dependencies
├── src/
│   ├── agent/            # AI agent system
│   ├── servers/          # MCP server implementations
│   ├── ui/              # UI components and styles
│   └── utils/           # Utility functions
└── README.md            # This file
```

## 🎯 What's New

### Simplified Interface
- **Removed Advanced Tools**: Focus on core functionality
- **Cleaner Navigation**: Streamlined tab system
- **Better UX**: Improved user experience
- **Reduced Complexity**: Easier to understand and use

### Enhanced Backend
- **Tool Tracking**: See which tools are being used
- **Server Monitoring**: Real-time server status
- **Progress Feedback**: Multi-stage progress indicators
- **Error Handling**: Better error messages and recovery

### Improved UI
- **Modern Design**: Clean, professional appearance
- **Responsive Layout**: Works on all devices
- **Better Typography**: Improved readability
- **Enhanced Components**: Better buttons, forms, and inputs

## 🔧 Configuration

### AI Models
The application uses Groq AI models for analysis:
- `llama-3.1-70b-versatile` (default and recommended)

### Analysis Settings
- **Analysis Depth**: Control how deep to explore repository structure (1-5)
- **Tool Usage Display**: Toggle visibility of which tools were used in responses
- **Server Status**: Monitor FastMCP server connections in real-time

### Server Management
- **Individual Server Control**: Start/stop each of the 4 MCP servers independently
- **Bulk Operations**: Start all, stop all, or restart all servers with one click
- **Health Monitoring**: Real-time system health percentage and status indicators
- **Auto-Start**: Automatic server startup when the application detects offline servers

## 🚀 Performance

### Optimizations
- **Efficient Tool Usage**: Only use necessary tools
- **Caching**: Smart caching of repository data
- **Async Operations**: Non-blocking server communication
- **Resource Management**: Proper cleanup and memory usage

### Scalability
- **Modular Design**: Easy to add new analysis tools
- **Server Independence**: Each MCP server operates independently
- **Configurable Depth**: Adjustable analysis levels
- **Extensible Architecture**: Easy to extend with new features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:
1. Check the server status in the sidebar
2. Ensure your Groq API key is configured
3. Restart the application if needed
4. Check the console for error messages

---

**🚀 GitHub Repository Analyzer** - Making repository analysis simple, clean, and effective!
