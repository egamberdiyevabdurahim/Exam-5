import random

from mail.send_mail import send_email

from queries.for_confirmation_codes import get_confirmation_code_by_code_query, insert_confirmation_code_query


from .for_beautiful_terminal import init, error, enter, success

init(autoreset=True)


def randomer():
    """
    Function to generate a random 6-digit confirmation code.
    """
    confirmation_code = random.randint(100000, 999999)

    data = get_confirmation_code_by_code_query(str(confirmation_code))

    if data:
        return randomer()

    insert_confirmation_code_query(str(confirmation_code))

    return confirmation_code


def verify_confirmation(email: str, confirmation_code: str):
    """
    Verifies the confirmation code.
    """
    confirm = input(enter+"Enter Confirmation Code: ")

    if confirm == "sent":
        return send_confirmation(email)

    if int(confirm) != int(confirmation_code):
        print(error+"Invalid Confirmation Code!\n"
              "If Confirmation Code Didn't Receive Enter sent")
        return verify_confirmation(email, confirmation_code)

    return True


def send_confirmation(email: str):
    """
    Function to send a confirmation email to the user.
    """
    confirmation_code = randomer()
    subject = "MasterPhone's OpenBudget - Confirmation Code"
    message = f"Your confirmation code is: {confirmation_code}"
    print(success+"Confirmation Code Sent!")

    send_email(subject, message, email)

    verify_confirmation(email, confirmation_code)
    return True
