"""
Basic Usage Example

This script demonstrates basic usage of the GitHub Repository Analyzer.
Shows how to use MCP servers and AI agent programmatically.
"""

import asyncio
import os
from typing import Dict, Any

# TODO: Import required modules
# from mcp_servers.start_servers import MCPServerManager
# from ai_agent.agent import GitHubRepositoryAgent
# from utils.config import load_config

async def main():
    """
    Main example function demonstrating basic usage.
    """
    print("🚀 GitHub Repository Analyzer - Basic Usage Example")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    print(f"✅ Configuration loaded")
    
    # Initialize MCP server manager
    server_manager = MCPServerManager()
    print(f"✅ MCP server manager initialized")
    
    # Start MCP servers
    print("🔄 Starting MCP servers...")
    await server_manager.start_all_servers()
    print(f"✅ MCP servers started")
    
    # Initialize AI agent
    agent = GitHubRepositoryAgent(
        model_provider=config["llm"]["provider"],
        model_name=config["llm"]["model"]
    )
    print(f"✅ AI agent initialized with {config['llm']['provider']}/{config['llm']['model']}")
    
    # Example repository to analyze
    repository = "microsoft/vscode"  # Example repository
    
    # Example questions
    example_questions = [
        "What is this repository about?",
        "Show me the main entry points",
        "What are the recent changes?",
        "Find all authentication functions"
    ]
    
    print(f"\n📁 Analyzing repository: {repository}")
    print("-" * 30)
    
    # Process example questions
    for i, question in enumerate(example_questions, 1):
        print(f"\n❓ Question {i}: {question}")
        
        try:
            # Process question
            response = await agent.process_question(question, repository)
            
            print(f"🤖 Answer: {response['answer']}")
            print(f"🔧 Tools used: {len(response['tool_usage'])}")
            print(f"🎯 Confidence: {response['confidence']:.2f}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Get conversation history
    print(f"\n📚 Conversation History:")
    history = agent.get_conversation_history()
    for entry in history[-3:]:  # Show last 3 entries
        print(f"  - {entry['timestamp']}: {entry['question']}")
    
    # Get tool usage history
    print(f"\n🔧 Tool Usage History:")
    tool_history = agent.get_tool_usage_history()
    for entry in tool_history[-3:]:  # Show last 3 entries
        print(f"  - {entry['timestamp']}: {len(entry['tools_used'])} tools used")
    
    # Stop servers
    print(f"\n🔄 Stopping MCP servers...")
    await server_manager.stop_all_servers()
    print(f"✅ MCP servers stopped")
    
    print(f"\n🎉 Example completed successfully!")

async def analyze_specific_repository(repository: str, questions: list):
    """
    Analyze a specific repository with custom questions.
    
    Args:
        repository: Repository name in format 'owner/repo'
        questions: List of questions to ask
    """
    print(f"🔍 Analyzing {repository} with custom questions")
    
    # TODO: Implement repository analysis
    # 1. Initialize components
    # 2. Process questions
    # 3. Generate report
    # 4. Save results
    
    pass

async def generate_repository_report(repository: str) -> Dict[str, Any]:
    """
    Generate a comprehensive repository report.
    
    Args:
        repository: Repository name in format 'owner/repo'
        
    Returns:
        Dictionary containing comprehensive report
    """
    print(f"📊 Generating comprehensive report for {repository}")
    
    # TODO: Implement comprehensive report generation
    # 1. Get repository overview
    # 2. Analyze structure
    # 3. Analyze code patterns
    # 4. Analyze commit history
    # 5. Generate insights
    # 6. Return structured report
    
    report = {
        "repository": repository,
        "overview": "Repository overview coming soon...",
        "structure": "Structure analysis coming soon...",
        "code_patterns": "Code pattern analysis coming soon...",
        "commit_history": "Commit history analysis coming soon...",
        "insights": "Key insights coming soon...",
        "recommendations": "Recommendations coming soon..."
    }
    
    return report

if __name__ == "__main__":
    # Run basic example
    asyncio.run(main())
    
    # Example: Analyze specific repository
    # asyncio.run(analyze_specific_repository("facebook/react", [
    #     "What is the main purpose of this repository?",
    #     "How is the project structured?",
    #     "What are the main components?"
    # ]))
    
    # Example: Generate comprehensive report
    # report = asyncio.run(generate_repository_report("microsoft/vscode"))
    # print(f"📄 Report generated: {report['repository']}") 