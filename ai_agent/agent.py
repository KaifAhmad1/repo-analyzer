"""
AI Agent Implementation using Agno Framework

This module contains the main AI agent class that handles LLM integration,
tool calling, and intelligent reasoning about GitHub repositories using Agno.
"""

import asyncio
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from agno import Agno
from agno.tools import Tool
from agno.models import OpenAI, Anthropic

logger = logging.getLogger(__name__)

class GitHubRepositoryAgent:
    """
    AI Agent for analyzing GitHub repositories using Agno framework.
    
    This agent can:
    - Understand natural language questions about repositories
    - Call appropriate MCP tools to gather information
    - Synthesize responses using LLM reasoning
    - Maintain conversation context
    - Handle multi-step reasoning and tool chaining
    """
    
    def __init__(self, model_provider: str = "openai", model_name: str = "gpt-4"):
        self.model_provider = model_provider
        self.model_name = model_name
        self.conversation_history = []
        self.tool_usage_history = []
        
        # Initialize Agno agent
        self.agno = self._initialize_agno_agent()
        
        # Initialize MCP tools
        self.tools = self._initialize_tools()
        
        logger.info(f"Initialized GitHub Repository Agent with {model_provider}/{model_name}")
    
    def _initialize_agno_agent(self) -> Agno:
        """
        Initialize the Agno agent with the specified model.
        """
        if self.model_provider == "openai":
            model = OpenAI(
                model=self.model_name,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif self.model_provider == "anthropic":
            model = Anthropic(
                model=self.model_name,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")
        
        return Agno(model=model)
    
    def _initialize_tools(self) -> List[Tool]:
        """
        Initialize available MCP tools for the agent.
        """
        tools = [
            Tool(
                name="get_file_content",
                description="Retrieve the content of a specific file from a GitHub repository",
                function=self._get_file_content,
                parameters={
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "file_path": "string (required): Path to the file within the repository",
                    "branch": "string (optional): Branch name, defaults to 'main'"
                }
            ),
            Tool(
                name="get_repository_tree",
                description="Get the complete directory tree structure of a repository",
                function=self._get_repository_tree,
                parameters={
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "branch": "string (optional): Branch name, defaults to 'main'"
                }
            ),
            Tool(
                name="get_recent_commits",
                description="Get recent commits from a repository with details",
                function=self._get_recent_commits,
                parameters={
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "limit": "integer (optional): Number of commits to return, defaults to 10"
                }
            ),
            Tool(
                name="search_code",
                description="Search for specific code patterns or functions in the repository",
                function=self._search_code,
                parameters={
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "query": "string (required): Search query or pattern to find",
                    "file_type": "string (optional): Filter by file type (e.g., 'py', 'js')"
                }
            ),
            Tool(
                name="get_issues",
                description="Get issues and pull requests from the repository",
                function=self._get_issues,
                parameters={
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "state": "string (optional): Issue state ('open', 'closed'), defaults to 'open'",
                    "limit": "integer (optional): Number of issues to return, defaults to 10"
                }
            ),
            Tool(
                name="get_documentation",
                description="Extract and process README files and documentation",
                function=self._get_documentation,
                parameters={
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "file_path": "string (optional): Specific documentation file path"
                }
            ),
            Tool(
                name="analyze_code_quality",
                description="Analyze code quality, complexity, and patterns",
                function=self._analyze_code_quality,
                parameters={
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "file_path": "string (optional): Specific file to analyze"
                }
            ),
            Tool(
                name="get_dependencies",
                description="Extract and analyze project dependencies",
                function=self._get_dependencies,
                parameters={
                    "repository": "string (required): Repository name in format 'owner/repo'"
                }
            )
        ]
        
        # Register tools with Agno
        for tool in tools:
            self.agno.add_tool(tool)
        
        return tools
    
    async def process_question(self, question: str, repository: str, 
                             context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a question about a GitHub repository using Agno.
        
        Args:
            question: The user's question
            repository: Repository name in format 'owner/repo'
            context: Additional context information
            
        Returns:
            Dictionary containing response and tool usage information
        """
        try:
            logger.info(f"Processing question: {question} for repository: {repository}")
            
            # Add to conversation history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "repository": repository
            })
            
            # Create system prompt with repository context
            system_prompt = self._create_system_prompt(repository, context)
            
            # Process with Agno
            response = await self.agno.run(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ]
            )
            
            # Extract tool usage from response
            tool_usage = self._extract_tool_usage(response)
            
            result = {
                "answer": response.content,
                "tool_usage": tool_usage,
                "reasoning": "Question processed successfully using Agno",
                "confidence": 0.9,
                "model_used": f"{self.model_provider}/{self.model_name}"
            }
            
            # Track tool usage
            self.tool_usage_history.append({
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "tools_used": tool_usage,
                "repository": repository
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return {
                "answer": "I encountered an error while processing your question. Please try again.",
                "tool_usage": [],
                "reasoning": f"Error: {str(e)}",
                "confidence": 0.0
            }
    
    def _create_system_prompt(self, repository: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a system prompt with repository context and instructions.
        """
        prompt = f"""
You are an intelligent AI assistant specialized in analyzing GitHub repositories. 
You have access to various tools to explore and understand codebases.

Current Repository: {repository}

Your capabilities include:
- Reading and analyzing file contents
- Exploring repository structure and organization
- Examining commit history and changes
- Searching for specific code patterns
- Analyzing issues and pull requests
- Extracting documentation and README files
- Analyzing code quality and complexity
- Mapping project dependencies

When answering questions:
1. Use the appropriate tools to gather information
2. Provide clear, well-structured responses
3. Include relevant code examples when helpful
4. Explain technical concepts in an accessible way
5. Highlight important patterns or insights
6. Be thorough but concise

Available tools:
- get_file_content: Read specific files
- get_repository_tree: Explore directory structure
- get_recent_commits: View recent changes
- search_code: Find specific code patterns
- get_issues: Check issues and PRs
- get_documentation: Extract documentation
- analyze_code_quality: Assess code quality
- get_dependencies: Map project dependencies

Always use tools to gather accurate information before providing answers.
"""
        
        if context:
            prompt += f"\nAdditional Context: {json.dumps(context, indent=2)}"
        
        return prompt
    
    def _extract_tool_usage(self, response) -> List[Dict[str, Any]]:
        """
        Extract tool usage information from Agno response.
        """
        tool_usage = []
        
        # Extract tool calls from response
        if hasattr(response, 'tool_calls') and response.tool_calls:
            for tool_call in response.tool_calls:
                tool_usage.append({
                    "tool": tool_call.name,
                    "arguments": tool_call.arguments,
                    "result": tool_call.result if hasattr(tool_call, 'result') else None
                })
        
        return tool_usage
    
    # MCP Tool Implementations
    async def _get_file_content(self, repository: str, file_path: str, branch: str = "main") -> str:
        """Get file content from GitHub repository."""
        # TODO: Implement actual GitHub API call
        return f"Content of {file_path} in {repository} (branch: {branch})"
    
    async def _get_repository_tree(self, repository: str, branch: str = "main") -> str:
        """Get repository directory tree."""
        # TODO: Implement actual GitHub API call
        return f"Directory tree for {repository} (branch: {branch})"
    
    async def _get_recent_commits(self, repository: str, limit: int = 10) -> str:
        """Get recent commits from repository."""
        # TODO: Implement actual GitHub API call
        return f"Recent {limit} commits from {repository}"
    
    async def _search_code(self, repository: str, query: str, file_type: Optional[str] = None) -> str:
        """Search for code patterns in repository."""
        # TODO: Implement actual GitHub API call
        return f"Search results for '{query}' in {repository}"
    
    async def _get_issues(self, repository: str, state: str = "open", limit: int = 10) -> str:
        """Get issues and pull requests."""
        # TODO: Implement actual GitHub API call
        return f"{limit} {state} issues from {repository}"
    
    async def _get_documentation(self, repository: str, file_path: Optional[str] = None) -> str:
        """Extract documentation from repository."""
        # TODO: Implement actual GitHub API call
        return f"Documentation from {repository}"
    
    async def _analyze_code_quality(self, repository: str, file_path: Optional[str] = None) -> str:
        """Analyze code quality and complexity."""
        # TODO: Implement actual code analysis
        return f"Code quality analysis for {repository}"
    
    async def _get_dependencies(self, repository: str) -> str:
        """Extract project dependencies."""
        # TODO: Implement actual dependency analysis
        return f"Dependencies for {repository}"
    
    async def analyze_repository_overview(self, repository: str) -> Dict[str, Any]:
        """
        Generate a comprehensive overview of a repository.
        
        Args:
            repository: Repository name in format 'owner/repo'
            
        Returns:
            Dictionary containing repository overview
        """
        question = f"Provide a comprehensive overview of the {repository} repository. Include its purpose, main features, technology stack, and key components."
        
        return await self.process_question(question, repository)
    
    async def find_code_patterns(self, repository: str, pattern_type: str) -> Dict[str, Any]:
        """
        Find specific code patterns in the repository.
        
        Args:
            repository: Repository name in format 'owner/repo'
            pattern_type: Type of patterns to find (e.g., 'functions', 'classes', 'imports')
            
        Returns:
            Dictionary containing found patterns
        """
        question = f"Find and analyze all {pattern_type} in the {repository} repository. Show me the patterns and explain their purpose."
        
        return await self.process_question(question, repository)
    
    async def explain_code_section(self, repository: str, file_path: str, 
                                  section: Optional[str] = None) -> Dict[str, Any]:
        """
        Explain a specific code section or file.
        
        Args:
            repository: Repository name in format 'owner/repo'
            file_path: Path to the file
            section: Specific section to explain (optional)
            
        Returns:
            Dictionary containing code explanation
        """
        if section:
            question = f"Explain the {section} section in {file_path} from the {repository} repository."
        else:
            question = f"Explain the code in {file_path} from the {repository} repository."
        
        return await self.process_question(question, repository)
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the conversation history.
        
        Returns:
            List of conversation entries
        """
        return self.conversation_history
    
    def get_tool_usage_history(self) -> List[Dict[str, Any]]:
        """
        Get the tool usage history.
        
        Returns:
            List of tool usage entries
        """
        return self.tool_usage_history
    
    def clear_history(self):
        """
        Clear conversation and tool usage history.
        """
        self.conversation_history = []
        self.tool_usage_history = [] 