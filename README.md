# 🚀 GitHub Repository Analyzer

> A powerful, AI-driven GitHub repository analysis system built with Streamlit, FastMCP v2 servers, and Google Gemini AI. This system provides comprehensive insights into any public GitHub repository through an intuitive Q&A interface.

## ✨ Features

### 🤖 AI-Powered Analysis
- **Smart Q&A Interface**: Ask natural language questions about repositories
- **Google Gemini AI**: Powered by state-of-the-art AI models
- **Comprehensive Analysis**: Get detailed insights about code, structure, and activity

### 🔍 Multi-Server MCP Ecosystem
- **Repository Analyzer Server**: Overview and metadata analysis
- **File Content Server**: Read and analyze file contents
- **Repository Structure Server**: Directory trees and file organization
- **Commit History Server**: Track changes and development activity
- **Issues Server**: Monitor issues and pull requests
- **Code Search Server**: Find specific code patterns and functions

### 📊 Rich Visualizations
- **Repository Overview**: Key metrics and project information
- **Activity Charts**: Commit patterns and development trends
- **Structure Analysis**: File organization and architecture insights
- **Issue Tracking**: Open issues and pull request status
- **Code Metrics**: Quality and complexity analysis

### 💬 Enhanced Q&A Interface
- **Quick Questions**: Pre-built question categories for common analysis
- **Chat History**: Track your analysis session
- **Export Capabilities**: Download analysis results
- **Real-time Responses**: Instant AI-powered insights

## 🎯 Sample Questions Your System Can Handle

The system is designed to answer these types of questions effectively:

- **"What is this repository about and what does it do?"**
- **"Show me the main entry points of this application"**
- **"What are the recent changes in the last 10 commits?"**
- **"Find all functions related to authentication"**
- **"What dependencies does this project use?"**
- **"Are there any open issues related to performance?"**
- **"Explain how the database connection is implemented"**
- **"What's the testing strategy used in this project?"**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key
- GitHub access (for public repositories)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd repo-analyzer-12
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**
   - Set your Google Gemini API key in the Streamlit interface
   - The system will guide you through the setup process

4. **Start the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the interface**
   - Open your browser to `http://localhost:8501`
   - Enter a GitHub repository URL
   - Start asking questions!

## 🏗️ System Architecture

### Simplified AI Agent System
The system uses a streamlined AI agent that:
- **Focuses on core functionality**: No complex multi-agent teams
- **Uses clear, effective prompts**: Optimized for repository analysis
- **Integrates all MCP servers**: Comprehensive data access
- **Provides actionable insights**: Clear, structured responses

### MCP Server Integration
- **Unified MCP Client**: Single interface to all servers
- **Error Handling**: Robust error management and recovery
- **Rate Limiting**: Respects API limits and best practices
- **Caching**: Efficient data retrieval and storage

### User Interface
- **Tabbed Interface**: Organized sections for different analysis types
- **Real-time Updates**: Live data from GitHub repositories
- **Responsive Design**: Works on desktop and mobile devices
- **Export Features**: Download analysis results and chat history

## 📁 Project Structure

```
repo-analyzer-12/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── test_simplified_system.py       # System test script
└── src/
    ├── agent/
    │   └── ai_agent.py            # Simplified AI agent system
    ├── servers/
    │   ├── mcp_client_improved.py # Unified MCP client
    │   ├── server_manager.py      # Server management
    │   ├── repository_analyzer_server.py
    │   ├── file_content_server.py
    │   ├── repository_structure_server.py
    │   ├── commit_history_server.py
    │   ├── issues_server.py
    │   └── code_search_server.py
    └── ui/
        ├── chat_interface.py      # Enhanced Q&A interface
        ├── repository_selector.py # Repository selection
        ├── settings_sidebar.py    # Configuration panel
        └── modern_styles.css      # Custom styling
```

## 🔧 Configuration

### API Keys
The system requires the following API keys:
- **Google Gemini API**: For AI-powered analysis
- **GitHub Token** (optional): For higher rate limits

### Environment Variables
```bash
GOOGLE_GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_token  # Optional
```

## 🧪 Testing

Run the test script to verify system functionality:

```bash
python test_simplified_system.py
```

This will test:
- MCP client connectivity
- AI agent functionality
- Specific question types from requirements

## 🎨 Usage Examples

### Basic Repository Analysis
1. Enter a GitHub repository URL
2. Navigate to the "📊 Overview" tab
3. View repository metadata and statistics

### Q&A Analysis
1. Go to the "💬 Q&A" tab
2. Use quick question buttons or type custom questions
3. Get AI-powered insights about the repository

### Advanced Analysis
1. Explore different tabs for specific analysis types
2. Use the chat interface for detailed questions
3. Export results for further analysis

## 🔍 Question Categories

### 📊 Repository Overview
- Project description and purpose
- File structure and organization
- Dependencies and requirements
- README and documentation

### 🔍 Code Analysis
- Authentication and security patterns
- Database implementations
- Testing strategies
- Performance considerations

### 📈 Recent Activity
- Recent commits and changes
- Open issues and pull requests
- Commit statistics and patterns
- Contributor activity

## 🚀 Advanced Features

### Export Capabilities
- **Chat History**: Download complete Q&A sessions
- **Analysis Reports**: Export structured analysis results
- **Markdown Format**: Easy to read and share

### Real-time Updates
- **Live Data**: Always current repository information
- **Server Status**: Monitor MCP server health
- **Error Recovery**: Automatic retry and fallback mechanisms


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastMCP v2**: For the MCP server ecosystem
- **Google Gemini**: For AI capabilities
- **Streamlit**: For the web interface
- **GitHub API**: For repository data access
- **Agno**: For building AI Agent


---

**Built with ❤️ using Streamlit, FastMCP, Agno Ecosystem, and Google Gemini AI**
