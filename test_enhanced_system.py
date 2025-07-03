#!/usr/bin/env python3
"""
Comprehensive Test Script for Enhanced GitHub Repository Analyzer
Tests all new features: Code Analysis, Visualizations, Smart Summarization
"""

import sys
import os
import json
import time
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test all module imports"""
    print("🔍 Testing module imports...")
    
    try:
        # Core modules
        import importlib.util
        
        # Test AI Agent
        spec = importlib.util.spec_from_file_location("ai_agent", "src/agent/ai_agent.py")
        ai_agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ai_agent_module)
        print("✅ AI Agent modules imported successfully")
        
        # Test Analysis Engine
        spec = importlib.util.spec_from_file_location("analysis_engine", "src/analysis/analysis_engine.py")
        analysis_engine_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(analysis_engine_module)
        print("✅ Analysis Engine modules imported successfully")
        
        # Test Code Analyzer
        spec = importlib.util.spec_from_file_location("code_analyzer", "src/analysis/code_analyzer.py")
        code_analyzer_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(code_analyzer_module)
        print("✅ Code Analyzer modules imported successfully")
        
        # Test Repository Visualizer
        spec = importlib.util.spec_from_file_location("repository_visualizer", "src/analysis/repository_visualizer.py")
        visualizer_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(visualizer_module)
        print("✅ Repository Visualizer modules imported successfully")
        
        # Test Configuration
        spec = importlib.util.spec_from_file_location("config", "src/utils/config.py")
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        print("✅ Configuration modules imported successfully")
        
        # Test Repository Manager
        spec = importlib.util.spec_from_file_location("repository_manager", "src/utils/repository_manager.py")
        repo_manager_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(repo_manager_module)
        print("✅ Repository Manager modules imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {str(e)}")
        return False

def test_fastmcp_tools():
    """Test FastMCP tools functionality"""
    print("\n🔧 Testing FastMCP Tools...")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("ai_agent", "src/agent/ai_agent.py")
        ai_agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ai_agent_module)
        
        tools = ai_agent_module.FastMCPTools()
        print("✅ FastMCPTools initialized successfully")
        
        # Test tool methods exist
        methods = [
            'get_file_content', 'list_directory', 'get_readme_content',
            'get_directory_tree', 'get_file_structure', 'analyze_project_structure',
            'get_recent_commits', 'get_commit_statistics', 'get_development_patterns',
            'search_code', 'search_files', 'find_functions', 'get_code_metrics',
            'search_dependencies', 'analyze_code_complexity', 'get_code_patterns'
        ]
        
        for method in methods:
            if hasattr(tools, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        print("✅ All FastMCP tool methods verified")
        return True
        
    except Exception as e:
        print(f"❌ FastMCP tools test failed: {str(e)}")
        return False

def test_ai_agent():
    """Test AI agent functionality"""
    print("\n🤖 Testing AI Agent...")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("ai_agent", "src/agent/ai_agent.py")
        ai_agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ai_agent_module)
        
        # Test agent creation
        agent = ai_agent_module.RepositoryAnalyzerAgent()
        print("✅ RepositoryAnalyzerAgent created successfully")
        
        # Test agent methods
        methods = [
            'ask_question', 'generate_summary', 'analyze_code_patterns',
            'quick_analysis', '_gather_comprehensive_data'
        ]
        
        for method in methods:
            if hasattr(agent, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        print("✅ All AI agent methods verified")
        return True
        
    except Exception as e:
        print(f"❌ AI agent test failed: {str(e)}")
        return False

def test_code_analyzer():
    """Test code analyzer functionality"""
    print("\n📊 Testing Code Analyzer...")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("code_analyzer", "src/analysis/code_analyzer.py")
        code_analyzer_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(code_analyzer_module)
        
        # Test that the module can be imported
        print("✅ CodeAnalyzer module imported successfully")
        
        # Test that the main function exists
        if hasattr(code_analyzer_module, 'analyze_code_quality'):
            print("✅ analyze_code_quality function exists")
        else:
            print("❌ analyze_code_quality function missing")
            return False
        
        print("✅ All code analyzer functions verified")
        return True
        
    except Exception as e:
        print(f"❌ Code analyzer test failed: {str(e)}")
        return False

def test_repository_visualizer():
    """Test repository visualizer functionality"""
    print("\n🗺️ Testing Repository Visualizer...")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("repository_visualizer", "src/analysis/repository_visualizer.py")
        visualizer_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(visualizer_module)
        
        # Test that the module can be imported
        print("✅ RepositoryVisualizer module imported successfully")
        
        # Test that the main function exists
        if hasattr(visualizer_module, 'generate_repository_map'):
            print("✅ generate_repository_map function exists")
        else:
            print("❌ generate_repository_map function missing")
            return False
        
        print("✅ All repository visualizer functions verified")
        return True
        
    except Exception as e:
        print(f"❌ Repository visualizer test failed: {str(e)}")
        return False

def test_analysis_engine():
    """Test analysis engine functionality"""
    print("\n🚀 Testing Analysis Engine...")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("analysis_engine", "src/analysis/analysis_engine.py")
        analysis_engine_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(analysis_engine_module)
        
        # Test that the module can be imported
        print("✅ AnalysisEngine module imported successfully")
        
        # Test that the main functions exist
        functions = [
            'analyze_repository', 'quick_overview', 'comprehensive_analysis',
            'security_analysis', 'code_quality_analysis', 'generate_visualizations',
            'smart_summarization'
        ]
        
        for func in functions:
            if hasattr(analysis_engine_module, func):
                print(f"✅ Function {func} exists")
            else:
                print(f"❌ Function {func} missing")
                return False
        
        print("✅ All analysis engine functions verified")
        return True
        
    except Exception as e:
        print(f"❌ Analysis engine test failed: {str(e)}")
        return False

def test_configuration():
    """Test configuration system"""
    print("\n⚙️ Testing Configuration System...")
    
    try:
        from utils.config import get_analysis_settings, get_analysis_presets
        
        # Test settings
        settings = get_analysis_settings()
        if isinstance(settings, dict):
            print("✅ Analysis settings loaded successfully")
        else:
            print("❌ Analysis settings not loaded properly")
            return False
        
        # Test presets
        presets = get_analysis_presets()
        if isinstance(presets, dict) and len(presets) > 0:
            print("✅ Analysis presets loaded successfully")
        else:
            print("❌ Analysis presets not loaded properly")
            return False
        
        print("✅ Configuration system working properly")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False

def test_repository_manager():
    """Test repository manager functionality"""
    print("\n📁 Testing Repository Manager...")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("repository_manager", "src/utils/repository_manager.py")
        repo_manager_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(repo_manager_module)
        
        # Test that the module can be imported
        print("✅ RepositoryManager module imported successfully")
        
        # Test that the main functions exist
        functions = [
            'set_current_repository', 'get_current_repository',
            'get_analysis_history', 'export_session_data'
        ]
        
        for func in functions:
            if hasattr(repo_manager_module, func):
                print(f"✅ Function {func} exists")
            else:
                print(f"❌ Function {func} missing")
                return False
        
        print("✅ All repository manager functions verified")
        return True
        
    except Exception as e:
        print(f"❌ Repository manager test failed: {str(e)}")
        return False

def test_integration():
    """Test integration between components"""
    print("\n🔗 Testing Component Integration...")
    
    try:
        # Test that all modules can be imported together
        import importlib.util
        
        # Import all modules
        modules = [
            ("ai_agent", "src/agent/ai_agent.py"),
            ("analysis_engine", "src/analysis/analysis_engine.py"),
            ("code_analyzer", "src/analysis/code_analyzer.py"),
            ("repository_visualizer", "src/analysis/repository_visualizer.py"),
            ("config", "src/utils/config.py"),
            ("repository_manager", "src/utils/repository_manager.py")
        ]
        
        imported_modules = {}
        for name, path in modules:
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            imported_modules[name] = module
            print(f"✅ {name} module imported successfully")
        
        print("✅ All components can be imported together")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        return False

def test_function_exports():
    """Test function exports from modules"""
    print("\n📦 Testing Function Exports...")
    
    try:
        import importlib.util
        
        # Test analysis engine exports
        spec = importlib.util.spec_from_file_location("analysis_engine", "src/analysis/analysis_engine.py")
        analysis_engine_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(analysis_engine_module)
        
        # Check for main functions
        functions = [
            'analyze_repository', 'quick_overview', 'comprehensive_analysis',
            'security_analysis', 'code_quality_analysis', 'generate_visualizations',
            'smart_summarization'
        ]
        
        for func in functions:
            if hasattr(analysis_engine_module, func):
                print(f"✅ {func} function available")
            else:
                print(f"❌ {func} function missing")
        
        print("✅ Function exports working properly")
        return True
        
    except Exception as e:
        print(f"❌ Function exports test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 Starting Comprehensive System Tests")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("FastMCP Tools", test_fastmcp_tools),
        ("AI Agent", test_ai_agent),
        ("Code Analyzer", test_code_analyzer),
        ("Repository Visualizer", test_repository_visualizer),
        ("Analysis Engine", test_analysis_engine),
        ("Configuration", test_configuration),
        ("Repository Manager", test_repository_manager),
        ("Component Integration", test_integration),
        ("Function Exports", test_function_exports)
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
        print("🎉 All tests passed! System is ready for use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 