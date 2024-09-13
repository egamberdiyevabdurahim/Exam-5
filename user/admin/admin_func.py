import json
from datetime import datetime

from queries.for_category import get_all_categories_query, get_category_by_id_query, delete_category_query, \
    get_category_by_name_query, insert_category_query, update_category_name_query, get_total_votes_by_category_query
from queries.for_city import get_cities_by_region_query, get_city_by_id_query, delete_city_query, \
    get_city_by_name_query, insert_city_query, update_city_name_query, get_all_cities_query, \
    get_total_votes_by_city_query
from queries.for_email import get_email_by_id_query
from queries.for_petition import get_winners_query, \
    get_petition_by_id_query, get_all_none_petitions_by_appeal_id_query, \
    accept_petition_query, reject_petition_query, get_all_accepted_petitions_by_appeal_id_query, \
    get_all_rejected_petitions_by_appeal_id_query, get_all_petitions_by_appeal_id_query, \
    get_all_won_petitions_by_appeal_id_query, get_all_lost_petitions_by_appeal_id_query, get_total_voices_query, \
    get_total_voices_by_appeal_id_query, winner_petition_query, get_all_petitions_query, loser_petition_query

from queries.for_phone_number import get_phone_number_by_id_query
from queries.for_region import get_all_regions_query, get_region_by_id_query, delete_region_query, \
    get_region_by_name_query, insert_region_query, update_region_name_query, get_total_votes_by_region_query
from queries.for_season import activate_season_query, add_end_date_query, get_active_season_query, \
    deactivate_season_query, get_all_seasons_query, get_season_by_id_query

from queries.for_appeal import activate_appeal_query, get_active_appeal_query, deactivate_appeal_query, \
    get_appeal_by_season_query, get_appeal_by_id_query

from queries.for_user_for_vote import get_all_user_for_votes_query
from queries.for_users import get_user_by_id_query, delete_user_query, get_all_users_query, update_user_query
from queries.for_voice import get_all_voices_by_petition_id_query
from queries.for_vote import activate_vote_query, get_active_vote_query, get_vote_by_season_query, deactivate_vote_query

from utils.printer import petition_printer, full_petition_printer, user_printer, region_printer, city_printer, \
    category_printer
from utils.for_beautiful_terminal import init, error, enter, re_enter, success, prints

init(autoreset=True)


def start_appeal() -> None:
    """
    Handles the starting of an appeal for a specific season.
    """
    season_id = get_active_season_query()['id']
    print(f"Starting appeal for season ID: {season_id}")

    while True:
        end_date = input(enter+"Enter End Date for Appeal (YYYY-MM-DD): ")

        try:
            datetime.strptime(end_date, "%Y-%m-%d").date()
            break
        except ValueError:
            print(error+"Invalid date format. Please use YYYY-MM-DD.")

    categories = get_all_categories_query()
    winners_for_each_category = dict()
    for category in categories:
        print(f"{category['id']}. {category['name']}")
        winners_for_category = input(enter+"Enter Number of winners for This category: ")
        while not winners_for_category.isdigit() or int(winners_for_category) <= 0:
            print(error+"Invalid number of winners. Please enter a positive integer.")
            winners_for_category = input(re_enter+"Re-Enter Number of winners for This category: ")
        winners_for_each_category[category['id']] = winners_for_category

    data = json.dumps(winners_for_each_category)

    activate_appeal_query(season_id=season_id, end_date=end_date, winners_for_each_category=data)
    print(success+f"Appeal Activated Successfully For {season_id} - Season!")
    return None


def start_season() -> None:
    """
    Handles the starting of a new season.
    """
    active_season = get_active_season_query()
    if active_season:
        print(error+"There is already an active season.\n"
              "For Starting a new season first: end season!")
        return None

    activate_season_query()

    start_appeal()

    while True:
        end_date = input(enter+"Enter End Date for Season (YYYY-MM-DD): ")

        try:
            datetime.strptime(end_date, "%Y-%m-%d").date()
            break
        except ValueError:
            print(error+"Invalid date format. Please use YYYY-MM-DD.")

    add_end_date_query(end_date)
    print(success+"Season Started Successfully!")
    return None


