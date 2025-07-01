"""
Advanced AI Agent System for GitHub Repository Analysis
Integrates with all FastMCP v2 servers using Google Gemini AI
"""

import os
import json
from typing import Dict, List, Any, Optional
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.team.team import Team
from src.servers.mcp_client_improved import UnifiedMCPClient

class UnifiedMCPTools:
    """Comprehensive agent tools wrapper for all FastMCP v2 servers"""
    
    def __init__(self):
        self.mcp_client = UnifiedMCPClient()
    
    # Repository Analyzer Server Tools
    def get_repository_overview(self, repo_url: str) -> str:
        """Get repository overview using MCP server"""
        try:
            with self.mcp_client as client:
                result = client.get_repository_overview(repo_url)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting repository overview: {str(e)}"
    
    def analyze_repository(self, repo_url: str) -> str:
        """Perform comprehensive repository analysis"""
        try:
            with self.mcp_client as client:
                result = client.analyze_repository(repo_url)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error analyzing repository: {str(e)}"
    
    def get_repository_activity(self, repo_url: str, days: int = 30) -> str:
        """Get repository activity analysis"""
        try:
            with self.mcp_client as client:
                result = client.get_repository_activity(repo_url, days)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting repository activity: {str(e)}"
    
    # File Content Server Tools
    def get_file_content(self, repo_url: str, file_path: str) -> str:
        """Get file content"""
        try:
            with self.mcp_client as client:
                result = client.get_file_content(repo_url, file_path)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting file content: {str(e)}"
    
    def list_directory(self, repo_url: str, directory_path: str = "") -> str:
        """List directory contents"""
        try:
            with self.mcp_client as client:
                result = client.list_directory(repo_url, directory_path)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    # Repository Structure Server Tools
    def get_directory_tree(self, repo_url: str, max_depth: int = 3) -> str:
        """Get directory tree structure"""
        try:
            with self.mcp_client as client:
                result = client.get_directory_tree(repo_url, max_depth)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting directory tree: {str(e)}"
    
    def get_file_structure(self, repo_url: str) -> str:
        """Get file structure analysis"""
        try:
            with self.mcp_client as client:
                result = client.get_file_structure(repo_url)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting file structure: {str(e)}"
    
    # Commit History Server Tools
    def get_recent_commits(self, repo_url: str, limit: int = 10) -> str:
        """Get recent commit history"""
        try:
            with self.mcp_client as client:
                result = client.get_recent_commits(repo_url, limit)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting commits: {str(e)}"
    
    def get_commit_statistics(self, repo_url: str, days: int = 30) -> str:
        """Get commit statistics"""
        try:
            with self.mcp_client as client:
                result = client.get_commit_statistics(repo_url, days)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting commit statistics: {str(e)}"
    
    def get_commit_details(self, repo_url: str, commit_sha: str) -> str:
        """Get detailed commit information"""
        try:
            with self.mcp_client as client:
                result = client.get_commit_details(repo_url, commit_sha)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting commit details: {str(e)}"
    
    # Issues Server Tools
    def get_issues(self, repo_url: str, state: str = "open", limit: int = 10) -> str:
        """Get repository issues"""
        try:
            with self.mcp_client as client:
                result = client.get_issues(repo_url, state, limit)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting issues: {str(e)}"
    
    def get_pull_requests(self, repo_url: str, state: str = "open", limit: int = 10) -> str:
        """Get pull requests"""
        try:
            with self.mcp_client as client:
                result = client.get_pull_requests(repo_url, state, limit)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting pull requests: {str(e)}"
    
    def get_issue_statistics(self, repo_url: str) -> str:
        """Get issue statistics"""
        try:
            with self.mcp_client as client:
                result = client.get_issue_statistics(repo_url)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting issue statistics: {str(e)}"
    
    # Code Search Server Tools
    def search_code(self, repo_url: str, query: str, language: str = "") -> str:
        """Search for code patterns"""
        try:
            with self.mcp_client as client:
                result = client.search_code(repo_url, query, language)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error searching code: {str(e)}"
    
    def search_files(self, repo_url: str, filename_pattern: str) -> str:
        """Search for files by pattern"""
        try:
            with self.mcp_client as client:
                result = client.search_files(repo_url, filename_pattern)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error searching files: {str(e)}"
    
    def get_code_metrics(self, repo_url: str) -> str:
        """Get code metrics and statistics"""
        try:
            with self.mcp_client as client:
                result = client.get_code_metrics(repo_url)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting code metrics: {str(e)}"

