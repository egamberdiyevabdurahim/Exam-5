from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_users_table_query() -> None:
    """
    Creates a table for storing users.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS users (
        id BIGSERIAL PRIMARY KEY,
        first_name VARCHAR(64) NOT NULL,
        last_name VARCHAR(64) NOT NULL,
        email_id BIGINT NOT NULL,
        phone_number_id BIGINT NOT NULL,
        password VARCHAR(64) NOT NULL,
        status BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    return None


def get_user_by_id_query(user_id: int) -> DictRow:
    """
    Gets a user by its ID.

    Args:
    user_id (int): The ID of the user.

    Returns:
    DictRow: The user details or None if the user does not exist.
    """
    query = "SELECT * FROM users WHERE id = %s AND status = %s;"
    return execute_query(query, (user_id, True), "one")


def get_user_by_email_id_query(email_id: int) -> DictRow:
    """
    Gets a user by its email ID.

    Args:
    email_id (int): The email ID of the user.

    Returns:
    DictRow: The user details or None if the user does not exist.
    """
    query = "SELECT * FROM users WHERE email_id = %s AND status = %s;"
    return execute_query(query, (email_id, True), "one")


def get_user_by_phone_number_id_query(phone_number_id: int) -> DictRow:
    """
    Gets a user by its phone number ID.

    Args:
    phone_number_id (int): The phone number ID of the user.

    Returns:
    DictRow: The user details or None if the user does not exist.
    """
    query = "SELECT * FROM users WHERE phone_number_id = %s AND status = %s;"
    return execute_query(query, (phone_number_id, True), "one")


def insert_user_query(first_name: str, last_name: str, email_id: int, phone_number_id: int, password: str) -> None:
    """
    Inserts a new user into the users table.

    Args:
    first_name (str): The first name of the user.
    last_name (str): The last name of the user.
    email_id (int): The email ID of the user.
    phone_number_id (int): The phone number ID of the user.
    password (str): The password of the user.
    """
    execute_query(
        "INSERT INTO users (first_name, last_name, email_id, phone_number_id, password) VALUES (%s, %s, %s, %s, %s)",
        (first_name, last_name, email_id, phone_number_id, password)
    )
    return None


def update_user_query(user_id: int, first_name: str, last_name: str, password: str) -> None:
    """
    Updates the details of a user.

    Args:
    user_id (int): The ID of the user.
    first_name (str): The new first name of the user.
    last_name (str): The new last name of the user.
    password (str): The new password of the user.
    """
    execute_query(
        """UPDATE users SET first_name = %s, last_name = %s, password = %s, 
        updated_at = CURRENT_TIMESTAMP WHERE id = %s;""",
        (first_name, last_name, password, user_id)
    )
    return None


def delete_user_query(user_id: int) -> None:
    """
    Deletes a user from the users table.

    Args:
    user_id (int): The ID of the user.
    """
    execute_query("UPDATE users SET status = %s WHERE id = %s;", (False, user_id))
    return None


def get_all_users_query() -> list:
    """
    Gets all users.

    Returns:
    list: A list of user details.
    """
    return execute_query("SELECT * FROM users WHERE status = %s;", (True,), "all")