def end_appeal() -> None:
    """
    Handles the ending of the active appeal for a specific season.
    """
    active_appeal = get_active_appeal_query()
    if active_appeal is None:
        print(error+"No active appeal found.")
        return None
    print(f"Ending appeal for season ID: {active_appeal['season_id']}")
    deactivate_appeal_query()
    print(success+"Appeal Ended Successfully!")
    return None


def start_vote() -> None:
    """
    Handles the starting of a new vote for a specific season.
    """
    season_data = get_active_season_query()
    if season_data is None:
        print(error+"No active season found.")
        return None
    season_id = season_data['id']

    seasons_vote = get_vote_by_season_query(season_id)
    if seasons_vote:
        print(error+"There is already exists a vote for this season.\n"
              "For Starting a new vote first: end season!")
        return None

    active_appeal = get_active_appeal_query()
    if active_appeal:
        print(error+f"There is an active appeal for this season.\n"
              "For Starting a new vote first: end appeal!")
        return None

    print(f"Starting voting for season ID: {season_id}")
    while True:
        end_date = input(enter+"Enter End Date for Vote (YYYY-MM-DD): ")

        try:
            datetime.strptime(end_date, "%Y-%m-%d").date()
            break
        except ValueError:
            print(error+"Invalid date format. Please use YYYY-MM-DD.")

    activate_vote_query(season_id=season_id, end_date=end_date)
    print(success+f"Voting Activated Successfully For {season_id} - Season!")
    return None


def end_vote() -> None:
    """
    Handles the ending of the active vote for a specific season.
    """
    active_vote = get_active_vote_query()
    if active_vote is None:
        print(error+"No active vote found.")
        return None
    print(f"Ending voting for season ID: {active_vote['season_id']}")
    deactivate_vote_query()
    print(success+"Voting Ended Successfully!")
    return None


def end_season() -> None:
    """
    Handles the ending of the active season.
    """
    active_season = get_active_season_query()
    if active_season is None:
        print(error+"No active season found.")
        return None
    print(f"Ending season for season ID: {active_season['id']}")
    appeal = get_appeal_by_season_query(active_season['id'])
    if appeal:
        if appeal['is_active'] is True:
            deactivate_appeal_query()

    vote = get_vote_by_season_query(active_season['id'])
    if vote:
        if vote['is_active'] is True:
            deactivate_vote_query()
    else:
        print(error+"You can't end season\n"
              "Because voting is not started\n"
              "First start vote")
        return None

    determine_the_winner(appeal['id'])

    deactivate_season_query()

    print(success+"Season Ended Successfully!")
    return None


def determine_the_winner(appeal_id: int) -> None:
    """
    Determines the winner of the election based on the total votes.
    """
    winners = []
    appeal = get_appeal_by_id_query(appeal_id)
    for category_id, category_limit in appeal[6].items():
        winner = get_winners_query(category_id=category_id, limit=category_limit)
        for winner_ in winner:
            winners.append(winner_)

    if not winners:
        print(error+"No winner found.")
        return None

    for winner in winners:
        winner_petition_query(winner['id'])

    for petition in get_all_petitions_by_appeal_id_query(appeal_id):
        if petition['is_winner'] is not True:
            loser_petition_query(petition['id'])


def accept_reject_petitions_second_func() -> None:
    """
    Accepts petitions for the active appeal.
    """
    petition_id = input(enter+"Enter petition id: ")
    while not get_petition_by_id_query(int(petition_id)):
        print(error+"Petition not found.")
        petition_id = input(re_enter+"Re-Enter petition id: ")

    petition_data = get_petition_by_id_query(int(petition_id))
    full_petition_printer(petition_data)
    is_accepted = input(enter+"Do you want to accept this petition? (y/n): ").strip()
    while is_accepted not in ['y', 'n', 'yes', 'no']:
        print(error+"Invalid input. Please enter 'y' or 'n'.")
        is_accepted = input(re_enter+"Do you want to accept this petition? (y/n): ").strip()

    if is_accepted in ['y', 'yes']:
        accept_petition_query(petition_data['id'])
        print(success+"Petition accepted successfully.")

    else:
        reject_petition_query(petition_data['id'])
        print(success+"Petition rejected successfully.")

    return None


