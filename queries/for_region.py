from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_region_table_query() -> None:
    """
    Creates a table for storing regions.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS region (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        status BOOLEAN DEFAULT TRUE
    )
    """)
    return None


def get_region_by_name_query(region_name: str) -> DictRow:
    """
    Gets a region by its name.

    Args:
    region_name (str): The name of the region.

    Returns:
    DictRow: The region details or None if the region does not exist.
    """
    query = "SELECT * FROM region WHERE name = %s AND status = %s;"
    return execute_query(query, (region_name, True), "one")


def get_region_by_id_query(region_id: int) -> DictRow:
    """
    Gets a region by its ID.

    Args:
    region_id (int): The ID of the region.

    Returns:
    DictRow: The region details or None if the region does not exist.
    """
    query = "SELECT * FROM region WHERE id = %s AND status = %s;"
    return execute_query(query, (region_id, True), "one")


def insert_region_query(region_name) -> None:
    """
    Inserts a new region into the region table.

    Args:
    region_name (str): The name of the region.
    """
    execute_query("INSERT INTO region (name) VALUES (%s)", (region_name,))
    return None


def update_region_name_query(region_id: int, new_name: str) -> None:
    """
    Updates the name of a region.

    Args:
    region_id (int): The ID of the region.
    new_name (str): The new name of the region.
    """
    execute_query("UPDATE region SET name = %s WHERE id = %s", (new_name, region_id))
    return None


def delete_region_query(region_id: int) -> None:
    """
    Deletes a region from the region table.

    Args:
    region_id (int): The ID of the region.
    """
    execute_query("UPDATE region SET status = %s WHERE id = %s", (False, region_id))
    return None


def get_all_regions_query() -> list:
    """
    Retrieves all regions from the region table.

    Returns:
    list: A list of region details.
    """
    query = "SELECT * FROM region WHERE status = %s;"
    return execute_query(query, (True,), "all")
