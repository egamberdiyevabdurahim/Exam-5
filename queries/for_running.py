import os

from database_config.db_settings import execute_query

from .for_category import create_category_table_query
from .for_confirmation_codes import create_confirmation_codes_table_query
from .for_email import create_email_table_query
from.for_phone_number import create_phone_number_table_query
from .for_region import create_region_table_query
from .for_city import create_city_table_query
from .for_season import create_season_table_query
from .for_appeal import create_appeal_table_query
from .for_vote import create_vote_table_query
from .for_petition import create_petition_table_query
from .for_user_for_vote import create_user_for_vote_table_query
from .for_voice import create_voice_table_query
from .for_users import create_users_table_query

def create_is_used_table_query() -> None:
    """
    Creates a new table for tracking whether the application is already run.
    """
    query = """
        CREATE TABLE IF NOT EXISTS is_used (
            id BIGSERIAL PRIMARY KEY,
            is_used BOOLEAN DEFAULT FALSE
        );
    """
    execute_query(query)
    return None


def insert_is_used_query():
    """
    Inserts a new record into the is_used table.
    """
    query = """
        SELECT * FROM is_used
        ORDER BY id DESC
        LIMIT 1;
        """
    data = execute_query(query, fetch="one")
    if data is None:
        query = "INSERT INTO is_used (is_used) VALUES (False);"
        execute_query(query)
    return None


def update_is_used_query():
    """
    Updates the is_used column in the is_used table.
    """
    query = "UPDATE is_used SET is_used = TRUE;"
    execute_query(query)
    return None


def is_used():
    query = """
    SELECT * FROM is_used
    ORDER BY id
    LIMIT 1;
    """
    data = execute_query(query, fetch="one")
    return data['is_used'] is True


def before_run() -> None:
    """
    Creates all required tables before running the application.
    """
    create_category_table_query()
    create_email_table_query()
    create_phone_number_table_query()
    create_region_table_query()
    create_city_table_query()
    create_season_table_query()
    create_users_table_query()
    create_appeal_table_query()
    create_vote_table_query()
    create_petition_table_query()
    create_user_for_vote_table_query()
    create_voice_table_query()
    create_confirmation_codes_table_query()
    return None


def if_not_used():
    path = os.path.dirname(os.path.abspath(__file__))  # Get absolute path
    create_is_used_table_query()
    insert_is_used_query()

    if not is_used():
        before_run()

        # Read and execute SQL for category insertion
        with open(os.path.join(path, 'inserter_for_category.sql'), 'r') as insert_file:
            for line in insert_file:
                query = line.strip()
                execute_query(query)

        # Read and execute SQL for region insertion
        with open(os.path.join(path, 'inserter_for_region.sql'), 'r') as insert_file:
            for line in insert_file:
                query = line.strip()
                execute_query(query)

        # Read and execute SQL for city insertion
        with open(os.path.join(path, 'inserter_for_city.sql'), 'r') as insert_file:
            for line in insert_file:
                query = line.strip()
                execute_query(query)

        update_is_used_query()

    return None
