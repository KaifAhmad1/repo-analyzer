# 🚀 GitHub Repository Analyzer

A powerful AI-powered repository analysis tool that uses FastMCP v2 servers and Groq AI to provide comprehensive insights about GitHub repositories with advanced AST (Abstract Syntax Tree) and CST (Concrete Syntax Tree) analysis capabilities.

## ✨ Core Features

### 🔍 **AI-Powered Analysis**
- **Quick Analysis**: Instant structured insights about any repository
- **Smart Summary**: Comprehensive AI-powered reports with technical depth
- **Q&A Chat**: Natural language questions with context-aware responses
- **Code Pattern Analysis**: Deep technical analysis using AST/CST parsing

### 🛠️ **Advanced Code Analysis**
- **AST Analysis**: Abstract Syntax Tree parsing for code structure understanding
- **CST Analysis**: Concrete Syntax Tree analysis for detailed syntax examination
- **Pattern Recognition**: Identify coding patterns, anti-patterns, and best practices
- **Architecture Mapping**: Visualize code architecture and dependencies

### 📊 **Real-Time Processing**
- **Live Tool Status**: Real-time MCP tool usage tracking
- **Progress Monitoring**: Step-by-step analysis progress
- **Server Health**: Active MCP server monitoring and status

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys**:
   ```bash
   # Set your Groq API key
   export GROQ_API_KEY=your_key_here
   ```

3. **Start Servers & App**:
   ```bash
   # Start all MCP servers
   python start_servers.py
   
   # Run the Streamlit app
   streamlit run app.py
   ```

## 🛠️ MCP Server Architecture

The application uses four specialized MCP servers for comprehensive repository analysis:

### 📄 **File Content Server**
- **Purpose**: Access and read repository files
- **Capabilities**: 
  - File content retrieval
  - Binary file detection
  - File size analysis
  - Content type identification
- **Use Cases**: Code analysis, documentation review, configuration inspection

### 📁 **Repository Structure Server**
- **Purpose**: Analyze directory organization and project structure
- **Capabilities**:
  - Directory tree exploration
  - File type categorization
  - Project structure mapping
  - Module organization analysis
- **Use Cases**: Architecture understanding, project organization assessment

### 📝 **Commit History Server**
- **Purpose**: Track development activity and patterns
- **Capabilities**:
  - Commit analysis and statistics
  - Contributor activity tracking
  - Development timeline analysis
  - Change pattern identification
- **Use Cases**: Development activity analysis, contributor insights

### 🔍 **Code Search Server**
- **Purpose**: Search and analyze code patterns and dependencies
- **Capabilities**:
  - Semantic code search
  - Pattern matching
  - Dependency analysis
  - Function and class discovery
- **Use Cases**: Code exploration, dependency mapping, pattern identification

## 🔬 AST/CST Analysis Features

### Abstract Syntax Tree (AST) Analysis
- **Code Structure Parsing**: Parse code into abstract syntax trees
- **Semantic Analysis**: Understand code meaning and relationships
- **Pattern Detection**: Identify coding patterns and anti-patterns
- **Complexity Metrics**: Calculate cyclomatic complexity and other metrics

### Concrete Syntax Tree (CST) Analysis
- **Detailed Syntax Examination**: Analyze exact syntax structure
- **Formatting Analysis**: Understand code formatting and style
- **Token-level Analysis**: Examine individual code tokens
- **Syntax Error Detection**: Identify potential syntax issues

### Advanced Code Intelligence
- **Function Analysis**: Map function calls and dependencies
- **Class Hierarchy**: Analyze class relationships and inheritance
- **Import Analysis**: Track module dependencies and imports
- **Code Quality Metrics**: Assess code quality and maintainability

## 📋 Analysis Types

### 🔍 **Quick Analysis**
Provides instant structured insights:
- **Project Overview**: Purpose, type, and main functionality
- **Technology Stack**: Languages, frameworks, and tools used
- **Architecture Analysis**: System design and organization
- **Dependency Analysis**: External libraries and their purposes
- **Code Quality Assessment**: Quality metrics and recommendations

