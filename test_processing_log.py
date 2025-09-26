#!/usr/bin/env python3
"""
Test script for processing log functionality
"""

import os
import sys
import pandas as pd

# Add current directory to Python path
sys.path.append(os.getcwd())

from multi_agent_system import FeedbackAnalysisSystem
from processing_logger import get_processing_logger

def test_processing_log():
    """Test the processing log functionality"""
    
    print("🧪 Testing Processing Log Functionality")
    print("=" * 60)
    
    # Remove existing log if exists
    log_file = "processing_log.csv"
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"🗑️ Removed existing {log_file}")
    
    # Initialize system (this will create a new session)
    print("🚀 Initializing FeedbackAnalysisSystem...")
    system = FeedbackAnalysisSystem()
    print(f"📋 Session ID: {system.session_id}")
    
    # Check if sample data exists
    if not os.path.exists('app_store_reviews.csv'):
        print("❌ No sample data files found")
        print("💡 Creating mock data for testing...")
        
        # Create simple test data
        test_data = [
            {
                'review_id': 'TEST001',
                'review_text': 'The app keeps crashing when I try to sync data. Very frustrating!',
                'rating': 1,
                'date': '2024-01-01',
                'platform': 'Google Play',
                'app_version': '3.2.1'
            },
            {
                'review_id': 'TEST002', 
                'review_text': 'Please add dark mode! It would be amazing for night usage.',
                'rating': 4,
                'date': '2024-01-02',
                'platform': 'App Store',
                'app_version': '3.2.1'
            }
        ]
        
        df = pd.DataFrame(test_data)
        df.to_csv('test_app_reviews.csv', index=False)
        print("✅ Created test_app_reviews.csv")
        
        # Test processing
        print("\n🔄 Processing test data...")
        try:
            results = system.process_feedback_hybrid('test_app_reviews.csv', None)
            print(f"✅ Processed {len(results)} items successfully")
        except Exception as e:
            print(f"❌ Error during processing: {str(e)}")
            return
        
        # Clean up test file
        if os.path.exists('test_app_reviews.csv'):
            os.remove('test_app_reviews.csv')
    
    else:
        print("📊 Found existing app_store_reviews.csv")
        # Test with existing data (limit to first few items)
        print("\n🔄 Processing sample data...")
        try:
            results = system.process_feedback_hybrid('app_store_reviews.csv', None)
            print(f"✅ Processed {len(results)} items successfully")
        except Exception as e:
            print(f"❌ Error during processing: {str(e)}")
            return
    
    # Verify processing log was created
    print(f"\n📋 Checking {log_file}...")
    if os.path.exists(log_file):
        print(f"✅ Processing log created successfully!")
        
        # Read and display some stats
        log_df = pd.read_csv(log_file)
        print(f"📊 Log entries: {len(log_df)}")
        print(f"📅 Session ID: {log_df['session_id'].iloc[0] if len(log_df) > 0 else 'None'}")
        
        # Show agent activity summary
        if len(log_df) > 0:
            agent_counts = log_df['agent_name'].value_counts()
            print(f"\n🤖 Agent Activity Summary:")
            for agent, count in agent_counts.items():
                print(f"  • {agent}: {count} actions")
            
            # Show some sample decision points
            print(f"\n🎯 Sample Decision Points:")
            decision_points = log_df['decision_point'].unique()[:5]
            for decision in decision_points:
                print(f"  • {decision}")
            
            # Show processing times
            avg_times = log_df.groupby('agent_name')['processing_time_ms'].mean()
            print(f"\n⏱️ Average Processing Times:")
            for agent, avg_time in avg_times.items():
                print(f"  • {agent}: {avg_time:.1f}ms")
            
            # Display first few rows
            print(f"\n📋 First 3 log entries:")
            display_cols = ['timestamp', 'agent_name', 'action_type', 'decision_point', 'confidence_score']
            available_cols = [col for col in display_cols if col in log_df.columns]
            print(log_df[available_cols].head(3).to_string(index=False))
        
    else:
        print(f"❌ Processing log not found!")
        return
    
    # Test session statistics
    print(f"\n📊 Testing Session Statistics...")
    processing_logger = get_processing_logger()
    stats = processing_logger.get_session_stats(system.session_id)
    
    if stats:
        print(f"✅ Session stats retrieved:")
        print(f"  • Total operations: {stats.get('total_operations', 0)}")
        print(f"  • Successful operations: {stats.get('successful_operations', 0)}")
        print(f"  • Success rate: {stats.get('success_rate', 0):.1%}")
        print(f"  • Total processing time: {stats.get('total_processing_time_ms', 0):.0f}ms")
        
        if 'agent_statistics' in stats:
            print(f"  • Agents used: {len(stats['agent_statistics'])}")
    else:
        print(f"❌ No session stats found")
    
    print(f"\n" + "=" * 60)
    print(f"🎉 Processing log test completed!")
    print(f"📁 Check '{log_file}' for detailed processing history")
    print(f"=" * 60)

if __name__ == "__main__":
    test_processing_log()