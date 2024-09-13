from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_petition_table_query() -> None:
    """
    Creates a table for storing appeals.
    """
    execute_query("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp";""")

    execute_query("""
    CREATE TABLE IF NOT EXISTS petition (
        id BIGSERIAL PRIMARY KEY,
        code uuid default uuid_generate_v4(),
        user_id BIGINT REFERENCES users(id) NOT NULL,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        money BIGINT NOT NULL,
        city_id BIGINT REFERENCES city(id) NOT NULL,
        is_winner VARCHAR(6) DEFAULT NULL,
        is_accepted VARCHAR(6) DEFAULT NULL,
        appeal_id BIGINT NOT NULL,
        category_id BIGINT NOT NULL,
        total_voices BIGINT DEFAULT 0,
        status BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    return None


def get_petition_by_id_query(petition_id: int) -> DictRow:
    """
    Gets a petition by its ID.

    Args:
    petition_id (int): The ID of the petition.

    Returns:
    DictRow: The petition details or None if the petition does not exist.
    """
    query = "SELECT * FROM petition WHERE id = %s AND status = %s;"
    return execute_query(query, (petition_id, True,), "one")


def get_petition_by_code_query(code: str) -> DictRow:
    """
    Gets a petition by its unique code.

    Args:
    code (str): The unique code of the petition.

    Returns:
    DictRow: The petition details or None if the petition does not exist.
    """
    query = "SELECT * FROM petition WHERE code = %s AND status = %s;"
    return execute_query(query, (code, True,), "one")


def get_all_petitions_by_user_id_query(user_id: int) -> list:
    """
    Gets all petitions created by a user.

    Args:
    user_id (int): The ID of the user.

    Returns:
    list: A list of petitions created by the user.
    """
    query = "SELECT * FROM petition WHERE user_id = %s AND status = %s;"
    return execute_query(query, (user_id, True,), "all")


def get_all_petitions_by_category_id_query(category_id: int) -> list:
    """
    Gets all petitions in a specific category.

    Args:
    category_id (int): The ID of the category.

    Returns:
    list: A list of petitions in the specified category.
    """
    query = "SELECT * FROM petition WHERE category_id = %s AND status = %s;"
    return execute_query(query, (category_id, True,), "all")


def get_all_accepted_petitions_by_appeal_id_query(appeal_id: int) -> list:
    """
    Gets all petitions associated with a specific appeal.

    Args:
    appeal_id (int): The ID of the appeal.

    Returns:
    list: A list of petitions associated with the appeal.
    """
    query = "SELECT * FROM petition WHERE appeal_id = %s AND is_accepted = '%s';"
    return execute_query(query, (appeal_id, True,), "all")


def get_all_rejected_petitions_by_appeal_id_query(appeal_id: int) -> list:
    """
    Gets all petitions associated with a specific appeal.

    Args:
    appeal_id (int): The ID of the appeal.

    Returns:
    list: A list of petitions associated with the appeal.
    """
    query = "SELECT * FROM petition WHERE appeal_id = %s AND is_accepted = '%s';"
    return execute_query(query, (appeal_id, False,), "all")


def get_all_petitions_by_appeal_id_query(appeal_id: int) -> list:
    """
    Gets all petitions associated with a specific appeal.

    Args:
    appeal_id (int): The ID of the appeal.

    Returns:
    list: A list of petitions associated with the appeal.
    """
    query = "SELECT * FROM petition WHERE appeal_id = %s AND status = %s;"
    return execute_query(query, (appeal_id, True), "all")


def get_all_none_petitions_by_appeal_id_query(appeal_id: int) -> list:
    """
    Gets all petitions associated with a specific appeal.

    Args:
    appeal_id (int): The ID of the appeal.

    Returns:
    list: A list of petitions associated with the appeal.
    """
    query = "SELECT * FROM petition WHERE appeal_id = %s AND status = %s AND is_accepted IS NULL;"
    return execute_query(query, (appeal_id, True), "all")


def get_all_won_petitions_by_appeal_id_query(appeal_id: int) -> list:
    """
    Gets all petitions associated with a specific appeal that have been won.

    Args:
    appeal_id (int): The ID of the appeal.

    Returns:
    list: A list of petitions associated with the appeal that have been won.
    """
    query = "SELECT * FROM petition WHERE appeal_id = %s AND is_winner = '%s';"
    return execute_query(query, (appeal_id, True), "all")


def get_all_lost_petitions_by_appeal_id_query(appeal_id: int) -> list:
    """
    Gets all petitions associated with a specific appeal that have been lost.

    Args:
    appeal_id (int): The ID of the appeal.

    Returns:
    list: A list of petitions associated with the appeal that have been won.
    """
    query = "SELECT * FROM petition WHERE appeal_id = %s AND is_winner = '%s';"
    return execute_query(query, (appeal_id, False), "all")


def get_total_voices_by_appeal_id_query(appeal_id: int) -> int:

    query = """
    SELECT SUM(total_voices) AS total_voices
    FROM petition
    WHERE appeal_id = %s
    GROUP BY title;"""
    return execute_query(query, (appeal_id,), "one")


def get_total_voices_query() -> list:
    query = """
    SELECT SUM(total_voices) AS total_voices
    FROM petition
    WHERE status = %s;
"""
    return execute_query(query, (True,), "one")


def insert_petition_query(user_id: int, title: str, content: str, city_id: int,
                          money: int, appeal_id: int, category_id: int) -> None:
    """
    Inserts a new petition into the petition table.

    Args:
    user_id (int): The ID of the user.
    title (str): The title of the petition.
    content (str): The content of the petition.
    money (int): The amount of money the petition is asking for.
    appeal_id (int): The ID of the appeal.
    category_id (int): The ID of the category.
    """
    execute_query("""
    INSERT INTO petition (user_id, title, content, money, appeal_id, category_id, city_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,(user_id, title, content, money, appeal_id, category_id, city_id))
    return None


def update_total_voices_query(petition_id: int) -> None:
    """
    Updates the total number of voices for a petition.

    Args:
    petition_id (int): The ID of the petition.
    """
    execute_query("UPDATE petition SET total_voices = total_voices + 1 WHERE id = %s;", (petition_id,))
    return None


def accept_petition_query(petition_id: int) -> None:
    """
    Accepts a petition.

    Args:
    petition_id (int): The ID of the petition.
    """
    execute_query("UPDATE petition SET is_accepted = %s WHERE id = %s;", (True, petition_id))
    return None


def reject_petition_query(petition_id: int) -> None:
    """
    Rejects a petition.

    Args:
    petition_id (int): The ID of the petition.
    """
    execute_query("UPDATE petition SET is_accepted = %s WHERE id = %s;", (False, petition_id))
    return None


def winner_petition_query(petition_id: int) -> None:
    """
    Updates the winner status of a petition.

    Args:
    petition_id (int): The ID of the petition.
    """
    execute_query("UPDATE petition SET is_winner = %s WHERE id = %s;", (True, petition_id))
    return None


def loser_petition_query(petition_id: int) -> None:
    """
    Updates the loser status of a petition.

    Args:
    petition_id (int): The ID of the petition.
    """
    execute_query("UPDATE petition SET is_winner = %s WHERE id = %s;", (False, petition_id))
    return None


def get_accepted_petitions_query(appeal_id: int) -> list:
    """
    Gets all petitions that are accepted in a specific appeal.

    Args:
    appeal_id (int): The ID of the appeal.

    Returns:
    list: A list of accepted petitions in the specified appeal.
    """
    query = "SELECT * FROM petition WHERE appeal_id = %s AND is_accepted = '%s' AND status = %s;"
    return execute_query(query, (appeal_id, True, True,), "all")


def get_winner_petitions_query(appeal_id: int) -> list:
    """
    Gets all petitions that are winners in a specific appeal.

    Args:
    appeal_id (int): The ID of the appeal.

    Returns:
    list: A list of winning petitions in the specified appeal.
    """
    query = "SELECT * FROM petition WHERE appeal_id = %s AND is_winner = '%s' AND status = %s;"
    return execute_query(query, (appeal_id, True, True,), "all")


def get_petitions_query() -> list:
    """
    Retrieves all petitions from the petition table.

    Returns:
    list: A list of petition details.
    """
    query = "SELECT * FROM petition WHERE status = %s;"
    return execute_query(query, (True,), "all")


def get_winners_query(category_id: int, limit: int):
    """
    Retrieves all winners in a specific category.

    Args:
    category_id (int): The ID of the category.

    Returns:
    list: A list of winners in the specified category.
    """
    query = """
    SELECT * FROM petition 
    WHERE category_id = %s AND status = %s
    ORDER BY total_voices DESC
    LIMIT %s;"""
    return execute_query(query, (category_id, True, limit), "all")


def get_all_accepted_petitions_by_user_id_query(user_id: int) -> list:
    """
    Gets all accepted petitions by a specific user.

    Args:
    user_id (int): The ID of the user.

    Returns:
    list: A list of accepted petitions by the user.
    """
    query = "SELECT * FROM petition WHERE user_id = %s AND is_accepted = '%s' AND status = %s;"
    return execute_query(query, (user_id, True, True,), "all")


def get_all_rejected_petitions_by_user_id_query(user_id: int) -> list:
    """
    Gets all rejected petitions by a specific user.

    Args:
    user_id (int): The ID of the user.

    Returns:
    list: A list of rejected petitions by the user.
    """
    query = "SELECT * FROM petition WHERE user_id = %s AND is_accepted = '%s' AND status = %s;"
    return execute_query(query, (user_id, False, True,), "all")


def get_all_won_petitions_by_user_id_query(user_id: int) -> list:
    """
    Gets all won petitions by a specific user.

    Args:
    user_id (int): The ID of the user.

    Returns:
    list: A list of won petitions by the user.
    """
    query = "SELECT * FROM petition WHERE user_id = %s AND is_winner = '%s' AND status = %s;"
    return execute_query(query, (user_id, True, True,), "all")


def get_all_lost_petitions_by_user_id_query(user_id: int) -> list:
    """
    Gets all lost petitions by a specific user.

    Args:
    user_id (int): The ID of the user.

    Returns:
    list: A list of lost petitions by the user.
    """
    query = "SELECT * FROM petition WHERE user_id = %s AND is_winner = '%s' AND status = %s;"
    return execute_query(query, (user_id, False, True,), "all")


def get_pending_petition_by_user_id_query(user_id: int) -> DictRow:
    """
    Gets a pending petition by a specific user.

    Args:
    user_id (int): The ID of the user.

    Returns:
    dict: A dictionary containing the pending petition details.
    """
    query = "SELECT * FROM petition WHERE user_id = %s AND is_accepted IS NULL;"
    return execute_query(query, (user_id,), "one")


def get_total_voices_by_user_id_query(user_id: int) -> DictRow:
    """
    Gets the total number of voices for all petitions by a specific user.

    Args:
    user_id (int): The ID of the user.

    Returns:
    list: A list of dictionaries containing the total voices for each petition by the user.
    """
    query = """
    SELECT SUM(total_voices) AS total_voices
    FROM petition
    WHERE user_id = %s AND status = %s;"""
    return execute_query(query, (user_id, True), "one")


def get_all_petitions_query() -> list:
    """
    Retrieves all petitions from the petition table.

    Returns:
    list: A list of petition details.
    """
    query = "SELECT * FROM petition WHERE status = %s;"
    return execute_query(query, (True,), "all")
