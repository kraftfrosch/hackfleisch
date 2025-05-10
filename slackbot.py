import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)

def send_slack_message(user_id, message):
    try:
        response = client.chat_postMessage(
            channel=user_id,
            text=message
        )
        print("Message sent:", response["ts"])
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")


def get_user_id_by_email(email):
    try:
        response = client.users_lookupByEmail(email=email)
        return response["user"]["id"]
    except SlackApiError as e:
        print(f"Error fetching user ID: {e.response['error']}")
        return None

def send_link_to_users(users, link, feedbacked_user_name):
    message = f"Hi there! Please take some time to jump on a call and give some feedback on {feedbacked_user_name}. Here is the link: {link}"
    for user in users:
        user_id = get_user_id_by_email(user)
        if user_id:
            send_slack_message(user_id, message)
        else:
            print(f"User {user} not found.")

def confirm_feedback(originator_email, user_email, feedbacked_user_email):
    originator_id = get_user_id_by_email(originator_email)
    user_id = get_user_id_by_email(user_email)
    feedbacked_user_id = get_user_id_by_email(feedbacked_user_email)
    message_originator = f"Hi there! <@{user_id}> has just completed their feedback on <@{feedbacked_user_id}>."
    message_user = f"Hi there! Thank you for giving feedback on <@{feedbacked_user_id}>."
    send_slack_message(originator_id, message_originator)
    send_slack_message(user_id, message_user)