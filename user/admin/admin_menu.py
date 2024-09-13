from auth.register import register

from user.admin.admin_func import start_season, end_appeal, start_vote, end_vote, end_season, accept_reject_petitions, \
    reject_all_petitions, accept_all_petitions, view_all_accepted_petitions, view_all_rejected_petitions, \
    view_all_petitions, view_all_won_petitions, view_all_lost_petitions, get_total_voices, \
    get_total_voices_for_active_appeal, remove_user, update_user_details, view_user_details, view_all_users, \
    view_all_user_for_votes, add_region, edit_region, remove_region, view_all_regions, add_city, edit_city, remove_city, \
    view_all_cities, add_category, edit_category, remove_category, view_all_categories, \
    view_total_voices_for_categories, view_total_voices_for_cities, view_total_voices_for_regions

from utils.for_beautiful_terminal import init, error, enter, success, command

init(autoreset=True)


def season_management():
    """
    Handles the season management for an admin.
    """
    print(command+"\n1. Start Season\n"
                  "2. End Receiving Applications\n"
                  "3. Start Vote\n"
                  "4. End Vote\n"
                  "5. End Season\n"
                  "6. Accept/Reject Petitions\n"
                  "7. Accept All Petitions\n"
                  "8. Reject All Petitions\n"
                  "9. View All Accepted Petitions For Active Season\n"
                  "10. View All Rejected Petitions For Active Season\n"
                  "11. View All Petitions\n"
                  "12. View All Won Petitions\n"
                  "13. View All Lost Petitions\n"
                  "14. View Total Voices for All Seasons\n"
                  "15. View Total Voices for Active Season\n"
                  "16. View Total Voices for Each Categories\n"
                  "17. View Total Voices for Each City\n"
                  "18. View Total Voices for Each Region\n"
                  "19. Back\n")
    choice = input(enter+"Enter your choice: ")

    if choice == '1':
        start_season()

    elif choice == '2':
        end_appeal()

    elif choice == '3':
        start_vote()

    elif choice == '4':
        end_vote()

    elif choice == '5':
        end_season()

    elif choice == '6':
        accept_reject_petitions()

    elif choice == '7':
        accept_all_petitions()

    elif choice == '8':
        reject_all_petitions()

    elif choice == '9':
        view_all_accepted_petitions()

    elif choice == '10':
        view_all_rejected_petitions()

    elif choice == '11':
        view_all_petitions()

    elif choice == '12':
        view_all_won_petitions()

    elif choice == '13':
        view_all_lost_petitions()

    elif choice == '14':
        get_total_voices()

    elif choice == '15':
        get_total_voices_for_active_appeal()

    elif choice == '16':
        view_total_voices_for_categories()

    elif choice == '17':
        view_total_voices_for_cities()

    elif choice == '18':
        view_total_voices_for_regions()

    elif choice == '19':
        print(success+"Backing...")
        return None

    else:
        print(error+"Invalid choice. Please try again.")

    return season_management()


def user_management():
    """
    Handles the user management for an admin.
    """
    print(command+"\n1. Add User\n"
          "2. Remove User\n"
          "3. Update User\n"
          "4. View User Details\n"
          "5. View All Users\n"
          "6. Back\n")
    choice = input(enter+"Enter your choice: ")

    if choice == '1':
        register()

    elif choice == '2':
        remove_user()

    elif choice == '3':
        update_user_details()

    elif choice == '4':
        view_user_details()

    elif choice == '5':
        view_all_users()

    elif choice == '6':
        print(success+"Backing...")
        return None

    else:
        print(error+"Invalid choice. Please try again.")

    return user_management()


def user_for_vote_management():
    """
    Handles the user management for a specific user.
    """
    print(command+"\n1. View All Users\n"
          "2. Back\n")
    choice = input(enter+"Enter your choice: ")

    if choice == '1':
        view_all_user_for_votes()

    elif choice == '2':
        print(success+"Backing...")
        return None

    else:
        print(error+"Invalid choice. Please try again.")

    return user_for_vote_management()


def region_management():
    """
    Handles the region management for an admin.
    """
    print(command+"\n1. Add New Region\n"
                  "2. Edit Region\n"
                  "3. Delete Region\n"
                  "4. Show All Regions\n"
                  "5. Back\n")
    choice = input(enter+"Enter your choice: ")

    if choice == '1':
        add_region()

    elif choice == '2':
        edit_region()

    elif choice == '3':
        remove_region()

    elif choice == '4':
        view_all_regions()

    elif choice == '5':
        print(success+"Backing...")
        return None

    else:
        print(error+"Invalid choice. Please try again.")

    return region_management()


def city_management():
    """
    Handles the city management for an admin.
    """
    print(command + "\n1. Add New City\n"
                    "2. Edit City\n"
                    "3. Delete City\n"
                    "4. Show All Cities\n"
                    "5. Back\n")
    choice = input(enter+"Enter your choice: ")

    if choice == '1':
        add_city()

    elif choice == '2':
        edit_city()

    elif choice == '3':
        remove_city()

    elif choice == '4':
        view_all_cities()

    elif choice == '5':
        print(success+"Backing...")
        return None

    else:
        print(error+"Invalid choice. Please try again.")

    return city_management()


def region_city_management():
    """
    Handles the region and city management for an admin.
    """
    print(command+"\n1. Add/Update/Delete/Show - Region\n"
          "2. Add/Update/Delete/Show - City\n"
          "3. Back\n")
    choice = input(enter+"Enter your choice: ")

    if choice == '1':
        region_management()

    elif choice == '2':
        city_management()

    elif choice == '3':
        print(success+"Backing...")
        return None

    else:
        print(error+"Invalid choice. Please try again.")

    return region_city_management()


def category_management():
    """
    Handles the category management for an admin.
    """
    print(command+"\n1. Add New Category\n"
                  "2. Edit Category\n"
                  "3. Delete Category\n"
                  "4. Show All Categories\n"
                  "5. Back\n")
    choice = input(enter+"Enter your choice: ")

    if choice == '1':
        # Add new category
        add_category()

    elif choice == '2':
        # Edit category
        edit_category()

    elif choice == '3':
        # Delete category
        remove_category()

    elif choice == '4':
        # Show all categories
        view_all_categories()

    elif choice == '5':
        print(success+"Backing...")
        return None

    else:
        print(error+"Invalid choice. Please try again.")

    return category_management()


def admin_menu():
    """
    Handles the admin menu for a specific user.
    """
    print(command+"\n1. Season Management\n"
                  "2. User Management\n"
                  "3. User For Vote Management\n"
                  "4. Region&City Management\n"
                  "5. Category Management\n"
                  "6. Logout\n")
    choice = input(enter+"Enter your choice: ")

    if choice == '1':
        season_management()

    elif choice == '2':
        user_management()

    elif choice == '3':
        user_for_vote_management()

    elif choice == '4':
        region_city_management()

    elif choice == '5':
        category_management()

    elif choice == '6':
        print(success+"Logout successful!")
        return None

    else:
        print(error+"Invalid choice. Please try again.")

    return admin_menu()
