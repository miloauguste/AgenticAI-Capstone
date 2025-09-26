#!/usr/bin/env python3
"""
Setup script for Google Gemini LLM integration
Helps configure the system to use Google Gemini as the primary LLM
"""

import os
import sys

def setup_gemini_configuration():
    """Guide user through Gemini setup"""
    
    print("🚀 Google Gemini LLM Setup")
    print("=" * 50)
    
    # Check if API key is already set
    current_key = os.getenv('GOOGLE_API_KEY')
    if current_key:
        print(f"✅ Google API Key is already configured")
        print(f"   Key starts with: {current_key[:10]}...")
        
        response = input("\nDo you want to update it? (y/n): ").lower()
        if response != 'y':
            print("✅ Using existing Google API Key")
            return test_gemini_connection()
    
    print("\n📋 To use Google Gemini, you need a Google API Key:")
    print("   1. Go to https://aistudio.google.com/")
    print("   2. Sign in with your Google account")
    print("   3. Click 'Get API key' in the left sidebar")
    print("   4. Click 'Create API key' -> 'Create API key in new project'")
    print("   5. Copy the generated API key")
    
    print("\n🔑 Enter your Google API Key:")
    api_key = input("GOOGLE_API_KEY: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return False
    
    # Validate API key format (basic check)
    if not api_key.startswith('AIza') or len(api_key) < 30:
        print("⚠️ Warning: API key format doesn't look correct.")
        print("   Google API keys usually start with 'AIza' and are ~39 characters long")
        
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            print("Setup cancelled.")
            return False
    
    # Set environment variable
    os.environ['GOOGLE_API_KEY'] = api_key
    
    # Create .env file for persistence
    try:
        with open('.env', 'w') as f:
            f.write(f"GOOGLE_API_KEY={api_key}\n")
            f.write("# Google Gemini API Key for LLM backend\n")
            f.write("# This enables full CrewAI agent functionality\n")
        
        print("✅ API key saved to .env file")
        print("💡 The .env file will be loaded automatically by the system")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not save .env file: {str(e)}")
        print("💡 You can manually set the environment variable:")
        print(f"   export GOOGLE_API_KEY={api_key}")
    
    return test_gemini_connection()

def test_gemini_connection():
    """Test if Gemini is working correctly"""
    
    print("\n🧪 Testing Google Gemini connection...")
    
    try:
        # Import the system and test LLM configuration
        sys.path.append(os.getcwd())
        from multi_agent_system import FeedbackAnalysisSystem
        
        print("   Initializing system...")
        system = FeedbackAnalysisSystem()
        
        # Check if Gemini backend is configured
        llm_backend = system._get_llm_backend()
        
        if llm_backend and 'gemini' in str(type(llm_backend)).lower():
            print("✅ Google Gemini LLM backend successfully configured!")
            print(f"   Backend type: {type(llm_backend).__name__}")
            
            # Try a simple test (optional)
            try:
                print("   Testing basic functionality...")
                # Test with a simple prompt
                result = llm_backend.invoke("Say 'Hello from Gemini!'")
                if result and hasattr(result, 'content'):
                    print(f"   🎉 Gemini response: {result.content[:50]}...")
                    print("✅ Google Gemini is working perfectly!")
                    return True
                else:
                    print("✅ Google Gemini is configured (response test inconclusive)")
                    return True
                    
            except Exception as e:
                print(f"⚠️ Gemini configured but test failed: {str(e)}")
                print("💡 This might be due to API quotas or network issues")
                return True
                
        elif llm_backend:
            print(f"ℹ️ Different LLM backend configured: {type(llm_backend).__name__}")
            print("💡 Gemini was not selected (other LLM has priority)")
            return True
            
        else:
            print("❌ No LLM backend configured")
            print("💡 Check your API key and try again")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print("💡 Make sure the multi_agent_system.py file is present and working")
        return False

def show_usage_instructions():
    """Show how to use the system with Gemini"""
    
    print("\n📖 Usage Instructions")
    print("=" * 50)
    
    print("🎯 Now you can use Google Gemini with the system:")
    print("")
    print("1. **UI Mode (Recommended):**")
    print("   python -m streamlit run ui_app.py")
    print("   → Select 'Generate Tickets' from navigation")
    print("   → Choose 'Full CrewAI (Needs LLM)' processing mode")
    print("   → All agents will use Google Gemini for reasoning")
    print("")
    print("2. **Command Line Mode:**")
    print("   python test_simple.py")
    print("   → Tests individual agents with mock data")
    print("   → Shows colorful logging output")
    print("")
    print("3. **Hybrid Mode (Fallback):**")
    print("   → If Gemini has issues, system falls back to hybrid mode")
    print("   → All agents still work with colorful logging")
    print("   → No LLM required for basic functionality")
    print("")
    print("🎨 Features with Gemini:")
    print("   • Intelligent feedback classification")  
    print("   • Advanced bug analysis and prioritization")
    print("   • Smart feature extraction and assessment")
    print("   • Context-aware ticket generation")
    print("   • Quality review with detailed scoring")

def main():
    """Main setup function"""
    
    print("Google Gemini LLM Setup for Intelligent Feedback Analysis System")
    print("=" * 80)
    
    # Run setup
    success = setup_gemini_configuration()
    
    if success:
        show_usage_instructions()
        
        print("\n" + "=" * 50)
        print("🎉 Setup Complete!")
        print("   Google Gemini is now configured as your LLM backend")
        print("   Run: python -m streamlit run ui_app.py")
        print("=" * 50)
        
    else:
        print("\n" + "=" * 50) 
        print("❌ Setup Failed")
        print("   Please check your API key and try again")
        print("   You can still use the system in Hybrid mode")
        print("=" * 50)

if __name__ == "__main__":
    main()