from user.admin.admin_func import view_all_petitions, view_all_won_petitions, view_all_lost_petitions
from user.user.user_func import vote, view_my_votes, vote_with_another_number, post_petition, view_all_my_petitions, \
    my_last_petition_for_last_season, get_my_accepted_petitions, get_my_lost_petitions, get_my_won_petitions, \
    get_my_rejected_petitions, get_total_voices_for_all_my_petitions, get_total_voices_for_last_seasons_my_petition, \
    get_my_pending_petition

from utils.for_beautiful_terminal import init, error, success, command

init(autoreset=True)


def user_menu(email: str):
    """
    Handles the user-specific menu.
    """
    print(command+"1. Vote\n"
                  "2. View My Votes\n"
                  "3. Vote With Another Number\n"
                  "4. Post Petition\n"
                  "5. My Petitions\n"
                  "6. My Last Petition for Last Season\n"
                  "7. My Accepted Petitions\n"
                  "8. My Rejected Petitions\n"
                  "9. My Won Petitions\n"
                  "10. My Lost Petitions\n"
                  "11. Total Voices for My All Petitions\n"
                  "12. Total Voice for My Last Season's Active Petition\n"
                  "13. Get My Pending Petition\n"
                  "14. View All Petitions\n"
                  "15. View All Won Petitions\n"
                  "16. View All Lost Petitions\n"
                  "17. Logout\n")
    choice = input("Enter your choice: ")

    if choice == '1':
        vote(email)

    elif choice == '2':
        view_my_votes(email)

    elif choice == '3':
        vote_with_another_number()

    elif choice == '4':
        post_petition(email)

    elif choice == '5':
        view_all_my_petitions(email)

    elif choice == '6':
        my_last_petition_for_last_season(email)

    elif choice == '7':
        get_my_accepted_petitions(email)

    elif choice == '8':
        get_my_rejected_petitions(email)

    elif choice == '9':
        get_my_won_petitions(email)

    elif choice == '10':
        get_my_lost_petitions(email)

    elif choice == '11':
        get_total_voices_for_all_my_petitions(email)

    elif choice == '12':
        get_total_voices_for_last_seasons_my_petition(email)

    elif choice == '13':
        get_my_pending_petition(email)

    elif choice == '14':
        view_all_petitions()

    elif choice == '15':
        view_all_won_petitions()

    elif choice == '16':
        view_all_lost_petitions()

    elif choice == '17':
        print(success+"Logging out...")
        return None

    else:
        print(error+"Invalid choice. Please try again.")

    return user_menu(email)