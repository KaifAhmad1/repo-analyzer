#!/usr/bin/env python3
"""
Simple Startup Script for GitHub Repository Analyzer
Ensures all MCP servers are running before starting the Streamlit app
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def start_mcp_servers():
    """Start all MCP servers"""
    print("🚀 Starting MCP servers...")
    
    servers = [
        "src/servers/file_content_server.py",
        "src/servers/repository_structure_server.py",
        "src/servers/commit_history_server.py",
        "src/servers/code_search_server.py"
    ]
    
    processes = []
    
    for server in servers:
        if os.path.exists(server):
            try:
                print(f"▶️ Starting {server}...")
                process = subprocess.Popen(
                    [sys.executable, server],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    text=True
                )
                processes.append((server, process))
                print(f"✅ {server} started (PID: {process.pid})")
            except Exception as e:
                print(f"❌ Failed to start {server}: {e}")
        else:
            print(f"⚠️ Server file not found: {server}")
    
    # Wait for servers to start
    print("⏳ Waiting for servers to initialize...")
    time.sleep(3)
    
    # Check if servers are running
    running_count = 0
    for server, process in processes:
        if process.poll() is None:  # Still running
            running_count += 1
            print(f"🟢 {server} is running")
        else:
            print(f"🔴 {server} failed to start")
    
    print(f"📊 {running_count}/{len(processes)} servers are running")
    
    return processes

def start_streamlit():
    """Start the Streamlit application"""
    print("🌐 Starting Streamlit application...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Streamlit stopped by user")
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")

def main():
    """Main function"""
    print("🚀 GitHub Repository Analyzer - Startup")
    print("=" * 50)
    
    # Start MCP servers
    server_processes = start_mcp_servers()
    
    print("\n" + "=" * 50)
    print("🎯 Starting main application...")
    print("=" * 50)
    
    try:
        # Start Streamlit
        start_streamlit()
    finally:
        # Cleanup: stop all server processes
        print("\n🧹 Cleaning up server processes...")
        for server, process in server_processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Stopped {server}")
            except:
                try:
                    process.kill()
                    print(f"⚠️ Force killed {server}")
                except:
                    print(f"❌ Could not stop {server}")

if __name__ == "__main__":
    main() 