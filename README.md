# 🚀 GitHub Repository Analyzer - Enhanced & Comprehensive

A powerful, systematic GitHub repository analyzer that provides **deep insights** through AI-powered analysis, Q&A capabilities, and multiple analysis types using **all available MCP servers** and **advanced LLMs**. This system ensures **comprehensive data gathering** from every repository for **accurate, detailed responses**.

## 🎯 **Key Improvements & Features**

### 🔥 **NEW: Enhanced AI Agent with Full MCP Utilization**
- **Guaranteed comprehensive data gathering** from all MCP servers for every Q&A and analysis
- **Parallel tool execution** using ThreadPoolExecutor for faster data collection from all MCP servers simultaneously
- **Advanced LLM integration** using Groq's latest models for superior reasoning
- **Smart data synthesis** that combines information from file content, structure, commits, and code search
- **Real-time progress tracking** with detailed status updates
- **Tool utilization tracking** - every response includes a list of which MCP tools were used for transparency

### 🗺️ **NEW: Interactive Repository Visualizations**
- **Directory Tree Maps**: Interactive treemap visualizations of repository structure
- **Dependency Graphs**: Network graphs showing project dependencies and relationships
- **Code Activity Heatmaps**: Visual representation of development activity over time
- **Language Distribution Charts**: Pie charts showing programming language usage
- **File Size Distribution**: Histograms of file sizes and complexity

### 📊 **NEW: Advanced Code Analysis**
- **Code Quality Metrics**: Comprehensive quality scoring with detailed recommendations
- **Complexity Analysis**: Cyclomatic and cognitive complexity measurements
- **Pattern Detection**: Automatic detection of design patterns, anti-patterns, and code smells
- **Architecture Analysis**: Deep insights into code organization and structure
- **Interactive Visualizations**: Quality score gauges, complexity distributions, and pattern analysis charts

### 🧠 **NEW: Smart Summarization**
- **Comprehensive Repository Summaries**: AI-powered summaries covering all aspects
- **Architecture Insights**: Detailed analysis of project structure and design decisions
- **Development Patterns**: Analysis of commit history and development workflow
- **Dependency Analysis**: Complete dependency mapping and security assessment
- **Recommendations**: Actionable insights for improvement

### 💬 **Enhanced Q&A System**
- **Deep Context Understanding**: Every question uses data from all MCP servers
- **Parallel Data Gathering**: All MCP tools execute simultaneously for faster responses
- **Comprehensive Answers**: Responses include code examples, patterns, and architectural insights
- **Follow-up Support**: Context-aware follow-up questions and clarifications
- **Evidence-Based Responses**: All answers include supporting evidence from the codebase
- **Tool Transparency**: Every response shows which MCP tools were used for complete transparency

## ✨ Features

### 🔍 **Enhanced Analysis Types**
- **Comprehensive Analysis**: Full repository analysis with multiple dimensions
- **Quick Overview**: Fast repository summary and insights
- **Security Analysis**: Security-focused analysis and vulnerability detection
- **Code Quality Analysis**: Advanced code quality, complexity, and pattern analysis
- **Visualization Analysis**: Interactive repository maps and dependency graphs
- **Smart Summarization**: AI-powered comprehensive repository summaries
- **Custom Analysis**: Tailored analysis based on specific requirements

### 💬 **AI-Powered Q&A**
- Ask specific questions about any repository
- Get detailed answers with context from the codebase
- Support for complex queries and follow-up questions
- Real-time analysis using multiple MCP servers

### 🛠️ **Advanced Tools & Servers**
- **File Content Server**: Retrieve and analyze file contents with code analysis
- **Repository Structure Server**: Analyze directory trees and file organization
- **Commit History Server**: Track changes and development patterns
- **Code Search Server**: Search for specific code patterns, functions, and dependencies
- **Enhanced AI Agent**: Comprehensive data synthesis using all MCP servers
- **Code Analyzer**: Advanced code quality, complexity, and pattern analysis
- **Repository Visualizer**: Interactive visualizations and dependency mapping

### 📊 **Session Management & Persistence**
- Save analysis sessions throughout your workflow
- Export analysis results and session data
- Track analysis history and progress
- Cache results for faster subsequent runs

### 🎯 **Enhanced User Interface**
- Modern, responsive Streamlit interface with multiple analysis tabs
- Real-time progress tracking with detailed status updates
- Interactive visualizations (treemaps, network graphs, heatmaps, charts)
- Easy-to-use repository selection and session management
- Comprehensive results display with AI summaries and recommendations

## 🚀 Quick Start

### 1. **Installation**

   ```bash
# Clone the repository
git clone <repository-url>
cd repo-analyzer

# Install dependencies
   pip install -r requirements.txt
   ```

### 2. **Configuration**

