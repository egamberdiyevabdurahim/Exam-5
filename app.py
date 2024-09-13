from threading import Thread

from queries.for_running import if_not_used

from auth.login import login
from auth.register import register
from user.admin.admin_menu import admin_menu
from user.user.user_func import vote_with_another_number
from user.user.user_menu import user_menu

from utils.for_beautiful_terminal import command, success, error, enter


def after_login(email: str, status: str):
    """
    Function to handle the after-login actions.
    """
    if status == "admin":
        print(success+"Welcome Admin!")
        return admin_menu()

    elif status == "user":
        print(success+"Welcome User!")
        return user_menu(email)

    elif status == "developer":
        print(success+"Welcome Developer!")


def main():
    print(command+"\n1. Login\n"
          "2. Register\n"
          "3. Vote\n"
          "4. Exit\n")

    print("""
    admin login&password = admin
    """)
    choice = input(enter+"Enter your choice: ")

    if choice == '1':
        data = login()
        if not data:
            return main()
        email, status = data
        after_login(email, status)

    elif choice == '2':
        email, status = register()
        after_login(email, status)

    elif choice == '3':
        vote_with_another_number()

    elif choice == '4':
        print(success+"Exiting...")
        return None

    else:
        print(error+"Invalid choice. Please try again.")

    return main()


if __name__ == "__main__":
    Thread(target=if_not_used()).start()
    main()