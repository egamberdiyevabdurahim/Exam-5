from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_category_table_query() -> None:
    """
    Creates a table for storing categories.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS category (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        status BOOLEAN DEFAULT TRUE
    )
    """)
    return None


def get_category_by_name_query(category_name: str) -> DictRow:
    """
    Gets a category by its name.

    Args:
    category_name (str): The name of the category.

    Returns:
    DictRow: The category details or None if the category does not exist.
    """
    query = "SELECT * FROM category WHERE name = %s AND status = %s;"
    return execute_query(query, (category_name, True), "one")


def get_category_by_id_query(category_id: int) -> DictRow:
    """
    Gets a category by its ID.

    Args:
    category_id (int): The ID of the category.

    Returns:
    DictRow: The category details or None if the category does not exist.
    """
    query = "SELECT * FROM category WHERE id = %s AND status = %s;"
    return execute_query(query, (category_id, True), "one")


def insert_category_query(category_name) -> None:
    """
    Inserts a new category into the category table.

    Args:
    category_name (str): The name of the category.
    """
    execute_query("INSERT INTO category (name) VALUES (%s)", (category_name,))
    return None


def update_category_name_query(category_id: int, new_name: str) -> None:
    """
    Updates the name of a category.

    Args:
    category_id (int): The ID of the category.
    new_name (str): The new name of the category.
    """
    execute_query("UPDATE category SET name = %s WHERE id = %s", (new_name, category_id))
    return None


def delete_category_query(category_id: int) -> None:
    """
    Deletes a category from the category table.

    Args:
    category_id (int): The ID of the category.
    """
    execute_query("UPDATE category SET status = %s WHERE id = %s", (False, category_id))
    return None


def get_all_categories_query() -> list:
    """
    Retrieves all categories from the category table.

    Returns:
    list: A list of category details.
    """
    query = "SELECT * FROM category WHERE status = %s;"
    return execute_query(query, (True,), "all")
