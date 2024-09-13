from queries.for_category import get_category_by_id_query
from queries.for_city import get_city_by_id_query
from queries.for_email import get_email_by_id_query
from queries.for_phone_number import get_phone_number_by_id_query
from queries.for_region import get_region_by_id_query
from queries.for_users import get_user_by_id_query

from .for_beautiful_terminal import init, prints

init(autoreset=True)


def petition_printer(petition_data):
    """
    Prints a formatted petition.

    Args:
    petition_data (dict): A dictionary containing the petition data.
    """
    print(prints+f"Petition ID: {petition_data['id']}. Title: {petition_data['title']}\n"
          f"Money: {petition_data['money']}.Description: {petition_data['content'][:15]}")


def full_petition_printer(petition_data):
    """
    Prints a formatted full petition.

    Args:
    petition_data (dict): A dictionary containing the petition data.
    """
    user_data = get_user_by_id_query(petition_data['user_id'])
    category_data = get_category_by_id_query(petition_data['category_id'])
    city_data = get_city_by_id_query(petition_data['city_id'])
    region_data = get_region_by_id_query(city_data['region_id'])
    print(prints+f"Petition ID: {petition_data['id']}. Title: {petition_data['title']}\n"
          f"Money: {petition_data['money']}. Description: {petition_data['content'][:15]}\n"
          f"User ID: {petition_data['user_id']}. User Name: {user_data['first_name']}\n"
          f"Total Votes: {petition_data['total_voices']}\n"
          f"Is Accepted: {petition_data['is_accepted']}\n"
          f"Is Winner: {petition_data['is_winner']}\n"
          f"Category: {category_data['name']}\n"
          f"City: {city_data['name']}. Region: {region_data['name']}")


def user_printer(user_data):
    """
    Prints a formatted user.

    Args:
    user_data (dict): A dictionary containing the user data.
    """
    print(prints+f"User ID: {user_data['id']}. First Name: {user_data['first_name']}\n"
          f"Last Name: {user_data['last_name']}. Email: {get_email_by_id_query(user_data['email_id'])['email']}\n"
          f"Phone Number: {get_phone_number_by_id_query(user_data['phone_number_id'])['phone_number']}")

