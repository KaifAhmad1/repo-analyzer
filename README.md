# Repository Analyzer - FastMCP v2 Edition 🚀

A powerful GitHub repository analysis tool built with **FastMCP v2** for simple, effective, and modern MCP server architecture.

## ✨ Features

- **FastMCP v2 Powered**: Built on the latest FastMCP framework for optimal performance
- **4 Core Servers**: Simplified architecture with essential functionality
- **Async Operations**: Efficient async/await patterns throughout
- **AI-Powered Analysis**: Intelligent repository analysis using Google Gemini
- **Modern UI**: Clean, responsive web interface

## 🏗️ Architecture

### Core Servers (FastMCP v2)

1. **📁 File Content Server** - Retrieve and read file contents
   - Get file content from repositories
   - List directory contents
   - Extract README files
   - Get file information

2. **🌳 Repository Structure Server** - Get directory trees and file listings
   - Build directory tree structures
   - Analyze project structure
   - Find files by pattern
   - Identify key components

3. **📝 Commit History Server** - Access commit messages and changes
   - Get recent commits
   - Detailed commit information
   - Commit statistics
   - Search commits by query

4. **🔍 Code Search Server** - Search for specific code patterns or functions
   - Search code patterns
   - Find function definitions
   - Get code metrics
   - Search dependencies

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd repo-analyzer-17

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the Streamlit application
streamlit run app.py
```

### Testing FastMCP v2 Implementation

```bash
# Run the test script
python test_fastmcp.py
```

## 🛠️ Development

### Server Management

```python
from src.servers.server_manager import start_all_servers, get_servers_status

# Start all servers
start_all_servers()

# Check status
status = get_servers_status()
print(f"Running: {status['running_servers']}/{status['total_servers']}")
```

### Using the AI Agent

```python
from src.agent.ai_agent import ask_question, analyze_repository

# Ask a question about a repository
answer = ask_question("What is this repository about?", "https://github.com/microsoft/vscode")

# Get comprehensive analysis
analysis = analyze_repository("https://github.com/microsoft/vscode")
```

### Direct FastMCP v2 Usage

```python
from fastmcp import Client

# Connect to a server
async with Client("src/servers/file_content_server.py") as client:
    # Get README content
    result = await client.call_tool("get_readme_content", {
        "repo_url": "https://github.com/microsoft/vscode"
    })
    print(result.content[0].text)
```

## 📁 Project Structure

```
repo-analyzer-17/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── test_fastmcp.py                # FastMCP v2 test script
├── src/
│   ├── agent/
│   │   └── ai_agent.py            # AI agent with FastMCP v2 tools
│   ├── servers/
│   │   ├── file_content_server.py      # File content operations
│   │   ├── repository_structure_server.py  # Structure analysis
│   │   ├── commit_history_server.py    # Commit history
│   │   ├── code_search_server.py       # Code search
│   │   └── server_manager.py           # Server management
│   └── ui/
│       ├── chat_interface.py      # Chat UI components
│       ├── repository_selector.py # Repository selection
│       └── modern_styles.css      # Styling
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file for configuration:

```env
# Google Gemini API Key
GOOGLE_API_KEY=your_gemini_api_key_here

# GitHub API Token (optional, for higher rate limits)
GITHUB_TOKEN=your_github_token_here
```

## 🧪 Testing

### Run All Tests

```bash
python test_fastmcp.py
```

### Test Individual Components

```python
# Test server manager
from src.servers.server_manager import get_servers_status
status = get_servers_status()

# Test AI agent
from src.agent.ai_agent import test_fastmcp_connection
result = test_fastmcp_connection()
```

## 🚀 FastMCP v2 Benefits

- **Simplified Architecture**: 4 focused servers instead of complex multi-server setup
- **Async by Default**: All operations use async/await for better performance
- **Easy Testing**: In-memory testing with FastMCP Client
- **Modern Patterns**: Clean, Pythonic code with type hints
- **Better Error Handling**: Comprehensive error handling and logging
- **Resource Management**: Automatic cleanup and resource management

## 📊 Performance

- **Fast Startup**: Servers start in under 2 seconds
- **Efficient Memory**: Minimal memory footprint
- **Scalable**: Easy to add new servers or modify existing ones
- **Reliable**: Robust error handling and recovery

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `python test_fastmcp.py`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastMCP Team**: For the excellent FastMCP v2 framework
- **Google Gemini**: For the AI capabilities
- **GitHub API**: For repository data access

---

**Built with ❤️ using FastMCP v2**
