import datetime
from tgbot import config
import base64

import re

def extract_links(text):
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # Alternatively, you can use the following pattern if you want to match www.example.com links as well:
    # pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F])|\w+\.[\w.]+)+'
    
    matches = re.findall(pattern, text)
    return matches

def send_notification(message):
    print("Notification:", message)


def message_age_filter_func(call):

    current_time = datetime.datetime.now()
    message_time = call.message.date
    datetime_obj = datetime.datetime.fromtimestamp(message_time)
    time_difference = current_time - datetime_obj
    minutes_difference = time_difference.total_seconds() / 60

    if minutes_difference > config.MAX_MESSAGE_AGE_MINUTES:
        return False
    # try:
    #     bot.answer_callback_query(
    #         call.id, text=f"Too old")
    # except:
    #     pass

    if call.message.content_type == 'callback_query' and minutes_difference > config.MAX_CALLBACK_AGE_MINUTES:
        send_notification("Callback from an old message triggered")

    return True


def get_user_profile_photo_url(user_id, bot):
    photos = bot.get_user_profile_photos(user_id=user_id)
    if photos.total_count > 0:
        photo = photos.photos[0][0]
        file_id = photo.file_id
        file = bot.get_file(file_id)
        photo_url = file.file_path

        with open(photo_url, "rb") as photo_file:
            base64_data = base64.b64encode(photo_file.read()).decode("utf-8")

        src = f"data:image/png;base64,{base64_data}"

        return src

    return None
