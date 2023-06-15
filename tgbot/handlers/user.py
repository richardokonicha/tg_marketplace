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
    

def make_category(message: Message, bot: TeleBot):
    message_text = message.text.split(" ")[1]
    category = db.get_category(message_text)
    if category:
        return bot.send_message(message.chat.id, f"Can't create new category: {message_text} Already Exist")
    else:
        category = db.create_category(category_name = message_text)
        return bot.send_message(message.chat.id, f"New Category: {message_text} Added!")
    