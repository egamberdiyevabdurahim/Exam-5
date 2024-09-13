from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_city_table_query() -> None:
    """
    Creates a table for storing cities.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS city (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        region_id BIGINT REFERENCES region(id),
        status BOOLEAN DEFAULT TRUE
    )
    """)
    return None


def get_city_by_name_query(city_name: str) -> DictRow:
    """
    Gets a city by its name.

    Args:
    city_name (str): The name of the city.

    Returns:
    DictRow: The city details or None if the city does not exist.
    """
    query = "SELECT * FROM city WHERE name = %s AND status = %s;"
    return execute_query(query, (city_name, True), "one")


def get_city_by_id_query(city_id: int) -> DictRow:
    """
    Gets a city by its ID.

    Args:
    city_id (int): The ID of the city.

    Returns:
    DictRow: The city details or None if the city does not exist.
    """
    query = "SELECT * FROM city WHERE id = %s AND status = %s;"
    return execute_query(query, (city_id, True), "one")


def insert_city_query(city_name, region_id) -> None:
    """
    Inserts a new city into the city table.

    Args:
    city_name (str): The name of the city.
    region_id (int): The ID of the region to which the city belongs.
    """
    execute_query("INSERT INTO city (name, region_id) VALUES (%s, %s)", (city_name, region_id))
    return None


def update_city_name_query(city_id: int, new_name: str) -> None:
    """
    Updates the name of a city.

    Args:
    city_id (int): The ID of the city.
    new_name (str): The new name of the city.
    """
    execute_query("UPDATE city SET name = %s WHERE id = %s", (new_name, city_id))
    return None


def delete_city_query(city_id: int) -> None:
    """
    Deletes a city from the city table.

    Args:
    city_id (int): The ID of the city.
    """
    execute_query("UPDATE city SET status = %s WHERE id = %s", (False, city_id))
    return None


def get_cities_by_region_query(region_id: int) -> list:
    """
    Retrieves all cities in a specific region from the city table.

    Args:
    region_id (int): The ID of the region.

    Returns:
    list: A list of city details.
    """
    query = "SELECT * FROM city WHERE region_id = %s AND status = %s;"
    return execute_query(query, (region_id, True), "all")


def get_all_cities_query() -> list:
    """
    Retrieves all cities from the city table.

    Returns:
    list: A list of city details.
    """
    query = "SELECT * FROM city WHERE status = %s;"
    return execute_query(query, (True,), "all")


def get_total_votes_by_city_query():
    """
    Retrieves the total number of votes for each city.
    """
    query = """
    SELECT c.id, c.name, COUNT(p.id) AS total_votes
    FROM city c
    JOIN petition p ON c.id = p.city_id
    WHERE p.status = %s
    GROUP BY c.id, c.name
    HAVING COUNT(p.total_voices) > 0
    ORDER BY total_votes DESC;;"""
    return execute_query(query, (True,), "all")
