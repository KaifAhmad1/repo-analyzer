# 🚀 GitHub Repository Analyzer

A powerful, AI-driven GitHub repository analysis tool powered by **Google Gemini AI** with advanced multi-agent system capabilities.

## ✨ Features

- **🤖 Google Gemini AI Integration**: Powered by the latest Google Gemini models for intelligent analysis
- **👥 Multi-Agent Team System**: Specialized agents for different aspects of repository analysis
- **🔍 Comprehensive Analysis**: Code quality, architecture, security, and community health assessment
- **📊 Beautiful Visualizations**: Interactive charts and data presentation
- **🛠️ MCP Server Integration**: Seamless integration with Model Context Protocol servers
- **🎨 Modern UI**: Beautiful, responsive interface with Streamlit

## 🏗️ Agent System Architecture

### Single Agent Mode
- **Repository Analyzer Agent**: Comprehensive analysis using Google Gemini
- Enhanced prompt engineering for detailed insights
- Professional analysis with actionable recommendations

### Multi-Agent Team Mode
- **Repository Overview Agent**: Metadata and basic information analysis
- **Code Analysis Agent**: Technical code patterns and architecture assessment
- **Activity Analysis Agent**: Project activity and community health evaluation
- **Security & Quality Agent**: Security vulnerabilities and code quality assessment
- **Team Coordinator**: Orchestrates all agents for comprehensive analysis

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Google API Key** for Gemini AI
3. **GitHub Token** (optional, for private repositories)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd repo-analyzer-8
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Required: Google Gemini API Key
   GOOGLE_API_KEY=your_google_api_key_here
   
   # Optional: GitHub Token for private repos
   GITHUB_TOKEN=your_github_token_here
   
   # Optional: Configuration
   GEMINI_MODEL=gemini-2.0-flash-001
   DEBUG=False
   LOG_LEVEL=INFO
   ```

4. **Get Google API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

### Running the Application

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:8501`

3. **Test the integration**
   ```bash
   python test_gemini_integration.py
   ```

## 🤖 Agent System Details

### Available Models
- `gemini-2.0-flash-001` (Recommended - Fast and efficient)
- `gemini-1.5-pro` (High-quality analysis)
- `gemini-1.5-flash` (Balanced performance)

### Agent Roles and Specializations

#### Repository Overview Agent
- Analyzes repository metadata and structure
- Provides project categorization and technology stack identification
- Focuses on README analysis and basic statistics

#### Code Analysis Agent
- Deep technical analysis of code patterns and architecture
- Identifies design patterns, anti-patterns, and improvement areas
- Assesses code quality, maintainability, and scalability

#### Activity Analysis Agent
- Evaluates project activity and community engagement
- Analyzes commit patterns and development velocity
- Assesses project maturity and maintenance status

#### Security & Quality Agent
- Identifies security vulnerabilities and code quality issues
- Analyzes dependency vulnerabilities and best practices
- Provides security improvement recommendations

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | Required |
| `GITHUB_TOKEN` | GitHub personal access token | Optional |
| `GEMINI_MODEL` | Default Gemini model | `gemini-2.0-flash-001` |
| `DEBUG` | Enable debug mode | `False` |
| `LOG_LEVEL` | Logging level | `INFO` |

### MCP Server Configuration

The application uses Model Context Protocol servers for enhanced functionality:

- **Repository Analyzer Server** (Port 8001)
- **Code Search Server** (Port 8002)
- **Commit History Server** (Port 8003)
- **File Content Server** (Port 8004)
- **Issues Server** (Port 8005)
- **Repository Structure Server** (Port 8006)

## 📊 Features

### Repository Analysis
- **Comprehensive Overview**: Project purpose, structure, and key features
- **Code Quality Assessment**: Architecture patterns, best practices, and improvement areas
- **Security Analysis**: Vulnerability assessment and security recommendations
- **Community Health**: Activity patterns, contributor engagement, and project sustainability

### Visualizations
- **Commit Activity Charts**: Recent development activity trends
- **Language Distribution**: Programming language usage analysis
- **Issue Tracking**: Open/closed issues and pull requests
- **Repository Structure**: File and directory organization

### Interactive Features
- **Real-time Analysis**: Instant repository insights
- **Multi-Agent Coordination**: Specialized analysis from different perspectives
- **Export Capabilities**: Save analysis results and visualizations
- **Custom Queries**: Ask specific questions about repositories

## 🔧 Development

### Project Structure
```
repo-analyzer-8/
├── app.py                          # Main Streamlit application
├── src/
│   ├── agent/
│   │   └── ai_agent.py            # Google Gemini agent system
│   ├── servers/                   # MCP server implementations
│   ├── ui/                        # User interface components
│   └── utils/
│       └── config.py              # Configuration management
├── test_gemini_integration.py     # Integration tests
└── requirements.txt               # Python dependencies
```

### Running Tests
```bash
# Test Google Gemini integration
python test_gemini_integration.py

# Run with specific model
GEMINI_MODEL=gemini-1.5-pro python test_gemini_integration.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for providing the AI capabilities
- **Streamlit** for the beautiful web interface
- **Agno Framework** for the multi-agent system
- **Model Context Protocol** for enhanced tool integration

## 🆘 Support

If you encounter any issues:

1. Check that your Google API key is correctly set
2. Ensure all dependencies are installed
3. Verify your internet connection
4. Check the logs for detailed error messages

For additional support, please open an issue on GitHub. 