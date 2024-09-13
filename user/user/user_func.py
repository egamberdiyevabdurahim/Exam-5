from queries.for_category import get_all_categories_query, get_category_by_id_query
from queries.for_city import get_cities_by_region_query, get_city_by_id_query
from queries.for_email import get_email_by_email_query, insert_email_query, get_all_emails_query
from queries.for_phone_number import insert_phone_number_query, get_all_phone_numbers_query, \
    get_phone_number_by_phone_number_query
from queries.for_region import get_all_regions_query, get_region_by_id_query
from queries.for_season import get_active_season_query, get_last_season_query
from queries.for_user_for_vote import get_user_for_vote_by_email_id_query, insert_user_for_vote_query
from queries.for_users import get_user_by_email_id_query
from queries.for_voice import insert_voice_query, get_all_voices_by_user_id_query, \
    get_all_voices_by_user_for_vote_id_query
from queries.for_vote import get_vote_by_season_query, add_vote_to_total_votes_query
from queries.for_appeal import get_appeal_by_season_query
from queries.for_petition import get_all_accepted_petitions_by_appeal_id_query, get_petition_by_id_query, \
    insert_petition_query, get_all_petitions_by_user_id_query, get_all_petitions_by_appeal_id_query, \
    get_all_accepted_petitions_by_user_id_query, get_all_rejected_petitions_by_user_id_query, \
    get_pending_petition_by_user_id_query, get_all_won_petitions_by_user_id_query, \
    get_all_lost_petitions_by_user_id_query, \
    get_total_voices_by_user_id_query, get_all_petitions_by_category_id_query, update_total_voices_query

from user.admin.admin_func import full_petition_viewer

from utils.additions import email_details, phone_details
from utils.for_confirmation import send_confirmation
from utils.printer import petition_printer
from utils.for_beautiful_terminal import init, error, enter, re_enter, success, prints

init(autoreset=True)


def vote(email: str) -> None:
    """
    Handles the voting process for a user.
    """
    season_data = get_active_season_query()
    if season_data is None:
        print(error+"No active season found.")
        return None

    active_vote = get_vote_by_season_query(season_data['id'])
    if active_vote is None:
        print(error+"Voting For Season Not Started!")
        return None

    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    appeal_data = get_appeal_by_season_query(season_data['id'])
    petitions_data = get_all_accepted_petitions_by_appeal_id_query(appeal_data['id'])

    voices_data = get_all_voices_by_user_id_query(user_data['id'])
    if voices_data is None:
        pass

    else:
        for voice in voices_data:
            if voice['vote_id'] == active_vote['id']:
                print(error+"You have already voted for this season.")
                return None

    categories = get_all_categories_query()
    print("Choose a category:")
    for category in categories:
        is_exists = get_all_petitions_by_category_id_query(category_id=category['id'])
        if is_exists:
            print(prints+f"{category['id']}. {category['name']}")

    category_id = input(enter+"Enter the category ID: ")
    while not get_category_by_id_query(int(category_id)):
        print(error+"Invalid category ID. Please try again.")
        category_id = input(re_enter+"Re-Enter the category ID: ")

    listed_data = list()
    for petition in petitions_data:
        if petition['category_id'] == int(category_id):
            petition_printer(petition)
            print(prints+f"\nTotal Votes: {petition['total_voices']}")
            print(""*20)
            listed_data.append(petition['id'])

    petition_id = input(enter+"Enter the petition ID you want to vote for: ")
    while petition_id not in str(listed_data):
        print(error+"Invalid petition ID. Please try again.")
        petition_id = input(re_enter+"Re-Enter the petition ID you want to vote for: ")

    insert_voice_query(vote_id=active_vote['id'], petition_id=int(petition_id), user_id=user_data['id'])
    add_vote_to_total_votes_query()
    update_total_voices_query(int(petition_id))
    print(success+f"Vote for petition ID: {petition_id} submitted successfully!")
    return None


