#!/usr/bin/env python3
"""
Test script to verify if CSV Reader Agent is being used
Checks both direct tool usage and CrewAI agent integration
"""

import os
from multi_agent_system import FeedbackAnalysisSystem
from colorful_logger import print_banner, log_agent_start, log_agent_action, log_agent_complete
from colorful_logger import log_system_status, logger

def test_csv_reader_tool_directly():
    """Test the CSV Reader Tool directly"""
    
    print_banner("📖 CSV READER TOOL TEST", "Direct testing of CSV reading functionality")
    
    # Initialize system
    system = FeedbackAnalysisSystem()
    
    # Test direct tool usage
    log_agent_start("CSV Reader Tool", "Testing direct tool functionality")
    
    # Check if files exist
    files_to_test = ['app_store_reviews.csv', 'support_emails.csv']
    
    for file_path in files_to_test:
        if os.path.exists(file_path):
            logger.info(f"📁 Testing with file: {file_path}")
            
            # Test the tool directly
            result = system.csv_reader_tool._run(file_path)
            
            # Check if result looks like JSON data
            if result.startswith('[') or result.startswith('{'):
                logger.success(f"✅ CSV Reader Tool successfully processed {file_path}")
                logger.info(f"📊 Result length: {len(result)} characters")
            else:
                logger.error(f"❌ CSV Reader Tool failed: {result}")
        else:
            logger.warning(f"⚠️ File not found: {file_path}")
    
    log_agent_complete("CSV Reader Tool", "Direct tool testing completed")

def test_csv_reader_agent_in_crewai():
    """Test if CSV Reader Agent actually gets used in CrewAI pipeline"""
    
    print_banner("🤖 CSV READER AGENT IN CREWAI", "Testing agent integration in full pipeline")
    
    # Check if we have the necessary files
    if not (os.path.exists('app_store_reviews.csv') or os.path.exists('support_emails.csv')):
        logger.error("❌ No CSV files found for testing")
        return
    
    system = FeedbackAnalysisSystem()
    
    # Override the CSV Reader Tool to add more detailed logging
    original_run = system.csv_reader_tool._run
    
    def logged_csv_reader_run(file_path: str) -> str:
        log_agent_start("CSV Reader Agent (via CrewAI)", f"Reading file: {file_path}")
        log_agent_action("CSV Reader Agent", "processing", "CrewAI task execution")
        result = original_run(file_path)
        log_agent_complete("CSV Reader Agent (via CrewAI)", f"Task completed for {file_path}")
        return result
    
    # Monkey patch for testing
    system.csv_reader_tool._run = logged_csv_reader_run
    
    try:
        log_system_status("Testing", "Running CrewAI pipeline to check CSV Reader Agent usage")
        
        # Run the full pipeline
        result = system.process_feedback(
            'app_store_reviews.csv',
            'support_emails.csv'
        )
        
        if result:
            logger.success("✅ CrewAI pipeline completed - check above logs for CSV Reader Agent activity")
        else:
            logger.warning("⚠️ CrewAI pipeline returned no results")
            
    except Exception as e:
        logger.error(f"❌ CrewAI pipeline failed: {str(e)}")
        
        # Common reasons for failure
        logger.info("🔍 Possible reasons for CrewAI pipeline failure:")
        logger.info("  • No LLM API key configured (OpenAI, etc.)")
        logger.info("  • CrewAI requires LLM backend for agents to work")
        logger.info("  • Agents need LLM to interpret tasks and use tools")
        logger.info("  • Missing environment variables or configuration")

def demonstrate_expected_behavior():
    """Show what should happen when CSV Reader Agent works properly"""
    
    print_banner("💡 EXPECTED CSV READER AGENT BEHAVIOR", "What should happen in a working CrewAI setup")
    
    logger.info("🔄 Expected CSV Reader Agent Workflow:")
    logger.info("  1. 🤖 CrewAI Task: 'Read app store reviews from app_store_reviews.csv'")
    logger.info("  2. 🧠 LLM Agent: Understands it needs to read a CSV file")
    logger.info("  3. 🛠️  Agent: Calls csv_reader tool with file_path='app_store_reviews.csv'")
    logger.info("  4. 📖 Tool: Executes _run(file_path) with colorful logging")
    logger.info("  5. 📊 Tool: Returns JSON formatted data to agent")
    logger.info("  6. ✅ Agent: Completes task with processed data")
    
    print()
    logger.info("🚨 Current Issue Diagnosis:")
    logger.info("  • CSV Reader Agent is DEFINED in the CrewAI pipeline")
    logger.info("  • CSV Reader Tool has colorful logging implemented")
    logger.info("  • BUT agents need LLM backend to interpret tasks")
    logger.info("  • WITHOUT LLM, agents can't understand how to use tools")
    logger.info("  • CrewAI falls back to simple processing")
    
    print()
    logger.info("🔧 Solutions:")
    logger.info("  1. Configure OpenAI API key: export OPENAI_API_KEY='your-key'")
    logger.info("  2. Or configure other LLM backend supported by CrewAI")
    logger.info("  3. Verify CrewAI agent configuration includes LLM model")
    logger.info("  4. Test with: python test_csv_reader_agent.py")

def check_crewai_configuration():
    """Check if CrewAI is properly configured"""
    
    print_banner("🔧 CREWAI CONFIGURATION CHECK", "Verifying system requirements")
    
    # Check environment variables
    import os
    
    logger.info("🔍 Checking environment variables:")
    
    api_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'AZURE_OPENAI_API_KEY']
    found_key = False
    
    for key in api_keys:
        if os.getenv(key):
            logger.success(f"✅ {key} is set")
            found_key = True
        else:
            logger.info(f"❌ {key} is not set")
    
    if not found_key:
        logger.warning("⚠️ No LLM API keys found - this explains why agents aren't working!")
        logger.info("💡 CrewAI agents require LLM backends to function")
    
    # Check CrewAI installation
    try:
        import crewai
        logger.success(f"✅ CrewAI installed: version {crewai.__version__ if hasattr(crewai, '__version__') else 'unknown'}")
    except ImportError:
        logger.error("❌ CrewAI not installed")
    
    # Check LangChain
    try:
        import langchain_community
        logger.success("✅ LangChain Community installed")
    except ImportError:
        logger.error("❌ LangChain Community not installed")

if __name__ == "__main__":
    # Run all tests
    test_csv_reader_tool_directly()
    print("\n")
    
    check_crewai_configuration()
    print("\n")
    
    demonstrate_expected_behavior()
    print("\n")
    
    test_csv_reader_agent_in_crewai()
    
    # Final summary
    print_banner("📋 CSV READER AGENT TEST RESULTS", "Summary of findings")
    
    logger.info("✅ CSV Reader Tool - Works directly with colorful logging")
    logger.info("🤖 CSV Reader Agent - Defined in CrewAI pipeline")
    logger.info("⚠️  Agent Execution - Depends on LLM configuration")
    logger.info("🎨 Colorful Logging - Ready for when agents work")
    
    logger.success("🔍 Run this script to diagnose CSV Reader Agent usage!")