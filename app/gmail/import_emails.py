from app.gmail.gmail_service import get_gmail_service
from app.gmail.email_parser import extract_email_body
from app.models import create_user, create_email


def get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]

    return None


service = get_gmail_service()

# Get the Gmail account's email address
profile = service.users().getProfile(
    userId="me"
).execute()

user_email = profile["emailAddress"]

print("Gmail account:", user_email)

# Create the user in our database
try:
    user_id = create_user(
        email=user_email,
        provider="gmail"
    )

    print("Created user with ID:", user_id)

except Exception:
    # User may already exist
    from app.database import get_connection

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (user_email,)
    )

    user = cursor.fetchone()

    connection.close()

    if user:
        user_id = user["id"]
        print("Existing user ID:", user_id)

    else:
        raise


# Fetch Gmail messages
results = service.users().messages().list(
    userId="me",
    maxResults=10
).execute()

messages = results.get("messages", [])

print(f"Found {len(messages)} Gmail messages")


imported = 0
skipped = 0


for message in messages:

    email = service.users().messages().get(
        userId="me",
        id=message["id"],
        format="full"
    ).execute()

    headers = email["payload"].get("headers", [])

    sender = get_header(headers, "From")
    recipient = get_header(headers, "To")
    subject = get_header(headers, "Subject")
    date = get_header(headers, "Date")

    body = extract_email_body(
        email["payload"]
    )

    try:

        create_email(
            user_id=user_id,
            message_id=email["id"],
            sender=sender or "",
            recipient=recipient or "",
            subject=subject,
            body=body,
            received_at=date
        )

        imported += 1

        print(
            f"Imported: {subject}"
        )

    except Exception as error:

        if "UNIQUE constraint failed" in str(error):

            skipped += 1

            print(
                f"Skipped existing email: {email['id']}"
            )

        else:
            raise


print()
print("Import complete!")
print("Imported:", imported)
print("Skipped:", skipped)