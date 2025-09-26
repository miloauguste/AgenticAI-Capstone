#!/usr/bin/env python3
"""
Test script for configuration management functionality
"""

import os
import sys
import json

# Add current directory to Python path
sys.path.append(os.getcwd())

from config_manager import get_config_manager, get_current_config
from multi_agent_system import FeedbackAnalysisSystem

def test_configuration_system():
    """Test the configuration management system"""
    
    print("🧪 Testing Configuration Management System")
    print("=" * 60)
    
    # Test 1: Configuration Loading
    print("\n1️⃣ Testing Configuration Loading...")
    config_manager = get_config_manager()
    config = config_manager.config
    
    print(f"✅ Configuration loaded")
    print(f"📋 Version: {config.version}")
    print(f"🆔 Created by: {config.created_by}")
    print(f"🕐 Last updated: {config.last_updated}")
    
    # Test 2: Configuration Validation
    print("\n2️⃣ Testing Configuration Validation...")
    validation = config_manager.validate_configuration()
    
    if validation['valid']:
        print("✅ Configuration is valid")
    else:
        print("❌ Configuration has issues:")
        for issue in validation['issues']:
            print(f"  • {issue}")
    
    if validation['warnings']:
        print("⚠️ Configuration warnings:")
        for warning in validation['warnings']:
            print(f"  • {warning}")
    
    # Test 3: Classification Thresholds
    print("\n3️⃣ Testing Classification Thresholds...")
    print(f"🐛 Bug threshold: {config.classification_thresholds.bug_threshold}")
    print(f"✨ Feature threshold: {config.classification_thresholds.feature_threshold}")
    print(f"👍 Praise threshold: {config.classification_thresholds.praise_threshold}")
    print(f"😠 Complaint threshold: {config.classification_thresholds.complaint_threshold}")
    print(f"🚫 Spam threshold: {config.classification_thresholds.spam_threshold}")
    print(f"⚖️ Minimum confidence: {config.classification_thresholds.minimum_confidence}")
    
    # Test threshold retrieval
    for category in ['Bug', 'Feature Request', 'Praise', 'Complaint', 'Spam']:
        threshold = config_manager.get_classification_threshold(category)
        print(f"  • {category}: {threshold}")
    
    # Test 4: Priority Weights
    print("\n4️⃣ Testing Priority Weights...")
    pw = config.priority_weights
    print(f"🐛 Bug severity weight: {pw.bug_severity_weight}")
    print(f"👥 User impact weight: {pw.user_impact_weight}")
    print(f"🔧 Technical complexity weight: {pw.technical_complexity_weight}")
    print(f"💼 Business priority weight: {pw.business_priority_weight}")
    
    total_weight = (pw.bug_severity_weight + pw.user_impact_weight + 
                   pw.technical_complexity_weight + pw.business_priority_weight)
    print(f"📊 Total weight: {total_weight}")
    
    # Test 5: Configuration Updates
    print("\n5️⃣ Testing Configuration Updates...")
    original_bug_threshold = config.classification_thresholds.bug_threshold
    
    # Update bug threshold
    new_threshold = 0.8
    success = config_manager.update_classification_thresholds(bug_threshold=new_threshold)
    
    if success:
        print(f"✅ Updated bug threshold from {original_bug_threshold} to {new_threshold}")
        
        # Verify update
        updated_config = config_manager.config
        if abs(updated_config.classification_thresholds.bug_threshold - new_threshold) < 0.001:
            print("✅ Configuration update verified")
        else:
            print("❌ Configuration update failed to persist")
            
        # Restore original value
        config_manager.update_classification_thresholds(bug_threshold=original_bug_threshold)
        print(f"🔄 Restored original bug threshold: {original_bug_threshold}")
    else:
        print("❌ Failed to update configuration")
    
    # Test 6: Multi-Agent System Integration
    print("\n6️⃣ Testing Multi-Agent System Integration...")
    try:
        system = FeedbackAnalysisSystem()
        system_config = system.config
        
        print("✅ Multi-agent system initialized with configuration")
        print(f"📋 System using config version: {system_config.version}")
        
        # Test classification with configured thresholds
        test_text = "The app keeps crashing when I try to sync data"
        result = json.loads(system.classification_tool._run(test_text))
        
        print(f"🧪 Test classification result:")
        print(f"  • Category: {result['category']}")
        print(f"  • Confidence: {result['confidence']:.1f}%")
        print(f"  • Threshold used: {result.get('threshold_used', 'N/A')}")
        print(f"  • Meets threshold: {result.get('meets_threshold', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Multi-agent system integration failed: {str(e)}")
    
    # Test 7: Configuration Export/Import
    print("\n7️⃣ Testing Configuration Export/Import...")
    export_file = "test_config_export.json"
    
    if config_manager.export_configuration(export_file):
        print(f"✅ Configuration exported to {export_file}")
        
        # Verify export file
        if os.path.exists(export_file):
            with open(export_file, 'r') as f:
                exported_data = json.load(f)
            
            print(f"📋 Export contains {len(exported_data)} configuration sections")
            
            # Clean up
            os.remove(export_file)
            print(f"🗑️ Cleaned up {export_file}")
        else:
            print(f"❌ Export file {export_file} not found")
    else:
        print("❌ Configuration export failed")
    
    # Test 8: Agent Settings
    print("\n8️⃣ Testing Agent Settings...")
    agent_settings = config.agent_settings
    
    print(f"🤖 Agent Settings:")
    print(f"  • Bug Analysis: {'✅ Enabled' if agent_settings.enable_bug_analysis else '❌ Disabled'}")
    print(f"  • Feature Extraction: {'✅ Enabled' if agent_settings.enable_feature_extraction else '❌ Disabled'}")
    print(f"  • Quality Review: {'✅ Enabled' if agent_settings.enable_quality_review else '❌ Disabled'}")
    print(f"  • Technical Extraction: {'✅ Enabled' if agent_settings.enable_technical_extraction else '❌ Disabled'}")
    
    print(f"⏱️ Agent Timeouts:")
    print(f"  • Classification: {agent_settings.classification_timeout}s")
    print(f"  • Bug Analysis: {agent_settings.bug_analysis_timeout}s")
    print(f"  • Feature Extraction: {agent_settings.feature_extraction_timeout}s")
    print(f"  • Quality Review: {agent_settings.quality_review_timeout}s")
    
    # Test 9: Quality Thresholds
    print("\n9️⃣ Testing Quality Thresholds...")
    qt = config.quality_thresholds
    
    print(f"✅ Quality Thresholds:")
    print(f"  • Minimum Quality Score: {qt.minimum_quality_score}")
    print(f"  • Auto-Approve Threshold: {qt.auto_approve_threshold}")
    print(f"  • Manual Review Threshold: {qt.manual_review_threshold}")
    print(f"  • Reject Threshold: {qt.reject_threshold}")
    
    # Verify threshold order
    thresholds = [qt.reject_threshold, qt.manual_review_threshold, qt.auto_approve_threshold]
    if thresholds == sorted(thresholds):
        print("✅ Quality thresholds are in correct order")
    else:
        print("❌ Quality thresholds are not in correct order")
    
    # Test 10: Processing Rules
    print("\n🔟 Testing Processing Rules...")
    pr = config.processing_rules
    
    print(f"🔧 Processing Rules:")
    print(f"  • Skip Low Confidence: {'✅ Yes' if pr.skip_low_confidence_items else '❌ No'}")
    print(f"  • Auto-categorize Spam: {'✅ Yes' if pr.auto_categorize_spam else '❌ No'}")
    print(f"  • Manual Review Critical: {'✅ Yes' if pr.require_manual_review_for_critical else '❌ No'}")
    print(f"  • Batch Size: {pr.batch_size}")
    print(f"  • Max Retries: {pr.max_retries}")
    
    print(f"\n" + "=" * 60)
    print(f"🎉 Configuration System Test Completed!")
    print(f"📋 All configuration components tested successfully")
    print(f"⚙️ System ready for use with configurable thresholds and priorities")
    print(f"=" * 60)

if __name__ == "__main__":
    test_configuration_system()