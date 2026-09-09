from app.models import (
    create_tables,
    create_user,
    get_user,
    create_email,
    get_emails_for_user
)


create_tables()

# Create user
user_id = create_user(
    "sai@example.com",
    "gmail"
)

print("Created user:", user_id)


# Get user
user = get_user(user_id)

print("\nUSER")
print("ID:", user["id"])
print("Email:", user["email"])
print("Provider:", user["provider"])


# Create email
email_id = create_email(
    user_id=user_id,
    message_id="test-message-001",
    sender="manager@example.com",
    recipient="sai@example.com",
    subject="Project Meeting",
    body="Hi Sai, we have a project meeting tomorrow at 10 AM.",
    received_at="2026-09-09 18:00:00"
)

print("\nCreated email:", email_id)


# Retrieve emails
emails = get_emails_for_user(user_id)

print("\nEMAILS")

for email in emails:
    print("--------------------")
    print("From:", email["sender"])
    print("To:", email["recipient"])
    print("Subject:", email["subject"])
    print("Body:", email["body"])