Create a `.env` file in the root directory:

```env
# Required: Get your API key from https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here

# Optional: GitHub token for higher rate limits
GITHUB_TOKEN=your_github_token_here
```

### 3. **Start the Application**

   ```bash
# Start the Streamlit app
streamlit run app.py
   ```

### 4. **Start MCP Servers (Recommended)**

For full functionality and enhanced analysis, start the MCP servers:

#### **Simple Startup Script**

```bash
# Start all MCP servers with one command
python start_servers.py
```

**Features:**
- ✅ Starts all 4 MCP servers automatically
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ Simple one-command startup
- ✅ Graceful shutdown with Ctrl+C
- ✅ Shows server status and PIDs
- ✅ UTF-8 encoded for compatibility

#### **Alternative: Start Individual Servers**

```bash
# Start servers individually
python src/servers/file_content_server.py
python src/servers/repository_structure_server.py
python src/servers/commit_history_server.py
python src/servers/code_search_server.py
```

### 5. **Run Tests (Optional)**

Verify all components are working correctly:

   ```bash
python test_enhanced_system.py
```

## 📖 Usage Guide

### **Step 1: Select a Repository**
1. Enter a GitHub repository URL in the sidebar
2. Click "Analyze Repository" to set it as the current repository
3. View basic repository information (stars, forks, description)

### **Step 2: Choose Analysis Type**

#### **🔍 Enhanced Analysis Tab**
- **Quick Overview**: Get a fast summary of the repository
- **Comprehensive Analysis**: Full analysis with multiple dimensions
  - Choose from presets: Quick, Standard, Deep, Security Focus
  - Configure analysis options (file limits, depth, etc.)
- **Security Analysis**: Focus on security aspects and vulnerabilities
- **Code Quality**: Advanced code quality, complexity, and pattern analysis
- **Visualizations**: Interactive repository maps and dependency graphs
- **Smart Summary**: AI-powered comprehensive repository summaries

#### **💬 Q&A Chat Tab**
- Ask specific questions about the repository
- Use quick question buttons for common queries
- Get detailed answers with context from the codebase

#### **⚙️ Advanced Settings Tab**
- Configure analysis parameters
- Set file size and count limits
- Enable/disable caching
- Choose analysis presets

### **Step 3: View Results**
- **Real-time Progress**: Track analysis progress with detailed status updates
- **Comprehensive Results**: View detailed analysis in organized sections
- **Interactive Visualizations**: Explore repository structure with interactive charts and graphs
- **AI Summaries**: Get AI-powered summaries of analysis results with recommendations
- **Tool Utilization**: See exactly which MCP tools were called for each query/analysis
- **Quality Metrics**: View code quality scores and improvement recommendations
- **Performance**: Experience faster analysis with parallel tool execution

### **Step 4: Session Management**
- **Export Results**: Download session data and analysis results
- **View History**: Track previous analyses
- **Clear Session**: Start fresh with a new session

## 🔧 Analysis Types Explained

### **Quick Overview**
- Repository information and statistics
- README content analysis
- Basic file structure
- AI-generated summary

### **Comprehensive Analysis**
- **Repository Information**: Stars, forks, language, topics, etc.
- **File Structure**: Directory trees, file organization, project structure
- **Code Metrics**: Lines of code, functions, classes, complexity
- **Dependencies**: Package files, dependency analysis
- **Commit History**: Recent commits, statistics, development patterns
- **Security Analysis**: Security patterns, risk assessment
- **AI Summary**: Comprehensive AI-generated analysis

### **Security Analysis**
- Security pattern detection
- Dependency vulnerability checks
- Code security patterns
- Risk level assessment
- Security recommendations

### **Code Quality Analysis**
- **Advanced Code Metrics**: Lines of code, functions, classes, complexity analysis
- **Quality Scoring**: Comprehensive quality score with detailed recommendations
- **Pattern Detection**: Design patterns, anti-patterns, code smells, and best practices
- **Complexity Analysis**: Cyclomatic and cognitive complexity measurements
- **Interactive Visualizations**: Quality gauges, complexity distributions, pattern charts
- **Documentation Assessment**: Code documentation and README analysis
- **Testing Analysis**: Test coverage and testing patterns

## 🛠️ Technical Architecture

### **Core Components**