def accept_reject_petitions() -> None:
    """
    Accepts petitions for the active appeal.
    """
    active_appeal = get_active_appeal_query()
    if active_appeal is None:
        print(error+"No active appeal found.")
        return None

    petitions_data = get_all_none_petitions_by_appeal_id_query(active_appeal['id'])
    if not petitions_data:
        print(error+"No new petitions found.")
        return None

    for petition in petitions_data:
        petition_printer(petition)
        print("-"*20)

    return accept_reject_petitions_second_func()


def accept_all_petitions() -> None:
    """
    Accepts all petitions for the active appeal.
    """
    active_appeal = get_active_appeal_query()
    if active_appeal is None:
        print(error+"No active appeal found.")
        return None

    petitions_data = get_all_none_petitions_by_appeal_id_query(active_appeal['id'])
    if not petitions_data:
        print(error+"No new petitions found.")
        return None

    for petition in petitions_data:
        accept_petition_query(petition['id'])

    print(success+"All petitions accepted successfully.")
    return None


def reject_all_petitions() -> None:
    """
    Rejects all petitions for the active appeal.
    """
    active_appeal = get_active_appeal_query()
    if active_appeal is None:
        print(error+"No active appeal found.")
        return None

    petitions_data = get_all_none_petitions_by_appeal_id_query(active_appeal['id'])
    if not petitions_data:
        print(error+"No new petitions found.")
        return None

    for petition in petitions_data:
        reject_petition_query(petition['id'])

    print(success+"All petitions rejected successfully.")
    return None


def full_petition_viewer(petition_id: int) -> None:
    """
    Views a full petition based on its ID.
    """
    petition_data = get_petition_by_id_query(petition_id)
    full_petition_printer(petition_data)
    return None


def view_all_accepted_petitions() -> None:
    """
    Views all accepted petitions for the active appeal.
    """
    active_season = get_active_season_query()
    if active_season is None:
        print(error+"No active season found.")
        return None

    active_appeal = get_appeal_by_season_query(active_season['id'])

    petitions_data = get_all_accepted_petitions_by_appeal_id_query(active_appeal['id'])
    if not petitions_data:
        print(error+"No accepted petitions found.")
        return None

    for petition in petitions_data:
        petition_printer(petition)
        print("-"*20)

    petition_id = input(enter+"Enter petition id for full info: ")
    while not get_petition_by_id_query(int(petition_id)):
        print(error+"Petition not found.")
        petition_id = input(re_enter+"Re-Enter petition id: ")

    full_petition_viewer(int(petition_id))

    return None


def view_all_rejected_petitions() -> None:
    """
    Views all rejected petitions for the active appeal.
    """
    active_season = get_active_season_query()
    if active_season is None:
        print(error+"No active season found.")
        return None

    active_appeal = get_appeal_by_season_query(active_season['id'])

    petitions_data = get_all_rejected_petitions_by_appeal_id_query(active_appeal['id'])
    if not petitions_data:
        print(error+"No rejected petitions found.")
        return None

    for petition in petitions_data:
        petition_printer(petition)
        print("-"*20)

    petition_id = input(enter+"Enter petition id for full info: ")
    while not get_petition_by_id_query(int(petition_id)):
        print(error+"Petition not found.")
        petition_id = input(re_enter+"Re-Enter petition id: ")

    full_petition_viewer(int(petition_id))

    return None


def view_all_petitions() -> None:
    """
    Views all petitions for the active appeal.
    """
    seasons = get_all_seasons_query()
    active_season = get_active_season_query()
    if active_season is None:
        active_season = dict()

    for season in seasons:
        if season['id'] == active_season.get('id'):
            active_season_str = "Active"
        else:
            active_season_str = "Inactive"

        print(f"Season {season['id']}: {season['start_date']} - {season['end_date']} ({active_season_str})")
        print("-"*20)

    season_id = input(enter+"Enter season id: ")
    while not get_season_by_id_query(int(season_id)):
        print(error+"Season not found.")
        season_id = input(re_enter+"Re-Enter season id: ")

    active_appeal = get_appeal_by_season_query(int(season_id))

    petitions_data = get_all_petitions_by_appeal_id_query(active_appeal['id'])
    if not petitions_data:
        print(error+"No petitions found.")
        return None

    for petition in petitions_data:
        petition_printer(petition)
        print("-"*20)

    petition_id = input(enter+"Enter petition id for full info: ")
    while not get_petition_by_id_query(int(petition_id)):
        print(error+"Petition not found.")
        petition_id = input(re_enter+"Re-Enter petition id: ")

    full_petition_viewer(int(petition_id))

    show_or_no = input(enter+"Do you want to view all voiced users for this petition(y/n): ").strip() == "y"
    if show_or_no:
        view_all_voiced_users(int(petition_id))

    return None