def view_my_votes(email: str) -> None:
    """
    Views the votes submitted by a user.
    """
    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    voices = get_all_voices_by_user_id_query(user_data['id'])
    if not voices:
        print(error+"No votes found.")
        return None

    voiced_data = list()
    for voice in voices:
        petition_data = get_petition_by_id_query(voice['petition_id'])
        petition_printer(petition_data)
        print("-"*20)
        voiced_data.append(petition_data['id'])

    petition_id = input(enter+"Enter petition ID to get all info: ")
    while petition_id not in str(voiced_data):
        print(error+"Invalid petition ID. Please try again.")
        petition_id = input(re_enter+"Re-Enter the petition ID to get all info: ")

    full_petition_viewer(int(petition_id))

    return None


def vote_with_another_number() -> None:
    """
    Allows a user to vote for another number.
    """
    season_data = get_active_season_query()
    if season_data is None:
        print(error+"No active season found.")
        return None

    active_vote = get_vote_by_season_query(season_data['id'])
    if active_vote is None:
        print(error+"Voting For Season Not Started!")
        return None

    email = input(enter+"Enter email for voting user: ")
    while not email.endswith(email_details):
        print(error+"Invalid email address. Please enter a valid email address.")
        email = input(re_enter+"Re-Enter email for voting user: ")

    phone_number = input(enter+"Enter phone number for voting user: ")
    while not phone_number.startswith(phone_details):
        print(error+"Invalid phone number. Please enter a valid phone number.")
        phone_number = input(re_enter+"Re-Enter phone number for voting user: ")

    if email not in [em['email'] for em in get_all_emails_query()]:
        insert_email_query(email)

    if not phone_number in [phone_num['phone_number'] for phone_num in get_all_phone_numbers_query()]:
        insert_phone_number_query(phone_number)

    email_id = get_email_by_email_query(email)
    phone_number_id = get_phone_number_by_phone_number_query(phone_number)
    user_data = get_user_for_vote_by_email_id_query(email_id['id'])
    org_user_data = get_user_by_email_id_query(email_id['id'])
    if user_data is None:
        if org_user_data is not None:
            print(error+"Bunday Emaillik Xaqiqiy User Mavjud Faqat Ovoz Berish Uchun Yasalgan User Emas!")
            return None

        send_confirmation(email)

        insert_user_for_vote_query(email_id['id'], phone_number_id['id'])
        user_data = get_user_for_vote_by_email_id_query(email_id['id'])

    appeal_data = get_appeal_by_season_query(season_data['id'])
    petitions_data = get_all_accepted_petitions_by_appeal_id_query(appeal_data['id'])

    voices_data = get_all_voices_by_user_for_vote_id_query(user_data['id'])
    if voices_data is None:
        pass

    else:
        for voice in voices_data:
            if voice['vote_id'] == active_vote['id']:
                print(error+"You have already voted for this season.")
                return None

    categories = get_all_categories_query()
    print("Choose a category:")
    for category in categories:
        is_exists = get_all_petitions_by_category_id_query(category_id=category['id'])
        if is_exists:
            print(prints+f"{category['id']}. {category['name']}")

    category_id = input(enter+"Enter the category ID: ")
    while not get_category_by_id_query(int(category_id)):
        print(error+"Invalid category ID. Please try again.")
        category_id = input(re_enter+"Re-Enter the category ID: ")

    listed_data = list()
    for petition in petitions_data:
        if petition['category_id'] == int(category_id):
            petition_printer(petition)
            print(prints+f"\nTotal Votes: {petition['total_voices']}")
            print("" * 20)
            listed_data.append(petition['id'])

    petition_id = input(enter+"Enter the petition ID you want to vote for: ")
    while int(petition_id) not in listed_data:
        print(error+"Invalid petition ID. Please try again.")
        petition_id = input(re_enter+"Re-Enter the petition ID you want to vote for: ")

    insert_voice_query(vote_id=active_vote['id'], petition_id=int(petition_id), user_for_vote_id=user_data['id'])
    print(success+f"Vote for petition ID: {petition_id} submitted successfully!")
    add_vote_to_total_votes_query()
    update_total_voices_query(int(petition_id))
    return None


