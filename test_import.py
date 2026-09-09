from app.models import get_emails_for_user


USER_ID = 4

emails = get_emails_for_user(USER_ID)

print(f"Total emails: {len(emails)}")

for email in emails:
    print("=" * 60)

    print("Database ID:", email["id"])
    print("Message ID:", email["message_id"])
    print("From:", email["sender"])
    print("To:", email["recipient"])
    print("Subject:", email["subject"])
    print("Received:", email["received_at"])

    print("\nBody:")
    print(email["body"][:500])