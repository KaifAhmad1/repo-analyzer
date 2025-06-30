"""
Advanced Multi-Agent Usage Example
Demonstrates how to use the advanced multi-agent system with MCP servers
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.ai_agent import (
    create_advanced_agent,
    create_agent_team,
    ask_question_advanced,
    analyze_repository_advanced
)

def main():
    """Main function to demonstrate advanced multi-agent usage"""
    
    # Set your API keys
    os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key-here"
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
    
    # Example repository to analyze
    repo_url = "https://github.com/microsoft/vscode"
    
    print("🚀 Advanced Multi-Agent Repository Analyzer")
    print("=" * 50)
    
    # Example 1: Simple question with single agent
    print("\n1️⃣ Simple Question with Single Agent:")
    print("-" * 40)
    
    question = "What is this repository about?"
    response = ask_question_advanced(question, repo_url, use_team=False)
    print(f"Question: {question}")
    print(f"Response: {response[:200]}...")
    
    # Example 2: Complex analysis with team
    print("\n2️⃣ Complex Analysis with Team:")
    print("-" * 40)
    
    question = "Analyze the repository structure, recent activity, and code quality"
    response = ask_question_advanced(question, repo_url, use_team=True)
    print(f"Question: {question}")
    print(f"Response: {response[:300]}...")
    
    # Example 3: Comprehensive repository analysis
    print("\n3️⃣ Comprehensive Repository Analysis:")
    print("-" * 40)
    
    analysis = analyze_repository_advanced(repo_url)
    print(f"Analysis: {analysis[:400]}...")
    
    # Example 4: Direct agent usage
    print("\n4️⃣ Direct Agent Usage:")
    print("-" * 40)
    
    agent = create_advanced_agent()
    response = agent.run(f"Find authentication-related code in {repo_url}")
    print(f"Agent Response: {response.content[:200]}...")
    
    # Example 5: Team usage
    print("\n5️⃣ Direct Team Usage:")
    print("-" * 40)
    
    team = create_agent_team()
    response = team.run(f"Compare the performance and activity of {repo_url} with other popular editors")
    print(f"Team Response: {response.content[:300]}...")

if __name__ == "__main__":
    main() 