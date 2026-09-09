import base64


def decode_body(data):
    if not data:
        return ""

    try:
        decoded_bytes = base64.urlsafe_b64decode(data)
        return decoded_bytes.decode("utf-8", errors="replace")
    except Exception:
        return ""


def extract_email_body(payload):
    """
    Extract the best available body from a Gmail message.

    Priority:
    1. text/plain
    2. text/html
    3. recursively search nested MIME parts
    """

    mime_type = payload.get("mimeType", "")
    body = payload.get("body", {})

    # Direct text/plain body
    if mime_type == "text/plain":
        text = decode_body(body.get("data"))

        if text.strip():
            return text

    # Direct text/html body
    if mime_type == "text/html":
        html = decode_body(body.get("data"))

        if html.strip():
            return html

    # Check MIME parts
    parts = payload.get("parts", [])

    # First preference: text/plain
    for part in parts:
        if part.get("mimeType") == "text/plain":
            text = decode_body(
                part.get("body", {}).get("data")
            )

            if text.strip():
                return text

    # Second preference: text/html
    for part in parts:
        if part.get("mimeType") == "text/html":
            html = decode_body(
                part.get("body", {}).get("data")
            )

            if html.strip():
                return html

    # Search nested MIME parts
    for part in parts:
        if part.get("parts"):
            result = extract_email_body(part)

            if result.strip():
                return result

    return ""