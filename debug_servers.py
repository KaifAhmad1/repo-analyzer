#!/usr/bin/env python3
"""
Debug script for FastMCP v2 servers
"""

import asyncio
from fastmcp import Client

async def test_server(server_name, script_path):
    """Test a single server"""
    print(f"\n🔧 Testing {server_name}...")
    try:
        async with Client(script_path) as client:
            tools = await client.list_tools()
            print(f"  ✅ {server_name}: {len(tools)} tools available")
            for tool in tools:
                print(f"    - {tool.name}")
            return True
    except Exception as e:
        print(f"  ❌ {server_name}: {str(e)}")
        return False

async def main():
    """Test all servers"""
    servers = {
        "file_content": "src/servers/file_content_server.py",
        "repository_structure": "src/servers/repository_structure_server.py",
        "commit_history": "src/servers/commit_history_server.py",
        "code_search": "src/servers/code_search_server.py"
    }
    
    results = {}
    for server_name, script_path in servers.items():
        success = await test_server(server_name, script_path)
        results[server_name] = success
    
    print(f"\n📊 Results: {sum(results.values())}/{len(results)} servers working")
    for server_name, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {server_name}")

if __name__ == "__main__":
    asyncio.run(main()) 