def view_all_voiced_users(petition_id: int) -> None:
    """
    Views all voiced users for a specific petition, displaying masked phone numbers.
    """
    voices = get_all_voices_by_petition_id_query(petition_id)
    if not voices:
        print(error + "No voiced users found for this petition.")
        return None

    counter = 0
    for voice in voices:
        counter += 1
        user_data = get_user_by_id_query(voice['user_id'])
        phone_number_data = get_phone_number_by_id_query(user_data['phone_number_id'])['phone_number']

        masked_phone_number = '*' * (len(phone_number_data) - 4) + phone_number_data[-4:]

        print(f"{counter}: {masked_phone_number}")

    print(success + f"Total Voiced Users: {counter}")
    return None


def view_all_won_petitions() -> None:
    """
    Views all won petitions for the active appeal.
    """
    seasons = get_all_seasons_query()
    active_season = get_active_season_query()
    if active_season is None:
        active_season = dict()

    for season in seasons:
        if season['id'] == active_season.get('id'):
            active_season_str = "Active"
        else:
            active_season_str = "Inactive"

        print(f"Season {season['id']}: {season['start_date']} - {season['end_date']} ({active_season_str})")
        print("-" * 20)

    season_id = input(enter + "Enter season id: ")
    while not get_season_by_id_query(int(season_id)):
        print(error + "Season not found.")
        season_id = input(re_enter + "Re-Enter season id: ")

    active_appeal = get_appeal_by_season_query(int(season_id))

    petitions_data = get_all_won_petitions_by_appeal_id_query(active_appeal['id'])
    if not petitions_data:
        print(error+"No won petitions found.")
        return None

    won_petitions = list()
    for petition in petitions_data:
        petition_printer(petition)
        print("-"*20)
        won_petitions.append(petition['id'])

    petition_id = input(enter+"Enter petition id for full info: ")
    while petition_id not in str(won_petitions):
        print(error+"Petition not found.")
        petition_id = input(re_enter+"Re-Enter petition id: ")

    full_petition_viewer(int(petition_id))

    return None


def view_all_lost_petitions() -> None:
    """
    Views all lost petitions for the active appeal.
    """
    seasons = get_all_seasons_query()
    active_season = get_active_season_query()
    if active_season is None:
        active_season = dict()

    for season in seasons:
        if season['id'] == active_season.get('id'):
            active_season_str = "Active"
        else:
            active_season_str = "Inactive"

        print(f"Season {season['id']}: {season['start_date']} - {season['end_date']} ({active_season_str})")
        print("-"*20)

    season_id = input(enter+"Enter season id: ")
    while not get_season_by_id_query(int(season_id)):
        print(error+"Season not found.")
        season_id = input(re_enter+"Re-Enter season id: ")

    active_appeal = get_appeal_by_season_query(int(season_id))

    petitions_data = get_all_lost_petitions_by_appeal_id_query(active_appeal['id'])
    if not petitions_data:
        print(error+"No lost petitions found.")
        return None

    lost_petitions = list()
    for petition in petitions_data:
        petition_printer(petition)
        print("-" * 20)
        lost_petitions.append(petition['id'])

    petition_id = input(enter + "Enter petition id for full info: ")
    while petition_id not in str(lost_petitions):
        print(error+"Petition not found.")
        petition_id = input(re_enter+"Re-Enter petition id: ")

    full_petition_viewer(int(petition_id))

    return None


def get_total_voices() -> None:
    """
    Gets the total number of voices cast in the active appeal.
    """
    active_appeal = get_all_petitions_query()
    if len(active_appeal) == 0:
        print(error+"No petitions found.")
        return None

    total_voices = get_total_voices_query()
    if total_voices[0] is None:
        total_voices[0] = 0

    print(prints+f"Total voices: {total_voices[0]}")
    return None