```
repo-analyzer/
├── start_servers.py      # 🚀 Simple MCP Server Starter
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── src/
    ├── agent/                 # AI agent implementation
    │   └── ai_agent.py       # Enhanced AI agent with comprehensive MCP integration
    ├── analysis/             # Analysis engine and tools
    │   ├── analysis_engine.py # Comprehensive analysis engine
    │   ├── code_analyzer.py  # Advanced code quality and complexity analysis
    │   └── repository_visualizer.py # Interactive visualization generator
    ├── servers/              # FastMCP v2 servers
    │   ├── file_content_server.py
    │   ├── repository_structure_server.py
    │   ├── commit_history_server.py
    │   ├── code_search_server.py
    │   └── server_manager.py
    ├── ui/                   # User interface components
    │   ├── repository_selector.py
    │   ├── chat_interface.py
    │   ├── analysis_interface.py # Enhanced with new analysis tabs
    │   ├── settings_sidebar.py
    │   └── modern_styles.css
    └── utils/                # Utilities and configuration
        ├── config.py         # Configuration management
        └── repository_manager.py # Repository and session management
```

### **Server Management**

The project includes a simple server management system:

- **`start_servers.py`**: Simple Python script for starting all MCP servers
  - Cross-platform compatibility (Windows, macOS, Linux)
  - Automatic server startup with status reporting
  - Graceful shutdown with Ctrl+C
  - Shows process IDs for monitoring
  - UTF-8 encoded for maximum compatibility

### **MCP Servers**

1. **File Content Server** 📄
   - Retrieve file contents
   - Analyze file structure
   - Get README content
   - Code analysis and metrics

2. **Repository Structure Server** 📁
   - Directory tree analysis
   - File structure analysis
   - Project organization insights

3. **Commit History Server** 📝
   - Recent commit analysis
   - Commit statistics
   - Development pattern analysis

4. **Code Search Server** 🔍
   - Code pattern search
   - Function and class discovery
   - Dependency analysis
   - Code metrics and complexity analysis

### **Enhanced Components**

5. **Enhanced AI Agent** 🤖
   - Comprehensive data gathering from all MCP servers
   - Advanced LLM integration with Groq models
   - Smart data synthesis and reasoning
   - Real-time progress tracking

6. **Code Analyzer** 📊
   - Code quality metrics and scoring
   - Complexity analysis (cyclomatic, cognitive)
   - Pattern detection (design patterns, anti-patterns)
   - Interactive visualizations

7. **Repository Visualizer** 🗺️
   - Interactive directory tree maps
   - Dependency network graphs
   - Activity heatmaps
   - Language distribution charts

## ⚙️ Configuration

### **Analysis Presets**

- **Quick**: Fast analysis with basic insights (20 files, 2 depth)
- **Standard**: Comprehensive analysis with metrics (50 files, 3 depth)
- **Deep**: In-depth analysis with all features (100 files, 5 depth)
- **Security**: Security-focused analysis (75 files, 4 depth)

### **Settings**

- **Max File Size**: Maximum file size to analyze (default: 1MB)
- **Max Files**: Maximum number of files per analysis (default: 100)
- **Include Hidden Files**: Whether to analyze hidden files
- **Enable Caching**: Cache results for faster subsequent runs
- **Analysis Timeout**: Maximum time for analysis (default: 5 minutes)

## 🔑 API Requirements

### **Required**
- **Groq API Key**: For AI-powered analysis and Q&A
  - Get from: https://console.groq.com/
  - Supports models: llama-3.1-70b-versatile, llama-3.1-8b-instant, etc.

### **Optional**
- **GitHub Token**: For higher rate limits and private repository access
  - Get from: https://github.com/settings/tokens

## 📊 Example Use Cases

### **1. Repository Exploration**
```
Question: "What is this repository about and what are its main features?"
Analysis: Quick overview with AI summary
```

### **2. Code Quality Assessment**
```
Question: "How well is this codebase structured and what are the quality metrics?"
Analysis: Code quality analysis with metrics and patterns
```

### **3. Security Review**
```
Question: "Are there any security vulnerabilities in this codebase?"
Analysis: Security analysis with pattern detection
```

### **4. Dependency Analysis**
```
Question: "What dependencies does this project use and are there any security issues?"
Analysis: Comprehensive analysis with dependency focus
```

### **5. Development Patterns**
```
Question: "What are the recent development patterns and commit frequency?"
Analysis: Commit history analysis with statistics
```

## 🧪 Testing

Run the comprehensive test suite to verify all enhanced components:

```bash
python test_enhanced_system.py
```

This will test:
- **Module Imports**: All enhanced modules and components
- **FastMCP Tools**: All MCP server integrations
- **AI Agent**: Enhanced AI agent with comprehensive data gathering
- **Code Analyzer**: Advanced code quality and complexity analysis
- **Repository Visualizer**: Interactive visualization generation
- **Analysis Engine**: Complete analysis engine with new features
- **Configuration**: Settings and preset management
- **Repository Manager**: Session and data management
- **Component Integration**: All components working together
- **Function Exports**: All public functions and APIs

## 🚀 Advanced Usage

