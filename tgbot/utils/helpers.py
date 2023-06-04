import datetime
from tgbot import config


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
