#!/usr/bin/env python3
"""
Test script for AST/CST analysis tools
"""

import asyncio
import json
from src.agent.ai_agent import FastMCPTools

async def test_ast_tools():
    """Test the new AST/CST analysis tools"""
    
    # Test repository (using this repo itself)
    test_repo = "https://github.com/KaifAhmad1/repo-analyzer"
    
    print("🧪 Testing AST/CST Analysis Tools")
    print("=" * 50)
    
    tools = FastMCPTools()
    
    # Test 1: Analyze codebase structure
    print("\n1. Testing analyze_codebase_structure...")
    try:
        result = await tools.analyze_codebase_structure(test_repo)
        print("✅ Codebase structure analysis completed")
        data = json.loads(result)
        if data.get("success"):
            print(f"   - Total files: {data.get('total_files', 0)}")
            print(f"   - Python files: {data.get('code_analysis', {}).get('total_python_files', 0)}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    # Test 2: Analyze specific file structure
    print("\n2. Testing analyze_code_structure for app.py...")
    try:
        result = await tools.analyze_code_structure(test_repo, "app.py")
        print("✅ Code structure analysis completed")
        data = json.loads(result)
        if data.get("success"):
            ast_data = data.get("ast_analysis", {})
            print(f"   - Functions: {len(ast_data.get('functions', []))}")
            print(f"   - Classes: {len(ast_data.get('classes', []))}")
            print(f"   - Complexity: {ast_data.get('complexity', 0)}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    # Test 3: Find code patterns
    print("\n3. Testing find_code_patterns for async functions...")
    try:
        result = await tools.find_code_patterns(test_repo, "async_functions")
        print("✅ Code pattern search completed")
        data = json.loads(result)
        if data.get("success"):
            print(f"   - Files with patterns: {data.get('count', 0)}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    # Test 4: Analyze file content
    print("\n4. Testing analyze_file_content for app.py...")
    try:
        result = await tools.analyze_file_content(test_repo, "app.py")
        print("✅ File content analysis completed")
        data = json.loads(result)
        if data.get("success"):
            analysis = data.get("code_analysis", {})
            print(f"   - Functions: {len(analysis.get('functions', []))}")
            print(f"   - Classes: {len(analysis.get('classes', []))}")
            print(f"   - Metrics: {analysis.get('metrics', {})}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    # Test 5: Get code summary
    print("\n5. Testing get_code_summary for app.py...")
    try:
        result = await tools.get_code_summary(test_repo, "app.py")
        print("✅ Code summary completed")
        data = json.loads(result)
        if data.get("success"):
            structure = data.get("structure", {})
            print(f"   - Functions: {structure.get('functions', 0)}")
            print(f"   - Classes: {structure.get('classes', 0)}")
            print(f"   - Complexity: {structure.get('complexity', 0)}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    # Test 6: Find code issues
    print("\n6. Testing find_code_issues for app.py...")
    try:
        result = await tools.find_code_issues(test_repo, "app.py")
        print("✅ Code issues analysis completed")
        data = json.loads(result)
        if data.get("success"):
            print(f"   - Issues found: {data.get('issue_count', 0)}")
            severity_counts = data.get("severity_counts", {})
            print(f"   - Warnings: {severity_counts.get('warning', 0)}")
            print(f"   - Info: {severity_counts.get('info', 0)}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 AST/CST Tools Testing Complete!")

if __name__ == "__main__":
    asyncio.run(test_ast_tools()) 