from datetime import datetime

from psycopg2.extras import DictRow

from database_config.db_settings import execute_query
from queries.for_petition import winner_petition_query


def create_appeal_table_query() -> None:
    """
    Creates a table for storing appeals.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS appeal (
        id BIGSERIAL PRIMARY KEY,
        start_date DATE NOT NULL,
        end_date DATE,
        season_id BIGINT REFERENCES season(id) NOT NULL,
        total_appeals BIGINT DEFAULT 0,
        is_active BOOLEAN DEFAULT TRUE,
        winners_for_each_category JSONB,
        status BOOLEAN DEFAULT TRUE
    )
    """)
    return None


def get_appeal_by_id_query(appeal_id: int):
    """
    Gets an appeal by its ID.

    Args:
    appeal_id (int): The ID of the appeal.

    Returns:
    DictRow: The appeal or None if the appeal does not exist.
    """
    query = "SELECT * FROM appeal WHERE id = %s;"
    return execute_query(query, (appeal_id,), "one")


def activate_appeal_query(season_id: int, end_date: str, winners_for_each_category) -> None:
    """
    Activates the appeal for the given season.
    """
    execute_query("""
    INSERT INTO appeal (start_date, end_date, season_id, winners_for_each_category)
    VALUES (%s, %s, %s, %s)
    """, (datetime.now().date(), end_date, season_id, winners_for_each_category))
    return None


def get_active_appeal_query() -> DictRow:
    """
    Gets the active appeal.

    Returns:
    DictRow: The active appeal or None if there is no active appeal.
    """
    query = "SELECT * FROM appeal WHERE is_active = %s;"
    return execute_query(query, (True,), "one")


def deactivate_appeal_query() -> None:
    """
    Deactivates the active appeal.

    Returns:
    DictRow: The deactivated appeal or None if there is no active appeal.
    """
    query = "UPDATE appeal SET is_active = %s WHERE is_active = %s"
    return execute_query(query, (False, True,))


def get_appeal_by_season_query(season_id: int) -> DictRow:
    """
    Gets the appeal for the given season.

    Args:
    season_id (int): The season ID.

    Returns:
    DictRow: The appeal details or None if there is no appeal for the given season.
    """
    query = "SELECT * FROM appeal WHERE season_id = %s AND status = %s;"
    return execute_query(query, (season_id, True), "one")


def add_appeal_to_total_appeals_query() -> None:
    """
    Adds 1 to the total appeals count in the appeal table.
    """
    execute_query("UPDATE appeal SET total_appeals = total_appeals + 1")
    return None


def delete_appeal_query() -> None:
    """
    Deletes the active appeal from the appeal table.
    """
    execute_query("UPDATE appeal SET status = %s, is_active = %s WHERE is_active = %s",
                  (False, False, True,))
    return None


def get_all_appeals_query() -> list:
    """
    Gets all active appeals.

    Returns:
    list: A list of active appeals.
    """
    query = "SELECT * FROM appeal WHERE is_active = %s AND status = %s;"
    return execute_query(query, (True, True,), "all")
