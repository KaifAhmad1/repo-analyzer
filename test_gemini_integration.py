"""
Test script for Google Gemini integration with Repository Analyzer
"""

import asyncio
import os
from dotenv import load_dotenv
from src.agent.ai_agent import create_advanced_agent, create_agent_team, ask_question_advanced

# Load environment variables
load_dotenv()

def test_single_agent():
    """Test single agent with Google Gemini"""
    print("🤖 Testing Single Agent with Google Gemini...")
    
    try:
        # Create agent
        agent = create_advanced_agent("gemini-2.0-flash-001")
        
        # Test question
        question = "What is the main purpose of this repository?"
        repo_url = "https://github.com/microsoft/vscode"
        
        print(f"📝 Question: {question}")
        print(f"🔗 Repository: {repo_url}")
        
        # Get response
        response = agent.run(f"Repository: {repo_url}\n\nQuestion: {question}")
        
        print("\n📋 Response:")
        print(response.content)
        print("\n✅ Single agent test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in single agent test: {e}")

def test_agent_team():
    """Test agent team with Google Gemini"""
    print("\n🤝 Testing Agent Team with Google Gemini...")
    
    try:
        # Create team
        team = create_agent_team()
        
        # Test analysis
        repo_url = "https://github.com/microsoft/vscode"
        
        print(f"🔗 Analyzing repository: {repo_url}")
        
        # Get response
        response = team.run(f"Provide a comprehensive analysis of the repository: {repo_url}")
        
        print("\n📋 Team Analysis:")
        print(response.content)
        print("\n✅ Agent team test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in agent team test: {e}")

def test_advanced_functions():
    """Test advanced functions"""
    print("\n🚀 Testing Advanced Functions...")
    
    try:
        repo_url = "https://github.com/microsoft/vscode"
        
        # Test ask_question_advanced with single agent
        print("📝 Testing ask_question_advanced (single agent)...")
        response1 = ask_question_advanced(
            "What are the main features of this repository?",
            repo_url,
            use_team=False
        )
        print("Single Agent Response:")
        print(response1[:500] + "..." if len(response1) > 500 else response1)
        
        # Test ask_question_advanced with team
        print("\n📝 Testing ask_question_advanced (team)...")
        response2 = ask_question_advanced(
            "Analyze the code quality and architecture of this repository",
            repo_url,
            use_team=True
        )
        print("Team Response:")
        print(response2[:500] + "..." if len(response2) > 500 else response2)
        
        print("\n✅ Advanced functions test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in advanced functions test: {e}")

def main():
    """Main test function"""
    print("🧪 Google Gemini Integration Test Suite")
    print("=" * 50)
    
    # Check if Google API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set!")
        print("Please set your Google API key in the .env file or environment variables.")
        return
    
    print(f"✅ Google API key found: {api_key[:10]}...")
    
    # Run tests
    test_single_agent()
    test_agent_team()
    test_advanced_functions()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main() 