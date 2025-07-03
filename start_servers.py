#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple MCP Server Starter
Starts all FastMCP v2 servers for the GitHub Repository Analyzer
"""

import subprocess
import sys
import os
import time

def start_server(script_path, server_name):
    print(f"Starting {server_name}...")
    try:
        process = subprocess.Popen([sys.executable, script_path])
        time.sleep(1)
        if process.poll() is None:
            print(f"Started {server_name} (PID: {process.pid})")
            return process
        else:
            print(f"Failed to start {server_name}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    servers = [
        ("src/servers/file_content_server.py", "File Content Server"),
        ("src/servers/repository_structure_server.py", "Repository Structure Server"),
        ("src/servers/commit_history_server.py", "Commit History Server"),
        ("src/servers/code_search_server.py", "Code Search Server"),
    ]
    processes = []
    for script, name in servers:
        if os.path.exists(script):
            proc = start_server(script, name)
            if proc: processes.append((proc, name))
        else:
            print(f"File not found: {script}")
    if not processes:
        print("No servers started.")
        return
    print("\nPress Ctrl+C to stop all servers.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        for proc, name in processes:
            try:
                proc.terminate()
                print(f"Stopped {name}")
            except Exception:
                pass

if __name__ == "__main__":
    main() 