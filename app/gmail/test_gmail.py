from app.gmail.gmail_service import get_gmail_service
from app.gmail.email_parser import extract_email_body


def get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]

    return None


service = get_gmail_service()

results = service.users().messages().list(
    userId="me",
    maxResults=10
).execute()

messages = results.get("messages", [])

print(f"Found {len(messages)} emails\n")


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

    print("=" * 60)

    print("Message ID:", email["id"])
    print("From:", sender)
    print("To:", recipient)
    print("Subject:", subject)
    print("Date:", date)

    print("\nBODY:")
    print(body[:1000])