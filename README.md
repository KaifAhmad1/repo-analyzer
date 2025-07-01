# 🚀 GitHub Repository Analyzer

> A comprehensive, AI-powered GitHub repository analysis tool that leverages Model Context Protocol (MCP) servers and Google Gemini AI to provide intelligent insights about code repositories. Built with Streamlit for a modern, interactive web interface.

## ✨ Key Features

- **🤖 Advanced AI Analysis**: Powered by Google Gemini AI for intelligent repository insights
- **🔍 MCP Server Integration**: 6 specialized Model Context Protocol servers for structured data access
- **💬 Interactive Q&A**: Natural language interface for asking questions about repositories
- **📊 Real-time Visualizations**: Dynamic charts and analytics for repository data
- **🎯 Multi-Agent System**: Specialized AI agents for different analysis aspects
- **🔄 Live Data**: Real-time repository information and commit history
- **🎨 Modern UI**: Clean, responsive interface built with Streamlit

## 🏗️ System Architecture

### MCP Servers (Model Context Protocol)
The application uses 6 specialized MCP servers for comprehensive repository analysis:

1. **Repository Analyzer Server** - Main server for comprehensive analysis
2. **File Content Server** - Retrieve and read file contents
3. **Repository Structure Server** - Get directory trees and file listings
4. **Commit History Server** - Access commit messages and changes
5. **Issues Server** - Query issues and pull requests
6. **Code Search Server** - Search for specific code patterns

### AI Agent System
- **Single Agent Mode**: General-purpose repository analysis using Google Gemini
- **Multi-Agent Team Mode**: Specialized agents working together:
  - **Repository Overview Agent**: Metadata and basic information analysis
  - **Code Analysis Agent**: Technical code patterns and architecture assessment
  - **Activity Analysis Agent**: Project activity and community health evaluation

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.8 or higher**
- **GitHub Personal Access Token** (for enhanced API access)
- **Google Gemini API Key** (required for AI functionality)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd repo-analyzer-11
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   Create a `.env` file in the project root:
   ```bash
   # Create .env file
   echo "GITHUB_TOKEN=your_github_token_here" > .env
   echo "GOOGLE_API_KEY=your_gemini_api_key_here" >> .env
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the Application**
   Open your browser and navigate to `http://localhost:8501`

### Getting API Keys

#### GitHub Personal Access Token
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:user`, `read:org`
4. Copy the generated token

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the generated key

## 📋 Sample Questions & Use Cases

The system can handle various types of repository analysis questions:

### Repository Overview
- "What is this repository about and what does it do?"
- "What are the main features of this project?"
- "What technologies and frameworks does this use?"

### Code Structure & Architecture
- "Show me the main entry points of this application"
- "What is the overall architecture of this project?"
- "How is the code organized and structured?"

### Recent Activity & Changes
- "What are the recent changes in the last 10 commits?"
- "What features have been added recently?"
- "Who are the main contributors to this project?"

### Code Search & Analysis
- "Find all functions related to authentication"
- "Show me how database connections are implemented"
- "Find error handling patterns in the code"

### Dependencies & Configuration
- "What dependencies does this project use?"
- "What are the main configuration files?"
- "How is the project set up and deployed?"

### Issues & Community
- "Are there any open issues related to performance?"
- "What are the most common issues reported?"
- "How active is the development community?"

### Testing & Quality
- "What's the testing strategy used in this project?"
- "How is code quality maintained?"
- "What are the code review practices?"

## 🛠️ Configuration Options

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GITHUB_TOKEN` | GitHub Personal Access Token | No* | None |
| `GOOGLE_API_KEY` | Google Gemini API Key | Yes | None |
| `GEMINI_MODEL` | Default Gemini model | No | `gemini-2.0-flash-001` |
| `DEBUG` | Enable debug mode | No | `False` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

*GitHub token is optional but recommended for better API rate limits

### Agent Configuration
- **Model Selection**: Choose from available Gemini models
- **Agent Type**: Single agent or multi-agent team
- **Analysis Depth**: Configure the level of detail in responses

## 📁 Project Structure

