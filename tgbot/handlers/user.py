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
    
    
def removecategory(message: Message, bot: TeleBot):
    try:
        message_text = message.text.split(" ")[1]
    except IndexError:
        return bot.send_message(message.chat.id, "Invalid Category: Use the format /removecategory <category_name>")
        
    try:
        category = db.get_category(message_text)
        category.delete()
        return bot.send_message(message.chat.id, f"Category: {message_text} removed!")
    except:
        category = None
        return bot.send_message(message.chat.id, f"Category: {message_text} does not exist.")
        

def make_category(message: Message, bot: TeleBot):
    try:
        message_text = message.text.split(" ")[1]
    except IndexError:
        return bot.send_message(message.chat.id, "Invalid Category: Use the format /newcategory <category_name>")
        
    try:
        category = db.get_category(message_text)
    except:
        category = None

    if category:
        return bot.send_message(message.chat.id, f"Can't create new category: {message_text} already exists")
    else:
        category = db.create_category(category_name=message_text.lower())
        return category and bot.send_message(message.chat.id, f"New Category: {message_text} Added!")
