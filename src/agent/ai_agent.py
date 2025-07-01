"""
GitHub Repository Analyzer - AI Agent System
Simple, effective AI agent for GitHub repository analysis using MCP servers
"""

import os
import json
from typing import Dict, List, Any, Optional
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from src.servers.mcp_client_improved import UnifiedMCPClient

class RepositoryAnalysisTools:
    """Simple tools wrapper for GitHub repository analysis"""
    
    def __init__(self):
        self.mcp_client = UnifiedMCPClient()
    
    def get_repository_overview(self, repo_url: str) -> str:
        """Get basic repository information"""
        try:
            with self.mcp_client as client:
                result = client.get_repository_overview(repo_url)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_file_structure(self, repo_url: str) -> str:
        """Get repository file structure"""
        try:
            with self.mcp_client as client:
                result = client.get_file_structure(repo_url)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_directory_tree(self, repo_url: str, max_depth: int = 3) -> str:
        """Get directory tree structure"""
        try:
            with self.mcp_client as client:
                result = client.get_directory_tree(repo_url, max_depth)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_file_content(self, repo_url: str, file_path: str) -> str:
        """Get content of a specific file"""
        try:
            with self.mcp_client as client:
                result = client.get_file_content(repo_url, file_path)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_recent_commits(self, repo_url: str, limit: int = 10) -> str:
        """Get recent commit history"""
        try:
            with self.mcp_client as client:
                result = client.get_recent_commits(repo_url, limit)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_issues(self, repo_url: str, state: str = "open", limit: int = 10) -> str:
        """Get repository issues"""
        try:
            with self.mcp_client as client:
                result = client.get_issues(repo_url, state, limit)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def search_code(self, repo_url: str, query: str, language: str = "") -> str:
        """Search for code patterns"""
        try:
            with self.mcp_client as client:
                result = client.search_code(repo_url, query, language)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_code_metrics(self, repo_url: str) -> str:
        """Get code metrics and statistics"""
        try:
            with self.mcp_client as client:
                result = client.get_code_metrics(repo_url)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

def create_repository_analyzer_agent(model_name: str = "gemini-2.0-flash-001") -> Agent:
    """Create a focused repository analysis agent"""
    
    tools = RepositoryAnalysisTools()
    
    # Clear, focused instructions for the agent
    agent_instructions = [
        "You are a GitHub Repository Analyzer. Your job is to answer questions about GitHub repositories using available tools.",
        "",
        "Available Tools:",
        "- get_repository_overview: Get basic repo info (description, stats, etc.)",
        "- get_file_structure: Get file structure analysis",
        "- get_directory_tree: Get directory tree structure", 
        "- get_file_content: Read specific file contents",
        "- get_recent_commits: Get recent commit history",
        "- get_issues: Get issues and pull requests",
        "- search_code: Search for code patterns",
        "- get_code_metrics: Get code statistics",
        "",
        "How to Answer Questions:",
        "1. Always use the appropriate tools to get accurate information",
        "2. For 'what is this repo about' - use get_repository_overview and get_file_content for README",
        "3. For 'main entry points' - use get_file_structure and look for main files",
        "4. For 'recent changes' - use get_recent_commits",
        "5. For 'find functions' - use search_code",
        "6. For 'dependencies' - use get_file_content on requirements.txt, package.json, etc.",
        "7. For 'issues' - use get_issues",
        "8. For 'database connection' - use search_code for database-related terms",
        "9. For 'testing strategy' - use search_code for test files and get_file_structure",
        "",
        "Response Format:",
        "- Be clear and concise",
        "- Use markdown formatting",
        "- Include relevant code examples when helpful",
        "- Structure answers with headers and bullet points",
        "- Always explain what you found and how you found it",
        "",
        "Remember: Use tools first, then provide analysis based on the data you gather."
    ]
    
    agent = Agent(
        name="Repository Analyzer",
        model=Gemini(id=model_name),
        tools=[
            ReasoningTools(add_instructions=True),
            tools.get_repository_overview,
            tools.get_file_structure,
            tools.get_directory_tree,
            tools.get_file_content,
            tools.get_recent_commits,
            tools.get_issues,
            tools.search_code,
            tools.get_code_metrics,
        ],
        instructions=agent_instructions,
        markdown=True,
        add_datetime_to_instructions=True,
    )
    
    return agent

def ask_question(question: str, repository_url: str) -> str:
    """Ask a question about a repository"""
    try:
        agent = create_repository_analyzer_agent()
        response = agent.run(f"Question: {question}\nRepository: {repository_url}")
        return response
    except Exception as e:
        return f"Error getting response: {str(e)}"

def analyze_repository(repository_url: str) -> str:
    """Perform comprehensive repository analysis"""
    try:
        agent = create_repository_analyzer_agent()
        response = agent.run(f"Provide a comprehensive analysis of this repository: {repository_url}")
        return response
    except Exception as e:
        return f"Error analyzing repository: {str(e)}"

# Legacy compatibility functions
def create_ai_agent(model_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create AI agent (legacy function)"""
    agent = create_repository_analyzer_agent(model_name)
    return {
        "agent": agent,
        "model": model_name,
        "config": config
    }

def ask_question_advanced(question: str, repository_url: str, use_team: bool = False) -> str:
    """Advanced question function (simplified to use single agent)"""
    return ask_question(question, repository_url)

def analyze_repository_advanced(repository_url: str) -> str:
    """Advanced analysis function (simplified to use single agent)"""
    return analyze_repository(repository_url) 
