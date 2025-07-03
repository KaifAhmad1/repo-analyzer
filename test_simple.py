#!/usr/bin/env python3
"""
Simple Test Script for Enhanced GitHub Repository Analyzer
Tests basic functionality and imports
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_imports():
    """Test basic module imports"""
    print("🔍 Testing basic imports...")
    
    try:
        # Test configuration
        from utils.config import get_analysis_settings, get_analysis_presets
        print("✅ Configuration imported successfully")
        
        # Test repository manager
        from utils.repository_manager import set_current_repository, get_current_repository
        print("✅ Repository manager imported successfully")
        
        # Test AI agent
        from agent.ai_agent import FastMCPTools, RepositoryAnalyzerAgent
        print("✅ AI agent imported successfully")
        
        # Test analysis engine
        from analysis.analysis_engine import analyze_repository, quick_analysis
        print("✅ Analysis engine imported successfully")
        
        # Test code analyzer
        from analysis.code_analyzer import analyze_code_quality
        print("✅ Code analyzer imported successfully")
        
        # Test repository visualizer
        from analysis.repository_visualizer import generate_repository_map
        print("✅ Repository visualizer imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {str(e)}")
        return False

def test_configuration():
    """Test configuration system"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        from utils.config import get_analysis_settings, get_analysis_presets
        
        settings = get_analysis_settings()
        print(f"✅ Settings loaded: {len(settings)} settings")
        
        presets = get_analysis_presets()
        print(f"✅ Presets loaded: {len(presets)} presets")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False

def test_ai_agent():
    """Test AI agent creation"""
    print("\n🤖 Testing AI Agent...")
    
    try:
        from agent.ai_agent import FastMCPTools, RepositoryAnalyzerAgent
        
        # Test FastMCPTools
        tools = FastMCPTools()
        print("✅ FastMCPTools created successfully")
        
        # Test RepositoryAnalyzerAgent
        agent = RepositoryAnalyzerAgent()
        print("✅ RepositoryAnalyzerAgent created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ AI agent test failed: {str(e)}")
        return False

def test_analysis_functions():
    """Test analysis functions"""
    print("\n📊 Testing Analysis Functions...")
    
    try:
        from analysis.analysis_engine import (
            analyze_repository, quick_analysis, comprehensive_analysis,
            security_analysis, code_quality_analysis, generate_visualizations,
            smart_summarization
        )
        print("✅ All analysis functions imported successfully")
        
        from analysis.code_analyzer import analyze_code_quality
        print("✅ Code analyzer function imported successfully")
        
        from analysis.repository_visualizer import generate_repository_map
        print("✅ Repository visualizer function imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis functions test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Starting Simple System Tests")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Configuration", test_configuration),
        ("AI Agent", test_ai_agent),
        ("Analysis Functions", test_analysis_functions)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {str(e)}")
        
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 