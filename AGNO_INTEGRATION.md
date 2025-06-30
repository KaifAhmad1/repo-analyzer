# Advanced Multi-Agent Framework Integration

This project now uses an **advanced multi-agent framework** for building intelligent agents that seamlessly integrate with all MCP (Model Context Protocol) servers.

## 🚀 What is the Advanced Multi-Agent Framework?

The advanced multi-agent framework is a Python system for building multi-agent systems with shared memory, knowledge, and reasoning. It provides:

- **Level 1**: Agents with tools and instructions
- **Level 2**: Agents with knowledge and storage  
- **Level 3**: Agents with memory and reasoning
- **Level 4**: Agent Teams that can reason and collaborate
- **Level 5**: Agentic Workflows with state and determinism

## 🏗️ Architecture

### Single Agent
```python
from src.agent.ai_agent import create_advanced_agent

# Create a single agent with MCP tools
agent = create_advanced_agent("claude-sonnet-4-20250514")

# Ask questions
response = agent.run("What is this repository about?")
```

### Multi-Agent Team
```python
from src.agent.ai_agent import create_agent_team

# Create a team of specialized agents
team = create_agent_team()

# Complex analysis with team collaboration
response = team.run("Analyze repository structure and activity")
```

## 🛠️ MCP Tools Integration

The advanced agents seamlessly integrate with all MCP servers through the `MCPTools` class:

### Available Tools
- `get_repository_overview()` - Get repository metadata and statistics
- `search_code()` - Search for code patterns and functions
- `get_recent_commits()` - Get recent commit history
- `get_issues()` - Get issues and pull requests
- `analyze_repository()` - Comprehensive repository analysis

### Tool Usage
```python
from src.agent.ai_agent import MCPTools

mcp_tools = MCPTools()

# Get repository overview
overview = mcp_tools.get_repository_overview("https://github.com/microsoft/vscode")

# Search for code
results = mcp_tools.search_code("https://github.com/microsoft/vscode", "authentication")

# Get recent commits
commits = mcp_tools.get_recent_commits("https://github.com/microsoft/vscode", limit=10)
```

## 🎯 Agent Specializations

### 1. Repository Overview Agent
- **Role**: Handle repository metadata and basic information
- **Tools**: `get_repository_overview`
- **Focus**: Repository description, statistics, and metadata

### 2. Code Analysis Agent  
- **Role**: Handle code search and analysis
- **Tools**: `search_code`, `analyze_repository`
- **Focus**: Code patterns, structure, and technical analysis

### 3. Activity Analysis Agent
- **Role**: Handle commits, issues, and project activity
- **Tools**: `get_recent_commits`, `get_issues`
- **Focus**: Project activity, recent changes, and community engagement

## 📋 Usage Examples

### Simple Question
```python
from src.agent.ai_agent import ask_question_advanced

response = ask_question_advanced(
    "What is this repository about?", 
    "https://github.com/microsoft/vscode",
    use_team=False
)
```

### Complex Analysis with Team
```python
response = ask_question_advanced(
    "Analyze the repository structure, recent activity, and code quality",
    "https://github.com/microsoft/vscode", 
    use_team=True
)
```

### Comprehensive Analysis
```python
from src.agent.ai_agent import analyze_repository_advanced

analysis = analyze_repository_advanced("https://github.com/microsoft/vscode")
```

## 🔧 Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Keys
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

### 3. Run Example
```bash
python examples/agno_usage_example.py
```

## 🎨 Features

### Reasoning Tools
- Agents use `ReasoningTools` for improved response quality
- Step-by-step reasoning before responding
- Analysis of tool call results

### Team Coordination
- Multiple specialized agents work together
- Coordinated responses for complex queries
- Shared context and knowledge

### MCP Integration
- Seamless integration with all MCP servers
- Automatic tool calling and result processing
- Error handling and fallback mechanisms

### Backward Compatibility
- All existing functions remain compatible
- Gradual migration path from old system
- No breaking changes to existing code

## 🔄 Migration Guide

### From Old System
```python
# Old way
from src.agent.ai_agent import create_ai_agent, ask_question

agent = create_ai_agent("claude-sonnet-4-20250514", {})
response = ask_question(agent, "What is this about?", repo_url)

# New way (still works)
agent = create_ai_agent("claude-sonnet-4-20250514", {})
response = ask_question(agent, "What is this about?", repo_url)

# New advanced way
from src.agent.ai_agent import ask_question_advanced
response = ask_question_advanced("What is this about?", repo_url)
```

## 🚀 Advanced Usage

### Custom Agent Creation
```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from src.agent.ai_agent import MCPTools

# Create custom agent
mcp_tools = MCPTools()
custom_agent = Agent(
    model=Claude(id="claude-sonnet-4-20250514"),
    tools=[
        ReasoningTools(add_instructions=True),
        mcp_tools.search_code,
        mcp_tools.get_recent_commits,
    ],
    instructions="Focus on code analysis and recent changes",
    markdown=True,
)
```

### Team Customization
```python
from src.agent.ai_agent import create_agent_team

team = create_agent_team()

# Customize team behavior
team.instructions = [
    "Provide detailed technical analysis",
    "Focus on security and performance",
    "Include code examples and recommendations"
]
```

## 🔍 Monitoring and Debugging

### Enable Debug Mode
```bash
export AGNO_DEBUG=true
```

### View System Prompts
```python
agent = create_advanced_agent()
agent.debug_mode = True
```

### Monitor Tool Calls
```python
# Tool calls are automatically logged
response = agent.run("Search for authentication code")
# Check logs for tool call details
```

## 📊 Performance

### Caching
- Tool results are cached for improved performance
- Repeated queries use cached data
- Automatic cache invalidation

### Parallel Processing
- Team agents can work in parallel
- Concurrent tool calls for faster responses
- Optimized for large repository analysis

## 🛡️ Error Handling

### Graceful Degradation
- MCP server failures are handled gracefully
- Fallback to alternative tools when available
- Clear error messages for debugging

### Retry Logic
- Automatic retries for transient failures
- Exponential backoff for rate limits
- Circuit breaker pattern for persistent failures

## 🔮 Future Enhancements

### Planned Features
- **Memory Integration**: Persistent conversation history
- **Knowledge Base**: Repository-specific knowledge storage
- **Workflow Automation**: Complex analysis pipelines
- **Real-time Updates**: Live repository monitoring
- **Custom Tools**: User-defined analysis tools

### Extensibility
- Easy to add new MCP servers
- Plugin architecture for custom tools
- Configurable agent behaviors
- Custom team compositions

## 📚 Resources

- [Advanced Multi-Agent Framework Documentation](https://docs.agno.com)
- [MCP Protocol](https://modelcontextprotocol.io)
- [Anthropic Claude API](https://docs.anthropic.com)
- [OpenAI API](https://platform.openai.com/docs)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your advanced multi-agent enhancements
4. Test with multiple MCP servers
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 