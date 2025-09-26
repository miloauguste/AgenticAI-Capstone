#!/usr/bin/env python3
"""
Deployment readiness checker for Streamlit Community Cloud
"""

import os
import sys
from pathlib import Path

def check_deployment_readiness():
    """Check if the application is ready for deployment"""
    
    print("DEPLOYMENT READINESS CHECK")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Essential files exist
    essential_files = [
        'ui_app.py',
        'multi_agent_system.py', 
        'config_manager.py',
        'processing_logger.py',
        'requirements.txt',
        'README.md'
    ]
    
    print("\nEssential Files Check:")
    for file in essential_files:
        total_checks += 1
        if os.path.exists(file):
            print(f"PASS: {file}")
            checks_passed += 1
        else:
            print(f"FAIL: {file} - MISSING")
    
    # Check 2: Streamlit configuration
    print("\nStreamlit Configuration:")
    streamlit_config = ".streamlit/config.toml"
    total_checks += 1
    if os.path.exists(streamlit_config):
        print(f"PASS: {streamlit_config}")
        checks_passed += 1
    else:
        print(f"FAIL: {streamlit_config} - MISSING")
    
    # Check 3: Git ignore file
    print("\nGit Configuration:")
    gitignore = ".gitignore"
    total_checks += 1
    if os.path.exists(gitignore):
        print(f"PASS: {gitignore}")
        checks_passed += 1
    else:
        print(f"FAIL: {gitignore} - MISSING")
    
    # Check 4: Requirements validation
    print("\nDependencies Check:")
    total_checks += 1
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
            required_packages = ['streamlit', 'pandas', 'plotly', 'openai']
            missing_packages = []
            
            for package in required_packages:
                if package not in requirements:
                    missing_packages.append(package)
            
            if not missing_packages:
                print("PASS: All required packages in requirements.txt")
                checks_passed += 1
            else:
                print(f"FAIL: Missing packages: {missing_packages}")
    except FileNotFoundError:
        print("FAIL: requirements.txt not found")
    
    # Check 5: Sample data
    print("\nSample Data Check:")
    sample_files = ['app_store_reviews.csv', 'support_emails.csv']
    sample_found = 0
    for file in sample_files:
        if os.path.exists(file):
            sample_found += 1
            print(f"FOUND: {file}")
    
    if sample_found > 0:
        print(f"PASS: Sample data available ({sample_found}/{len(sample_files)} files)")
        total_checks += 1
        checks_passed += 1
    else:
        print("WARNING: No sample data found - users will need to upload data")
        total_checks += 1
    
    # Check 6: Application import test
    print("\nApplication Import Test:")
    total_checks += 1
    try:
        # Test if main modules can be imported
        import ui_app
        import multi_agent_system
        import config_manager
        import processing_logger
        print("PASS: All modules import successfully")
        checks_passed += 1
    except ImportError as e:
        print(f"FAIL: Import error: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Deployment Readiness: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("READY FOR DEPLOYMENT!")
        print("\nNext Steps:")
        print("1. Create GitHub repository")
        print("2. Push code to repository")
        print("3. Deploy to Streamlit Community Cloud")
        print("4. Configure secrets (API keys)")
        print("5. Test deployed application")
        return True
    else:
        print("DEPLOYMENT BLOCKED - Fix the issues above first")
        failed_checks = total_checks - checks_passed
        print(f"\n{failed_checks} issue(s) need to be resolved before deployment")
        return False

def show_deployment_commands():
    """Show git commands for deployment"""
    print("\nGit Commands for Deployment:")
    print("=" * 40)
    print("# Initialize repository")
    print("git init")
    print("git add .")
    print('git commit -m "Initial commit: Feedback Analysis System"')
    print()
    print("# Push to GitHub (replace with your repository URL)")
    print("git branch -M main") 
    print("git remote add origin https://github.com/yourusername/feedback-analysis-system.git")
    print("git push -u origin main")
    print()
    print("# After pushing, deploy on Streamlit Community Cloud:")
    print("1. Go to https://share.streamlit.io")
    print("2. Connect your GitHub repository")
    print("3. Select main branch and ui_app.py")
    print("4. Add API keys in secrets management")

if __name__ == "__main__":
    ready = check_deployment_readiness()
    
    if ready:
        show_deployment_commands()
    
    print(f"\nFull deployment guide: DEPLOYMENT_PLAN.md")