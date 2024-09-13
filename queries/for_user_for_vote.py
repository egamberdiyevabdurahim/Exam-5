from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_user_for_vote_table_query() -> None:
    """
    Creates a table for storing user votes for a specific poll.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS user_for_vote (
        id BIGSERIAL PRIMARY KEY,
        email_id BIGINT REFERENCES email(id) NOT NULL,
        phone_number_id BIGINT REFERENCES phone_number(id) NOT NULL,
        status BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    return None


def get_user_for_vote_by_id_query(user_for_vote_id: int) -> DictRow:
    """
    Gets a user for vote by its ID.

    Args:
    user_for_vote_id (int): The ID of the user for vote.

    Returns:
    DictRow: The user for vote details or None if the user for vote does not exist.
    """
    query = "SELECT * FROM user_for_vote WHERE id = %s AND status = %s;"
    return execute_query(query, (user_for_vote_id, True), "one")


def get_user_for_vote_by_email_id_query(email_id: int) -> DictRow:
    """
    Gets a user for vote by its email ID.

    Args:
    email_id (int): The email ID of the user for vote.

    Returns:
    DictRow: The user for vote details or None if the user for vote does not exist.
    """
    query = "SELECT * FROM user_for_vote WHERE email_id = %s AND status = %s;"
    return execute_query(query, (email_id, True), "one")


def get_user_for_vote_by_phone_number_id_query(phone_number_id: int) -> DictRow:
    """
    Gets a user for vote by its phone number ID.

    Args:
    phone_number_id (int): The phone number ID of the user for vote.

    Returns:
    DictRow: The user for vote details or None if the user for vote does not exist.
    """
    query = "SELECT * FROM user_for_vote WHERE phone_number_id = %s AND status = %s;"
    return execute_query(query, (phone_number_id, True), "one")


def insert_user_for_vote_query(email_id: int, phone_number_id: int) -> None:
    """
    Inserts a new user for vote into the user_for_vote table.

    Args:
    email_id (int): The email ID of the user for vote.
    phone_number_id (int): The phone number ID of the user for vote.
    """
    execute_query("INSERT INTO user_for_vote (email_id, phone_number_id) VALUES (%s, %s)", (email_id, phone_number_id))
    return None


def get_all_user_for_votes_query() -> list:
    """
    Retrieves all user for votes from the user_for_vote table.

    Returns:
    list: A list of user for vote details.
    """
    query = "SELECT * FROM user_for_vote WHERE status = %s;"
    return execute_query(query, (True,), "all")
