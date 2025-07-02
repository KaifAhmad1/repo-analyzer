#!/usr/bin/env python3
"""
Start all MCP servers before testing
"""

import sys
import os
from pathlib import Path

# Add src to path so we can import server_manager
sys.path.insert(0, str(Path(__file__).parent / "src"))

from servers.server_manager import start_all_servers, get_quick_status, check_servers_health

def main():
    """Start all MCP servers and verify they're running"""
    print("🚀 Starting all MCP servers...")
    
    # Start all servers
    results = start_all_servers()
    
    print("\n📊 Server startup results:")
    for server_name, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {server_name}")
    
    # Check overall status
    status = get_quick_status()
    print(f"\n{status}")
    
    # Verify all servers are healthy
    health = check_servers_health()
    all_healthy = all(health.values())
    
    if all_healthy:
        print("🎉 All servers started successfully!")
        print("\nReady for testing! You can now run your tests.")
    else:
        print("⚠️ Some servers may not be running properly.")
        print("Check the output above for any errors.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 