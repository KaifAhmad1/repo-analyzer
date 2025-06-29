# GitHub Repository Analyzer Documentation

## Overview

The GitHub Repository Analyzer is an intelligent question-answering system that can understand and query GitHub repositories using Model Context Protocol (MCP) servers and a Streamlit interface.

## Architecture

### Components

1. **MCP Servers**: Specialized servers for different repository aspects
2. **Streamlit Application**: Interactive Q&A interface
3. **AI Agent**: LLM integration and intelligent reasoning
4. **Utilities**: Shared utilities and configuration management

### MCP Servers

#### File Content Server
- **Purpose**: Retrieve and read file contents
- **Tools**:
  - `get_file_content`: Get raw file content
  - `get_file_metadata`: Get file information
  - `search_file_content`: Search within files
  - `get_file_history`: Get file change history
  - `list_directory_files`: List directory contents

#### Repository Structure Server
- **Purpose**: Analyze repository structure and organization
- **Tools**:
  - `get_repository_tree`: Get directory tree
  - `analyze_structure`: Analyze structure patterns
  - `find_files_by_type`: Find files by type
  - `get_directory_stats`: Get directory statistics
  - `identify_project_type`: Identify project type

#### Commit History Server
- **Purpose**: Access commit messages and changes
- **Tools**:
  - `get_recent_commits`: Get recent commits
  - `get_commit_details`: Get commit details
  - `analyze_commit_patterns`: Analyze commit patterns
  - `get_file_changes`: Get file changes
  - `get_contributor_stats`: Get contributor statistics

#### Issue/PR Server
- **Purpose**: Query issues and pull requests
- **Tools**:
  - `get_issues`: Get repository issues
  - `get_pull_requests`: Get pull requests
  - `search_issues`: Search issues
  - `get_issue_details`: Get issue details

#### Code Search Server
- **Purpose**: Search for specific code patterns
- **Tools**:
  - `search_code`: Search code patterns
  - `find_functions`: Find function definitions
  - `find_classes`: Find class definitions
  - `search_imports`: Search import statements

#### Documentation Server
- **Purpose**: Extract and process documentation
- **Tools**:
  - `get_readme`: Get README content
  - `get_documentation`: Get documentation files
  - `extract_examples`: Extract code examples
  - `analyze_documentation`: Analyze documentation quality

## Installation

### Prerequisites

- Python 3.8+
- GitHub Personal Access Token
- OpenAI API Key (or Anthropic API Key)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd repo-analyzer-1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your API keys
```

4. Start MCP servers:
```bash
python -m mcp_servers.start_servers
```

5. Run Streamlit application:
```bash
streamlit run streamlit_app/main.py
```

## Configuration

### Environment Variables

- `GITHUB_TOKEN`: GitHub Personal Access Token
- `OPENAI_API_KEY`: OpenAI API Key
- `ANTHROPIC_API_KEY`: Anthropic API Key
- `MCP_SERVER_HOST`: MCP server host (default: localhost)
- `MCP_SERVER_PORT`: MCP server port (default: 8000)

### Configuration Files

- `config/settings.yaml`: Main configuration file
- `env.example`: Environment variables template

## Usage

### Starting the Application

1. **Start MCP Servers**:
```bash
python -m mcp_servers.start_servers
```

2. **Run Streamlit App**:
```bash
streamlit run streamlit_app/main.py
```

3. **Access the Interface**:
   - Open browser to `http://localhost:8501`
   - Select a repository
   - Start asking questions

### Example Questions

- "What is this repository about?"
- "Show me the main entry points"
- "What are the recent changes?"
- "Find all authentication functions"
- "What dependencies does this project use?"
- "Are there any open issues related to performance?"
- "Explain how the database connection is implemented"
- "What's the testing strategy used in this project?"

## Advanced Features

### Code Analysis
- Analyze code quality and complexity
- Identify code patterns and anti-patterns
- Generate code metrics and reports

### Visual Repository Map
- Generate interactive repository visualizations
- Show file relationships and dependencies
- Visualize commit history and activity

### Smart Summarization
- Create comprehensive repository summaries
- Generate project overviews
- Extract key insights and patterns

### Change Detection
- Track recent changes and updates
- Identify breaking changes
- Monitor repository activity

### Dependency Analysis
- Map project dependencies
- Identify dependency conflicts
- Analyze dependency relationships

### Documentation Generation
- Auto-generate missing documentation
- Improve existing documentation
- Create API documentation

## Development

### Project Structure

```
repo-analyzer-1/
├── mcp_servers/           # MCP server implementations
│   ├── base_server.py     # Base server class
│   ├── file_content_server.py
│   ├── repository_structure_server.py
│   ├── commit_history_server.py
│   └── start_servers.py   # Server startup script
├── streamlit_app/         # Streamlit Q&A interface
│   ├── main.py           # Main application
│   └── components/       # UI components
├── ai_agent/             # AI agent and LLM integration
│   └── agent.py          # Main agent class
├── utils/                # Shared utilities
│   └── config.py         # Configuration management
├── config/               # Configuration files
│   └── settings.yaml     # Main settings
├── tests/                # Test suite
│   └── test_mcp_servers.py
├── docs/                 # Documentation
└── requirements.txt      # Python dependencies
```

### Adding New MCP Servers

1. Create a new server class inheriting from `BaseMCPServer`
2. Implement required methods:
   - `initialize_tools()`
   - `handle_tool_call()`
3. Add server to `start_servers.py`
4. Update documentation

### Testing

Run tests:
```bash
pytest tests/
```

Run specific test file:
```bash
pytest tests/test_mcp_servers.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **GitHub API Rate Limits**:
   - Check your GitHub token permissions
   - Implement rate limiting in your code

2. **MCP Server Connection Issues**:
   - Verify server ports are available
   - Check firewall settings

3. **LLM API Issues**:
   - Verify API keys are correct
   - Check API quota limits

### Logs

Check logs in `logs/app.log` for detailed error information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting guide 