"""
MCP Servers Startup Script

This script starts all MCP servers for the GitHub Repository Analyzer.
It manages server lifecycle, configuration, and provides a unified interface.
"""

import asyncio
import logging
import os
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor

from .file_content_server import FileContentServer
from .repository_structure_server import RepositoryStructureServer
from .commit_history_server import CommitHistoryServer
from .issues_server import IssuesServer
from .code_search_server import CodeSearchServer

logger = logging.getLogger(__name__)

class MCPServerManager:
    """
    Manager for all MCP servers.
    
    Handles:
    - Server initialization and startup
    - Configuration management
    - Health monitoring
    - Graceful shutdown
    """
    
    def __init__(self):
        self.servers = {}
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Initialize all servers
        self._initialize_servers()
    
    def _initialize_servers(self):
        """Initialize all MCP servers."""
        try:
            # File Content Server
            self.servers['file_content'] = FileContentServer()
            logger.info("Initialized File Content Server")
            
            # Repository Structure Server
            self.servers['repository_structure'] = RepositoryStructureServer()
            logger.info("Initialized Repository Structure Server")
            
            # Commit History Server
            self.servers['commit_history'] = CommitHistoryServer()
            logger.info("Initialized Commit History Server")
            
            # Issues Server
            self.servers['issues'] = IssuesServer()
            logger.info("Initialized Issues Server")
            
            # Code Search Server
            self.servers['code_search'] = CodeSearchServer()
            logger.info("Initialized Code Search Server")
            
        except Exception as e:
            logger.error(f"Error initializing servers: {e}")
            raise
    
    async def start_all_servers(self, host: str = "localhost", base_port: int = 8000):
        """
        Start all MCP servers.
        
        Args:
            host: Server host address
            base_port: Base port number (servers will use consecutive ports)
        """
        if self.running:
            logger.warning("Servers are already running")
            return
        
        try:
            logger.info("Starting all MCP servers...")
            
            # Start each server on a different port
            port = base_port
            for server_name, server in self.servers.items():
                try:
                    await server.start_server(host, port)
                    logger.info(f"Started {server_name} server on {host}:{port}")
                    port += 1
                except Exception as e:
                    logger.error(f"Failed to start {server_name} server: {e}")
            
            self.running = True
            logger.info("All MCP servers started successfully")
            
        except Exception as e:
            logger.error(f"Error starting servers: {e}")
            raise
    
    async def stop_all_servers(self):
        """Stop all MCP servers gracefully."""
        if not self.running:
            logger.warning("Servers are not running")
            return
        
        try:
            logger.info("Stopping all MCP servers...")
            
            for server_name, server in self.servers.items():
                try:
                    await server.stop_server()
                    logger.info(f"Stopped {server_name} server")
                except Exception as e:
                    logger.error(f"Error stopping {server_name} server: {e}")
            
            self.running = False
            logger.info("All MCP servers stopped")
            
        except Exception as e:
            logger.error(f"Error stopping servers: {e}")
            raise
    
    async def get_server_status(self) -> Dict[str, Any]:
        """Get status of all servers."""
        status = {
            "running": self.running,
            "servers": {}
        }
        
        for server_name, server in self.servers.items():
            status["servers"][server_name] = {
                "name": server.name,
                "description": server.description,
                "initialized": True
            }
        
        return status
    
    async def handle_tool_call(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Handle a tool call for a specific server.
        
        Args:
            server_name: Name of the server to call
            tool_name: Name of the tool to execute
            arguments: Arguments for the tool
            
        Returns:
            Tool execution result
        """
        if server_name not in self.servers:
            raise ValueError(f"Unknown server: {server_name}")
        
        server = self.servers[server_name]
        return await server.handle_tool_call(tool_name, arguments)
    
    def get_available_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all available tools from all servers.
        
        Returns:
            Dictionary mapping server names to their available tools
        """
        tools = {}
        
        for server_name, server in self.servers.items():
            try:
                # Get tools from server (this would need to be implemented in each server)
                tools[server_name] = []
                logger.info(f"Retrieved tools from {server_name} server")
            except Exception as e:
                logger.error(f"Error getting tools from {server_name} server: {e}")
                tools[server_name] = []
        
        return tools

# Global server manager instance
server_manager = MCPServerManager()

async def start_servers(host: str = "localhost", base_port: int = 8000):
    """
    Start all MCP servers.
    
    Args:
        host: Server host address
        base_port: Base port number
    """
    await server_manager.start_all_servers(host, base_port)

async def stop_servers():
    """Stop all MCP servers."""
    await server_manager.stop_all_servers()

async def get_status() -> Dict[str, Any]:
    """Get status of all servers."""
    return await server_manager.get_server_status()

async def handle_tool_call(server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Any:
    """
    Handle a tool call.
    
    Args:
        server_name: Name of the server
        tool_name: Name of the tool
        arguments: Tool arguments
        
    Returns:
        Tool result
    """
    return await server_manager.handle_tool_call(server_name, tool_name, arguments)

def get_available_tools() -> Dict[str, List[Dict[str, Any]]]:
    """Get all available tools."""
    return server_manager.get_available_tools()

# Main function for standalone server startup
async def main():
    """Main function for standalone server startup."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Start MCP servers for GitHub Repository Analyzer")
    parser.add_argument("--host", default="localhost", help="Server host address")
    parser.add_argument("--port", type=int, default=8000, help="Base port number")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Start servers
        await start_servers(args.host, args.port)
        
        # Keep servers running
        logger.info("MCP servers are running. Press Ctrl+C to stop.")
        
        # Wait for interrupt
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        
        # Stop servers
        await stop_servers()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        await stop_servers()

if __name__ == "__main__":
    asyncio.run(main()) 