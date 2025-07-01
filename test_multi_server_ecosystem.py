#!/usr/bin/env python3
"""
Test script for the Multi-Server FastMCP v2 Ecosystem
Verifies that all servers are working together properly
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.servers.server_manager import start_mcp_servers, check_servers_status, get_detailed_server_status
from src.servers.mcp_client_improved import UnifiedMCPClient
from src.agent.ai_agent import create_advanced_agent, ask_question_advanced

def test_server_startup():
    """Test starting all MCP servers"""
    print("🧪 Testing Multi-Server Startup...")
    
    # Start all servers
    results = start_mcp_servers()
    
    print(f"✅ Started {sum(results.values())}/{len(results)} servers")
    for server_name, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {server_name}")
    
    return results

def test_server_status():
    """Test server status checking"""
    print("\n🔍 Testing Server Status...")
    
    status = check_servers_status()
    detailed_status = get_detailed_server_status()
    
    print(f"📊 Server Status Summary:")
    print(f"  Total servers: {detailed_status['total_servers']}")
    print(f"  Running: {detailed_status['running_servers']}")
    print(f"  Stopped: {detailed_status['stopped_servers']}")
    
    for server_name, server_info in detailed_status["servers"].items():
        status_icon = "✅" if server_info["running"] else "❌"
        print(f"  {status_icon} {server_info['name']}")
    
    return status

def test_unified_client():
    """Test the unified MCP client"""
    print("\n🔧 Testing Unified MCP Client...")
    
    test_repo = "https://github.com/microsoft/vscode"
    
    try:
        with UnifiedMCPClient() as client:
            print("✅ Unified client initialized successfully")
            
            # Test repository overview
            print("  Testing repository overview...")
            overview = client.get_repository_overview(test_repo)
            if overview.get("success"):
                print("  ✅ Repository overview working")
            else:
                print(f"  ❌ Repository overview failed: {overview.get('error', 'Unknown error')}")
            
            # Test code search
            print("  Testing code search...")
            search = client.search_code(test_repo, "README")
            if search.get("success"):
                print("  ✅ Code search working")
            else:
                print(f"  ❌ Code search failed: {search.get('error', 'Unknown error')}")
            
            # Test commit history
            print("  Testing commit history...")
            commits = client.get_recent_commits(test_repo, limit=5)
            if commits.get("success"):
                print("  ✅ Commit history working")
            else:
                print(f"  ❌ Commit history failed: {commits.get('error', 'Unknown error')}")
            
            # Test issues
            print("  Testing issues...")
            issues = client.get_issues(test_repo, limit=5)
            if issues.get("success"):
                print("  ✅ Issues working")
            else:
                print(f"  ❌ Issues failed: {issues.get('error', 'Unknown error')}")
            
            # Test directory tree
            print("  Testing directory tree...")
            tree = client.get_directory_tree(test_repo, max_depth=2)
            if tree.get("success"):
                print("  ✅ Directory tree working")
            else:
                print(f"  ❌ Directory tree failed: {tree.get('error', 'Unknown error')}")
            
            # Test file content
            print("  Testing file content...")
            content = client.get_file_content(test_repo, "README.md")
            if content.get("success"):
                print("  ✅ File content working")
            else:
                print(f"  ❌ File content failed: {content.get('error', 'Unknown error')}")
            
            return True
    
    except Exception as e:
        print(f"❌ Unified client test failed: {e}")
        return False

def test_ai_agent():
    """Test AI agent integration"""
    print("\n🤖 Testing AI Agent Integration...")
    
    # Check if API keys are configured
    from src.utils.config import get_github_token, get_google_api_key
    
    github_token = get_github_token()
    google_api_key = get_google_api_key()
    
    if not github_token or not google_api_key:
        print("⚠️ Skipping AI agent test - API keys not configured")
        print("  Set GITHUB_TOKEN and GOOGLE_API_KEY environment variables to test AI features")
        return False
    
    try:
        # Test agent creation
        print("  Testing agent creation...")
        agent = create_advanced_agent()
        print("  ✅ Agent created successfully")
        
        # Test simple question
        print("  Testing agent question...")
        test_repo = "https://github.com/microsoft/vscode"
        response = ask_question_advanced(
            "What is this repository about?",
            test_repo,
            use_team=False
        )
        
        if response and not response.startswith("Error"):
            print("  ✅ Agent question working")
            print(f"  📝 Response length: {len(response)} characters")
        else:
            print(f"  ❌ Agent question failed: {response}")
        
        return True
    
    except Exception as e:
        print(f"❌ AI agent test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Multi-Server FastMCP v2 Ecosystem")
    print("=" * 50)
    
    # Test server startup
    startup_results = test_server_startup()
    
    # Wait a moment for servers to fully start
    import time
    time.sleep(5)
    
    # Test server status
    status_results = test_server_status()
    
    # Test unified client
    client_success = test_unified_client()
    
    # Test AI agent
    agent_success = test_ai_agent()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"  Server Startup: {sum(startup_results.values())}/{len(startup_results)} successful")
    print(f"  Server Status: {sum(status_results.values())}/{len(status_results)} running")
    print(f"  Unified Client: {'✅' if client_success else '❌'}")
    print(f"  AI Agent: {'✅' if agent_success else '❌'}")
    
    if all(startup_results.values()) and client_success:
        print("\n🎉 All core tests passed! The multi-server ecosystem is working properly.")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
    
    print("\n💡 To run the full application:")
    print("  streamlit run app.py")

if __name__ == "__main__":
    main() 