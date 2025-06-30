"""
Basic Usage Example for GitHub Repository Analyzer
Demonstrates how to use the AI agent and MCP servers programmatically
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.agent.ai_agent import create_ai_agent, ask_question
from src.utils.config import load_config
from src.utils.github import validate_github_token, get_repository_info

def main():
    """Basic usage example"""
    print("🔍 GitHub Repository Analyzer - Basic Usage Example")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    print(f"✅ Configuration loaded: {config['app']['name']} v{config['app']['version']}")
    
    # Check environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not github_token:
        print("❌ GITHUB_TOKEN not found. Please set it in your environment.")
        return
    
    if not openai_key and not anthropic_key:
        print("❌ No AI API key found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY.")
        return
    
    # Validate GitHub token
    print("🔐 Validating GitHub token...")
    if not validate_github_token(github_token):
        print("❌ Invalid GitHub token.")
        return
    print("✅ GitHub token validated successfully!")
    
    # Create AI agent
    model = "gpt-4" if openai_key else "claude-3-sonnet"
    print(f"🤖 Creating AI agent with model: {model}")
    
    try:
        agent = create_ai_agent(model, config)
        print("✅ AI agent created successfully!")
    except Exception as e:
        print(f"❌ Failed to create AI agent: {e}")
        return
    
    # Example repository
    repo_url = "https://github.com/microsoft/vscode"
    print(f"📁 Analyzing repository: {repo_url}")
    
    # Set environment variable for MCP servers
    os.environ['GITHUB_REPO_URL'] = repo_url
    
    # Get repository info
    repo_info = get_repository_info(repo_url, github_token)
    if repo_info:
        print(f"📊 Repository: {repo_info['full_name']}")
        print(f"📝 Description: {repo_info['description']}")
        print(f"💻 Language: {repo_info['language']}")
        print(f"⭐ Stars: {repo_info['stars']}")
        print(f"🍴 Forks: {repo_info['forks']}")
        print(f"🐛 Issues: {repo_info['issues']}")
    
    # Example questions
    questions = [
        "What is this repository about?",
        "What are the main entry points of this application?",
        "What programming languages are used?",
        "Are there any recent changes in the last 5 commits?"
    ]
    
    print("\n" + "=" * 50)
    print("💬 Example Questions and Answers")
    print("=" * 50)
    
    for i, question in enumerate(questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("-" * 30)
        
        try:
            response = ask_question(agent, question, repo_url)
            
            if response["success"]:
                print(f"🤖 Answer: {response['response'][:200]}...")
                if response.get("tools_used"):
                    print(f"🔧 Tools used: {', '.join(response['tools_used'])}")
            else:
                print(f"❌ Error: {response['response']}")
        
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()
    
    print("✅ Basic usage example completed!")

if __name__ == "__main__":
    main() 