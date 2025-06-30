"""
Improved Server Manager for MCP servers
Handles starting and stopping MCP servers using the official Anthropic MCP SDK
"""

import subprocess
import time
import os
import signal
from typing import List, Dict, Any
from pathlib import Path

class ServerManager:
    """Manages MCP server processes using the official SDK"""
    
    def __init__(self):
        self.processes = []
        self.server_script = "src/servers/repository_analyzer_server.py"
        self.server_name = "Repository Analyzer MCP Server"
    
    def start_servers(self) -> bool:
        """Start the MCP server using the official SDK"""
        try:
            # Check if server script exists
            if not os.path.exists(self.server_script):
                print(f"❌ Server script not found: {self.server_script}")
                return False
            
            # Start the MCP server process
            process = subprocess.Popen(
                ["python", self.server_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.processes.append(process)
            
            # Wait for server to start
            time.sleep(3)
            
            # Check if server is running
            if self.check_server():
                print(f"✅ {self.server_name} started successfully")
                return True
            else:
                print(f"❌ {self.server_name} failed to start")
                return False
        
        except Exception as e:
            print(f"❌ Error starting {self.server_name}: {e}")
            return False
    
    def stop_servers(self) -> bool:
        """Stop all MCP servers"""
        try:
            success = True
            for process in self.processes:
                try:
                    # Try graceful shutdown first
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if graceful shutdown fails
                    process.kill()
                    process.wait()
                except Exception as e:
                    print(f"❌ Error stopping server: {e}")
                    success = False
            
            self.processes.clear()
            print(f"✅ {self.server_name} stopped")
            return success
        
        except Exception as e:
            print(f"❌ Error stopping servers: {e}")
            return False
    
    def check_server(self) -> bool:
        """Check if the MCP server is running"""
        try:
            # Try to import and test the MCP client
            from src.servers.mcp_client_improved import SyncMCPClient
            
            with SyncMCPClient() as client:
                # Test a simple operation
                result = client.get_repository_overview("https://github.com/microsoft/vscode")
                return result.get("success", False)
        
        except Exception as e:
            print(f"❌ Server check failed: {e}")
            return False
    
    def get_server_status(self) -> Dict[str, Any]:
        """Get detailed server status"""
        status = {
            "server_name": self.server_name,
            "running": False,
            "process_count": len(self.processes),
            "script_path": self.server_script,
            "script_exists": os.path.exists(self.server_script)
        }
        
        if self.processes:
            for i, process in enumerate(self.processes):
                status[f"process_{i}_pid"] = process.pid
                status[f"process_{i}_alive"] = process.poll() is None
        
        status["running"] = self.check_server()
        return status
    
    def restart_servers(self) -> bool:
        """Restart all MCP servers"""
        print(f"🔄 Restarting {self.server_name}...")
        if self.stop_servers():
            time.sleep(2)
            return self.start_servers()
        return False

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
    status = manager.get_server_status()
    
    return {
        "repository_analyzer": status["running"]
    }

def restart_mcp_servers() -> bool:
    """Restart MCP servers"""
    manager = get_server_manager()
    return manager.restart_servers()

def get_detailed_server_status() -> Dict[str, Any]:
    """Get detailed server status information"""
    manager = get_server_manager()
    return manager.get_server_status()

# Development utilities
def install_mcp_server() -> bool:
    """Install the MCP server for development"""
    try:
        import subprocess
        import sys
        
        # Check if mcp CLI is available
        result = subprocess.run([sys.executable, "-m", "mcp", "--version"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            # Install the server
            server_path = Path("src/servers/repository_analyzer_server.py")
            if server_path.exists():
                result = subprocess.run([
                    sys.executable, "-m", "mcp", "install", str(server_path)
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ MCP server installed successfully")
                    return True
                else:
                    print(f"❌ Failed to install MCP server: {result.stderr}")
                    return False
            else:
                print(f"❌ Server script not found: {server_path}")
                return False
        else:
            print("❌ MCP CLI not available. Install with: pip install 'mcp[cli]'")
            return False
    
    except Exception as e:
        print(f"❌ Error installing MCP server: {e}")
        return False

def dev_mcp_server() -> bool:
    """Start MCP server in development mode"""
    try:
        import subprocess
        import sys
        
        server_path = Path("src/servers/repository_analyzer_server.py")
        if server_path.exists():
            print("🚀 Starting MCP server in development mode...")
            subprocess.run([
                sys.executable, "-m", "mcp", "dev", str(server_path)
            ])
            return True
        else:
            print(f"❌ Server script not found: {server_path}")
            return False
    
    except Exception as e:
        print(f"❌ Error starting MCP server in dev mode: {e}")
        return False

if __name__ == "__main__":
    # Test the server manager
    print("🧪 Testing Server Manager...")
    
    manager = get_server_manager()
    
    # Test server start
    print("Starting server...")
    if manager.start_servers():
        print("✅ Server started successfully")
        
        # Test server status
        status = manager.get_server_status()
        print(f"Server status: {status}")
        
        # Test server stop
        print("Stopping server...")
        if manager.stop_servers():
            print("✅ Server stopped successfully")
        else:
            print("❌ Failed to stop server")
    else:
        print("❌ Failed to start server") 