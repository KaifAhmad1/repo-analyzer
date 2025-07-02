# Repository Analyzer - FastMCP v2 Edition 🚀

A powerful GitHub repository analysis tool built with **FastMCP v2** and **Groq AI** for simple, effective, and modern repository analysis.

## ✨ Features

- **FastMCP v2 Powered**: Built on the latest FastMCP framework for optimal performance
- **Groq AI Integration**: High-performance AI analysis using Groq's LLM models
- **4 Core Servers**: Simplified architecture with essential functionality
- **Async Operations**: Efficient async/await patterns throughout
- **AI-Powered Analysis**: Intelligent repository analysis using Groq's advanced models
- **Advanced Code Analysis**: AST/CST parsing with Tree-sitter for deep code understanding
- **Modern UI**: Clean, responsive web interface with organized sidebar and user controls
- **User Controllability**: Customizable analysis settings, model selection, and UI preferences
- **Automatic Configuration**: API key automatically loaded from .env file

## 🏗️ Architecture

### Core Servers (FastMCP v2)

1. **📁 File Content Server** - Retrieve and read file contents
   - Get file content from repositories
   - List directory contents
   - Extract README files
   - Get file information
   - **Advanced Analysis**: AST-based code analysis for Python files
   - **Code Summary**: Quick overview of functions, classes, and metrics
   - **Issue Detection**: Identify potential code problems and suggestions

2. **🌳 Repository Structure Server** - Get directory trees and file listings
   - Build directory tree structures
   - Analyze project structure
   - Find files by pattern
   - Identify key components
   - **Codebase Analysis**: Comprehensive Python file analysis with AST parsing
   - **Aggregate Metrics**: Function counts, complexity statistics, import analysis

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
   - **AST/CST Analysis**: Analyze code structure using Abstract Syntax Trees
   - **Pattern Detection**: Find async functions, decorators, type hints, exceptions
   - **Code Complexity**: Calculate cyclomatic complexity and metrics

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd repo-analyzer-19

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. **Get Groq API Key**: Visit [Groq Console](https://console.groq.com/keys) to get your API key
2. **Create .env file**: Create a `.env` file in the project root:

```env
# Groq API Key (Required)
GROQ_API_KEY=your_groq_api_key_here
```

3. **Restart the application**: The API key will be automatically loaded

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

## 🎛️ User Interface & Controls

### Organized Sidebar

The application features a well-organized sidebar with:

- **📁 Repository Section**: Repository selector and info display
- **⚙️ Settings Section**: 
  - **🔑 API Configuration**: Shows status of .env API key (no input required)
  - **🤖 AI Model Settings**: Choose from available Groq models
  - **🔍 Analysis Settings**: Customize analysis depth and preferences
  - **🎨 UI Preferences**: Theme and interface customization
- **⚡ Quick Actions**: Refresh, metrics, and export options
- **📊 Status**: Real-time configuration and server status

### Available Groq Models

- `llama-3.1-70b-versatile` (Default) - Best for general analysis
- `llama-3.1-8b-instant` - Fast responses
- `llama-3.1-405b-reasoning` - Advanced reasoning capabilities
- `mixtral-8x7b-32768` - Good balance of speed and quality
- `gemma2-9b-it` - Efficient for specific tasks

### Analysis Controls

- **Analysis Depth**: Control how deep to analyze repository structure (1-5 levels)
- **Include Patterns**: Select what types of files to include in analysis
- **Response Style**: Choose between Detailed, Concise, Technical, or Beginner-friendly responses
- **Tool Usage Display**: Toggle visibility of which tools were used in responses

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
repo-analyzer-19/
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
│   ├── ui/
│   │   ├── chat_interface.py      # Chat UI components
│   │   ├── repository_selector.py # Repository selection
│   │   ├── settings_sidebar.py    # Settings and controls
│   │   └── modern_styles.css      # Styling
│   └── utils/
│       └── config.py              # Configuration utilities
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file for configuration:

```env
# Groq API Key (Required)
GROQ_API_KEY=your_groq_api_key_here

# Example: GROQ_API_KEY=gsk_abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

**Note**: The application automatically loads the API key from the `.env` file. No manual input is required in the interface.

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

## 🔍 Advanced Code Analysis

### AST/CST Analysis Features

The system now includes powerful code analysis capabilities using Abstract Syntax Trees (AST) and Concrete Syntax Trees (CST):

- **Function Analysis**: Extract function definitions, parameters, complexity, and docstrings
- **Class Analysis**: Identify classes, methods, inheritance, and structure
- **Import Analysis**: Track module imports and dependencies
- **Pattern Detection**: Find async functions, decorators, type hints, and exception handling
- **Code Metrics**: Calculate cyclomatic complexity, line counts, and structure metrics
- **Issue Detection**: Identify potential code problems like missing docstrings, high complexity, and deep nesting

### Available Analysis Tools

```python
# Analyze code structure of a specific file
result = tools.analyze_code_structure(repo_url, "src/main.py")

# Find specific code patterns
result = tools.find_code_patterns(repo_url, "async_functions")
result = tools.find_code_patterns(repo_url, "decorators")
result = tools.find_code_patterns(repo_url, "type_hints")

# Get comprehensive file analysis
result = tools.analyze_file_content(repo_url, "src/main.py")
```

## 🎨 UI/UX Improvements

### Systematic Organization

- **Organized Sidebar**: Clear sections for different functionalities
- **Expandable Settings**: Collapsible sections to reduce clutter
- **Visual Hierarchy**: Clear typography and spacing
- **Consistent Styling**: Unified design language throughout

### User Controllability

- **Model Selection**: Choose the AI model that best fits your needs
- **Analysis Customization**: Control depth, file types, and response style
- **UI Preferences**: Customize theme and interface behavior
- **Quick Actions**: Easy access to common operations
- **Real-time Status**: Always know the current state of the system

### Better UX

- **Progressive Disclosure**: Show only what's needed when it's needed
- **Clear Feedback**: Visual indicators for all operations
- **Responsive Design**: Works well on different screen sizes
- **Accessibility**: Proper contrast and keyboard navigation
- **Automatic Configuration**: No manual API key input required

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastMCP Team**: For the excellent FastMCP v2 framework
- **Groq AI**: For the advanced AI capabilities
- **GitHub API**: For repository data access

---

**Built with ❤️ using FastMCP v2**
