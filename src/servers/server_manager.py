"""
Simple Server Manager for FastMCP v2 Servers
Manages the 4 core MCP servers for repository analysis
"""

import subprocess
import time
import os
import signal
from typing import List, Dict, Any
from pathlib import Path

class SimpleServerManager:
    """Manages the 4 core FastMCP v2 server processes"""
    
    def __init__(self):
        self.servers = {
            "file_content": {
                "script": "src/servers/file_content_server.py",
                "name": "File Content Server 📁",
                "description": "Retrieve and read file contents from repositories"
            },
            "repository_structure": {
                "script": "src/servers/repository_structure_server.py",
                "name": "Repository Structure Server 🌳",
                "description": "Get directory trees and file listings"
            },
            "commit_history": {
                "script": "src/servers/commit_history_server.py",
                "name": "Commit History Server 📝",
                "description": "Access commit messages and changes"
            },
            "code_search": {
                "script": "src/servers/code_search_server.py",
                "name": "Code Search Server 🔍",
                "description": "Search for specific code patterns or functions"
            }
        }
        self.processes = {}
    
    def start_servers(self, server_names: List[str] = None) -> Dict[str, bool]:
        """Start specified MCP servers or all servers if none specified"""
        if server_names is None:
            server_names = list(self.servers.keys())
        
        results = {}
        
        for server_name in server_names:
            if server_name not in self.servers:
                results[server_name] = False
                print(f"❌ Unknown server: {server_name}")
                continue
            
            server_info = self.servers[server_name]
            script_path = server_info["script"]
            
            if not os.path.exists(script_path):
                results[server_name] = False
                print(f"❌ Server script not found: {script_path}")
                continue
            
            try:
                # Start the MCP server process
                process = subprocess.Popen(
                    ["python", script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                self.processes[server_name] = process
                results[server_name] = True
                print(f"✅ Started {server_info['name']}")
                
            except Exception as e:
                results[server_name] = False
                print(f"❌ Error starting {server_info['name']}: {e}")
        
        # Wait for servers to start
        time.sleep(2)
        
        return results
    
    def stop_servers(self, server_names: List[str] = None) -> Dict[str, bool]:
        """Stop specified MCP servers or all servers if none specified"""
        if server_names is None:
            server_names = list(self.processes.keys())
        
        results = {}
        
        for server_name in server_names:
            if server_name not in self.processes:
                results[server_name] = True  # Already stopped
                continue
            
            process = self.processes[server_name]
            server_info = self.servers[server_name]
            
            try:
                # Try graceful shutdown first
                process.terminate()
                process.wait(timeout=5)
                results[server_name] = True
                print(f"✅ Stopped {server_info['name']}")
                
            except subprocess.TimeoutExpired:
                # Force kill if graceful shutdown fails
                process.kill()
                process.wait()
                results[server_name] = True
                print(f"⚠️ Force killed {server_info['name']}")
                
            except Exception as e:
                results[server_name] = False
                print(f"❌ Error stopping {server_info['name']}: {e}")
            
            finally:
                self.processes[server_name] = None
        
        return results
    
    def get_server_status(self) -> Dict[str, Any]:
        """Get status of all servers"""
        status = {
            "servers": {},
            "total_servers": len(self.servers),
            "running_servers": 0,
            "stopped_servers": 0
        }
        
        for server_name, server_info in self.servers.items():
            is_running = server_name in self.processes and self.processes[server_name] is not None
            if is_running:
                status["running_servers"] += 1
            else:
                status["stopped_servers"] += 1
            
            status["servers"][server_name] = {
                "name": server_info["name"],
                "description": server_info["description"],
                "script_path": server_info["script"],
                "script_exists": os.path.exists(server_info["script"]),
                "running": is_running,
                "process_id": self.processes[server_name].pid if is_running else None
            }
        
        return status
    
    def restart_servers(self, server_names: List[str] = None) -> Dict[str, bool]:
        """Restart specified servers or all servers if none specified"""
        if server_names is None:
            server_names = list(self.servers.keys())
        
        print("🔄 Restarting servers...")
        
        # Stop servers
        stop_results = self.stop_servers(server_names)
        
        # Wait a moment
        time.sleep(1)
        
        # Start servers
        start_results = self.start_servers(server_names)
        
        # Combine results
        results = {}
        for server_name in server_names:
            results[server_name] = stop_results.get(server_name, True) and start_results.get(server_name, False)
        
        return results

# Global server manager instance
_server_manager = None

def get_server_manager() -> SimpleServerManager:
    """Get the global server manager instance"""
    global _server_manager
    if _server_manager is None:
        _server_manager = SimpleServerManager()
    return _server_manager

def start_mcp_servers(server_names: List[str] = None) -> Dict[str, bool]:
    """Start MCP servers"""
    manager = get_server_manager()
    return manager.start_servers(server_names)

def stop_mcp_servers(server_names: List[str] = None) -> Dict[str, bool]:
    """Stop MCP servers"""
    manager = get_server_manager()
    return manager.stop_servers(server_names)

def restart_mcp_servers(server_names: List[str] = None) -> Dict[str, bool]:
    """Restart MCP servers"""
    manager = get_server_manager()
    return manager.restart_servers(server_names)

def get_servers_status() -> Dict[str, Any]:
    """Get status of all servers"""
    manager = get_server_manager()
    return manager.get_server_status()

def check_servers_health() -> Dict[str, bool]:
    """Check if all servers are running properly"""
    status = get_servers_status()
    health = {}
    
    for server_name, server_info in status["servers"].items():
        health[server_name] = server_info["running"] and server_info["script_exists"]
    
    return health

def get_server_info(server_name: str) -> Dict[str, Any]:
    """Get detailed information about a specific server"""
    manager = get_server_manager()
    if server_name not in manager.servers:
        return {"error": f"Unknown server: {server_name}"}
    
    server_info = manager.servers[server_name]
    is_running = server_name in manager.processes and manager.processes[server_name] is not None
    
    return {
        "name": server_info["name"],
        "description": server_info["description"],
        "script_path": server_info["script"],
        "script_exists": os.path.exists(server_info["script"]),
        "running": is_running,
        "process_id": manager.processes[server_name].pid if is_running else None
    }

def list_available_servers() -> List[Dict[str, str]]:
    """List all available servers with their descriptions"""
    manager = get_server_manager()
    servers = []
    
    for server_name, server_info in manager.servers.items():
        servers.append({
            "name": server_name,
            "display_name": server_info["name"],
            "description": server_info["description"],
            "script_path": server_info["script"]
        })
    
    return servers

def test_server_connection(server_name: str) -> Dict[str, Any]:
    """Test connection to a specific server"""
    try:
        from fastmcp import Client
        
        manager = get_server_manager()
        if server_name not in manager.servers:
            return {"error": f"Unknown server: {server_name}", "success": False}
        
        script_path = manager.servers[server_name]["script"]
        
        if not os.path.exists(script_path):
            return {"error": f"Server script not found: {script_path}", "success": False}
        
        # Test with a simple client connection
        async def test_connection():
            try:
                async with Client(script_path) as client:
                    tools = await client.list_tools()
                    return {
                        "success": True,
                        "tools_count": len(tools),
                        "tools": [tool.name for tool in tools]
                    }
            except Exception as e:
                return {"error": str(e), "success": False}
        
        import asyncio
        return asyncio.run(test_connection())
        
    except Exception as e:
        return {"error": f"Connection test failed: {str(e)}", "success": False}

# Convenience functions for common operations
def start_all_servers() -> Dict[str, bool]:
    """Start all 4 core servers"""
    return start_mcp_servers()

def stop_all_servers() -> Dict[str, bool]:
    """Stop all 4 core servers"""
    return stop_mcp_servers()

def restart_all_servers() -> Dict[str, bool]:
    """Restart all 4 core servers"""
    return restart_mcp_servers()

def get_quick_status() -> str:
    """Get a quick status summary"""
    status = get_servers_status()
    running = status["running_servers"]
    total = status["total_servers"]
    
    if running == total:
        return f"✅ All {total} servers running"
    elif running == 0:
        return f"❌ All {total} servers stopped"
    else:
        return f"⚠️ {running}/{total} servers running"

if __name__ == "__main__":
    # Simple CLI for testing
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python server_manager.py [start|stop|restart|status|health]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "start":
        results = start_all_servers()
        print(f"Started servers: {results}")
    elif command == "stop":
        results = stop_all_servers()
        print(f"Stopped servers: {results}")
    elif command == "restart":
        results = restart_all_servers()
        print(f"Restarted servers: {results}")
    elif command == "status":
        status = get_servers_status()
        print(f"Server status: {status}")
    elif command == "health":
        health = check_servers_health()
        print(f"Server health: {health}")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1) 