def create_advanced_agent(model_name: str = "gemini-2.0-flash-001") -> Agent:
    """Create advanced agent with comprehensive MCP tools integration using Google Gemini"""
    
    # Initialize unified MCP tools
    mcp_tools = UnifiedMCPTools()
    
    # Enhanced prompt engineering for the main agent
    main_agent_instructions = [
        "You are an expert GitHub repository analyzer powered by Google Gemini AI.",
        "Your role is to provide comprehensive, insightful analysis of code repositories using all available MCP tools.",
        "You have access to multiple specialized MCP servers that provide different types of repository data:",
        "- Repository Analyzer: Overview, analysis, and activity data",
        "- File Content: File contents and directory listings", 
        "- Repository Structure: Directory trees and structure analysis",
        "- Commit History: Commit data and statistics",
        "- Issues: Issues and pull requests data",
        "- Code Search: Code search and metrics",
        "Always use the appropriate MCP tools to gather accurate information before making conclusions.",
        "Structure your responses with clear sections: Overview, Analysis, Insights, and Recommendations.",
        "Include relevant code examples and technical details when appropriate.",
        "Use markdown formatting for better readability including tables, code blocks, and lists.",
        "Be thorough but concise, focusing on actionable insights.",
        "Consider code quality, architecture patterns, security practices, and maintainability.",
        "Always explain your reasoning and methodology.",
        "Provide specific, actionable recommendations for improvement.",
        "Use a professional yet approachable tone.",
    ]
    
    # Create advanced agent with all available tools
    agent = Agent(
        name="Repository Analyzer Agent",
        model=Gemini(id=model_name),
        tools=[
            ReasoningTools(add_instructions=True),
            # Repository Analyzer Tools
            mcp_tools.get_repository_overview,
            mcp_tools.analyze_repository,
            mcp_tools.get_repository_activity,
            # File Content Tools
            mcp_tools.get_file_content,
            mcp_tools.list_directory,
            # Repository Structure Tools
            mcp_tools.get_directory_tree,
            mcp_tools.get_file_structure,
            # Commit History Tools
            mcp_tools.get_recent_commits,
            mcp_tools.get_commit_statistics,
            mcp_tools.get_commit_details,
            # Issues Tools
            mcp_tools.get_issues,
            mcp_tools.get_pull_requests,
            mcp_tools.get_issue_statistics,
            # Code Search Tools
            mcp_tools.search_code,
            mcp_tools.search_files,
            mcp_tools.get_code_metrics,
        ],
        instructions=main_agent_instructions,
        markdown=True,
        add_datetime_to_instructions=True,
    )
    
    return agent

