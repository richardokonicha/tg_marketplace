from telebot import TeleBot
from telebot.types import Message
from tgbot.models import db


def make_vendor(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    name = message.from_user.full_name
    db.update_user(user_id=user_id, is_vendor=True)
    bot.send_message(message.chat.id, f"{name}, is now a vendor!")


def make_regular_user(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    name = message.from_user.full_name
    db.update_user(user_id=user_id, is_vendor=False)
    bot.send_message(message.chat.id, f"{name}, is now a regular user!")
