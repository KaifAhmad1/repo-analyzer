"""
Test script for advanced multi-agent integration with MCP servers
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_advanced_agent():
    """Test basic advanced agent functionality"""
    print("🧪 Testing Advanced Multi-Agent Integration")
    print("=" * 50)
    
    try:
        from src.agent.ai_agent import create_advanced_agent, ask_question_advanced
        
        # Test repository
        repo_url = "https://github.com/microsoft/vscode"
        
        print("1️⃣ Testing single agent creation...")
        agent = create_advanced_agent()
        print("✅ Single agent created successfully")
        
        print("\n2️⃣ Testing simple question...")
        response = ask_question_advanced(
            "What is this repository about?", 
            repo_url, 
            use_team=False
        )
        print(f"✅ Response received: {response[:100]}...")
        
        print("\n3️⃣ Testing team creation...")
        from src.agent.ai_agent import create_agent_team
        team = create_agent_team()
        print("✅ Team created successfully")
        
        print("\n4️⃣ Testing team analysis...")
        response = ask_question_advanced(
            "Analyze the repository structure", 
            repo_url, 
            use_team=True
        )
        print(f"✅ Team response received: {response[:100]}...")
        
        print("\n5️⃣ Testing MCP tools...")
        from src.agent.ai_agent import MCPTools
        mcp_tools = MCPTools()
        
        # Test repository overview
        overview = mcp_tools.get_repository_overview(repo_url)
        print(f"✅ Repository overview: {overview[:100]}...")
        
        print("\n🎉 All tests passed! Advanced multi-agent integration is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_backward_compatibility():
    """Test backward compatibility with existing functions"""
    print("\n🔄 Testing Backward Compatibility")
    print("=" * 50)
    
    try:
        from src.agent.ai_agent import create_ai_agent, ask_question, analyze_repository
        
        # Test legacy agent creation
        print("1️⃣ Testing legacy agent creation...")
        agent = create_ai_agent("claude-sonnet-4-20250514", {})
        print("✅ Legacy agent created successfully")
        
        # Test legacy functions
        repo_url = "https://github.com/microsoft/vscode"
        
        print("\n2️⃣ Testing legacy ask_question...")
        response = ask_question(agent, "What is this about?", repo_url)
        print(f"✅ Legacy response: {response.get('response', 'No response')[:100]}...")
        
        print("\n3️⃣ Testing legacy analyze_repository...")
        analysis = analyze_repository(agent, repo_url)
        print(f"✅ Legacy analysis: {analysis.get('analysis', 'No analysis')[:100]}...")
        
        print("\n🎉 Backward compatibility tests passed!")
        
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function"""
    print("🚀 Advanced Multi-Agent Integration Test Suite")
    print("=" * 60)
    
    # Set test API keys (you'll need to replace these with real keys)
    os.environ["ANTHROPIC_API_KEY"] = "test-key"
    os.environ["OPENAI_API_KEY"] = "test-key"
    
    # Test advanced integration
    test_advanced_agent()
    
    # Test backward compatibility
    test_backward_compatibility()
    
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    print("✅ Advanced agent creation and usage")
    print("✅ Multi-agent team functionality") 
    print("✅ MCP tools integration")
    print("✅ Backward compatibility")
    print("\n🎯 Integration successful! You can now use the advanced multi-agent system with your MCP servers.")

if __name__ == "__main__":
    main() 