def post_petition(email: str) -> None:
    """
    Allows a user to post a new petition.
    """
    season_data = get_active_season_query()
    if season_data is None:
        print(error+"No active season found.")
        return None

    active_appeal = get_appeal_by_season_query(season_data['id'])
    if active_appeal is None or active_appeal['is_active'] is False:
        print(error+"Appeal for Season Not Started!\n"
              "Or Already Ended!")
        return None

    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    petitions_data = get_all_petitions_by_appeal_id_query(active_appeal['id'])
    if len([petition for petition in petitions_data if petition['user_id'] == user_data['id']]) > 0:
        print(error+"You have already posted a petition for this Season.")
        return None

    petition_title = input(enter+"Enter petition title: ")
    while not petition_title:
        print(error+"Petition title cannot be empty. Please enter a valid title.")
        petition_title = input(re_enter+"Re-Enter petition title: ")

    petition_description = input(enter+"Enter petition description: ")
    while not petition_description:
        print(error+"Petition description cannot be empty. Please enter a valid description.")
        petition_description = input(re_enter+"Re-Enter petition description: ")

    money = input(enter+"Enter money that you need: ")
    while not money.isdigit() or int(money) <= 0:
        print(error+"Invalid money amount. Please enter a valid positive integer.")
        money = input(error+"Re-Enter money that you need: ")

    regions = get_all_regions_query()
    for region in regions:
        print(prints+f"{region['id']}. {region['name']}")

    region_id = input(enter+"Enter region ID for this petition: ")
    while not get_region_by_id_query(int(region_id)):
        print(error+"Invalid region ID. Please try again.")
        region_id = input(re_enter+"Re-Enter region ID for this petition: ")

    cities = get_cities_by_region_query(int(region_id))
    for city in cities:
        print(prints+f"{city['id']}. {city['name']}")

    city_id = input(enter+"Enter city ID for this petition: ")
    while not get_city_by_id_query(int(city_id)):
        print(error+"Invalid city ID. Please try again.")
        city_id = input(re_enter+"Re-Enter city ID for this petition: ")

    categories = get_all_categories_query()
    for category in categories:
        print(prints+f"{category['id']}. {category['name']}")

    category_id = input(enter+"Enter category ID for this petition: ")
    while not get_category_by_id_query(int(category_id)):
        print(error+"Invalid category ID. Please try again.")
        category_id = input(re_enter+"Re-Enter category ID for this petition: ")

    insert_petition_query(title=petition_title, content=petition_description,
                          money=int(money), user_id=user_data['id'], appeal_id=active_appeal['id'],
                          city_id=int(city_id), category_id=int(category_id))
    print(success+"Petition posted successfully!")
    print("Petition is progress to accepting from Admins")

    return None


def view_all_my_petitions(email: str) -> None:
    """
    Views all the petitions submitted by a user.
    """
    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    petitions = get_all_petitions_by_user_id_query(user_data['id'])
    if not petitions:
        print(error+"No petitions found.")
        return None

    petition_data = list()
    for petition in petitions:
        petition_printer(petition)
        print("-"*20)
        petition_data.append(petition['id'])

    petition_id = input(enter+"Enter petition ID to get all info: ")
    while petition_id not in str(petition_data):
        print(error+"Invalid petition ID. Please try again.")
        petition_id = input(re_enter+"Re-Enter the petition ID to get all info: ")

    full_petition_viewer(int(petition_id))

    return None


def my_last_petition_for_last_season(email: str) -> None:
    """
    Views the last petition submitted by a user for the last season.
    """
    season_data = get_last_season_query()
    if season_data is None:
        print(error+"No seasons found.")
        return None

    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    appeal_data = get_appeal_by_season_query(season_data['id'])
    petitions_data = get_all_petitions_by_appeal_id_query(appeal_data['id'])
    if petitions_data is None:
        print(error+"No petition found for last season.")
        return None

    petition_data = [petition for petition in petitions_data if petition['user_id'] == user_data['id']]
    if len(petition_data) == 0:
        print(error+"No petition found of you for last season.")
        return None

    full_petition_viewer(petition_data[0]['id'])

    return None


def get_my_accepted_petitions(email: str) -> None:
    """
    Views all the accepted petitions submitted by a user.
    """
    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    petitions = get_all_accepted_petitions_by_user_id_query(user_data['id'])
    if not petitions:
        print(error+"No accepted petitions found.")
        return None

    petition_data = list()
    for petition in petitions:
        petition_printer(petition)
        print("-"*20)
        petition_data.append(petition['id'])

    petition_id = input(enter+"Enter petition ID to get all info: ")
    while petition_id not in str(petition_data):
        print(error+"Invalid petition ID. Please try again.")
        petition_id = input(re_enter+"Re-Enter the petition ID to get all info: ")

    full_petition_viewer(int(petition_id))

    return None


