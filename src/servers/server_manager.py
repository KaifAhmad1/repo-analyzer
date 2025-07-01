"""
Multi-Server Manager for FastMCP v2 Servers
Handles starting and stopping all MCP servers in the repository analyzer ecosystem
"""

import subprocess
import time
import os
import signal
from typing import List, Dict, Any
from pathlib import Path

class MultiServerManager:
    """Manages multiple FastMCP v2 server processes"""
    
    def __init__(self):
        self.servers = {
            "repository_analyzer": {
                "script": "src/servers/repository_analyzer_server.py",
                "name": "Repository Analyzer MCP Server",
                "description": "Provides repository overview and analysis tools"
            },
            "file_content": {
                "script": "src/servers/file_content_server.py",
                "name": "File Content MCP Server", 
                "description": "Provides file content and directory listing tools"
            },
            "repository_structure": {
                "script": "src/servers/repository_structure_server.py",
                "name": "Repository Structure MCP Server",
                "description": "Provides directory tree and structure analysis tools"
            },
            "commit_history": {
                "script": "src/servers/commit_history_server.py",
                "name": "Commit History MCP Server",
                "description": "Provides commit history and statistics tools"
            },
            "issues": {
                "script": "src/servers/issues_server.py",
                "name": "Issues MCP Server",
                "description": "Provides issues and pull requests tools"
            },
            "code_search": {
                "script": "src/servers/code_search_server.py",
                "name": "Code Search MCP Server",
                "description": "Provides code search and metrics tools"
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
        time.sleep(3)
        
        # Verify servers are running
        for server_name in server_names:
            if results.get(server_name, False):
                if not self.check_server(server_name):
                    results[server_name] = False
                    print(f"❌ {self.servers[server_name]['name']} failed to start properly")
        
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
    
    def check_server(self, server_name: str) -> bool:
        """Check if a specific MCP server is running"""
        if server_name not in self.processes:
            return False
        
        process = self.processes[server_name]
        if process is None:
            return False
        
        # Check if process is alive
        if process.poll() is not None:
            return False
        
        # Try to test the server with a simple operation
        try:
            from src.servers.mcp_client_improved import UnifiedMCPClient
            
            with UnifiedMCPClient() as client:
                # Test with a simple tool call based on server type
                if server_name == "repository_analyzer":
                    result = client.get_repository_overview("https://github.com/microsoft/vscode")
                elif server_name == "file_content":
                    result = client.list_directory("https://github.com/microsoft/vscode")
                elif server_name == "repository_structure":
                    result = client.get_directory_tree("https://github.com/microsoft/vscode", max_depth=1)
                elif server_name == "commit_history":
                    result = client.get_recent_commits("https://github.com/microsoft/vscode", limit=1)
                elif server_name == "issues":
                    result = client.get_issues("https://github.com/microsoft/vscode", limit=1)
                elif server_name == "code_search":
                    result = client.search_code("https://github.com/microsoft/vscode", "README")
                else:
                    return True  # Unknown server, assume it's running
                
                return result.get("success", False)
        
        except Exception as e:
            print(f"❌ Server check failed for {server_name}: {e}")
            return False
    
    def get_server_status(self) -> Dict[str, Any]:
        """Get detailed status of all servers"""
        status = {
            "servers": {},
            "total_servers": len(self.servers),
            "running_servers": 0,
            "stopped_servers": 0
        }
        
        for server_name, server_info in self.servers.items():
            server_status = {
                "name": server_info["name"],
                "description": server_info["description"],
                "script_path": server_info["script"],
                "script_exists": os.path.exists(server_info["script"]),
                "running": False,
                "process_id": None
            }
            
            if server_name in self.processes and self.processes[server_name]:
                process = self.processes[server_name]
                server_status["process_id"] = process.pid
                server_status["running"] = self.check_server(server_name)
            
            status["servers"][server_name] = server_status
            
            if server_status["running"]:
                status["running_servers"] += 1
            else:
                status["stopped_servers"] += 1
        
        return status
    
    def restart_servers(self, server_names: List[str] = None) -> Dict[str, bool]:
        """Restart specified MCP servers or all servers if none specified"""
        if server_names is None:
            server_names = list(self.servers.keys())
        
        print(f"🔄 Restarting servers: {', '.join(server_names)}")
        
        # Stop servers
        stop_results = self.stop_servers(server_names)
        time.sleep(2)
        
        # Start servers
        start_results = self.start_servers(server_names)
        
        # Combine results
        results = {}
        for server_name in server_names:
            results[server_name] = stop_results.get(server_name, True) and start_results.get(server_name, False)
        
        return results
    
    def get_server_info(self, server_name: str) -> Dict[str, Any]:
        """Get information about a specific server"""
        if server_name not in self.servers:
            return {"error": f"Unknown server: {server_name}"}
        
        server_info = self.servers[server_name].copy()
        server_info["running"] = self.check_server(server_name)
        server_info["process_id"] = self.processes.get(server_name, None)
        
        return server_info

# Global server manager instance
_server_manager = None

def get_server_manager() -> MultiServerManager:
    """Get global server manager instance"""
    global _server_manager
    if _server_manager is None:
        _server_manager = MultiServerManager()
    return _server_manager

def start_mcp_servers(server_names: List[str] = None) -> Dict[str, bool]:
    """Start MCP servers"""
    manager = get_server_manager()
    return manager.start_servers(server_names)

def stop_mcp_servers(server_names: List[str] = None) -> Dict[str, bool]:
    """Stop MCP servers"""
    manager = get_server_manager()
    return manager.stop_servers(server_names)

def check_servers_status() -> Dict[str, bool]:
    """Check status of all servers"""
    manager = get_server_manager()
    status = manager.get_server_status()
    
    return {
        server_name: server_status["running"]
        for server_name, server_status in status["servers"].items()
    }

def restart_mcp_servers(server_names: List[str] = None) -> Dict[str, bool]:
    """Restart MCP servers"""
    manager = get_server_manager()
    return manager.restart_servers(server_names)

def get_detailed_server_status() -> Dict[str, Any]:
    """Get detailed server status information"""
    manager = get_server_manager()
    return manager.get_server_status()

def get_server_info(server_name: str) -> Dict[str, Any]:
    """Get information about a specific server"""
    manager = get_server_manager()
    return manager.get_server_info(server_name)

# Development utilities
def install_mcp_servers() -> Dict[str, bool]:
    """Install all MCP servers for development"""
    results = {}
    
    try:
        import subprocess
        import sys
        
        # Check if mcp CLI is available
        result = subprocess.run([sys.executable, "-m", "mcp", "--version"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            manager = get_server_manager()
            
            for server_name, server_info in manager.servers.items():
                server_path = Path(server_info["script"])
                if server_path.exists():
                    result = subprocess.run([
                        sys.executable, "-m", "mcp", "install", str(server_path)
                    ], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        results[server_name] = True
                        print(f"✅ Installed {server_info['name']}")
                    else:
                        results[server_name] = False
                        print(f"❌ Failed to install {server_info['name']}: {result.stderr}")
                else:
                    results[server_name] = False
                    print(f"❌ Server script not found: {server_path}")
        else:
            print("❌ MCP CLI not available. Install with: pip install 'mcp[cli]'")
            return {name: False for name in manager.servers.keys()}
    
    except Exception as e:
        print(f"❌ Error installing MCP servers: {e}")
        return {name: False for name in get_server_manager().servers.keys()}
    
    return results

def dev_mcp_servers(server_names: List[str] = None) -> bool:
    """Start MCP servers in development mode"""
    try:
        import subprocess
        import sys
        
        manager = get_server_manager()
        if server_names is None:
            server_names = list(manager.servers.keys())
        
        for server_name in server_names:
            if server_name in manager.servers:
                server_path = Path(manager.servers[server_name]["script"])
                if server_path.exists():
                    print(f"🚀 Starting {manager.servers[server_name]['name']} in development mode...")
                    subprocess.run([
                        sys.executable, "-m", "mcp", "dev", str(server_path)
                    ])
                    return True
                else:
                    print(f"❌ Server script not found: {server_path}")
                    return False
            else:
                print(f"❌ Unknown server: {server_name}")
                return False
    
    except Exception as e:
        print(f"❌ Error starting MCP servers in dev mode: {e}")
        return False

if __name__ == "__main__":
    # Test the server manager
    print("🧪 Testing Multi-Server Manager...")
    
    manager = get_server_manager()
    
    # Test server start
    print("Starting all servers...")
    results = manager.start_servers()
    print(f"Start results: {results}")
    
    # Test server status
    status = manager.get_server_status()
    print(f"Server status: {status}")
    
    # Test server stop
    print("Stopping all servers...")
    stop_results = manager.stop_servers()
    print(f"Stop results: {stop_results}") 