### 📊 **Smart Summary**
Generate comprehensive technical reports:
- **Complete Repository Analysis**: Full technical assessment
- **Architecture Review**: System design and patterns
- **Code Quality Report**: Metrics, issues, and improvements
- **Development Activity**: Recent changes and contributor insights
- **Best Practices Assessment**: Adherence to coding standards

### 💬 **Q&A Chat**
Natural language repository exploration:
- **Context-Aware Responses**: AI understands repository context
- **Code Examples**: Specific code snippets from the repository
- **Technical Explanations**: Detailed technical insights
- **Actionable Recommendations**: Practical improvement suggestions

## 🎯 Use Cases

### **For Developers**
- **Code Review**: Quickly understand unfamiliar codebases
- **Architecture Analysis**: Evaluate system design and patterns
- **Dependency Management**: Understand and optimize dependencies
- **Code Quality**: Assess and improve code quality

### **For Teams**
- **Onboarding**: Help new team members understand codebases
- **Documentation**: Generate comprehensive project documentation
- **Code Standards**: Ensure adherence to coding standards
- **Technical Debt**: Identify and prioritize technical debt

### **For Managers**
- **Project Assessment**: Evaluate project health and complexity
- **Resource Planning**: Understand development effort and complexity
- **Risk Assessment**: Identify potential technical risks
- **Progress Tracking**: Monitor development activity and patterns

## 🔧 Configuration & Settings

### **Analysis Configuration**
- **Analysis Depth**: Control exploration depth (1-5 levels)
- **AI Model Selection**: Choose from multiple Groq models
- **Tool Usage Display**: Toggle detailed tool usage information
- **Auto-start Servers**: Automatically manage MCP server lifecycle

### **System Monitoring**
- **Server Health**: Real-time MCP server status monitoring
- **Performance Metrics**: Analysis speed and efficiency tracking
- **Error Handling**: Graceful error recovery and reporting
- **Resource Management**: Optimized memory and processing usage

## 📈 Performance & Scalability

### **Optimized Processing**
- **Parallel Execution**: Concurrent MCP tool usage
- **Caching**: Intelligent result caching for repeated queries
- **Memory Management**: Efficient handling of large repositories
- **Network Optimization**: Optimized API calls and data transfer

### **Scalability Features**
- **Large Repository Support**: Handle repositories of any size
- **Incremental Analysis**: Process changes incrementally
- **Background Processing**: Non-blocking analysis operations
- **Resource Monitoring**: Real-time resource usage tracking

## 🔍 Troubleshooting

### **Common Issues**
1. **Server Connection Issues**: Check API keys and network connectivity
2. **Analysis Failures**: Verify repository URL and accessibility
3. **Performance Issues**: Large repositories may require more time
4. **Memory Issues**: Ensure sufficient RAM for large analysis tasks

### **System Requirements**
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum (8GB+ recommended)
- **Storage**: 1GB free space for caching and temporary files
- **Network**: Stable internet connection for repository access

## 🚀 Advanced Features

### **Real-Time Analytics**
- **Live Processing**: Real-time analysis progress tracking
- **Tool Usage Analytics**: Detailed MCP tool usage statistics
- **Performance Metrics**: Analysis speed and efficiency monitoring
- **Error Tracking**: Comprehensive error logging and reporting

### **Enhanced AI Capabilities**
- **Context Awareness**: AI understands repository context and history
- **Multi-language Support**: Analysis across multiple programming languages
- **Pattern Recognition**: Advanced pattern detection and classification
- **Predictive Analysis**: Identify potential issues and improvements

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for:
- Bug reports and feature requests
- Code contributions and pull requests
- Documentation improvements
- Testing and quality assurance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using FastMCP v2, Groq AI, and Streamlit**
