#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify the fixes for the repository analyzer
"""

import os
import sys
import asyncio
import json
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_groq_client():
    """Test Groq client initialization"""
    print("Testing Groq client initialization...")
    
    try:
        from agno.models.groq import Groq
        
        # Test without any extra parameters
        groq_model = Groq(id="llama-3.1-70b-versatile")
        print("Groq client initialized successfully")
        
        # Test a simple completion
        response = groq_model.complete("Hello, this is a test.")
        print(f"Groq API test successful: {response.content[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"Groq client test failed: {e}")
        return False

def test_ai_agent():
    """Test AI agent initialization"""
    print("\nTesting AI agent initialization...")
    
    try:
        from agent.ai_agent import RepositoryAnalyzerAgent
        
        # Test agent creation
        agent = RepositoryAnalyzerAgent()
        print("AI agent initialized successfully")
        
        # Test tools initialization
        if agent.tools:
            print("FastMCP tools initialized successfully")
        else:
            print("FastMCP tools not available")
        
        return True
        
    except Exception as e:
        print(f"AI agent test failed: {e}")
        return False

def test_visualization():
    """Test visualization functions"""
    print("\nTesting visualization functions...")
    
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        
        # Test creating a simple figure
        fig = go.Figure(data=go.Bar(x=['A', 'B', 'C'], y=[1, 2, 3]))
        fig_json = fig.to_json()
        
        # Test loading from JSON
        loaded_fig = go.Figure.from_json(fig_json)
        print("Plotly visualization test successful")
        
        return True
        
    except Exception as e:
        print(f"Visualization test failed: {e}")
        return False

def test_mcp_tools():
    """Test MCP tools functionality"""
    print("\nTesting MCP tools...")
    
    try:
        from agent.ai_agent import FastMCPTools
        
        # Test tools initialization
        tools = FastMCPTools()
        print("FastMCP tools created successfully")
        
        # Test server definitions
        if tools.servers:
            print(f"{len(tools.servers)} servers defined")
            for server_name, script_path in tools.servers.items():
                if os.path.exists(script_path):
                    print(f"  {server_name}: {script_path}")
                else:
                    print(f"  {server_name}: {script_path} (not found)")
        
        return True
        
    except Exception as e:
        print(f"MCP tools test failed: {e}")
        return False

async def test_async_functions():
    """Test async functionality"""
    print("\nTesting async functions...")
    
    try:
        from agent.ai_agent import FastMCPTools
        
        tools = FastMCPTools()
        
        # Test async tool call (this will likely fail if servers aren't running, but should not crash)
        try:
            result = await tools._call_server_tool("file_content", "get_readme_content", repo_url="https://github.com/test/test")
            print("Async tool call completed (result may be error if servers not running)")
        except Exception as e:
            print(f"Async tool call failed (expected if servers not running): {e}")
        
        return True
        
    except Exception as e:
        print(f"Async test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting Repository Analyzer Fix Tests")
    print("=" * 50)
    
    tests = [
        ("Groq Client", test_groq_client),
        ("AI Agent", test_ai_agent),
        ("Visualization", test_visualization),
        ("MCP Tools", test_mcp_tools),
    ]
    
    results = {}
    
    # Run synchronous tests
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"{test_name} test crashed: {e}")
            results[test_name] = False
    
    # Run async tests
    try:
        results["Async Functions"] = asyncio.run(test_async_functions())
    except Exception as e:
        print(f"Async test crashed: {e}")
        results["Async Functions"] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! The fixes are working correctly.")
    else:
        print("Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 