from datetime import datetime

from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_vote_table_query() -> None:
    """
    Creates a table for storing votes.
    """
    execute_query("""
        CREATE TABLE IF NOT EXISTS vote (
            id BIGSERIAL PRIMARY KEY,
            start_date DATE NOT NULL,
            end_date DATE,
            season_id BIGINT REFERENCES season(id) NOT NULL,
            total_votes BIGINT DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            status BOOLEAN DEFAULT TRUE
        );
    """)
    return None


def activate_vote_query(season_id: int, end_date: str) -> None:
    """
    Activates the vote for the given season.
    """
    execute_query("""
    INSERT INTO vote (start_date, end_date, season_id)
    VALUES (%s, %s, %s)
    """, (datetime.now().date(), end_date, season_id))
    return None


def get_active_vote_query() -> DictRow:
    """
    Gets the active vote.

    Returns:
    DictRow: The active vote or None if there is no active vote.
    """
    query = "SELECT * FROM vote WHERE is_active = %s;"
    return execute_query(query, (True,), "one")


def deactivate_vote_query() -> None:
    """
    Deactivates the active vote.

    Returns:
    DictRow: The deactivated vote or None if there is no active vote.
    """
    query = "UPDATE vote SET is_active = %s WHERE is_active = %s"
    return execute_query(query, (False, True,))


def get_vote_by_season_query(season_id: int) -> DictRow:
    """
    Gets the vote for the given season.

    Args:
        season_id (int): The ID of the season.

    Returns:
    DictRow: The vote details or None if the season does not have a vote.
    """
    query = "SELECT * FROM vote WHERE season_id = %s;"
    return execute_query(query, (season_id,), "one")


def add_vote_to_total_votes_query() -> None:
    """
    Adds 1 to the total votes count in the vote table.
    """
    execute_query("UPDATE vote SET total_votes = total_votes + 1")
    return None


def delete_vote_query() -> None:
    """
    Deletes the active vote from the vote table.
    """
    execute_query("""
    UPDATE vote
    SET is_active = %s, status = %s
    WHERE is_active = %s
    """, (False, False, True))
    return None


def get_all_votes_query() -> list:
    """
    Gets all active votes.

    Returns:
    list: A list of active votes.
    """
    query = "SELECT * FROM vote WHERE is_active = %s AND status = %s;"
    return execute_query(query, (True, True,), "all")
