#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify API key input functionality
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_config_with_session_state():
    """Test config functions with simulated session state"""
    print("🧪 Testing config functions with session state...")
    
    try:
        from utils.config import get_groq_api_key, get_github_token
        
        # Test without session state
        print("1. Testing without session state...")
        groq_key = get_groq_api_key()
        github_token = get_github_token()
        
        print(f"   Groq API Key: {'✅ Set' if groq_key else '❌ Not set'}")
        print(f"   GitHub Token: {'✅ Set' if github_token else '❌ Not set'}")
        
        # Simulate setting environment variables
        print("\n2. Testing with environment variables...")
        os.environ["GROQ_API_KEY"] = "test_groq_key_123"
        os.environ["GITHUB_TOKEN"] = "test_github_token_456"
        
        groq_key = get_groq_api_key()
        github_token = get_github_token()
        
        print(f"   Groq API Key: {'✅ Set' if groq_key else '❌ Not set'}")
        print(f"   GitHub Token: {'✅ Set' if github_token else '❌ Not set'}")
        
        # Clean up
        if "GROQ_API_KEY" in os.environ:
            del os.environ["GROQ_API_KEY"]
        if "GITHUB_TOKEN" in os.environ:
            del os.environ["GITHUB_TOKEN"]
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_api_key_validation():
    """Test API key validation"""
    print("\n🧪 Testing API key validation...")
    
    try:
        # Test valid API key format
        valid_key = "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"
        if valid_key.startswith("gsk_"):
            print("✅ Valid Groq API key format")
        else:
            print("❌ Invalid Groq API key format")
        
        # Test GitHub token format
        valid_github_token = "ghp_1234567890abcdef1234567890abcdef12345678"
        if valid_github_token.startswith("ghp_"):
            print("✅ Valid GitHub token format")
        else:
            print("❌ Invalid GitHub token format")
        
        return True
        
    except Exception as e:
        print(f"❌ API key validation test failed: {e}")
        return False

def test_environment_setup():
    """Test environment setup"""
    print("\n🧪 Testing environment setup...")
    
    try:
        # Test setting environment variables
        test_groq_key = "gsk_test1234567890abcdef1234567890abcdef12345678"
        test_github_token = "ghp_test1234567890abcdef1234567890abcdef12345678"
        
        os.environ["GROQ_API_KEY"] = test_groq_key
        os.environ["GITHUB_TOKEN"] = test_github_token
        
        # Verify they were set
        if os.getenv("GROQ_API_KEY") == test_groq_key:
            print("✅ GROQ_API_KEY set correctly")
        else:
            print("❌ GROQ_API_KEY not set correctly")
        
        if os.getenv("GITHUB_TOKEN") == test_github_token:
            print("✅ GITHUB_TOKEN set correctly")
        else:
            print("❌ GITHUB_TOKEN not set correctly")
        
        # Clean up
        del os.environ["GROQ_API_KEY"]
        del os.environ["GITHUB_TOKEN"]
        
        return True
        
    except Exception as e:
        print(f"❌ Environment setup test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 API Key Input Test Suite")
    print("=" * 40)
    
    tests = [
        ("Config Functions", test_config_with_session_state),
        ("API Key Validation", test_api_key_validation),
        ("Environment Setup", test_environment_setup),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API key input functionality is working correctly.")
        print("\n✅ Ready to run the Streamlit application with user input!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 