def create_agent_team() -> Team:
    """Create team with specialized agents using Google Gemini and all MCP tools"""
    
    # Repository Overview Agent - Specialized in metadata and basic analysis
    overview_agent_instructions = [
        "You are a Repository Overview Specialist Agent powered by Google Gemini.",
        "Your expertise lies in analyzing repository metadata, structure, and basic characteristics.",
        "Focus on: repository description, README analysis, project structure, dependencies, and basic statistics.",
        "Provide clear, structured overviews with key metrics and project categorization.",
        "Identify the main purpose, target audience, and technology stack of the repository.",
        "Use tables to present metadata clearly and concisely.",
        "Always verify information using the repository overview and structure tools before making statements.",
        "Use file content tools to analyze README and documentation files.",
    ]
    
    overview_agent = Agent(
        name="Repository Overview Agent",
        role="Handle repository metadata and basic information",
        model=Gemini(id="gemini-2.0-flash-001"),
        tools=[
            UnifiedMCPTools().get_repository_overview,
            UnifiedMCPTools().get_directory_tree,
            UnifiedMCPTools().get_file_structure,
            UnifiedMCPTools().get_file_content,
            UnifiedMCPTools().list_directory,
        ],
        instructions=overview_agent_instructions,
        add_datetime_to_instructions=True,
    )
    
    # Code Analysis Agent - Specialized in technical code analysis
    code_agent_instructions = [
        "You are a Code Analysis Specialist Agent powered by Google Gemini.",
        "Your expertise lies in deep technical analysis of code patterns, architecture, and quality.",
        "Focus on: code structure, design patterns, complexity analysis, best practices, and potential issues.",
        "Analyze code quality, maintainability, scalability, and security considerations.",
        "Identify architectural patterns, anti-patterns, and areas for improvement.",
        "Provide specific code examples and technical recommendations.",
        "Use code search tools to find relevant examples and patterns.",
        "Analyze file contents to understand implementation details.",
        "Consider performance implications and optimization opportunities.",
        "Always provide evidence-based analysis with concrete examples.",
    ]
    
    code_agent = Agent(
        name="Code Analysis Agent",
        role="Handle code search and technical analysis",
        model=Gemini(id="gemini-2.0-flash-001"),
        tools=[
            UnifiedMCPTools().search_code,
            UnifiedMCPTools().search_files,
            UnifiedMCPTools().get_code_metrics,
            UnifiedMCPTools().get_file_content,
            UnifiedMCPTools().analyze_repository,
        ],
        instructions=code_agent_instructions,
        add_datetime_to_instructions=True,
    )
    
    # Activity Analysis Agent - Specialized in project activity and community health
    activity_agent_instructions = [
        "You are a Project Activity Specialist Agent powered by Google Gemini.",
        "Your expertise lies in analyzing project activity, community engagement, and development health.",
        "Focus on: commit patterns, issue management, community participation, and project momentum.",
        "Analyze development velocity, contributor activity, and project maintenance status.",
        "Identify trends in development activity, bug reports, and feature requests.",
        "Assess community health, documentation quality, and project sustainability.",
        "Provide insights on project maturity, maintenance practices, and future outlook.",
        "Use commit and issue data to understand project priorities and development focus.",
        "Consider the project's lifecycle stage and community engagement levels.",
        "Analyze repository activity patterns and development cycles.",
    ]
    
    activity_agent = Agent(
        name="Activity Analysis Agent",
        role="Handle commits, issues, and project activity",
        model=Gemini(id="gemini-2.0-flash-001"),
        tools=[
            UnifiedMCPTools().get_recent_commits,
            UnifiedMCPTools().get_commit_statistics,
            UnifiedMCPTools().get_commit_details,
            UnifiedMCPTools().get_issues,
            UnifiedMCPTools().get_pull_requests,
            UnifiedMCPTools().get_issue_statistics,
            UnifiedMCPTools().get_repository_activity,
        ],
        instructions=activity_agent_instructions,
        add_datetime_to_instructions=True,
    )
    
    # Team Coordinator - Orchestrates the specialized agents
    team_instructions = [
        "You are the Team Coordinator for the Repository Analysis Team powered by Google Gemini.",
        "Your role is to orchestrate specialized agents to provide comprehensive repository analysis.",
        "Coordinate the following specialists: Overview, Code Analysis, and Activity Analysis.",
        "Each agent has access to multiple MCP servers providing different types of repository data.",
        "Synthesize findings from all agents into a cohesive, well-structured analysis report.",
        "Ensure each agent's expertise is utilized appropriately for the given question.",
        "Provide a comprehensive response that covers all relevant aspects of the repository.",
        "Structure the final response with clear sections and actionable insights.",
        "Always maintain a professional and informative tone.",
        "Leverage the full power of the multi-server MCP ecosystem for complete analysis.",
    ]
    
    # Create the team
    team = Team(
        name="Repository Analysis Team",
        agents=[overview_agent, code_agent, activity_agent],
        instructions=team_instructions,
        model=Gemini(id="gemini-2.0-flash-001"),
        markdown=True,
        add_datetime_to_instructions=True,
    )
    
    return team

def ask_question_advanced(question: str, repository_url: str, use_team: bool = False) -> str:
    """Ask a question about a repository using advanced AI agents with full MCP ecosystem"""
    try:
        if use_team:
            # Use team of specialized agents
            team = create_agent_team()
            response = team.run(f"Question: {question}\nRepository: {repository_url}")
        else:
            # Use single advanced agent
            agent = create_advanced_agent()
            response = agent.run(f"Question: {question}\nRepository: {repository_url}")
        
        return response
    
    except Exception as e:
        return f"Error getting AI response: {str(e)}"

def analyze_repository_advanced(repository_url: str) -> str:
    """Perform comprehensive repository analysis using advanced agents with full MCP ecosystem"""
    try:
        team = create_agent_team()
        response = team.run(f"Provide a comprehensive analysis of this repository: {repository_url}")
        return response
    
    except Exception as e:
        return f"Error analyzing repository: {str(e)}"

# Legacy functions for backward compatibility
def create_ai_agent(model_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create AI agent (legacy function)"""
    agent = create_advanced_agent(model_name)
    return {
        "agent": agent,
        "model": model_name,
        "config": config
    }

def ask_question(agent: Dict[str, Any], question: str, repository_url: str) -> Dict[str, Any]:
    """Ask question using legacy agent format"""
    try:
        response = agent["agent"].run(f"Question: {question}\nRepository: {repository_url}")
        return {
            "success": True,
            "response": response,
            "question": question,
            "repository": repository_url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "question": question,
            "repository": repository_url
        }

def analyze_repository(agent: Dict[str, Any], repository_url: str) -> Dict[str, Any]:
    """Analyze repository using legacy agent format"""
    try:
        response = agent["agent"].run(f"Provide a comprehensive analysis of this repository: {repository_url}")
        return {
            "success": True,
            "response": response,
            "repository": repository_url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "repository": repository_url
        } 