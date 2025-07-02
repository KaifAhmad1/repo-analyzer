"""
Test script for the enhanced AI agent system
"""

import os
import sys
from src.agent.ai_agent import (
    create_analyzer_agent,
    ask_repository_question,
    generate_repository_summary,
    analyze_repository_patterns,
    get_repository_overview
)

def test_agent_functions():
    """Test the enhanced agent functions"""
    print("🧪 Testing Enhanced AI Agent System")
    print("=" * 50)
    
    # Test repository URL
    test_repo = "https://github.com/streamlit/streamlit"
    
    try:
        print("1. Testing repository overview...")
        overview = get_repository_overview(test_repo)
        print(f"✅ Overview generated: {len(overview)} characters")
        
        print("\n2. Testing question answering...")
        response, tools = ask_repository_question(
            "What is this repository about?", 
            test_repo
        )
        print(f"✅ Question answered: {len(response)} characters")
        print(f"   Tools used: {len(tools)}")
        
        print("\n3. Testing summary generation...")
        summary, tools = generate_repository_summary(test_repo)
        print(f"✅ Summary generated: {len(summary)} characters")
        print(f"   Tools used: {len(tools)}")
        
        print("\n4. Testing code pattern analysis...")
        analysis, tools = analyze_repository_patterns(test_repo)
        print(f"✅ Analysis completed: {len(analysis)} characters")
        print(f"   Tools used: {len(tools)}")
        
        print("\n🎉 All tests passed! Enhanced agent system is working correctly.")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_agent_functions()
    sys.exit(0 if success else 1) 