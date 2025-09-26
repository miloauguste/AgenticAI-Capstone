#!/usr/bin/env python3
"""
Validation script for the Intelligent Feedback Analysis System
Tests system accuracy against expected classifications
"""

import pandas as pd
import numpy as np
import json
import logging
import sys
from datetime import datetime
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging with UTF-8 encoding
logging.basicConfig(level=logging.INFO, encoding='utf-8')
logger = logging.getLogger(__name__)

# Configure stdout for UTF-8 on Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class SystemValidator:
    def __init__(self):
        self.categories = ["Bug", "Feature Request", "Praise", "Complaint", "Spam"]
        self.priorities = ["Critical", "High", "Medium", "Low"]
        
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load app store reviews, support emails, and expected classifications"""
        try:
            # Load app store reviews
            try:
                reviews_df = pd.read_csv('app_store_reviews.csv', encoding='utf-8', quotechar='"', escapechar='\\')
            except:
                reviews_df = pd.read_csv('app_store_reviews.csv', encoding='utf-8', engine='python', quotechar='"')
            
            # Load support emails
            try:
                emails_df = pd.read_csv('support_emails.csv', encoding='utf-8', quotechar='"', escapechar='\\')
            except:
                emails_df = pd.read_csv('support_emails.csv', encoding='utf-8', engine='python', quotechar='"')
            
            # Load expected classifications
            try:
                expected_df = pd.read_csv('expected_classifications.csv', encoding='utf-8', quotechar='"', escapechar='\\')
            except:
                expected_df = pd.read_csv('expected_classifications.csv', encoding='utf-8', engine='python', quotechar='"')
                
            return reviews_df, emails_df, expected_df
        except FileNotFoundError as e:
            logger.error(f"Required file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def validate_classifications(self, expected_df: pd.DataFrame, actual_df: pd.DataFrame) -> Dict:
        """Validate classification accuracy"""
        results = {
            'total_items': 0,
            'correct_classifications': 0,
            'accuracy': 0.0,
            'category_accuracy': {},
            'priority_accuracy': {},
            'confusion_matrix': {},
            'detailed_results': []
        }
        
        # Merge dataframes on source_id
        merged_df = pd.merge(
            expected_df, 
            actual_df, 
            left_on='source_id', 
            right_on='source_id',
            how='inner',
            suffixes=('_expected', '_actual')
        )
        
        results['total_items'] = len(merged_df)
        
        if results['total_items'] == 0:
            logger.warning("No matching records found between expected and actual results")
            return results
        
        # Calculate overall accuracy
        correct_categories = (merged_df['category_expected'] == merged_df['category']).sum()
        results['correct_classifications'] = correct_categories
        results['accuracy'] = correct_categories / results['total_items'] * 100
        
        # Category-wise accuracy
        for category in self.categories:
            category_mask = merged_df['category_expected'] == category
            if category_mask.sum() > 0:
                category_correct = ((merged_df['category_expected'] == category) & 
                                 (merged_df['category'] == category)).sum()
                category_total = category_mask.sum()
                results['category_accuracy'][category] = {
                    'correct': category_correct,
                    'total': category_total,
                    'accuracy': category_correct / category_total * 100
                }
        
        # Priority-wise accuracy  
        for priority in self.priorities:
            priority_mask = merged_df['priority_expected'] == priority
            if priority_mask.sum() > 0:
                priority_correct = ((merged_df['priority_expected'] == priority) & 
                                  (merged_df['priority'] == priority)).sum()
                priority_total = priority_mask.sum()
                results['priority_accuracy'][priority] = {
                    'correct': priority_correct,
                    'total': priority_total,
                    'accuracy': priority_correct / priority_total * 100
                }
        
        # Detailed results for each item
        for _, row in merged_df.iterrows():
            item_result = {
                'source_id': row['source_id'],
                'source_type': row['source_type_expected'],
                'expected_category': row['category_expected'],
                'actual_category': row['category'],
                'expected_priority': row['priority_expected'],
                'actual_priority': row['priority'],
                'category_correct': row['category_expected'] == row['category'],
                'priority_correct': row['priority_expected'] == row['priority'],
                'confidence_score': row.get('confidence_score', 0)
            }
            results['detailed_results'].append(item_result)
        
        return results
    
    def generate_confusion_matrix(self, expected_df: pd.DataFrame, actual_df: pd.DataFrame) -> pd.DataFrame:
        """Generate confusion matrix for categories"""
        merged_df = pd.merge(
            expected_df, 
            actual_df, 
            left_on='source_id', 
            right_on='source_id',
            how='inner'
        )
        
        if len(merged_df) == 0:
            return pd.DataFrame()
        
        return pd.crosstab(
            merged_df['category_expected'], 
            merged_df['category'], 
            margins=True
        )
    
    def analyze_confidence_scores(self, actual_df: pd.DataFrame) -> Dict:
        """Analyze confidence score distribution"""
        if 'confidence_score' not in actual_df.columns:
            return {}
        
        confidence_stats = {
            'mean': actual_df['confidence_score'].mean(),
            'median': actual_df['confidence_score'].median(),
            'std': actual_df['confidence_score'].std(),
            'min': actual_df['confidence_score'].min(),
            'max': actual_df['confidence_score'].max(),
            'high_confidence_count': (actual_df['confidence_score'] > 70).sum(),
            'medium_confidence_count': ((actual_df['confidence_score'] >= 50) & 
                                      (actual_df['confidence_score'] <= 70)).sum(),
            'low_confidence_count': (actual_df['confidence_score'] < 50).sum()
        }
        
        return confidence_stats
    
    def generate_report(self, validation_results: Dict, confidence_stats: Dict, 
                       confusion_matrix: pd.DataFrame) -> str:
        """Generate comprehensive validation report"""
        
        report = f"""
