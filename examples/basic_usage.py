"""
Basic Usage Example

This example demonstrates how to use the GitHub Repository Analyzer
with Agno-based AI agent to analyze repositories.
"""

import asyncio
import os
from ai_agent.agent import GitHubRepositoryAgent

async def main():
    """
    Main example function demonstrating repository analysis.
    """
    print("🔍 GitHub Repository Analyzer - Basic Usage Example")
    print("=" * 50)
    
    # Check for required environment variables
    if not os.getenv("GITHUB_TOKEN"):
        print("❌ Error: GITHUB_TOKEN environment variable is required")
        print("Please set your GitHub token: export GITHUB_TOKEN=your_token")
        return
    
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: Either OPENAI_API_KEY or ANTHROPIC_API_KEY is required")
        print("Please set one of them: export OPENAI_API_KEY=your_key")
        return
    
    # Initialize the AI agent
    print("🤖 Initializing AI Agent...")
    try:
        # Use OpenAI if available, otherwise use Anthropic
        if os.getenv("OPENAI_API_KEY"):
            agent = GitHubRepositoryAgent("openai", "gpt-4")
            print("✅ Initialized with OpenAI GPT-4")
        else:
            agent = GitHubRepositoryAgent("anthropic", "claude-3-sonnet")
            print("✅ Initialized with Anthropic Claude-3")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return
    
    # Example repository to analyze
    repository = "microsoft/vscode"
    print(f"\n📁 Analyzing repository: {repository}")
    
    # Example questions to ask
    example_questions = [
        "What is this repository about and what does it do?",
        "Show me the main entry points of this application",
        "What are the recent changes in the last 10 commits?",
        "Find all functions related to authentication",
        "What dependencies does this project use?"
    ]
    
    # Process each question
    for i, question in enumerate(example_questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("-" * 40)
        
        try:
            # Process the question
            response = await agent.process_question(question, repository)
            
            # Display the answer
            print(f"🤖 Answer: {response['answer']}")
            
            # Display tool usage if any
            if response.get('tool_usage'):
                print(f"🔧 Tools used: {len(response['tool_usage'])}")
                for tool in response['tool_usage']:
                    print(f"   - {tool.get('tool', 'Unknown')}")
            
            print(f"📊 Confidence: {response.get('confidence', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error processing question: {e}")
        
        print()
    
    # Demonstrate repository overview
    print("📊 Generating repository overview...")
    try:
        overview = await agent.analyze_repository_overview(repository)
        print(f"📝 Overview: {overview['answer']}")
    except Exception as e:
        print(f"❌ Error generating overview: {e}")
    
    # Demonstrate code pattern analysis
    print("\n🔍 Analyzing code patterns...")
    try:
        patterns = await agent.find_code_patterns(repository, "functions")
        print(f"🔧 Functions found: {patterns['answer']}")
    except Exception as e:
        print(f"❌ Error analyzing patterns: {e}")
    
    print("\n✅ Example completed successfully!")

if __name__ == "__main__":
    # Run the example
    asyncio.run(main()) 