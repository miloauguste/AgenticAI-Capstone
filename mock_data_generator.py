import csv
import random
from datetime import datetime, timedelta

def create_mock_data():
    """Generate mock CSV files for the feedback analysis system"""
    
    # Sample data for app store reviews
    app_store_data = [
        # Bug examples
        ("REV001", "Google Play", 1, "App crashes when I try to sync my data. Happens every time after the latest update.", "user123", "2024-01-15", "2.1.3"),
        ("REV002", "App Store", 2, "Can't login since update. Keeps saying invalid credentials but I know they're correct.", "appuser456", "2024-01-14", "2.1.3"),
        ("REV003", "Google Play", 1, "Data sync not working properly. Lost all my important notes yesterday.", "productivityfan", "2024-01-13", "2.1.2"),
        ("REV004", "App Store", 2, "App freezes constantly on iPhone 14. Makes it unusable.", "iphoneuser789", "2024-01-12", "2.1.3"),
        
        # Feature requests
        ("REV005", "Google Play", 4, "Please add dark mode! My eyes hurt using this at night.", "nightowl22", "2024-01-11", "2.1.2"),
        ("REV006", "App Store", 3, "Would love to see calendar integration. That would make this perfect.", "busyexec", "2024-01-10", "2.1.1"),
        ("REV007", "Google Play", 4, "Missing functionality for bulk operations. Please consider adding this.", "poweruser99", "2024-01-09", "2.1.2"),
        ("REV008", "App Store", 3, "Please add export to PDF feature. Really need this for work.", "consultant123", "2024-01-08", "2.1.1"),
        
        # Praise
        ("REV009", "Google Play", 5, "Amazing app! Works perfectly and saves me so much time.", "happyuser", "2024-01-07", "2.1.2"),
        ("REV010", "App Store", 5, "Love the new feature in the latest update. Great work developers!", "satisfied_customer", "2024-01-06", "2.1.3"),
        ("REV011", "Google Play", 5, "Best productivity app I've ever used. Highly recommended!", "productivity_guru", "2024-01-05", "2.1.1"),
        ("REV012", "App Store", 4, "Really solid app. Does exactly what it promises.", "honest_reviewer", "2024-01-04", "2.1.2"),
        
        # Complaints
        ("REV013", "Google Play", 2, "Too expensive for what it offers. Should have more features for this price.", "budget_conscious", "2024-01-03", "2.1.1"),
        ("REV014", "App Store", 2, "Poor customer service. Sent multiple emails but no response.", "frustrated_user", "2024-01-02", "2.1.2"),
        ("REV015", "Google Play", 2, "App is slow and laggy. Takes forever to load anything.", "impatient_user", "2024-01-01", "2.1.1"),
        
        # Spam
        ("REV016", "Google Play", 5, "Click here for amazing deals!!! www.spam-site.com", "spammer1", "2023-12-31", "2.0.9"),
        ("REV017", "App Store", 1, "asdfkjasldkfjasldkfj random text here", "random_user", "2023-12-30", "2.0.8"),
        ("REV018", "Google Play", 5, "Make money fast! Contact us now for exclusive offers!", "money_maker", "2023-12-29", "2.0.7"),
    ]
    
    # Create app_store_reviews.csv
    with open('app_store_reviews.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['review_id', 'platform', 'rating', 'review_text', 'user_name', 'date', 'app_version'])
        writer.writerows(app_store_data)
    
    # Sample data for support emails
    support_email_data = [
        # Bug reports
        ("EMAIL001", "App Crash Report", "Hi, I'm experiencing crashes on my Samsung Galaxy S21 running Android 13. The app crashes whenever I try to export data. Steps to reproduce: 1. Open app 2. Go to export section 3. Select any format 4. App crashes. Please help!", "user1@email.com", "2024-01-15 09:30:00", "High"),
        ("EMAIL002", "Login Issue", "Dear Support Team, I cannot login to my account since yesterday. I'm using version 2.1.3 on iOS 16.2. Error message: 'Authentication failed'. I've tried resetting password but still can't access my account.", "user2@email.com", "2024-01-14 14:15:00", "Medium"),
        ("EMAIL003", "Data Loss Problem", "URGENT: All my data has disappeared after the latest update. I had 6 months of important work data. Device: iPad Pro 12.9, iOS 16.1, App version 2.1.3. This is critical for my business!", "business_user@company.com", "2024-01-13 11:45:00", "Critical"),
        
        # Feature requests
        ("EMAIL004", "Feature Request: Dark Mode", "Hello, I really love your app but would appreciate a dark mode option. I use the app frequently at night and the bright interface strains my eyes. Many users would benefit from this feature. Thanks for considering!", "night_user@email.com", "2024-01-12 20:30:00", "Low"),
        ("EMAIL005", "Suggestion for Improvement", "Dear Team, Your app is great but could benefit from better calendar integration. Currently, I have to manually sync events. Native calendar integration would save significant time. Best regards, John", "john.doe@email.com", "2024-01-11 16:20:00", "Medium"),
        
        # General complaints
        ("EMAIL006", "Performance Issues", "The app has become very slow since the last update. Takes 10+ seconds to load on my iPhone 12 Pro. Previous version was much faster. Please optimize performance.", "speed_user@email.com", "2024-01-10 12:00:00", ""),
        ("EMAIL007", "Subscription Inquiry", "Hi, I'm having trouble with my subscription. I was charged twice this month but only have one active subscription. Can someone please look into this billing issue?", "subscriber@email.com", "2024-01-09 08:30:00", "High"),
        
        # Mixed technical issues
        ("EMAIL008", "Sync Problems", "Data synchronization between my devices isn't working properly. Changes made on my phone don't appear on my tablet. Both devices are running the latest version. Device info: iPhone 13 (iOS 16.2) and iPad Air (iOS 16.1).", "multi_device@email.com", "2024-01-08 13:45:00", "Medium"),
    ]
    
    # Create support_emails.csv
    with open('support_emails.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['email_id', 'subject', 'body', 'sender_email', 'timestamp', 'priority'])
        writer.writerows(support_email_data)
    
    # Expected classifications for validation
    expected_data = [
        # App store reviews
        ("REV001", "app_store_review", "Bug", "High", "Samsung device, sync crashes, version 2.1.3", "Fix: App crashes during data sync"),
        ("REV002", "app_store_review", "Bug", "High", "Login failure, credential validation issue", "Fix: Login authentication failure"),
        ("REV003", "app_store_review", "Bug", "Critical", "Data loss, sync malfunction", "Fix: Data sync causing data loss"),
        ("REV004", "app_store_review", "Bug", "High", "iPhone 14 freezing, app stability", "Fix: App freezing on iPhone 14"),
        ("REV005", "app_store_review", "Feature Request", "Medium", "Dark mode request, UI improvement", "Feature: Add dark mode option"),
        ("REV006", "app_store_review", "Feature Request", "Medium", "Calendar integration request", "Feature: Integrate with calendar apps"),
        ("REV007", "app_store_review", "Feature Request", "Low", "Bulk operations functionality", "Feature: Add bulk operations"),
        ("REV008", "app_store_review", "Feature Request", "Medium", "PDF export capability", "Feature: Add PDF export"),
        ("REV009", "app_store_review", "Praise", "Low", "Positive feedback, satisfied user", "Positive feedback received"),
        ("REV010", "app_store_review", "Praise", "Low", "Feature appreciation", "Positive feedback on new feature"),
        ("REV011", "app_store_review", "Praise", "Low", "App recommendation", "User recommends app"),
        ("REV012", "app_store_review", "Praise", "Low", "Satisfaction confirmation", "User satisfaction confirmed"),
        ("REV013", "app_store_review", "Complaint", "Low", "Pricing concerns", "Review: Pricing feedback"),
        ("REV014", "app_store_review", "Complaint", "Medium", "Customer service response", "Improve: Customer service response time"),
        ("REV015", "app_store_review", "Complaint", "Medium", "Performance issues", "Improve: App performance optimization"),
        ("REV016", "app_store_review", "Spam", "Low", "Promotional content, irrelevant", "Spam: Remove promotional content"),
        ("REV017", "app_store_review", "Spam", "Low", "Random text, no content", "Spam: Random text content"),
        ("REV018", "app_store_review", "Spam", "Low", "Money-making spam", "Spam: Financial spam content"),
        
        # Support emails
        ("EMAIL001", "support_email", "Bug", "High", "Samsung Galaxy S21, Android 13, export crashes", "Fix: Export functionality crash on Android"),
        ("EMAIL002", "support_email", "Bug", "Medium", "iOS login authentication failure", "Fix: iOS authentication system"),
        ("EMAIL003", "support_email", "Bug", "Critical", "Data loss after update, iPad Pro", "Fix: Data loss in version 2.1.3"),
        ("EMAIL004", "support_email", "Feature Request", "Low", "Dark mode for night usage", "Feature: Implement dark mode"),
        ("EMAIL005", "support_email", "Feature Request", "Medium", "Native calendar integration", "Feature: Calendar integration"),
        ("EMAIL006", "support_email", "Bug", "Medium", "Performance degradation, iPhone 12 Pro", "Fix: Performance optimization needed"),
        ("EMAIL007", "support_email", "Complaint", "High", "Billing issue, double charge", "Billing: Investigate double charging"),
        ("EMAIL008", "support_email", "Bug", "Medium", "Cross-device sync failure", "Fix: Device synchronization issues"),
    ]
    
    # Create expected_classifications.csv
    with open('expected_classifications.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['source_id', 'source_type', 'category', 'priority', 'technical_details', 'suggested_title'])
        writer.writerows(expected_data)
    
    print("Mock data files created successfully!")
    print("Files created:")
    print("- app_store_reviews.csv (18 reviews)")
    print("- support_emails.csv (8 emails)")
    print("- expected_classifications.csv (26 expected classifications)")

if __name__ == "__main__":
    create_mock_data()
