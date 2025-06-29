"""
MCP Servers Startup Script

This script starts all MCP servers for the GitHub Repository Analyzer.
"""

import asyncio
import logging
import os
from typing import List

# TODO: Import server classes
# from .file_content_server import FileContentServer
# from .repository_structure_server import RepositoryStructureServer
# from .commit_history_server import CommitHistoryServer
# from .issue_pr_server import IssuePRServer
# from .code_search_server import CodeSearchServer
# from .documentation_server import DocumentationServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MCPServerManager:
    """
    Manager for starting and stopping all MCP servers.
    """
    
    def __init__(self):
        self.servers = []
        self.running = False
        
    async def initialize_servers(self):
        """
        Initialize all MCP servers.
        """
        # TODO: Initialize all server instances
        # self.servers = [
        #     FileContentServer(),
        #     RepositoryStructureServer(),
        #     CommitHistoryServer(),
        #     IssuePRServer(),
        #     CodeSearchServer(),
        #     DocumentationServer()
        # ]
        
        logger.info(f"Initialized {len(self.servers)} MCP servers")
    
    async def start_all_servers(self, host: str = "localhost", base_port: int = 8000):
        """
        Start all MCP servers.
        
        Args:
            host: Host address for servers
            base_port: Base port number (each server gets base_port + offset)
        """
        if self.running:
            logger.warning("Servers are already running")
            return
        
        try:
            await self.initialize_servers()
            
            # Start each server on a different port
            for i, server in enumerate(self.servers):
                port = base_port + i
                logger.info(f"Starting {server.name} on {host}:{port}")
                # TODO: Start server asynchronously
                # await server.start_server(host, port)
            
            self.running = True
            logger.info("All MCP servers started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start servers: {e}")
            await self.stop_all_servers()
            raise
    
    async def stop_all_servers(self):
        """
        Stop all MCP servers gracefully.
        """
        if not self.running:
            return
        
        logger.info("Stopping all MCP servers...")
        
        for server in self.servers:
            try:
                # TODO: Stop server gracefully
                # await server.stop_server()
                logger.info(f"Stopped {server.name}")
            except Exception as e:
                logger.error(f"Error stopping {server.name}: {e}")
        
        self.running = False
        logger.info("All MCP servers stopped")
    
    def get_server_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all servers.
        
        Returns:
            List of server information dictionaries
        """
        return [
            {
                "name": server.name,
                "description": server.description,
                "status": "running" if self.running else "stopped"
            }
            for server in self.servers
        ]

async def main():
    """
    Main function to start all MCP servers.
    """
    manager = MCPServerManager()
    
    try:
        # Get configuration from environment
        host = os.getenv("MCP_SERVER_HOST", "localhost")
        base_port = int(os.getenv("MCP_SERVER_PORT", "8000"))
        
        logger.info("Starting GitHub Repository Analyzer MCP Servers...")
        await manager.start_all_servers(host, base_port)
        
        # Keep servers running
        logger.info("MCP servers are running. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        await manager.stop_all_servers()

if __name__ == "__main__":
    asyncio.run(main()) 