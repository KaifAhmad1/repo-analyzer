# Contributing to GitHub Repository Analyzer

Thank you for your interest in contributing to the GitHub Repository Analyzer! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- GitHub account
- Basic knowledge of Python, MCP protocol, and Streamlit

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/repo-analyzer-1.git
   cd repo-analyzer-1
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

5. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

6. **Run tests** to ensure everything is working:
   ```bash
   pytest tests/
   ```

## Development Guidelines

### Code Style

- Follow **PEP 8** style guidelines
- Use **type hints** for all function parameters and return values
- Write **docstrings** for all functions and classes
- Keep functions **small and focused**
- Use **descriptive variable names**

### Project Structure

```
repo-analyzer-1/
├── mcp_servers/           # MCP server implementations
├── streamlit_app/         # Streamlit Q&A interface
├── ai_agent/             # AI agent and LLM integration
├── utils/                # Shared utilities
├── config/               # Configuration files
├── tests/                # Test suite
├── docs/                 # Documentation
└── examples/             # Example usage
```

### Adding New Features

#### Adding a New MCP Server

1. **Create a new server file** in `mcp_servers/`:
   ```python
   from .base_server import BaseMCPServer
   
   class NewFeatureServer(BaseMCPServer):
       def __init__(self):
           super().__init__(
               name="new_feature_server",
               description="Description of the new server"
           )
       
       async def initialize_tools(self):
           # Define your tools here
           pass
       
       async def handle_tool_call(self, tool_name, arguments):
           # Handle tool calls here
           pass
   ```

2. **Add the server** to `mcp_servers/start_servers.py`
3. **Write tests** in `tests/test_mcp_servers.py`
4. **Update documentation** in `docs/README.md`

#### Adding New Streamlit Components

1. **Create component file** in `streamlit_app/components/`
2. **Import and use** in `streamlit_app/main.py`
3. **Add tests** for the component
4. **Update documentation**

### Testing

#### Writing Tests

- Write **unit tests** for all new functionality
- Use **pytest** as the testing framework
- Follow **AAA pattern** (Arrange, Act, Assert)
- Mock external dependencies

Example test structure:
```python
import pytest
from unittest.mock import Mock, patch

class TestNewFeature:
    @pytest.fixture
    def feature(self):
        return NewFeature()
    
    def test_feature_functionality(self, feature):
        # Arrange
        input_data = "test"
        
        # Act
        result = feature.process(input_data)
        
        # Assert
        assert result == "expected_output"
```

#### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_mcp_servers.py

# Run with coverage
pytest --cov=mcp_servers --cov=streamlit_app --cov=ai_agent

# Run with verbose output
pytest -v
```

### Documentation

#### Code Documentation

- Write **clear docstrings** for all functions and classes
- Include **type hints** for better IDE support
- Add **examples** in docstrings for complex functions

#### Project Documentation

- Update `README.md` for new features
- Add examples in `examples/` directory
- Update `docs/README.md` with new information
- Include **screenshots** for UI changes

### Git Workflow

#### Branch Naming

Use descriptive branch names:
- `feature/add-new-mcp-server`
- `bugfix/fix-rate-limiting`
- `docs/update-installation-guide`
- `test/add-integration-tests`

#### Commit Messages

Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(mcp): add new file content server

fix(streamlit): resolve session state issue

docs(readme): update installation instructions
```

#### Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the guidelines
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Run tests** and ensure they pass
6. **Create a pull request** with:
   - Clear title and description
   - Link to related issues
   - Screenshots for UI changes
   - Test results

## Issue Guidelines

### Reporting Bugs

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce**
3. **Expected vs actual behavior**
4. **Environment information**:
   - Python version
   - Operating system
   - Dependencies versions
5. **Error messages** and stack traces
6. **Screenshots** if applicable

### Feature Requests

When requesting features, please include:

1. **Clear description** of the feature
2. **Use case** and motivation
3. **Proposed implementation** (if you have ideas)
4. **Examples** of similar features in other projects

## Code Review Process

### Review Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New functionality has tests
- [ ] Documentation is updated
- [ ] No sensitive information is committed
- [ ] Commit messages are clear and descriptive

### Review Guidelines

When reviewing code:

- Be **constructive** and **respectful**
- Focus on **code quality** and **functionality**
- Suggest **improvements** rather than just pointing out issues
- Consider **security implications**
- Check for **performance issues**

## Getting Help

### Questions and Support

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check `docs/README.md` first

### Community Guidelines

- Be **respectful** and **inclusive**
- Help **new contributors**
- Share **knowledge** and **best practices**
- Follow the **code of conduct**

## Release Process

### Versioning

We follow **Semantic Versioning** (SemVer):
- `MAJOR.MINOR.PATCH`
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes (backward compatible)

### Release Checklist

Before releasing:

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Changelog is updated
- [ ] Version is bumped
- [ ] Release notes are prepared

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Thank you for contributing to the GitHub Repository Analyzer! Your contributions help make this project better for everyone. 