#!/usr/bin/env python3
"""
Test script for FastMCP v2 implementation
Tests all 4 core servers and the AI agent
"""

import asyncio
import json
from src.servers.server_manager import start_all_servers, stop_all_servers, get_servers_status
from src.agent.ai_agent import test_fastmcp_connection, list_available_tools

def test_server_manager():
    """Test the server manager functionality"""
    print("🧪 Testing Server Manager...")
    
    # Test server status
    status = get_servers_status()
    print(f"📊 Server Status: {status['running_servers']}/{status['total_servers']} servers running")
    
    # List available servers
    for server_name, server_info in status["servers"].items():
        status_icon = "✅" if server_info["running"] else "❌"
        print(f"  {status_icon} {server_info['name']}: {server_info['description']}")
    
    return status

def test_fastmcp_servers():
    """Test individual FastMCP servers"""
    print("\n🔧 Testing FastMCP Servers...")
    
    from fastmcp import Client
    
    servers = {
        "file_content": "src/servers/file_content_server.py",
        "repository_structure": "src/servers/repository_structure_server.py",
        "commit_history": "src/servers/commit_history_server.py",
        "code_search": "src/servers/code_search_server.py"
    }
    
    test_repo = "https://github.com/microsoft/vscode"
    results = {}
    
    async def test_server(server_name, script_path):
        try:
            async with Client(script_path) as client:
                tools = await client.list_tools()
                
                # Test a simple tool call
                if server_name == "file_content":
                    result = await client.call_tool("get_readme_content", {"repo_url": test_repo})
                elif server_name == "repository_structure":
                    result = await client.call_tool("get_directory_tree", {"repo_url": test_repo, "max_depth": 1})
                elif server_name == "commit_history":
                    result = await client.call_tool("get_recent_commits", {"repo_url": test_repo, "limit": 5})
                elif server_name == "code_search":
                    result = await client.call_tool("search_code", {"repo_url": test_repo, "query": "README"})
                
                return {
                    "success": True,
                    "tools_count": len(tools),
                    "tools": [tool.name for tool in tools],
                    "test_result": "Tool call successful"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Test each server
    for server_name, script_path in servers.items():
        print(f"  Testing {server_name}...")
        result = asyncio.run(test_server(server_name, script_path))
        results[server_name] = result
        
        if result["success"]:
            print(f"    ✅ {server_name}: {result['tools_count']} tools available")
        else:
            print(f"    ❌ {server_name}: {result['error']}")
    
    return results

def test_ai_agent():
    """Test the AI agent with FastMCP tools"""
    print("\n🤖 Testing AI Agent...")
    
    # Test FastMCP connection
    connection_test = test_fastmcp_connection()
    print(f"  FastMCP Connection: {'✅' if connection_test['success'] else '❌'}")
    if not connection_test['success']:
        print(f"    Error: {connection_test['error']}")
        return False
    
    # List available tools
    tools = list_available_tools()
    print(f"  Available Tools: {len(tools)} tools")
    for tool in tools:
        print(f"    - {tool}")
    
    return True

def main():
    """Main test function"""
    print("🚀 FastMCP v2 Implementation Test")
    print("=" * 50)
    
    try:
        # Test server manager
        server_status = test_server_manager()
        
        # Test FastMCP servers
        server_results = test_fastmcp_servers()
        
        # Test AI agent
        agent_success = test_ai_agent()
        
        # Summary
        print("\n📋 Test Summary")
        print("=" * 50)
        
        running_servers = server_status["running_servers"]
        total_servers = server_status["total_servers"]
        
        print(f"Servers: {running_servers}/{total_servers} running")
        
        successful_server_tests = sum(1 for result in server_results.values() if result["success"])
        print(f"Server Tests: {successful_server_tests}/{len(server_results)} successful")
        
        print(f"AI Agent: {'✅ Working' if agent_success else '❌ Failed'}")
        
        if running_servers == total_servers and successful_server_tests == len(server_results) and agent_success:
            print("\n🎉 All tests passed! FastMCP v2 implementation is working correctly.")
        else:
            print("\n⚠️ Some tests failed. Check the output above for details.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 