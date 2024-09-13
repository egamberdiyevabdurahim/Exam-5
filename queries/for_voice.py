from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_voice_table_query() -> None:
    """
    Creates a table for storing voices.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS voice (
        id BIGSERIAL PRIMARY KEY,
        vote_id BIGINT REFERENCES vote(id) NOT NULL,
        petition_id BIGINT REFERENCES petition(id) NOT NULL,
        user_id BIGINT REFERENCES users(id),
        user_for_vote_id BIGINT REFERENCES user_for_vote(id)
    )
    """)
    return None


def get_voice_by_id_query(voice_id: int) -> DictRow:
    """
    Gets a voice by its ID.

    Args:
    voice_id (int): The ID of the voice.

    Returns:
    DictRow: The voice details or None if the voice does not exist.
    """
    query = "SELECT * FROM voice WHERE id = %s;"
    return execute_query(query, (voice_id,), "one")


def get_all_voices_by_vote_id_query(vote_id: int) -> list:
    """
    Gets all voices associated with a specific vote.

    Args:
    vote_id (int): The ID of the vote.

    Returns:
    list: A list of voices associated with the vote.
    """
    query = "SELECT * FROM voice WHERE vote_id = %s;"
    return execute_query(query, (vote_id,), "all")


def get_all_voices_by_petition_id_query(petition_id: int) -> list:
    """
    Gets all voices associated with a specific petition.

    Args:
    petition_id (int): The ID of the petition.

    Returns:
    list: A list of voices associated with the petition.
    """
    query = "SELECT * FROM voice WHERE petition_id = %s;"
    return execute_query(query, (petition_id,), "all")


def get_all_voices_by_user_id_query(user_id: int) -> list:
    """
    Gets all voices created by a specific user.

    Args:
    user_id (int): The ID of the user.

    Returns:
    list: A list of voices created by the user.
    """
    query = "SELECT * FROM voice WHERE user_id = %s;"
    return execute_query(query, (user_id,), "all")


def get_all_voices_by_user_for_vote_id_query(user_for_vote_id: int) -> list:
    """
    Gets all voices for a specific user in a vote.

    Args:
    user_for_vote_id (int): The ID of the user for vote.

    Returns:
    list: A list of voices for the specified user in the vote.
    """
    query = "SELECT * FROM voice WHERE user_for_vote_id = %s;"
    return execute_query(query, (user_for_vote_id,), "all")


def insert_voice_query(vote_id: int, petition_id: int, user_id: int = None, user_for_vote_id: int = None) -> None:
    """
    Inserts a new voice into the voice table.

    Args:
    vote_id (int): The ID of the vote.
    petition_id (int): The ID of the petition.
    user_id (int): The ID of the user.
    user_for_vote_id (int): The ID of the user for vote.
    """
    execute_query("INSERT INTO voice (vote_id, petition_id, user_id, user_for_vote_id) VALUES (%s, %s, %s, %s)",
                  (vote_id, petition_id, user_id, user_for_vote_id))
    return None


def get_all_voices() -> list:
    """
    Retrieves all voices from the voice table.

    Returns:
    list: A list of voice details.
    """
    query = "SELECT * FROM voice;"
    return execute_query(query, (), "all")
