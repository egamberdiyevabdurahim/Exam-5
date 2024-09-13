from datetime import datetime

from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_season_table_query() -> None:
    """
    Creates a table for storing season.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS season (
        id BIGSERIAL PRIMARY KEY,
        start_date DATE NOT NULL,
        end_date DATE,
        is_active BOOLEAN DEFAULT TRUE,
        status BOOLEAN DEFAULT TRUE
    )
    """)
    return None


def activate_season_query() -> None:
    """
    Inserts a season into the season table.
    """
    execute_query("""
    INSERT INTO season (start_date)
    VALUES (%s)
    """, (datetime.now().date(),))
    return None


def add_end_date_query(end_date: str) -> None:
    """
    Adds an end date to the current season.

    Args:
        end_date (str): The new end date for the current season.
    """
    execute_query("""
    UPDATE season
    SET end_date = %s
    WHERE is_active = %s
    """, (end_date, True))
    return None


def deactivate_season_query() -> None:
    """
    Deactivates the current season.
    """
    execute_query("""
    UPDATE season
    SET is_active = %s
    WHERE is_active = %s
    """, (False, True))
    return None


def get_active_season_query() -> DictRow:
    """
    Retrieves the active season from the season table.

    Returns:
    DictRow: The active season details.
    """
    query = "SELECT * FROM season WHERE is_active = %s;"
    return execute_query(query, (True,), "one")


def get_last_season_query() -> DictRow:
    """"
    Retrieves the last active season from the season table.

    Returns:
    DictRow: The last active season details.
    """
    query = "SELECT * FROM season WHERE status = %s ORDER BY start_date DESC LIMIT 1;"
    return execute_query(query, (True,), "one")


def is_active_season_exists_query() -> bool:
    """
    Checks if an active season exists in the season table.

    Returns:
    bool: True if an active season exists, False otherwise.
    """
    query = "SELECT COUNT(*) FROM season WHERE is_active = %s;"
    return execute_query(query, (True,), "one")[0] > 0


def get_all_seasons_query() -> list:
    """
    Retrieves all seasons from the season table.

    Returns:
    list: The retrieved seasons.
    """
    query = "SELECT * FROM season WHERE status = %s;"
    return execute_query(query, (True,), "all")


def get_season_by_id_query(season_id: int) -> DictRow:
    """
    Retrieves a season by its ID from the season table.

    Args:
        season_id (int): The ID of the season.

    Returns:
        DictRow: The retrieved season details or None if the season does not exist.
    """
    query = "SELECT * FROM season WHERE id = %s AND status = %s;"
    return execute_query(query, (season_id, True), "one")


def delete_season_query() -> None:
    """
    Deletes the current season from the season table.
    """
    execute_query("""
    UPDATE season
    SET status = %s, is_active = %s
    WHERE is_active = %s
    """, (False, False, True))
    return None
