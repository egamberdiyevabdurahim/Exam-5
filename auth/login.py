from queries.for_email import get_email_by_email_query
from queries.for_users import get_user_by_email_id_query
from utils.for_confirmation import send_confirmation

from utils.for_beautiful_terminal import init, error, enter, success

init(autoreset=True)


def login():
    """
    Handles the login process for a user.
    """
    email: str = input(enter+"Enter your email address: ")
    password: str = input(enter+"Enter your password: ")

    if email == "admin" and password == "admin":
        print(success+"\nLogin successful as Admin!\n")
        return "admin", "admin"

    elif email == "developer" and password == "developer":
        print(success+"\nLogin successful as Developer!\n")
        return "super", "super"

    email_data = get_email_by_email_query(email)
    if email_data is None:
        print(error+"Invalid email address. Please try again.")
        return None

    user_data = get_user_by_email_id_query(email_data['id'])

    if user_data['password'] != password:
        print(error+"Invalid password. Please try again.")
        return None

    # if send_confirmation(email) is not True:
    #     return None, None

    return email_data['email'], "user"
