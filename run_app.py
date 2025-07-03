#!/usr/bin/env python3
"""
Helper script to run the GitHub Repository Analyzer correctly
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    print("🚀 Starting GitHub Repository Analyzer...")
    print("📝 Note: This application must be run with 'streamlit run'")
    print()
    
    try:
        # Check if streamlit is installed
        import streamlit
        print("✅ Streamlit is installed")
        
        # Run the application
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        
    except ImportError:
        print("❌ Streamlit is not installed!")
        print("📦 Please install it with: pip install streamlit")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 