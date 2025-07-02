#!/usr/bin/env python3
"""
Test script for the enhanced AI agent
Verifies that the agent provides meaningful responses based on actual repository data
"""

import asyncio
import sys
import os
import time

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_enhanced_agent():
    """Test the enhanced AI agent functionality"""
    print("🚀 Testing Enhanced AI Agent...")
    
    try:
        from agent.ai_agent import (
            ask_repository_question,
            generate_repository_summary,
            quick_repository_analysis,
            analyze_repository_patterns
        )
        
        # Test repository URL (using a well-known repository)
        test_repo = "https://github.com/streamlit/streamlit"
        
        print(f"📁 Testing with repository: {test_repo}")
        print("=" * 60)
        
        # Test 1: Quick Analysis (simplified)
        print("\n1️⃣ Testing Quick Analysis...")
        try:
            def status_callback(msg):
                print(f"   Status: {msg}")
            
            result, tools_used = quick_repository_analysis(test_repo, status_callback=status_callback)
            print("✅ Quick Analysis Result:")
            print(result[:300] + "..." if len(result) > 300 else result)
            print(f"🔧 Tools used: {tools_used}")
        except Exception as e:
            print(f"❌ Quick Analysis failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 2: Q&A
        print("\n2️⃣ Testing Q&A...")
        try:
            question = "What is this repository about and what are its main features?"
            result, tools_used = ask_repository_question(question, test_repo)
            print("✅ Q&A Result:")
            print(result[:500] + "..." if len(result) > 500 else result)
            print(f"🔧 Tools used: {tools_used}")
        except Exception as e:
            print(f"❌ Q&A failed: {e}")
        
        # Test 3: Summary
        print("\n3️⃣ Testing Summary Generation...")
        try:
            result, tools_used = generate_repository_summary(test_repo)
            print("✅ Summary Result:")
            print(result[:500] + "..." if len(result) > 500 else result)
            print(f"🔧 Tools used: {tools_used}")
        except Exception as e:
            print(f"❌ Summary failed: {e}")
        
        # Test 4: Code Patterns
        print("\n4️⃣ Testing Code Pattern Analysis...")
        try:
            result, tools_used = analyze_repository_patterns(test_repo)
            print("✅ Code Patterns Result:")
            print(result[:500] + "..." if len(result) > 500 else result)
            print(f"🔧 Tools used: {tools_used}")
        except Exception as e:
            print(f"❌ Code Patterns failed: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 Enhanced Agent Testing Complete!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed and the src directory is in the path.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_agent() 