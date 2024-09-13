from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_email_table_query() -> None:
    """
    Creates a table for storing emails.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS email (
        id BIGSERIAL PRIMARY KEY,
        email VARCHAR(64) NOT NULL UNIQUE,
        status BOOLEAN DEFAULT TRUE
    )
    """)
    return None


def get_email_by_id_query(email_id: int) -> DictRow:
    """
    Gets an email by its ID.

    Args:
    email_id (int): The ID of the email.

    Returns:
    DictRow: The email details or None if the email does not exist.
    """
    query = "SELECT * FROM email WHERE id = %s AND status = %s;"
    return execute_query(query, (email_id, True), "one")


def get_email_by_email_query(email_address: str) -> DictRow:
    """
    Gets an email by its email address.

    Args:
    email_address (str): The email address.

    Returns:
    DictRow: The email details or None if the email does not exist.
    """
    query = "SELECT * FROM email WHERE email = %s AND status = %s;"
    return execute_query(query, (email_address, True), "one")


def insert_email_query(email_address) -> None:
    """
    Inserts a new email into the email table.

    Args:
    email_address (str): The email address.
    """
    execute_query("INSERT INTO email (email) VALUES (%s)", (email_address,))
    return None


def get_all_emails_query() -> list:
    """
    Retrieves all emails from the email table.

    Returns:
    list: A list of email details.
    """
    query = "SELECT * FROM email WHERE status = %s;"
    return execute_query(query, (True,), "all")
