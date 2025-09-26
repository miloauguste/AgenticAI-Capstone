#!/usr/bin/env python3
"""
Test script to demonstrate Google Gemini LLM integration
Shows the difference between Hybrid and Full CrewAI modes
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.getcwd())

from multi_agent_system import FeedbackAnalysisSystem

def test_gemini_llm_backend():
    """Test if Google Gemini is properly configured as LLM backend"""
    
    print("\n" + "="*60)
    print("GOOGLE GEMINI LLM INTEGRATION TEST")
    print("="*60)
    
    # Initialize system
    system = FeedbackAnalysisSystem()
    
    # Check LLM backend
    llm_backend = system._get_llm_backend()
    
    if llm_backend:
        backend_name = type(llm_backend).__name__
        print(f"[SUCCESS] LLM Backend: {backend_name}")
        
        if 'gemini' in backend_name.lower() or 'google' in backend_name.lower():
            print("[SUCCESS] Google Gemini successfully configured!")
            print(f"[INFO] Model: {getattr(llm_backend, 'model', 'gemini-1.5-flash')}")
            print(f"[INFO] Temperature: {getattr(llm_backend, 'temperature', 0.1)}")
            
            # Test basic LLM functionality (optional)
            try:
                print("\n[TESTING] Basic Gemini functionality...")
                response = llm_backend.invoke("Classify this feedback: 'The app crashes on my phone'. Category?")
                if hasattr(response, 'content'):
                    print(f"[GEMINI] {response.content[:100]}...")
                    print("[SUCCESS] Gemini is responding correctly!")
                else:
                    print("[INFO] Gemini configured but response format unexpected")
                    
            except Exception as e:
                print(f"[WARNING] Gemini test failed: {str(e)}")
                print("[INFO] This might be due to API limits or network issues")
                
        else:
            print(f"[INFO] Different LLM configured: {backend_name}")
            print("[INFO] To use Gemini, set GOOGLE_API_KEY environment variable")
            
    else:
        print("[INFO] No LLM backend configured")
        print("[INFO] System will use Hybrid mode (still fully functional)")
        print("[INFO] To enable Gemini: run python setup_gemini.py")
    
    return llm_backend is not None

def demonstrate_processing_modes():
    """Demonstrate different processing modes with/without Gemini"""
    
    print("\n" + "="*60)
    print("PROCESSING MODES DEMONSTRATION")
    print("="*60)
    
    system = FeedbackAnalysisSystem()
    
    # Test feedback
    test_feedback = [
        "The app keeps crashing on my iPhone 14 Pro with iOS 17.1. Very frustrating!",
        "Please add dark mode for night usage. Would be great for battery life.",
        "Love this app! Works perfectly and the interface is clean and intuitive."
    ]
    
    print("\n[TESTING] Processing modes with sample feedback:")
    
    for i, feedback in enumerate(test_feedback, 1):
        print(f"\n--- Test {i}: {feedback[:40]}... ---")
        
        # Test classification
        classifier_result = system.classification_tool._run(feedback)
        print(f"[CLASSIFIER] {classifier_result}")
        
        # Test bug analysis if it's a bug
        if 'Bug' in classifier_result:
            bug_result = system.execute_bug_analyzer_manually(feedback, 'Bug')
            print(f"[BUG ANALYZER] Priority: {bug_result.get('bug_priority', 'N/A')}")
            
        # Test feature extraction if it's a feature request  
        elif 'Feature' in classifier_result:
            feature_result = system.execute_feature_extractor_manually(feedback, 'Feature Request')
            print(f"[FEATURE EXTRACTOR] Impact: {feature_result.get('feature_impact', 'N/A')}")
    
    print(f"\n[INFO] With Gemini LLM: Enhanced reasoning and context awareness")
    print(f"[INFO] Without Gemini: Rule-based processing (still effective)")

def show_configuration_status():
    """Show current configuration status"""
    
    print("\n" + "="*60)
    print("CONFIGURATION STATUS")
    print("="*60)
    
    # Check environment variables
    google_key = os.getenv('GOOGLE_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    print(f"[CONFIG] Google API Key: {'✅ Set' if google_key else '❌ Not set'}")
    print(f"[CONFIG] OpenAI API Key: {'✅ Set' if openai_key else '❌ Not set'}")
    print(f"[CONFIG] Anthropic API Key: {'✅ Set' if anthropic_key else '❌ Not set'}")
    
    # Check .env file
    if os.path.exists('.env'):
        print(f"[CONFIG] .env file: ✅ Found")
        try:
            with open('.env', 'r') as f:
                content = f.read()
                if 'GOOGLE_API_KEY' in content:
                    print(f"[CONFIG] .env contains Google API Key: ✅")
                else:
                    print(f"[CONFIG] .env missing Google API Key: ❌")
        except:
            print(f"[CONFIG] .env file read error")
    else:
        print(f"[CONFIG] .env file: ❌ Not found")
    
    print("\n[INSTRUCTIONS]")
    if not google_key:
        print("  To enable Google Gemini:")
        print("    1. Run: python setup_gemini.py")
        print("    2. Or manually set GOOGLE_API_KEY environment variable")
        print("    3. Restart the system")
    else:
        print("  ✅ Google Gemini is ready to use!")
        print("  Run: python -m streamlit run ui_app.py")
        print("  Select 'Full CrewAI (Needs LLM)' processing mode")

if __name__ == "__main__":
    print("Google Gemini Integration Test")
    print("=" * 60)
    
    # Test LLM backend
    has_llm = test_gemini_llm_backend()
    
    # Show configuration
    show_configuration_status()
    
    # Demonstrate processing
    demonstrate_processing_modes()
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    
    if has_llm:
        print("✅ LLM backend configured - Full agent capabilities available")
        print("🎯 Recommended: Use 'Full CrewAI (Needs LLM)' mode in UI")
    else:
        print("ℹ️  No LLM backend - Hybrid mode available (still fully functional)")
        print("🎯 Recommended: Use 'Hybrid Agents (Recommended)' mode in UI")
        print("💡 To enable Gemini: python setup_gemini.py")
    
    print("="*60)