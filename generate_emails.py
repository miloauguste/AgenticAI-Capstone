import csv
import datetime
import random

def generate_support_emails(num_emails=100):
    """Generates a CSV file with support emails."""

    with open('support_emails.csv', 'w', newline='') as csvfile:
        fieldnames = ['email_id', 'subject', 'body', 'sender_email', 'timestamp', 'priority']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for i in range(num_emails):
            subject = f"App Crash Report {i+1}"
            body = f"Dear Support Team,\n\nThis is a report regarding issue # {i+1}.  The application is crashing when attempting to [Describe the crash - be specific].  We suspect [Possible Cause - e.g., memory leak] is the root of the problem.  Please investigate and provide a fix. Thank you,\n[Your Name]"
            sender_email = f"support@example.com"  # Replace with actual sender email
            timestamp = datetime.datetime.now().isoformat()
            priority = random.choice(["High", "Medium", "Low"])

            writer.writerow({
                'email_id': i + 1,
                'subject': subject,
                'body': body,
                'sender_email': sender_email,
                'timestamp': timestamp,
                'priority': priority
            })

    print("Successfully generated support_emails.csv")

if __name__ == "__main__":
    generate_support_emails()
