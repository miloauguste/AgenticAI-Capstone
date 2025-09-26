#!/usr/bin/env python3
"""
Simple test script for agent functionality without Unicode issues
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.getcwd())

from multi_agent_system import FeedbackAnalysisSystem

def test_mock_data_processing():
    """Test processing of expected_classifications.csv as mock data"""
    
    print("\n" + "="*60)
    print("TESTING MOCK DATA PROCESSING")
    print("="*60)
    
    # Check if expected_classifications.csv exists
    if not os.path.exists('expected_classifications.csv'):
        print("[ERROR] expected_classifications.csv not found!")
        return
    
    print("[INFO] Found expected_classifications.csv")
    
    # Initialize system
    system = FeedbackAnalysisSystem()
    
    try:
        print("[INFO] Processing mock data from expected_classifications.csv...")
        
        # Run mock data processing
        results = system.process_mock_data_from_expected_classifications()
        
        if results:
            print(f"[SUCCESS] Processed {len(results)} mock items!")
            
            # Show some stats
            categories = {}
            for result in results:
                cat = result.get('category', 'Unknown')
                categories[cat] = categories.get(cat, 0) + 1
            
            print("[INFO] Category breakdown:")
            for cat, count in categories.items():
                print(f"  {cat}: {count} items")
                
            # Show a few examples
            print("\n[INFO] Sample results:")
            for i, result in enumerate(results[:3]):
                print(f"  {i+1}. {result.get('category', 'Unknown')} - {result.get('title', 'No title')[:50]}...")
                
        else:
            print("[ERROR] No results from mock data processing")
            
    except Exception as e:
        print(f"[ERROR] Mock data processing failed: {str(e)}")

def test_agents_individually():
    """Test individual agents with simple feedback"""
    
    print("\n" + "="*60)
    print("TESTING INDIVIDUAL AGENTS")
    print("="*60)
    
    system = FeedbackAnalysisSystem()
    
    # Test Bug Analyzer Agent
    print("\n[TESTING] Bug Analysis Agent")
    bug_result = system.execute_bug_analyzer_manually(
        "App crashes on iPhone 14 Pro with iOS 17.1. Data loss occurred.",
        "Bug"
    )
    print("[RESULT] Bug Analysis:", bug_result)
    
    # Test Feature Extractor Agent  
    print("\n[TESTING] Feature Extractor Agent")
    feature_result = system.execute_feature_extractor_manually(
        "Please add dark mode for better night usage and battery savings.",
        "Feature Request"
    )
    print("[RESULT] Feature Extraction:", feature_result)
    
    # Test CSV Reader Agent
    print("\n[TESTING] CSV Reader Agent")
    if os.path.exists('expected_classifications.csv'):
        csv_result = system.execute_csv_reader_manually('expected_classifications.csv')
        print("[RESULT] CSV Reader: Successfully read", len(csv_result), "characters of data")
    else:
        print("[SKIP] No CSV file found for testing")

if __name__ == "__main__":
    print("SIMPLE AGENT TESTING - NO UNICODE")
    print("=" * 60)
    
    # Test mock data processing first
    test_mock_data_processing()
    
    # Test agents individually
    test_agents_individually()
    
    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)