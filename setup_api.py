#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for API keys and environment configuration
"""

import os
import sys
import subprocess

def create_env_file():
    """Create .env file with API key"""
    env_content = """# Groq API Configuration
GROQ_API_KEY=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

# GitHub Configuration (Optional - for private repos)
GITHUB_TOKEN=

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def set_environment_variable():
    """Set GROQ_API_KEY in current environment"""
    api_key = "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"
    
    try:
        os.environ["GROQ_API_KEY"] = api_key
        print("✅ GROQ_API_KEY set in environment")
        return True
    except Exception as e:
        print(f"❌ Failed to set environment variable: {e}")
        return False

def test_api_key():
    """Test the API key with a simple request"""
    print("\n🧪 Testing Groq API key...")
    
    try:
        # Add src to path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        from agno.models.groq import Groq
        
        # Test the API key
        groq_model = Groq(id="llama-3.1-70b-versatile")
        response = groq_model.complete("Hello, this is a test.")
        
        if response and response.content:
            print("✅ API key is valid and working!")
            print(f"Response: {response.content[:100]}...")
            return True
        else:
            print("❌ API key test failed - no response received")
            return False
            
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
        print("✅ python-dotenv installed")
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "plotly"])
        print("✅ plotly upgraded")
        
        return True
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Repository Analyzer API Setup")
    print("=" * 40)
    
    # Step 1: Create .env file
    print("\n1. Creating .env file...")
    create_env_file()
    
    # Step 2: Set environment variable
    print("\n2. Setting environment variable...")
    set_environment_variable()
    
    # Step 3: Install dependencies
    print("\n3. Installing dependencies...")
    install_dependencies()
    
    # Step 4: Test API key
    print("\n4. Testing API key...")
    api_test_result = test_api_key()
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Setup Summary:")
    print("=" * 40)
    
    if api_test_result:
        print("✅ All setup steps completed successfully!")
        print("\n🎉 Your repository analyzer is ready to use!")
        print("\nTo start the application, run:")
        print("  streamlit run app.py")
    else:
        print("⚠️ Setup completed but API key test failed.")
        print("Please check your internet connection and try again.")
        print("\nYou can still run the application, but some AI features may not work.")

if __name__ == "__main__":
    main() 