"""
Multi-Agent System for GitHub Repository Analysis
Integrates seamlessly with all MCP servers using advanced agent framework
"""

import os
import json
from typing import Dict, List, Any, Optional
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.team.team import Team
from src.servers.mcp_client_improved import SyncMCPClient

class MCPTools:
    """Custom agent tools wrapper for MCP servers"""
    
    def __init__(self):
        self.mcp_client = SyncMCPClient()
    
    def get_repository_overview(self, repo_url: str) -> str:
        """Get repository overview using MCP server"""
        try:
            with self.mcp_client as client:
                result = client.get_repository_overview(repo_url)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting repository overview: {str(e)}"
    
    def search_code(self, repo_url: str, query: str, language: str = "") -> str:
        """Search code using MCP server"""
        try:
            with self.mcp_client as client:
                result = client.search_code(repo_url, query, language)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error searching code: {str(e)}"
    
    def get_recent_commits(self, repo_url: str, limit: int = 10) -> str:
        """Get recent commits using MCP server"""
        try:
            with self.mcp_client as client:
                result = client.get_recent_commits(repo_url, limit)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting commits: {str(e)}"
    
    def get_issues(self, repo_url: str, state: str = "open", limit: int = 10) -> str:
        """Get issues using MCP server"""
        try:
            with self.mcp_client as client:
                result = client.get_issues(repo_url, state, limit)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting issues: {str(e)}"
    
    def analyze_repository(self, repo_url: str) -> str:
        """Analyze repository using MCP server"""
        try:
            with self.mcp_client as client:
                result = client.analyze_repository(repo_url)
                return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error analyzing repository: {str(e)}"

def create_advanced_agent(model_name: str = "claude-sonnet-4-20250514") -> Agent:
    """Create advanced agent with MCP tools integration"""
    
    # Initialize MCP tools
    mcp_tools = MCPTools()
    
    # Create advanced agent
    agent = Agent(
        name="Repository Analyzer Agent",
        model=Claude(id=model_name),
        tools=[
            ReasoningTools(add_instructions=True),
            mcp_tools.get_repository_overview,
            mcp_tools.search_code,
            mcp_tools.get_recent_commits,
            mcp_tools.get_issues,
            mcp_tools.analyze_repository,
        ],
        instructions=[
            "You are an intelligent GitHub repository analyzer powered by advanced AI.",
            "Use the available MCP tools to gather comprehensive information about repositories.",
            "Always provide detailed, helpful explanations with context.",
            "Include code examples when relevant.",
            "Be conversational and friendly.",
            "Use tables to display data when appropriate.",
            "Always explain what you're doing and why.",
        ],
        markdown=True,
        add_datetime_to_instructions=True,
    )
    
    return agent

def create_agent_team() -> Team:
    """Create team with specialized agents"""
    
    # Repository Overview Agent
    overview_agent = Agent(
        name="Repository Overview Agent",
        role="Handle repository metadata and basic information",
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[MCPTools().get_repository_overview],
        instructions="Focus on repository metadata, description, and basic statistics.",
        add_datetime_to_instructions=True,
    )
    
    # Code Analysis Agent
    code_agent = Agent(
        name="Code Analysis Agent",
        role="Handle code search and analysis",
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[MCPTools().search_code, MCPTools().analyze_repository],
        instructions="Focus on code patterns, structure, and technical analysis.",
        add_datetime_to_instructions=True,
    )
    
    # Activity Analysis Agent
    activity_agent = Agent(
        name="Activity Analysis Agent",
        role="Handle commits, issues, and project activity",
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[MCPTools().get_recent_commits, MCPTools().get_issues],
        instructions="Focus on project activity, recent changes, and community engagement.",
        add_datetime_to_instructions=True,
    )
    
    # Create team
    team = Team(
        name="Repository Analysis Team",
        mode="coordinate",
        model=Claude(id="claude-sonnet-4-20250514"),
        members=[overview_agent, code_agent, activity_agent],
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "Collaborate to provide comprehensive repository analysis",
            "Consider repository structure, code quality, and project activity",
            "Use tables and charts to display data clearly",
            "Present findings in a structured, easy-to-follow format",
            "Only output the final consolidated analysis",
        ],
        markdown=True,
        show_members_responses=True,
        enable_agentic_context=True,
        add_datetime_to_instructions=True,
        success_criteria="The team has provided a complete repository analysis with data, insights, and actionable recommendations.",
    )
    
    return team

def ask_question_advanced(question: str, repository_url: str, use_team: bool = False) -> str:
    """Ask a question using advanced agent or team"""
    try:
        if use_team:
            # Use team for complex analysis
            team = create_agent_team()
            response = team.run(f"Analyze the repository {repository_url}. {question}")
            return response.content
        else:
            # Use single agent for simple questions
            agent = create_advanced_agent()
            response = agent.run(f"Repository: {repository_url}\n\nQuestion: {question}")
            return response.content
            
    except Exception as e:
        return f"Error processing request: {str(e)}"

def analyze_repository_advanced(repository_url: str) -> str:
    """Perform comprehensive repository analysis using advanced system"""
    try:
        team = create_agent_team()
        response = team.run(f"Provide a comprehensive analysis of the repository: {repository_url}")
        return response.content
    except Exception as e:
        return f"Error analyzing repository: {str(e)}"

# Backward compatibility functions
def create_ai_agent(model_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create advanced agent (backward compatibility)"""
    agent = create_advanced_agent(model_name)
    return {
        "agent": agent,
        "model": model_name,
        "config": config
    }

def get_available_tools() -> List[Dict[str, Any]]:
    """Get list of available MCP tools"""
    return [
        {
            "name": "get_repository_overview",
            "description": "Get comprehensive overview of a GitHub repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repository URL"}
                },
                "required": ["repo_url"]
            }
        },
        {
            "name": "search_code",
            "description": "Search for code patterns in the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repository URL"},
                    "query": {"type": "string", "description": "Search query"},
                    "language": {"type": "string", "description": "Programming language filter"}
                },
                "required": ["repo_url", "query"]
            }
        },
        {
            "name": "get_recent_commits",
            "description": "Get recent commit history",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repository URL"},
                    "limit": {"type": "integer", "description": "Number of commits to retrieve"}
                },
                "required": ["repo_url"]
            }
        },
        {
            "name": "get_issues",
            "description": "Get issues and pull requests",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repository URL"},
                    "state": {"type": "string", "description": "Issue state (open/closed)"},
                    "limit": {"type": "integer", "description": "Number of issues to retrieve"}
                },
                "required": ["repo_url"]
            }
        },
        {
            "name": "analyze_repository",
            "description": "Perform comprehensive repository analysis",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repository URL"}
                },
                "required": ["repo_url"]
            }
        }
    ]

def ask_question(agent: Dict[str, Any], question: str, repository_url: str) -> Dict[str, Any]:
    """Ask a question using advanced agent (backward compatibility)"""
    try:
        response = ask_question_advanced(question, repository_url)
        return {
            "response": response,
            "success": True,
            "model": agent.get("model", "advanced-agent")
        }
    except Exception as e:
        return {
            "error": str(e),
            "success": False,
            "model": agent.get("model", "advanced-agent")
        }

def analyze_repository(agent: Dict[str, Any], repository_url: str) -> Dict[str, Any]:
    """Analyze repository using advanced system (backward compatibility)"""
    try:
        response = analyze_repository_advanced(repository_url)
        return {
            "analysis": response,
            "success": True,
            "model": agent.get("model", "advanced-agent")
        }
    except Exception as e:
        return {
            "error": str(e),
            "success": False,
            "model": agent.get("model", "advanced-agent")
        } 