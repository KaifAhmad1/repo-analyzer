# 🚀 Repository Analyzer Performance Guide

## Quick Response Tips

### ⚡ Fast Mode (Recommended for Quick Questions)
- **Use Fast Mode** for simple questions about repository purpose, structure, or basic functionality
- **Response Time**: 15-30 seconds
- **Tools Used**: Only essential tools (README, file structure, overview)
- **Best For**: "What is this repo about?", "Show file structure", "What dependencies?"

### 🔍 Standard Mode (For Detailed Analysis)
- **Use Standard Mode** for comprehensive analysis, code patterns, and detailed insights
- **Response Time**: 30-60 seconds
- **Tools Used**: 10 optimized tools (reduced from 15)
- **Best For**: "Analyze code patterns", "Show development history", "Find performance issues"

## 🎯 Optimized Questions for Faster Responses

### ✅ Good Questions (Fast Response)
- "What is this repository about?"
- "Show me the main entry points"
- "What dependencies does this use?"
- "What's the project structure?"
- "Show me the README"

### ⚠️ Complex Questions (Slower Response)
- "Analyze all code patterns and architecture"
- "Find all performance bottlenecks"
- "Show me the complete development history"
- "Analyze code complexity metrics"

## 🛠️ Performance Optimizations Made

### Recent Improvements
1. **Reduced Tool Count**: From 15 to 10 tools in Standard mode
2. **Fast Mode**: New mode with only 3 essential tools
3. **Optimized Timeouts**: 30s for Fast mode, 60s for Standard mode
4. **Parallel Processing**: All tools run simultaneously
5. **Smart Tool Selection**: Only relevant tools based on question type

### Technical Optimizations
- **Reduced Directory Depth**: From 4 to 3 levels
- **Fewer Commits**: From 25 to 15 recent commits
- **Shorter History**: From 60 to 30 days
- **Essential Data Only**: Focus on key information

## 🚨 Troubleshooting Slow Responses

### If You're Still Getting Timeouts:
1. **Try Fast Mode First**: Always start with Fast Mode for basic questions
2. **Simplify Questions**: Break complex questions into smaller parts
3. **Check Repository Size**: Very large repositories may take longer
4. **Network Issues**: Ensure stable internet connection
5. **Server Status**: Verify all MCP servers are running

### Error Messages:
- **"Analysis timed out"**: Try Fast Mode or simpler question
- **"Error during analysis"**: Check server status and try again
- **"Connection failed"**: Verify repository URL and network

## 📊 Performance Comparison

| Mode | Tools | Timeout | Best For | Response Time |
|------|-------|---------|----------|---------------|
| ⚡ Fast | 3 | 30s | Quick overview | 15-30s |
| 🔍 Standard | 10 | 60s | Detailed analysis | 30-60s |

## 💡 Pro Tips

1. **Start with Fast Mode**: Always begin with Fast Mode to get quick insights
2. **Use Quick Questions**: Click the pre-built quick questions for instant results
3. **Break Down Questions**: Ask multiple simple questions instead of one complex one
4. **Check Server Status**: Ensure all servers are running before analysis
5. **Clear Cache**: Use the clear button if you experience issues

## 🔧 Advanced Settings

### For Developers:
- **Custom Timeouts**: Modify timeout values in `src/agent/ai_agent.py`
- **Tool Selection**: Customize which tools to use in each mode
- **Parallel Workers**: Adjust `max_workers` in `FastMCPTools` class
- **Cache Management**: Clear tool cache for fresh analysis

### Server Configuration:
- **MCP Server Timeouts**: Adjust in individual server files
- **Worker Threads**: Modify `max_workers` for better performance
- **Connection Pooling**: Optimize server connections

## 📈 Performance Monitoring

The system tracks:
- **Tool Execution Time**: How long each tool takes
- **Server Response Times**: MCP server performance
- **Cache Hit Rates**: Tool result caching efficiency
- **Error Rates**: Failed tool executions

Check performance insights in the UI for detailed metrics.

---

**Remember**: Fast Mode is your friend for quick questions! 🚀 