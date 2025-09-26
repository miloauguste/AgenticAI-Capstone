#!/usr/bin/env python3
"""
Test script for real-time agent display functionality
"""

import sys
import os
import time

# Add current directory to Python path
sys.path.append(os.getcwd())

from realtime_agent_display import get_realtime_logger
from multi_agent_system import FeedbackAnalysisSystem

def simulate_agent_interactions():
    """Simulate agent interactions for testing"""
    
    # Get the real-time logger
    logger = get_realtime_logger()
    logger.reset()
    
    print("🤖 Starting simulated agent interactions...")
    
    # Simulate initialization
    logger.log_phase_change("Initializing system")
    time.sleep(1)
    
    # Simulate CSV Reader Agent
    logger.log_agent_start("CSV Reader Agent", "Reading app_store_reviews.csv")
    time.sleep(0.5)
    logger.log_agent_action("CSV Reader Agent", "parsing", "CSV file structure")
    time.sleep(0.5)
    logger.log_agent_action("CSV Reader Agent", "validating", "data integrity")
    time.sleep(0.5)
    logger.log_agent_complete("CSV Reader Agent", "Successfully read 50 reviews")
    
    # Update progress
    logger.log_progress_update(10, 50)
    time.sleep(0.5)
    
    # Simulate Feedback Classifier Agent
    logger.log_agent_start("Feedback Classifier Agent", "Classifying feedback items")
    time.sleep(0.5)
    logger.log_agent_action("Feedback Classifier Agent", "analyzing", "text patterns and keywords")
    time.sleep(0.5)
    logger.log_agent_action("Feedback Classifier Agent", "categorizing", "feedback types")
    time.sleep(0.5)
    logger.log_agent_complete("Feedback Classifier Agent", "Classified 50 items with 95% confidence")
    
    logger.log_progress_update(20, 50)
    time.sleep(0.5)
    
    # Simulate Bug Analysis Agent
    logger.log_agent_start("Bug Analysis Agent", "Analyzing 15 bug reports")
    time.sleep(0.5)
    logger.log_agent_action("Bug Analysis Agent", "extracting", "technical details and device info")
    time.sleep(0.5)
    logger.log_agent_action("Bug Analysis Agent", "assessing", "severity and priority levels")
    time.sleep(0.5)
    logger.log_agent_complete("Bug Analysis Agent", "Analyzed 15 bugs: 3 Critical, 8 High, 4 Medium")
    
    logger.log_progress_update(30, 50)
    time.sleep(0.5)
    
    # Simulate Feature Extractor Agent
    logger.log_agent_start("Feature Extractor Agent", "Processing 12 feature requests")
    time.sleep(0.5)
    logger.log_agent_action("Feature Extractor Agent", "evaluating", "user impact and business value")
    time.sleep(0.5)
    logger.log_agent_action("Feature Extractor Agent", "assessing", "implementation complexity")
    time.sleep(0.5)
    logger.log_agent_complete("Feature Extractor Agent", "Extracted 12 features: 4 High impact, 8 Medium impact")
    
    logger.log_progress_update(40, 50)
    time.sleep(0.5)
    
    # Simulate Ticket Creator Agent
    logger.log_agent_start("Ticket Creator Agent", "Generating structured tickets")
    time.sleep(0.5)
    logger.log_agent_action("Ticket Creator Agent", "creating", "ticket templates and metadata")
    time.sleep(0.5)
    logger.log_agent_action("Ticket Creator Agent", "formatting", "titles and descriptions")
    time.sleep(0.5)
    logger.log_agent_complete("Ticket Creator Agent", "Generated 47 structured tickets")
    
    logger.log_progress_update(47, 50)
    time.sleep(0.5)
    
    # Simulate Quality Reviewer Agent
    logger.log_agent_start("Quality Reviewer Agent", "Reviewing ticket quality")
    time.sleep(0.5)
    logger.log_agent_action("Quality Reviewer Agent", "validating", "completeness and accuracy")
    time.sleep(0.5)
    logger.log_agent_action("Quality Reviewer Agent", "scoring", "quality metrics")
    time.sleep(0.5)
    logger.log_agent_complete("Quality Reviewer Agent", "Reviewed 47 tickets: Average quality 98%")
    
    logger.log_progress_update(47, 50)
    time.sleep(0.5)
    
    # Final completion
    logger.log_phase_change("Processing completed")
    
    print("\n✅ Simulation completed!")
    print("📊 Check the activity log and stats:")
    
    # Display final stats
    stats = logger.get_stats()
    print(f"  • Agents used: {len(stats['agents_used'])}")
    print(f"  • Processing phases: {stats['current_phase']}")
    print(f"  • Items processed: {stats['processed_items']}/{stats['total_items']}")
    
    # Display recent activities
    activities = logger.get_recent_activities(10)
    print(f"\n🎭 Last 10 activities:")
    for activity in activities[-10:]:
        print(f"  [{activity['timestamp']}] {activity['message']}")

def test_with_actual_system():
    """Test with actual system processing"""
    
    print("\n" + "="*60)
    print("TESTING WITH ACTUAL MULTI-AGENT SYSTEM")
    print("="*60)
    
    # Check if sample data exists
    if not (os.path.exists('app_store_reviews.csv') or os.path.exists('expected_classifications.csv')):
        print("❌ No sample data files found")
        print("💡 Run this from the directory with CSV files")
        return
    
    # Initialize system
    system = FeedbackAnalysisSystem()
    logger = get_realtime_logger()
    logger.reset()
    
    print("🚀 Running real agent processing with real-time logging...")
    
    try:
        # Use mock data if available
        if os.path.exists('expected_classifications.csv'):
            print("📊 Processing mock data from expected_classifications.csv")
            results = system.process_mock_data_from_expected_classifications()
        else:
            print("📊 Processing app store reviews")
            results = system.process_feedback_hybrid('app_store_reviews.csv', None)
        
        if results:
            print(f"✅ Successfully processed {len(results)} items")
            
            # Show final stats
            stats = logger.get_stats()
            print(f"📈 Agents used: {len(stats['agents_used'])}")
            for agent in sorted(stats['agents_used']):
                print(f"  • {agent}")
                
        else:
            print("❌ Processing returned no results")
            
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")

if __name__ == "__main__":
    print("Real-time Agent Display Test")
    print("=" * 60)
    
    # Test 1: Simulate agent interactions
    simulate_agent_interactions()
    
    # Test 2: Use actual system
    test_with_actual_system()
    
    print("\n" + "=" * 60)
    print("🎉 Real-time display testing completed!")
    print("💡 This demonstrates the agent activity logging system")
    print("🎯 In the UI, you'll see these interactions in real-time!")
    print("=" * 60)