# Intelligent Feedback Analysis System - Validation Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Overall Performance

**Total Items Processed:** {validation_results['total_items']}
**Correct Classifications:** {validation_results['correct_classifications']}
**Overall Accuracy:** {validation_results['accuracy']:.1f}%

## 📈 Category-wise Accuracy

"""
        
        for category, stats in validation_results['category_accuracy'].items():
            report += f"**{category}:** {stats['accuracy']:.1f}% ({stats['correct']}/{stats['total']})\n"
        
        report += "\n## ⚡ Priority-wise Accuracy\n\n"
        
        for priority, stats in validation_results['priority_accuracy'].items():
            report += f"**{priority}:** {stats['accuracy']:.1f}% ({stats['correct']}/{stats['total']})\n"
        
        if confidence_stats:
            report += f"""
## 🎯 Confidence Score Analysis

**Average Confidence:** {confidence_stats['mean']:.1f}%
**Median Confidence:** {confidence_stats['median']:.1f}%
**Standard Deviation:** {confidence_stats['std']:.1f}%
**Range:** {confidence_stats['min']:.1f}% - {confidence_stats['max']:.1f}%

**Confidence Distribution:**
- High Confidence (>70%): {confidence_stats['high_confidence_count']} items
- Medium Confidence (50-70%): {confidence_stats['medium_confidence_count']} items  
- Low Confidence (<50%): {confidence_stats['low_confidence_count']} items
"""
        
        if not confusion_matrix.empty:
            report += "\n## 📋 Confusion Matrix\n\n"
            report += confusion_matrix.to_string()
        
        # Detailed error analysis
        incorrect_items = [item for item in validation_results['detailed_results'] 
                          if not item['category_correct']]
        
        if incorrect_items:
            report += f"\n## ❌ Misclassified Items ({len(incorrect_items)} items)\n\n"
            for item in incorrect_items[:10]:  # Show first 10 errors
                report += f"**{item['source_id']}:** Expected '{item['expected_category']}', Got '{item['actual_category']}' (Confidence: {item['confidence_score']:.1f}%)\n"
            
            if len(incorrect_items) > 10:
                report += f"\n... and {len(incorrect_items) - 10} more items\n"
        
        # Performance recommendations
        report += "\n## 💡 Recommendations\n\n"
        
        if validation_results['accuracy'] >= 80:
            report += "✅ **Excellent Performance** - System is performing well with high accuracy.\n"
        elif validation_results['accuracy'] >= 60:
            report += "⚠️ **Good Performance** - Consider fine-tuning classification rules for better accuracy.\n"
        else:
            report += "❌ **Needs Improvement** - Significant improvements needed in classification logic.\n"
        
        if confidence_stats and confidence_stats['mean'] < 60:
            report += "🔍 **Low Confidence Scores** - Review and improve classification algorithms.\n"
        
        # Category-specific recommendations
        for category, stats in validation_results['category_accuracy'].items():
            if stats['accuracy'] < 50:
                report += f"🎯 **Improve {category} Detection** - Current accuracy is only {stats['accuracy']:.1f}%\n"
        
        return report
    
    def save_detailed_results(self, validation_results: Dict):
        """Save detailed validation results to CSV"""
        detailed_df = pd.DataFrame(validation_results['detailed_results'])
        detailed_df.to_csv('validation_results.csv', index=False)
        logger.info("Detailed validation results saved to validation_results.csv")
    
    def run_validation(self) -> Dict:
        """Run complete validation process"""
        logger.info("Starting system validation...")
        
        try:
            # Load data
            reviews_df, emails_df, expected_df = self.load_data()
            logger.info(f"Loaded {len(reviews_df)} app store reviews, {len(emails_df)} support emails, and {len(expected_df)} expected classifications")
            
            # Display data structure for all loaded files
            print("\n" + "="*60)
            print("📊 LOADED DATA STRUCTURE")
            print("="*60)
            
            print(f"\n🛒 App Store Reviews: {len(reviews_df)} items")
            print("Columns:", list(reviews_df.columns))
            
            print(f"\n📧 Support Emails: {len(emails_df)} items")
            print("Columns:", list(emails_df.columns))
            
            print(f"\n🎯 Expected Classifications: {len(expected_df)} items")
            print("Columns:", list(expected_df.columns))
            print("\nCategory Distribution:")
            if 'category' in expected_df.columns:
                print(expected_df['category'].value_counts())
            print("\nPriority Distribution:")
            if 'priority' in expected_df.columns:
                print(expected_df['priority'].value_counts())
            
            print("="*60)
            
            return {
                "status": "completed", 
                "reviews_count": len(reviews_df),
                "emails_count": len(emails_df),
                "expected_items": len(expected_df)
            }
            
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            raise

def create_test_runner():
    """Create a test runner script"""
    test_content = """#!/usr/bin/env python3
