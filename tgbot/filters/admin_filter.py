from telebot.custom_filters import SimpleCustomFilter
from tgbot import config
import datetime


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users
    """
    key = 'admin'

    def check(self, message):

        return int(message.chat.id) == int(config.ADMIN_ID)


class MessageAgeFilter(SimpleCustomFilter):
    key = 'message_age'

    def check(self, message):
        current_time = datetime.datetime.now()
        message_time = message.date
        time_difference = current_time - message_time
        minutes_difference = time_difference.total_seconds() / 60

        if minutes_difference > config.MAX_MESSAGE_AGE_MINUTES:
            return False

        if message.content_type == 'callback_query' and minutes_difference > config.MAX_CALLBACK_AGE_MINUTES:
            send_notification("Callback from an old message triggered")

        return True


def send_notification(message):
    print("Notification:", message)
