from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_confirmation_codes_table_query() -> None:
    """
    Creates a table for storing confirmation codes.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS confirmation_codes (
        id BIGSERIAL PRIMARY KEY,
        code VARCHAR(10) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );
    """)
    return None


def insert_confirmation_code_query(code: str) -> None:
    """
    Inserts a new confirmation code into the confirmation_codes table.
    """
    execute_query("INSERT INTO confirmation_codes (code) VALUES (%s)", (code,))
    return None


def get_confirmation_code_by_code_query(code: str) -> DictRow:
    """
    Gets a confirmation code by its code.

    Args:
    code (str): The confirmation code to search for.

    Returns:
    DictRow: The confirmation code details or None if the code does not exist.
    """
    query = "SELECT * FROM confirmation_codes WHERE code = %s;"
    return execute_query(query, (code,), "one")