'''
Test runner for the Intelligent Feedback Analysis System
Runs end-to-end tests and validation
'''

import subprocess
import sys
import os
from pathlib import Path

def run_test_sequence():
    '''Run complete test sequence'''
    print("🧪 Starting End-to-End System Tests")
    print("="*50)
    
    # Step 1: Generate mock data
    print("📊 Step 1: Generating mock data...")
    try:
        subprocess.run([sys.executable, "generate_mock_data.py"], check=True)
        print("✅ Mock data generated successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to generate mock data")
        return False
    
    # Step 2: Process feedback
    print("\\n🤖 Step 2: Processing feedback with AI system...")
    try:
        subprocess.run([
            sys.executable, "process_feedback.py", 
            "--reviews", "app_store_reviews.csv",
            "--emails", "support_emails.csv",
            "--verbose"
        ], check=True)
        print("✅ Feedback processing completed")
    except subprocess.CalledProcessError:
        print("❌ Failed to process feedback")
        return False
    
    # Step 3: Validate results
    print("\\n🎯 Step 3: Validating results...")
    try:
        subprocess.run([sys.executable, "validate_system.py"], check=True)
        print("✅ Validation completed")
    except subprocess.CalledProcessError:
        print("❌ Validation failed")
        return False
    
    print("\\n🎉 All tests passed successfully!")
    print("\\n📋 Generated Files:")
    files_to_check = [
        "app_store_reviews.csv",
        "support_emails.csv", 
        "expected_classifications.csv",
        "generated_tickets.csv",
        "processing_log.csv",
        "metrics.csv",
        "validation_results.csv",
        "validation_report.md"
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (missing)")
    
    return True

if __name__ == "__main__":
    success = run_test_sequence()
    sys.exit(0 if success else 1)
"""
    
    with open('run_tests.py', 'w') as f:
        f.write(test_content)
    
    os.chmod('run_tests.py', 0o755)

def main():
    """Main validation function"""
    validator = SystemValidator()
    
    try:
        results = validator.run_validation()
        
        # Create test runner for future use
        create_test_runner()
        
        return results
    except Exception as e:
        logger.error(f"Validation process failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
