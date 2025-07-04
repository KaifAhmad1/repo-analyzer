# 🧠 Smart Tool Selection System Guide

## Overview

The Repository Analyzer now features an intelligent tool selection system that automatically chooses the optimal MCP tools based on your question type and analysis needs. This dramatically improves performance and accuracy by using only the tools that are actually needed.

## 🎯 Analysis Types & Tool Selection

### 🤖 Auto-Detect Mode (Recommended)
The system automatically detects the best analysis type based on your question keywords:

| Question Keywords | Detected Type | Tools Used | Best For |
|------------------|---------------|------------|----------|
| "what", "how", "where", "when", "why" | Q&A Chat | 3-4 tools | General questions |
| "summarize", "overview", "summary" | Summarization | 4-6 tools | Repository summaries |
| "chart", "graph", "visualize", "statistics" | Chart Generation | 3-5 tools | Data visualization |
| "code", "function", "class", "pattern" | Code Analysis | 3-5 tools | Code deep-dive |
| "structure", "organization", "files" | Structure Analysis | 3-4 tools | Project organization |
| "history", "commits", "changes" | History Analysis | 3-4 tools | Development timeline |
| "dependencies", "packages", "requirements" | Dependency Analysis | 2-3 tools | Package management |
| "search", "find", "locate" | Search Analysis | 3-4 tools | Code discovery |

### 🎯 Manual Mode
You can manually select the analysis type for specialized needs:

#### 💬 Q&A Chat
- **Tools**: README, file structure, repository overview
- **Use Case**: General questions about repository purpose and functionality
- **Response Time**: 15-30 seconds

#### 📊 Summary
- **Tools**: README, structure, overview, directory tree, recent commits, dependencies
- **Use Case**: Comprehensive repository overview
- **Response Time**: 20-40 seconds

#### 📈 Chart Data
- **Tools**: Commit statistics, code metrics, recent commits, development patterns
- **Use Case**: Data for visualizations and charts
- **Response Time**: 25-45 seconds

#### 🔍 Code Analysis
- **Tools**: Code metrics, search code, dependencies, complexity analysis
- **Use Case**: Deep code analysis and patterns
- **Response Time**: 20-40 seconds

#### 🏗️ Structure Analysis
- **Tools**: File structure, directory tree, project structure analysis
- **Use Case**: Understanding project organization
- **Response Time**: 15-30 seconds

#### 📝 History Analysis
- **Tools**: Recent commits, commit statistics, development patterns
- **Use Case**: Development timeline and activity
- **Response Time**: 20-35 seconds

## 🚀 Performance Benefits

### Before Smart Selection
- **All Tools**: 15 tools executed for every question
- **Response Time**: 45-60 seconds
- **Resource Usage**: High
- **Relevance**: Often irrelevant tools

### After Smart Selection
- **Optimized Tools**: 2-6 tools based on question type
- **Response Time**: 15-45 seconds
- **Resource Usage**: 60-80% reduction
- **Relevance**: Only relevant tools used

## 📊 Tool Efficiency Matrix

| Analysis Type | Tools Used | Time Saved | Accuracy |
|---------------|------------|------------|----------|
| Q&A Chat | 3 | 70% | High |
| Summary | 5 | 60% | Very High |
| Chart Data | 4 | 65% | High |
| Code Analysis | 4 | 65% | Very High |
| Structure | 3 | 70% | High |
| History | 3 | 70% | High |

## 🎯 How to Use Smart Mode

### 1. Select Smart Mode
```
⚡ Fast Mode (30s) | 🔍 Standard Mode (60s) | 🧠 Smart Mode (Auto)
```

### 2. Choose Analysis Type (Optional)
- **Auto-detect**: Let AI choose the best type
- **Manual**: Select specific analysis type

### 3. Ask Your Question
The system will automatically:
- Detect the question type
- Select optimal tools
- Execute only relevant analysis
- Provide focused results

## 💡 Best Practices

### ✅ Optimal Questions for Each Type

#### Q&A Chat
- "What is this repository about?"
- "How does this project work?"
- "What are the main features?"

#### Summary
- "Summarize this repository"
- "Give me an overview of this project"
- "What does this codebase do?"

#### Chart Data
- "Generate chart data for this repository"
- "Show me development statistics"
- "Create visualization data"

#### Code Analysis
- "Analyze the code patterns"
- "What's the code quality like?"
- "Show me the architecture"

#### Structure Analysis
- "What's the project structure?"
- "How is this organized?"
- "Show me the file layout"

#### History Analysis
- "What's the development history?"
- "Show me recent changes"
- "What's the commit activity?"

### ⚠️ Avoid These Questions
- "Analyze everything" (too broad)
- "Tell me about the entire codebase" (use summary instead)
- "Show me all patterns" (use code analysis instead)

## 🔧 Technical Details

### Tool Selection Algorithm
1. **Keyword Analysis**: Scans question for relevant keywords
2. **Type Detection**: Matches keywords to analysis types
3. **Tool Mapping**: Selects essential and optional tools
4. **Relevance Check**: Filters tools based on question context
5. **Execution**: Runs only selected tools in parallel

### Server Optimization
- **File Content Server**: README, file analysis
- **Repository Structure Server**: Structure, organization
- **Commit History Server**: History, statistics, patterns
- **Code Search Server**: Code analysis, metrics, search

### Caching Strategy
- **Tool Results**: Cached for reuse
- **Analysis Types**: Remembered for similar questions
- **Performance Stats**: Tracked for optimization

## 📈 Performance Monitoring

The system tracks:
- **Tool Selection Accuracy**: How well tools match questions
- **Execution Time**: Time saved by smart selection
- **Cache Hit Rate**: Reuse of previous results
- **User Satisfaction**: Response relevance

## 🚨 Troubleshooting

### If Smart Mode is Slow:
1. **Check Question Type**: Ensure it matches an analysis type
2. **Use Auto-detect**: Let AI choose the best type
3. **Simplify Question**: Make it more specific
4. **Check Server Status**: Ensure all MCP servers are running

### If Results are Incomplete:
1. **Try Different Type**: Switch to a more comprehensive type
2. **Use Standard Mode**: For full analysis
3. **Ask Follow-up**: Use specific questions for missing data

### If Auto-detect is Wrong:
1. **Manual Selection**: Choose the analysis type manually
2. **Rephrase Question**: Use keywords that match the desired type
3. **Use Standard Mode**: For comprehensive analysis

## 🎯 Advanced Usage

### Custom Analysis Types
You can extend the system with custom analysis types:
```python
# Add custom analysis type
custom_tools = {
    "security_analysis": {
        "essential": ["search_code", "get_file_structure"],
        "keywords": ["security", "vulnerability", "auth"]
    }
}
```

### Performance Tuning
- **Adjust Timeouts**: Modify based on repository size
- **Tool Limits**: Set maximum tools per analysis
- **Cache Settings**: Configure caching behavior

## 📚 Examples

### Example 1: Quick Q&A
**Question**: "What is this repository about?"
**Detected Type**: Q&A Chat
**Tools Used**: README, file structure, overview
**Response Time**: 15 seconds

### Example 2: Code Analysis
**Question**: "Analyze the code patterns and architecture"
**Detected Type**: Code Analysis
**Tools Used**: Code metrics, search code, dependencies, complexity
**Response Time**: 25 seconds

### Example 3: Chart Data
**Question**: "Generate data for development activity charts"
**Detected Type**: Chart Generation
**Tools Used**: Commit statistics, code metrics, recent commits
**Response Time**: 30 seconds

---

**Remember**: Smart Mode is the most efficient way to get relevant, fast responses! 🚀 