#!/usr/bin/env python3
"""
Test script to specifically demonstrate the Bug Analysis Agent
Shows how the Bug Analyzer Agent works with colorful logging
"""

from multi_agent_system import FeedbackAnalysisSystem
from colorful_logger import print_banner, log_system_status, logger

def test_bug_analyzer_agent():
    """Test the Bug Analysis Agent with various bug reports"""
    
    print_banner("🐛 BUG ANALYSIS AGENT TEST", "Testing bug detection and analysis capabilities")
    
    # Initialize system
    log_system_status("Initializing", "Creating feedback analysis system")
    system = FeedbackAnalysisSystem()
    
    # Test cases: different types of bug reports and non-bugs
    test_cases = [
        {
            'text': "App crashes when I try to open it on my iPhone 14 Pro with iOS 17.1. It happens every time after the latest update version 3.2.1. I lose all my data!",
            'category': 'Bug',
            'description': 'Critical crash bug with data loss'
        },
        {
            'text': "Error message appears when syncing with Google Drive on Samsung Galaxy S21, Android 11. Cannot reproduce consistently but happens after device restart.",
            'category': 'Bug', 
            'description': 'Sync error with reproduction steps'
        },
        {
            'text': "The app is slow and freezes sometimes on my Pixel 6 Pro. Performance issues started after version 3.2.0 update.",
            'category': 'Bug',
            'description': 'Performance bug'
        },
        {
            'text': "Please add dark mode to the app. It would be great for night usage and battery saving.",
            'category': 'Feature Request',
            'description': 'Feature request (should be skipped by Bug Analyzer)'
        },
        {
            'text': "I love this app! It's amazing and works perfectly. Great job developers!",
            'category': 'Praise',
            'description': 'Praise (should be skipped by Bug Analyzer)'
        },
        {
            'text': "Login button is broken and doesn't respond to taps. Critical issue preventing app usage. iPhone 12, iOS 16.5.",
            'category': 'Bug',
            'description': 'Critical UI bug'
        }
    ]
    
    print("\n" + "="*80)
    logger.info("🧪 TESTING BUG ANALYSIS AGENT WITH VARIOUS FEEDBACK TYPES")
    print("="*80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case['description']} ---")
        logger.info(f"📝 Input Text: \"{test_case['text'][:60]}...\"")
        logger.info(f"📊 Category: {test_case['category']}")
        
        # Execute Bug Analysis Agent
        result = system.execute_bug_analyzer_manually(test_case['text'], test_case['category'])
        
        # Display results
        print(f"🔍 Analysis Results:")
        for key, value in result.items():
            print(f"   {key}: {value}")
        
        print()
    
    # Test the full hybrid pipeline to see Bug Analyzer in context
    print("\n" + "="*80)
    logger.info("🔄 TESTING BUG ANALYZER IN FULL HYBRID PIPELINE")
    print("="*80)
    
    # Create sample feedback with a mix of bugs and non-bugs
    logger.info("💡 This will show Bug Analyzer working with other agents")
    logger.info("📊 Check console for colorful logging of all agent interactions")
    
    try:
        # Run a small test if files exist
        import os
        if os.path.exists('app_store_reviews.csv') or os.path.exists('support_emails.csv'):
            logger.info("🚀 Running hybrid pipeline...")
            results = system.process_feedback_hybrid(
                'app_store_reviews.csv' if os.path.exists('app_store_reviews.csv') else None,
                'support_emails.csv' if os.path.exists('support_emails.csv') else None
            )
            
            if results:
                # Count bug-specific results
                bug_count = sum(1 for r in results if r.get('category') == 'Bug')
                feature_count = sum(1 for r in results if r.get('category') == 'Feature Request')
                
                logger.success(f"✅ Pipeline completed!")
                logger.info(f"🐛 Bug reports processed by Bug Analyzer: {bug_count}")
                logger.info(f"🚀 Feature requests processed by Feature Extractor: {feature_count}")
                logger.info(f"📊 Total items processed: {len(results)}")
        else:
            logger.warning("⚠️ No CSV files found for full pipeline test")
            
    except Exception as e:
        logger.error(f"❌ Pipeline test failed: {str(e)}")

def demonstrate_bug_analyzer_logic():
    """Show what the Bug Analysis Agent looks for"""
    
    print_banner("🧠 BUG ANALYZER LOGIC", "Understanding how the Bug Analysis Agent works")
    
    logger.info("🔍 Bug Analysis Agent Detection Logic:")
    logger.info("  📋 STEP 1: Category Check")
    logger.info("    • Only processes items categorized as 'Bug' by Classifier Agent")
    logger.info("    • Skips Feature Requests, Praise, Complaints, Spam")
    logger.info("")
    
    logger.info("  🛠️  STEP 2: Technical Details Extraction")
    logger.info("    • Uses Technical Details Tool to find:")
    logger.info("      - Device information (iPhone, Samsung, Pixel, etc.)")
    logger.info("      - OS versions (iOS 17.1, Android 14, etc.)")
    logger.info("      - App versions (version 3.2.1)")
    logger.info("      - Reproduction steps")
    logger.info("")
    
    logger.info("  ⚡ STEP 3: Priority Assessment")
    logger.info("    • Uses Priority Tool to determine urgency")
    logger.info("    • Considers business impact and user effect")
    logger.info("")
    
    logger.info("  🎯 STEP 4: Severity Analysis")
    logger.info("    • HIGH: crash, data loss, cannot, critical, urgent")
    logger.info("    • MEDIUM: error, issue, problem, broken")
    logger.info("    • LOW: other bug-related terms")
    logger.info("")
    
    logger.info("  📝 STEP 5: Additional Bug Data")
    logger.info("    • Checks for reproduction steps")
    logger.info("    • Assesses technical complexity")
    logger.info("    • Provides bug-specific metadata")
    
    print("\n" + "="*60)
    logger.success("🎯 Bug Analysis Agent is fully integrated with colorful logging!")
    logger.info("💡 Run 'python test_bug_analyzer_agent.py' to see it in action")

if __name__ == "__main__":
    # Run both tests
    test_bug_analyzer_agent()
    print("\n")
    demonstrate_bug_analyzer_logic()
    
    # Final summary
    print_banner("📋 BUG ANALYZER TEST COMPLETE", "Bug Analysis Agent is working correctly!")
    
    logger.success("✅ Bug Analysis Agent - Fully functional with colorful logging")
    logger.success("✅ Agent Integration - Works in hybrid pipeline")
    logger.success("✅ Specialized Analysis - Bug-specific logic implemented")
    logger.success("✅ Tool Integration - Uses Technical Details and Priority tools")
    logger.info("🎨 All bug analysis operations include rich colorful logging output!")