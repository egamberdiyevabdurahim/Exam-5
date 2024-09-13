from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_phone_number_table_query() -> None:
    """
    Creates a table for storing emails.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS phone_number (
        id BIGSERIAL PRIMARY KEY,
        phone_number VARCHAR(64) NOT NULL UNIQUE,
        status BOOLEAN DEFAULT TRUE
    )
    """)
    return None


def get_phone_number_by_id_query(phone_number_id: int) -> DictRow:
    """
    Gets a phone_number by its ID.

    Args:
    phone_number_id (int): The ID of the phone_number.

    Returns:
    DictRow: The phone_number details or None if the phone_number does not exist.
    """
    query = "SELECT * FROM phone_number WHERE id = %s AND status = %s;"
    return execute_query(query, (phone_number_id, True), "one")


def get_phone_number_by_phone_number_query(phone_number: str) -> DictRow:
    """
    Gets a phone_number by its phone_number.

    Args:
    phone_number (str): The phone_number.

    Returns:
    DictRow: The phone_number details or None if the phone_number does not exist.
    """
    query = "SELECT * FROM phone_number WHERE phone_number = %s AND status = %s;"
    return execute_query(query, (phone_number, True), "one")


def insert_phone_number_query(phone_number) -> None:
    """
    Inserts a new phone_number into the phone_number table.

    Args:
    phone_number (str): The phone_number.
    """
    execute_query("INSERT INTO phone_number (phone_number) VALUES (%s)", (phone_number,))
    return None


def get_all_phone_numbers_query() -> list:
    """
    Retrieves all phone_numbers from the phone_number table.

    Returns:
    list: A list of phone_number details.
    """
    query = "SELECT * FROM phone_number WHERE status = %s;"
    return execute_query(query, (True,), "all")
