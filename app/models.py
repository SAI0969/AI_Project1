from app.database import get_connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            provider TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message_id TEXT NOT NULL UNIQUE,
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            subject TEXT,
            body TEXT,
            received_at TIMESTAMP,
            is_read INTEGER DEFAULT 0,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
    """)

def create_user(email, provider):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (email, provider)
        VALUES (?, ?)
        """,
        (email, provider)
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id

def get_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    return user


def create_email(
    user_id,
    message_id,
    sender,
    recipient,
    subject,
    body,
    received_at
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO emails (
            user_id,
            message_id,
            sender,
            recipient,
            subject,
            body,
            received_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            message_id,
            sender,
            recipient,
            subject,
            body,
            received_at
        )
    )

    connection.commit()

    email_id = cursor.lastrowid

    connection.close()

    return email_id


def get_emails_for_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM emails
        WHERE user_id = ?
        ORDER BY received_at DESC
        """,
        (user_id,)
    )

    emails = cursor.fetchall()

    connection.close()

    return emails    