```
repo-analyzer-11/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                      # This documentation
├── LICENSE                        # MIT License
├── .env                           # Environment variables (create this)
├── src/
│   ├── agent/
│   │   └── ai_agent.py            # AI agent implementations
│   ├── servers/
│   │   ├── repository_analyzer_server.py  # Main MCP server
│   │   ├── file_content_server.py         # File content server
│   │   ├── commit_history_server.py       # Commit history server
│   │   ├── issues_server.py               # Issues server
│   │   ├── code_search_server.py          # Code search server
│   │   ├── repository_structure_server.py # Structure server
│   │   ├── server_manager.py              # Server management
│   │   └── mcp_client_improved.py         # MCP client
│   ├── ui/
│   │   ├── repository_selector.py         # Repository selection UI
│   │   ├── chat_interface.py              # Q&A interface
│   │   └── modern_styles.css              # Styling
│   └── utils/
│       ├── config.py                      # Configuration utilities
│       └── github.py                      # GitHub API utilities
```

## 🔧 Development Guide

### Running Tests
```bash
# Run all tests
pytest test_*.py

# Run with coverage
pytest --cov=src test_*.py
```

### Adding New MCP Servers
1. Create a new server file in `src/servers/`
2. Implement the MCP protocol using the FastMCP framework
3. Add server to `server_manager.py`
4. Update the main application to use the new server

### Extending AI Agents
1. Extend the agent system in `src/agent/ai_agent.py`
2. Add specialized tools and instructions
3. Integrate with the UI components
4. Test with various repository types

### Customizing the UI
1. Modify components in `src/ui/`
2. Update styling in `src/ui/modern_styles.css`
3. Add new visualizations as needed

## 🚀 Advanced Features

### Multi-Agent Team Analysis
The system can coordinate multiple specialized agents:
- **Overview Agent**: Analyzes repository metadata and structure
- **Code Agent**: Deep technical analysis of code patterns
- **Activity Agent**: Evaluates project activity and community health

### Real-time Data Visualization
- Commit activity charts
- Language distribution analysis
- Issue tracking and trends
- Repository structure visualization

### Intelligent Q&A System
- Natural language processing
- Context-aware responses
- Tool usage tracking
- Conversation history

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Submit a pull request**

### Development Setup
```bash
# Clone your fork
git clone https://github.com/your-username/repo-analyzer-11.git
cd repo-analyzer-11

# Install in development mode
pip install -e .

# Set up pre-commit hooks
pre-commit install
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Streamlit](https://streamlit.io/)** - Modern web framework for data applications
- **[Google Gemini](https://ai.google.dev/)** - Advanced AI capabilities
- **[Model Context Protocol](https://modelcontextprotocol.io/)** - Standardized server architecture
- **[GitHub API](https://docs.github.com/en/rest)** - Comprehensive repository data access
- **[Agno Framework](https://github.com/agno-agi/agno)** - Multi-agent system framework

## 📞 Support & Documentation

### Getting Help
- **GitHub Issues**: Open an issue for bugs or feature requests
- **Documentation**: Check the inline code documentation
- **Examples**: Review the sample questions and use cases

### Common Issues
1. **API Key Issues**: Ensure your Google Gemini API key is correctly set
2. **GitHub Rate Limits**: Use a GitHub token for higher rate limits
3. **Dependencies**: Make sure all requirements are installed
4. **Port Conflicts**: Change the port if 8501 is already in use

### Performance Tips
- Use GitHub tokens for better API rate limits
- Choose appropriate Gemini models for your use case
- Clear chat history periodically for better performance

---

## 🎯 Project Goals

This project demonstrates:
- **Modern AI Integration**: Seamless integration with Google Gemini AI
- **MCP Protocol Implementation**: Standardized server architecture
- **Interactive Web Applications**: Beautiful Streamlit-based UI
- **Repository Analysis**: Comprehensive code and project analysis
- **Multi-Agent Systems**: Coordinated AI agent workflows

**Built with ❤️ using Streamlit, MCP Servers, and Google Gemini AI**

---

*For more information, visit the project repository or contact the development team.* 