def get_total_voices_for_active_appeal() -> None:
    """
    Gets the total number of voices cast in the active appeal.
    """
    active_season = get_active_season_query()
    if active_season is None:
        print(error+"No active season found.")
        return None

    active_appeal = get_appeal_by_season_query(active_season['id'])

    total_voices = get_total_voices_by_appeal_id_query(active_appeal['id'])
    print(prints+f"Total voices for active appeal: {total_voices}")
    return None


# USER MANAGEMENT

def remove_user() -> None:
    """
    Removes a user from the system.
    """
    view_all_users()

    user_id = input(enter+"Enter user id: ")
    if not get_user_by_id_query(int(user_id)):
        print(error+"User not found.")
        return None

    delete_user_query(int(user_id))
    print(success+"User removed successfully.")
    return None


def view_all_users() -> None:
    """
    Views all users in the system.
    """
    users_data = get_all_users_query()
    if not users_data:
        print(error+"No users found.")
        return None

    for user in users_data:
        user_printer(user)
        print("-"*20)


def view_user_details() -> None:
    """
    Views detailed information about a user.
    """
    view_all_users()

    user_id = input(enter+"Enter user id: ")
    user_data = get_user_by_id_query(int(user_id))
    if user_data is None:
        print(error+"User not found.")
        return None

    user_printer(user_data)
    print("-"*20)

    return None


def update_user_details() -> None:
    """
    Updates user details.
    """
    view_all_users()

    user_id = input(enter+"Enter user id: ")
    if not get_user_by_id_query(int(user_id)):
        print(error+"User not found.")
        return None

    first_name = input(enter+"Enter New First Name or Tap Enter to Skip: ")
    last_name = input(enter+"Enter New Last Name or Tap Enter to Skip: ")
    password = input(enter+"Enter New Password or Tap Enter to Skip: ")

    if not first_name:
        first_name = get_user_by_id_query(int(user_id))['first_name']

    if not last_name:
        last_name = get_user_by_id_query(int(user_id))['last_name']

    if not password:
        password = get_user_by_id_query(int(user_id))['password']

    update_user_query(int(user_id), first_name, last_name, password)

    print(success+"User details updated successfully.")

    return None


def view_all_user_for_votes() -> None:
    """
    Views all users for casting votes.
    """
    users_data = get_all_user_for_votes_query()
    if not users_data:
        print(error+"No users found.")
        return None

    for user in users_data:
        print(prints+f"ID: {user['id']}. Email: {get_email_by_id_query(user['email_id'])}\n"
              f"Phone Number {get_phone_number_by_id_query(user['phone_number_id'])}. Regsitered At: {user['created_at']}")

    return None


# REGION&CITY MANAGEMENT

def remove_region() -> None:
    """
    Removes a region from the system.
    """
    for region in get_all_regions_query():
        region_printer(region)

    region_id = input(enter+"Enter region id: ")
    if not get_region_by_id_query(int(region_id)):
        print(error+"Region not found.")
        return None

    delete_region_query(int(region_id))
    print(success+"Region removed successfully.")
    return None


def add_region() -> None:
    """
    Adds a new region to the system.
    """
    name = input(enter+"Enter region name: ")

    if get_region_by_name_query(name):
        print(error+"Region already exists.")
        return None

    insert_region_query(name)
    print(success+"Region added successfully.")
    return None


def edit_region() -> None:
    """
    Edits a region in the system.
    """
    for region in get_all_regions_query():
        region_printer(region)

    region_id = input(enter+"Enter region id: ")
    region_data = get_region_by_id_query(int(region_id))
    if region_data is None:
        print(error+"Region not found.")
        return None

    name = input(enter+"Enter new region name or Tap Enter to Skip: ")
    if not name:
        name = region_data['name']

    update_region_name_query(int(region_id), name)
    print(success+"Region details updated successfully.")
    return None


def view_all_regions() -> None:
    """
    Views all regions in the system.
    """
    for region in get_all_regions_query():
        region_printer(region)

    return None


def remove_city() -> None:
    """
    Removes a city from the system.
    """
    for region in get_all_regions_query():
        region_printer(region)

    region_id = input(enter+"Enter region id: ")
    region_data = get_region_by_id_query(int(region_id))
    if region_data is None:
        print(error+"Region not found.")
        return None

    for city in get_cities_by_region_query(int(region_id)):
        city_printer(city)

    city_id = input(enter+"Enter city id: ")
    if not get_city_by_id_query(int(city_id)):
        print(error+"City not found.")
        return None

    delete_city_query(int(city_id))
    print(success+"City removed successfully.")
    return None


