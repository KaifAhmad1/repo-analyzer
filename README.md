# 🚀 GitHub Repository Analyzer

A powerful AI-powered repository analysis tool that uses FastMCP v2 servers and Groq AI to provide comprehensive insights about GitHub repositories.

## ✨ Features

### 🔍 **Enhanced AI Analysis**
- **Quick Analysis**: Get instant structured insights about any repository
- **Smart Summary**: Generate comprehensive AI-powered reports
- **Q&A Chat**: Ask natural language questions about repositories
- **Code Pattern Analysis**: Deep technical analysis of architecture and patterns

### 🛠️ **Real-Time Processing Status**
- **Live Tool Status**: See exactly which MCP tools are being used in real-time
- **Progress Tracking**: Watch the analysis progress step by step
- **Server Status**: Monitor which MCP servers are active and their health

### 📊 **MCP Server Integration**
- **File Content Server**: 📄 Access and analyze repository files
- **Repository Structure Server**: 📁 Explore directory structure and organization
- **Commit History Server**: 📝 Analyze development activity and patterns
- **Code Search Server**: 🔍 Search and analyze code patterns and dependencies

### 🎯 **User-Friendly Interface**
- **Modern UI**: Clean, intuitive interface with real-time feedback
- **System Health Monitoring**: Visual indicators of server status
- **Tool Usage Display**: See which analysis tools were used for each response
- **Progress Indicators**: Real-time status updates during analysis

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API Keys**:
   - Get a Groq API key from [Groq Console](https://console.groq.com/)
   - Set environment variable: `GROQ_API_KEY=your_key_here`

3. **Start the Application**:
   ```bash
   streamlit run app.py
   ```

4. **Analyze a Repository**:
   - Enter a GitHub repository URL
   - Choose your analysis type (Quick Analysis, Smart Summary, or Q&A Chat)
   - Watch real-time progress as the AI analyzes the repository

## 📋 Analysis Types

### 🔍 Quick Analysis
Provides structured insights including:
- Project type and purpose
- Technology stack
- Key features and capabilities
- Project structure overview
- Dependencies analysis
- Recent development activity
- Code quality indicators
- Documentation assessment

### 📊 Smart Summary
Generate comprehensive reports:
- **Complete Overview**: Full repository analysis
- **Technical Analysis**: Deep technical insights
- **Code Quality Report**: Quality metrics and recommendations
- **Architecture Review**: System design analysis

### 💬 Q&A Chat
Ask natural language questions:
- "What is this repository about?"
- "Show me the main entry points"
- "What dependencies does this project use?"
- "Find all authentication functions"
- "What's the testing strategy?"
- And much more!

## 🛠️ MCP Servers

The application uses four specialized MCP servers:

| Server | Icon | Purpose |
|--------|------|---------|
| **File Content** | 📄 | Access and read repository files |
| **Repository Structure** | 📁 | Analyze directory organization |
| **Commit History** | 📝 | Track development activity |
| **Code Search** | 🔍 | Search code patterns and dependencies |

## 📊 Real-Time Features

### Processing Status
- **Live Updates**: See exactly what the AI is doing
- **Tool Progress**: Watch each MCP tool being used
- **Server Status**: Monitor which servers are active
- **Health Indicators**: Visual system health monitoring

### Enhanced Display
- **Grouped Tools**: Tools organized by MCP server
- **Server Icons**: Visual indicators for each server type
- **Progress Bars**: Real-time progress tracking
- **Status Messages**: Detailed status updates

## 🔧 Configuration

### Analysis Settings
- **Analysis Depth**: Control how deep to explore (1-5 levels)
- **AI Model**: Choose from multiple Groq models
- **Tool Usage Display**: Toggle tool usage information
- **Auto-start Servers**: Automatically start offline servers

### System Health
- **Server Status**: Real-time monitoring of all MCP servers
- **Health Percentage**: Overall system health indicator
- **Quick Actions**: Start/stop servers with one click

## 🎯 Use Cases

- **Code Review**: Quickly understand unfamiliar codebases
- **Architecture Analysis**: Evaluate system design and patterns
- **Dependency Analysis**: Understand project dependencies and their purposes
- **Development Activity**: Track recent changes and contributor activity
- **Documentation Review**: Assess README and code documentation quality
- **Best Practices**: Identify code quality and adherence to standards

## 🚀 Advanced Features

### Real-Time Processing
Every analysis shows:
- Which MCP servers are being used
- Real-time progress updates
- Tool usage breakdown
- Processing status for each step

### Enhanced AI Responses
- **Structured Output**: Well-organized responses with headers
- **Specific Examples**: Code examples from the repository
- **Actionable Insights**: Practical recommendations
- **Metrics and Statistics**: Quantitative analysis where available

## 📈 Performance

- **Fast Analysis**: Quick insights using optimized MCP servers
- **Real-Time Feedback**: Immediate status updates
- **Efficient Processing**: Parallel tool execution where possible
- **Memory Management**: Optimized for large repositories

## 🔍 Troubleshooting

### Common Issues
1. **Servers Not Starting**: Check API keys and network connectivity
2. **Analysis Failing**: Ensure repository URL is valid and accessible
3. **Slow Performance**: Large repositories may take longer to analyze

### System Requirements
- Python 3.8+
- Groq API key
- Internet connection for repository access
- Sufficient memory for large repository analysis

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