def get_my_rejected_petitions(email: str) -> None:
    """
    Views all the accepted petitions rejected by a user.
    """
    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    petitions = get_all_rejected_petitions_by_user_id_query(user_data['id'])
    if not petitions:
        print(error+"No rejected petitions found.")
        return None

    petition_data = list()
    for petition in petitions:
        petition_printer(petition)
        print("-" * 20)

    petition_id = input(enter+"Enter petition ID to get all info: ")
    while petition_id not in str(petition_data):
        print(error+"Invalid petition ID. Please try again.")
        petition_id = input(re_enter+"Re-Enter the petition ID to get all info: ")

    full_petition_viewer(int(petition_id))

    return None


def get_my_pending_petition(email: str) -> None:
    """
    Views the pending petition by a user.
    """
    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    petition = get_pending_petition_by_user_id_query(user_data['id'])
    if not petition:
        print(error+"No pending petition found.")
        return None

    full_petition_viewer(petition['id'])

    return None


def get_my_won_petitions(email: str) -> None:
    """
    Views all the won petitions submitted by a user.
    """
    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    petitions = get_all_won_petitions_by_user_id_query(user_data['id'])
    if not petitions:
        print(error+"No won petitions found.")
        return None

    petition_data = list()
    for petition in petitions:
        petition_printer(petition)
        print("-" * 20)
        petition_data.append(petition['id'])

    petition_id = input(enter+"Enter petition ID to get all info: ")
    while petition_id not in str(petition_data):
        print(error+"Invalid petition ID. Please try again.")
        petition_id = input(re_enter+"Re-Enter the petition ID to get all info: ")

    full_petition_viewer(int(petition_id))

    return None


def get_my_lost_petitions(email: str) -> None:
    """
    Views all the lost petitions submitted by a user.
    """
    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    petitions = get_all_lost_petitions_by_user_id_query(user_data['id'])
    if not petitions:
        print(error+"No lost petitions found.")
        return None

    petition_data = list()
    for petition in petitions:
        petition_printer(petition)
        print("-" * 20)
        petition_data.append(petition['id'])

    petition_id = input(enter+"Enter petition ID to get all info: ")
    while petition_id not in str(petition_data):
        print(error+"Invalid petition ID. Please try again.")
        petition_id = input(re_enter+"Re-Enter the petition ID to get all info: ")

    full_petition_viewer(int(petition_id))

    return None


def get_total_voices_for_all_my_petitions(email: str) -> None:
    """
    Views the total number of voices for all my petitions.
    """
    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    total_voices = get_total_voices_by_user_id_query(user_data['id'])
    if total_voices[0] is None or total_voices[0] == 0:
        print(error+"No voices found.")
        return None
    print(prints+f"Total voices casted for all your petitions: {total_voices[0]}")
    print(prints+f"Average voices per petition: {(total_voices[0]) / len(total_voices)}")

    return None


def get_total_voices_for_last_seasons_my_petition(email: str) -> None:
    """
    Views the total number of voices for all my last season petitions.
    """
    season_data = get_last_season_query()
    if season_data is None:
        print(error+"No seasons found.")
        return None

    email_id = get_email_by_email_query(email)
    user_data = get_user_by_email_id_query(email_id['id'])

    appeal_data = get_appeal_by_season_query(season_data['id'])
    petitions_data = get_all_petitions_by_appeal_id_query(appeal_data['id'])
    if petitions_data is None:
        print(error+"No petition found for last season.")
        return None

    total_voices = [petition['total_voices'] for petition in petitions_data if petition['user_id'] == user_data['id']]
    if len(total_voices) == 0 or total_voices[0] == 0:
        print(error+"No your petitions found for last season.")
        return None

    print(prints+f"Total voices: {total_voices[0]}")
    print(prints+f"Average voices per petition: {int(total_voices[0]) / len(total_voices)}")

    return None