def add_city() -> None:
    """
    Adds a new city to the system.
    """
    for region in get_all_regions_query():
        region_printer(region)

    region_id = input(enter+"Enter region id: ")
    region_data = get_region_by_id_query(int(region_id))
    if region_data is None:
        print(error+"Region not found.")
        return None

    name = input(enter+"Enter city name: ")

    if get_city_by_name_query(name):
        print(error+"City already exists in this region.")
        return None

    insert_city_query(name, int(region_id))
    print(success+"City added successfully.")
    return None


def edit_city() -> None:
    """
    Edits a city in the system.
    """
    for region in get_all_regions_query():
        region_printer(region)

    region_id = input(enter+"Enter region id: ")
    region_data = get_region_by_id_query(int(region_id))
    if region_data is None:
        print(error+"Region not found.")
        return None

    for city in get_cities_by_region_query(int(region_id)):
        city_printer(city)

    city_id = input(enter+"Enter city id: ")
    city_data = get_city_by_id_query(int(city_id))
    if city_data is None:
        print(error+"City not found.")
        return None

    name = input(enter+"Enter new city name or Tap Enter to Skip: ")
    if not name:
        name = city_data['name']

    update_city_name_query(int(city_id), name)
    print(success+"City details updated successfully.")
    return None


def view_all_cities() -> None:
    """
    Views all cities in the system.
    """
    for region in get_all_regions_query():
        region_printer(region)

    region_id = input(enter+"Enter region id: ")
    region_data = get_region_by_id_query(int(region_id))
    if region_data is None:
        print(error+"Region not found.")
        return None

    for city in get_cities_by_region_query(int(region_id)):
        city_printer(city)

    return None


# CATEGORY MANAGEMENT

def remove_category() -> None:
    """
    Removes a category from the system.
    """
    for category in get_all_categories_query():
        category_printer(category)

    category_id = input(enter+"Enter category id: ")
    if not get_category_by_id_query(int(category_id)):
        print(error+"Category not found.")
        return None

    delete_category_query(int(category_id))
    print(success+"Category removed successfully.")
    return None


def add_category() -> None:
    """
    Adds a new category to the system.
    """
    name = input(enter+"Enter category name: ")

    if get_category_by_name_query(name):
        print(error+"Category already exists.")
        return None

    insert_category_query(name)
    print(success+"Category added successfully.")
    return None


def edit_category() -> None:
    """
    Edits a category in the system.
    """
    for category in get_all_categories_query():
        category_printer(category)

    category_id = input(enter+"Enter category id: ")
    category_data = get_category_by_id_query(int(category_id))
    if category_data is None:
        print(error+"Category not found.")
        return None

    name = input(enter+"Enter new category name or Tap Enter to Skip: ")
    if not name:
        name = category_data['name']

    update_category_name_query(int(category_id), name)
    print(success+"Category details updated successfully.")
    return None


def view_all_categories() -> None:
    """
    Views all categories in the system.
    """
    for category in get_all_categories_query():
        category_printer(category)

    return None


# STATISTICS

def view_total_voices_for_categories():
    """
    Views total votes for each category.
    """
    categories_data = get_all_categories_query()
    if not categories_data:
        print(error+"No categories found.")
        return None

    total_votes = get_total_votes_by_category_query()
    for category in total_votes:
        print(prints+f"Category ID: {category['id']}. Name: {category['name']} - Total Votes: {category['total_votes']}")

    return None


def view_total_voices_for_cities():
    """
    Views total votes for each city.
    """
    cities_data = get_all_cities_query()
    if not cities_data:
        print(error+"No cities found.")
        return None

    total_votes = get_total_votes_by_city_query()
    for city in total_votes:
        print(prints+f"City ID: {city['id']}. Name: {city['name']} - Total Votes: {city['total_votes']}")

    return None


def view_total_voices_for_regions():
    """
    Views total votes for each region.
    """
    regions_data = get_all_regions_query()
    if not regions_data:
        print(error+"No regions found.")
        return None

    total_votes = get_total_votes_by_region_query()
    for region in total_votes:
        print(prints+f"Region ID: {region[0]}. Name: {region[1]} - Total Votes: {region[2]}")

    return None
