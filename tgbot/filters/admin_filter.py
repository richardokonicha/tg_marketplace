from telebot.custom_filters import SimpleCustomFilter
from tgbot import config


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users
    """

    key = 'admin'
    def check(self, message):

        return int(message.chat.id) == int(config.ADMIN_ID)