### **Enhanced Analysis**
```python
from src.analysis.analysis_engine import (
    analyze_repository, 
    code_quality_analysis,
    generate_visualizations,
    smart_summarization
)

# Comprehensive analysis with all features
result = analyze_repository(
    repo_url="https://github.com/example/repo",
    analysis_type="comprehensive",
    preset="deep"
)

# Advanced code quality analysis
quality_result = code_quality_analysis("https://github.com/example/repo")

# Generate interactive visualizations
viz_result = generate_visualizations("https://github.com/example/repo")

# Smart summarization with AI insights
summary_result = smart_summarization("https://github.com/example/repo")
```

### **Session Management**
```python
from src.utils.repository_manager import (
    set_current_repository,
    get_analysis_history,
    export_session_data
)

# Set repository
set_current_repository("https://github.com/example/repo")

# Get analysis history
history = get_analysis_history()

# Export session data
session_data = export_session_data()
```

### **Enhanced MCP Integration**
```python
from src.agent.ai_agent import (
    FastMCPTools, 
    RepositoryAnalyzerAgent,
    ask_repository_question,
    generate_repository_summary
)

# Use enhanced MCP tools directly
tools = FastMCPTools()
file_content = tools.get_file_content("https://github.com/example/repo", "README.md")

# Use AI agent for comprehensive Q&A
agent = RepositoryAnalyzerAgent()
answer, tools_used = agent.ask_question(
    "What are the main architectural patterns?", 
    "https://github.com/example/repo"
)

# Generate comprehensive summary
summary, tools_used = generate_repository_summary("https://github.com/example/repo")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check the inline documentation and comments
- **Testing**: Run the test suite to verify functionality

## 🔮 Recent Enhancements & Future Plans

### ✅ **Recently Implemented**
- [x] **Enhanced AI Agent**: Comprehensive data gathering from all MCP servers
- [x] **Interactive Visualizations**: Repository maps, dependency graphs, activity heatmaps
- [x] **Advanced Code Analysis**: Quality metrics, complexity analysis, pattern detection
- [x] **Smart Summarization**: AI-powered comprehensive repository summaries
- [x] **Enhanced UI**: Multiple analysis tabs with real-time progress tracking
- [x] **Comprehensive Testing**: Full test suite for all enhanced components

### 🚀 **Future Enhancements**
- [ ] Integration with more vulnerability databases
- [ ] Support for more programming languages
- [ ] Advanced code visualization with 3D representations
- [ ] Team collaboration features and shared analysis sessions
- [ ] Integration with CI/CD pipelines for automated analysis
- [ ] Advanced caching and performance optimizations
- [ ] Machine learning-based code quality predictions
- [ ] Real-time collaboration and commenting features

## 🎯 **How This System Ensures Full MCP Utilization**

### **Guaranteed Comprehensive Data Gathering**
Every Q&A, analysis, and summary request automatically triggers data collection from **all available MCP servers**:

1. **File Content Server**: Retrieves README, key files, and code content
2. **Repository Structure Server**: Analyzes directory trees and file organization
3. **Commit History Server**: Gathers recent commits and development patterns
4. **Code Search Server**: Searches for patterns, functions, and dependencies

### **AI Agent Integration**
The enhanced AI agent:
- **Always calls all MCP servers** before generating responses
- **Executes tool calls in parallel** using ThreadPoolExecutor for faster data collection
- **Synthesizes data** from multiple sources for comprehensive answers
- **Provides evidence-based responses** with supporting code examples
- **Tracks tool utilization** for transparency and debugging
- **Returns tool usage list** with every response for complete transparency

### **Example: Q&A Process**
When you ask "What are the main architectural patterns in this repo?":

1. **Parallel Data Gathering Phase**:
   - All MCP servers execute simultaneously:
     - File Content Server → Analyzes main files and README
     - Structure Server → Maps directory organization
     - Commit Server → Identifies development patterns
     - Code Search Server → Finds design patterns and architecture
   - Results are collected as they complete for optimal performance

2. **AI Synthesis Phase**:
   - All data is combined and analyzed by the LLM
   - AI generates comprehensive answer with examples
   - Response includes evidence from multiple sources

3. **Result Display**:
   - Detailed answer with code examples
   - Complete list of MCP tools used for transparency
   - Supporting visualizations when relevant
   - Performance metrics showing parallel execution benefits

### **Quality Assurance**
- **Comprehensive Testing**: Full test suite verifies all components
- **Real-time Progress**: Users see exactly what data is being gathered
- **Tool Transparency**: Every result shows which MCP servers were used
- **Parallel Execution**: Optimized performance with concurrent tool calls
- **Error Handling**: Graceful fallbacks if any server is unavailable
- **Performance Monitoring**: Track execution time and tool utilization metrics

---

**Built with ❤️ using Streamlit, FastMCP v2, Groq AI, and Advanced LLMs**
