"""
Test Script for Simplified GitHub Repository Analyzer
Tests the core functionality of the simplified AI agent system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.agent.ai_agent import ask_question, analyze_repository
from src.servers.mcp_client_improved import UnifiedMCPClient

def test_mcp_client():
    """Test MCP client functionality"""
    print("🔧 Testing MCP Client...")
    
    try:
        with UnifiedMCPClient() as client:
            # Test repository overview
            print("  📊 Testing repository overview...")
            result = client.get_repository_overview("https://github.com/unclecode/crawl4ai")
            print(f"    Success: {result.get('success', False)}")
            
            # Test file structure
            print("  📁 Testing file structure...")
            result = client.get_file_structure("https://github.com/unclecode/crawl4ai")
            print(f"    Success: {result.get('success', False)}")
            
            # Test recent commits
            print("  🔄 Testing recent commits...")
            result = client.get_recent_commits("https://github.com/unclecode/crawl4ai", 5)
            print(f"    Success: {result.get('success', False)}")
            
            print("✅ MCP Client tests completed")
            
    except Exception as e:
        print(f"❌ MCP Client test failed: {e}")

def test_ai_agent():
    """Test AI agent functionality"""
    print("\n🤖 Testing AI Agent...")
    
    try:
        # Test simple question
        print("  💬 Testing simple question...")
        response = ask_question(
            "What is this repository about?", 
            "https://github.com/unclecode/crawl4ai"
        )
        print(f"    Response length: {len(response)} characters")
        print(f"    Response preview: {response[:200]}...")
        
        # Test repository analysis
        print("  📊 Testing repository analysis...")
        response = analyze_repository("https://github.com/unclecode/crawl4ai")
        print(f"    Response length: {len(response)} characters")
        print(f"    Response preview: {response[:200]}...")
        
        print("✅ AI Agent tests completed")
        
    except Exception as e:
        print(f"❌ AI Agent test failed: {e}")

def test_specific_questions():
    """Test specific question types from requirements"""
    print("\n🎯 Testing Specific Question Types...")
    
    questions = [
        "What is this repository about and what does it do?",
        "Show me the main entry points of this application",
        "What are the recent changes in the last 10 commits?",
        "Find all functions related to authentication",
        "What dependencies does this project use?",
        "Are there any open issues related to performance?",
        "Explain how the database connection is implemented",
        "What's the testing strategy used in this project?"
    ]
    
    repo_url = "https://github.com/unclecode/crawl4ai"
    
    for i, question in enumerate(questions, 1):
        try:
            print(f"  {i}. Testing: {question[:50]}...")
            response = ask_question(question, repo_url)
            print(f"     Response length: {len(response)} characters")
            
            # Check if response contains useful information
            if len(response) > 100 and not response.startswith("Error"):
                print(f"     ✅ Question {i} successful")
            else:
                print(f"     ⚠️ Question {i} may have issues")
                
        except Exception as e:
            print(f"     ❌ Question {i} failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Simplified GitHub Repository Analyzer Tests")
    print("=" * 60)
    
    # Test MCP client
    test_mcp_client()
    
    # Test AI agent
    test_ai_agent()
    
    # Test specific questions
    test_specific_questions()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")

if __name__ == "__main__":
    main() 