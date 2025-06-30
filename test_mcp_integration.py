"""
Test script for MCP integration
Verifies that the improved MCP server and client work correctly
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_mcp_server():
    """Test the MCP server directly"""
    print("🧪 Testing MCP Server...")
    
    try:
        from src.servers.repository_analyzer_server import mcp
        
        # Check if server has tools
        tools = mcp.get_tools()
        print(f"✅ Server has {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Check if server has resources
        resources = mcp.get_resources()
        print(f"✅ Server has {len(resources)} resources:")
        for resource in resources:
            print(f"  - {resource.uri}: {resource.title}")
        
        return True
    
    except Exception as e:
        print(f"❌ MCP server test failed: {e}")
        return False

def test_mcp_client():
    """Test the MCP client"""
    print("\n🧪 Testing MCP Client...")
    
    try:
        from src.servers.mcp_client_improved import SyncMCPClient
        
        # Test repository overview
        repo_url = "https://github.com/microsoft/vscode"
        
        with SyncMCPClient() as client:
            print("Testing repository overview...")
            result = client.get_repository_overview(repo_url)
            
            if result.get("success"):
                print("✅ Repository overview test passed")
                print(f"Result: {result['result'][:200]}...")
            else:
                print(f"❌ Repository overview test failed: {result.get('error')}")
                return False
            
            # Test code search
            print("Testing code search...")
            result = client.search_code(repo_url, "function main", "typescript")
            
            if result.get("success"):
                print("✅ Code search test passed")
            else:
                print(f"❌ Code search test failed: {result.get('error')}")
                return False
        
        return True
    
    except Exception as e:
        print(f"❌ MCP client test failed: {e}")
        return False

def test_ai_agent():
    """Test the AI agent integration"""
    print("\n🧪 Testing AI Agent...")
    
    try:
        from src.agent.ai_agent import create_ai_agent
        from src.utils.config import load_config
        
        # Load config
        config = load_config()
        
        # Create AI agent
        agent = create_ai_agent("gpt-4", config)
        print("✅ AI agent created successfully")
        
        # Test agent structure
        required_keys = ["client", "model", "mcp_client", "config"]
        for key in required_keys:
            if key not in agent:
                print(f"❌ Missing key in agent: {key}")
                return False
        
        print("✅ AI agent structure is correct")
        return True
    
    except Exception as e:
        print(f"❌ AI agent test failed: {e}")
        return False

def test_server_manager():
    """Test the server manager"""
    print("\n🧪 Testing Server Manager...")
    
    try:
        from src.servers.server_manager import get_server_manager
        
        manager = get_server_manager()
        print("✅ Server manager created successfully")
        
        # Test server status
        status = manager.get_server_status()
        print(f"Server status: {status}")
        
        return True
    
    except Exception as e:
        print(f"❌ Server manager test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting MCP Integration Tests")
    print("=" * 50)
    
    # Set up environment
    if not os.getenv("GITHUB_TOKEN"):
        print("⚠️  GITHUB_TOKEN not set. Some tests may fail.")
    
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  No AI API key set. AI agent tests may fail.")
    
    tests = [
        ("MCP Server", test_mcp_server),
        ("MCP Client", test_mcp_client),
        ("AI Agent", test_ai_agent),
        ("Server Manager", test_server_manager)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MCP integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 