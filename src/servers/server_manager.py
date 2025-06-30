"""
Server Manager for MCP servers
Handles starting and stopping MCP servers
"""

import subprocess
import time
import requests
import os
from typing import List, Dict, Any

class ServerManager:
    """Manages MCP server processes"""
    
    def __init__(self):
        self.processes = []
        self.server_urls = {
            "file_content": "http://localhost:8001",
            "repository_structure": "http://localhost:8002", 
            "commit_history": "http://localhost:8003",
            "code_search": "http://localhost:8004",
            "issues": "http://localhost:8005"
        }
    
    def start_servers(self) -> bool:
        """Start all MCP servers"""
        try:
            # Start each server in a separate process
            server_scripts = [
                "src/servers/file_content_server.py",
                "src/servers/repository_structure_server.py", 
                "src/servers/commit_history_server.py",
                "src/servers/code_search_server.py",
                "src/servers/issues_server.py"
            ]
            
            for script in server_scripts:
                if os.path.exists(script):
                    process = subprocess.Popen(
                        ["python", script],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    self.processes.append(process)
            
            # Wait for servers to start
            time.sleep(3)
            
            # Check if servers are running
            return self.check_servers()
        
        except Exception as e:
            print(f"Error starting servers: {e}")
            return False
    
    def stop_servers(self) -> bool:
        """Stop all MCP servers"""
        try:
            for process in self.processes:
                process.terminate()
                process.wait()
            
            self.processes.clear()
            return True
        
        except Exception as e:
            print(f"Error stopping servers: {e}")
            return False
    
    def check_servers(self) -> bool:
        """Check if all servers are running"""
        for name, url in self.server_urls.items():
            try:
                response = requests.get(f"{url}/health", timeout=5)
                if response.status_code != 200:
                    print(f"Server {name} not responding")
                    return False
            except:
                print(f"Server {name} not reachable")
                return False
        
        return True

# Global server manager instance
_server_manager = None

def get_server_manager() -> ServerManager:
    """Get global server manager instance"""
    global _server_manager
    if _server_manager is None:
        _server_manager = ServerManager()
    return _server_manager

def start_mcp_servers() -> bool:
    """Start MCP servers"""
    manager = get_server_manager()
    return manager.start_servers()

def stop_mcp_servers() -> bool:
    """Stop MCP servers"""
    manager = get_server_manager()
    return manager.stop_servers()

def check_servers_status() -> Dict[str, bool]:
    """Check status of all servers"""
    manager = get_server_manager()
    status = {}
    
    for name, url in manager.server_urls.items():
        try:
            response = requests.get(f"{url}/health", timeout=5)
            status[name] = response.status_code == 200
        except:
            status[name] = False
    
    return status 