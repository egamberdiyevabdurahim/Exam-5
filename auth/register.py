from queries.for_email import get_email_by_email_query, insert_email_query
from queries.for_phone_number import get_phone_number_by_phone_number_query, insert_phone_number_query
from queries.for_users import insert_user_query

from utils import additions
from utils.for_confirmation import send_confirmation
from utils.for_beautiful_terminal import init, error, enter, re_enter, success

init(autoreset=True)


def register():
    """
    Handles the registration process for a new user.
    """
    email: str = input(enter+"Enter your email: ")
    # Check if the email address is unique
    while not email.endswith(additions.email_details):
        print(error+"Invalid email format. Please use one of the following formats: @mail.ru, @gmail.com, @icloud.com")
        email = input(re_enter+"Re-Enter your email: ")

    # Check if the email address already exists in the database
    while get_email_by_email_query(email):
        print(error+"Email already exists! Please try again.")
        email = input(re_enter+"Re-Enter your email: ")

    phone_number: str = input(enter+"Enter your phone number: ")
    # Check if the phone number is valid
    while not phone_number.startswith(additions.phone_details):
        print(error+"Invalid phone number format. Please use the format 991234567")
        phone_number = input(re_enter+"Re-Enter your phone number: ")

    # Check if the phone number already exists in the database
    while get_phone_number_by_phone_number_query(phone_number):
        print(error+"Phone number already exists! Please try again.")
        phone_number = input(re_enter+"Re-Enter your phone number: ")

    password: str = input(enter+"Enter your password: ")
    while not password or len(password) < 8:
        print(error+"Password must be at least 8 characters long!")
        password = input(re_enter+"Re-Enter your password: ")

    password_confirmation: str = input(enter+"Confirm your password: ")
    # Check if the password and password confirmation match
    while password!= password_confirmation:
        print(error+"Passwords do not match!")
        password_confirmation = input(re_enter+"Re-Confirm your password: ")

    first_name: str = input(enter+"Enter your First Name: ")
    while not first_name:
        print(error+"First Name is required!")
        first_name = input(re_enter+"Re-Enter your First Name: ")

    last_name: str = input(enter+"Enter your Last Name: ")
    while not last_name:
        print(error+"Last Name is required!")
        last_name = input(re_enter+"Re-Enter your Last Name: ")

    if send_confirmation(email) is not True:
        return None, None

    insert_email_query(email)
    insert_phone_number_query(phone_number)

    email_id = get_email_by_email_query(email)['id']
    phone_number_id = get_phone_number_by_phone_number_query(phone_number)['id']

    # Create a new user in the database
    insert_user_query(first_name=first_name, last_name=last_name, email_id=email_id,
                      phone_number_id=phone_number_id, password=password)
    print(success+"Congratulations!!!")
    print(success+f"{first_name} {last_name} You Registered Successfully to MasterPhone's OpenBudget!")
    return email, "user"
