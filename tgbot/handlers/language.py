from telebot import TeleBot
from telebot.types import Message
from tgbot.utils.buttons import lang_keys
from tgbot.utils.messages import messages

from tgbot.models import db
from .start import start


def show_language(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    select_preferred_lang = messages["select_preferred_lang"]
    bot.send_message(
        chat_id,
        text=select_preferred_lang,
        reply_markup=lang_keys(),
    )


def set_language(message: Message, bot: TeleBot):
    """sets language and returns language value and send user confirmation message"""
    user_id = message.from_user.id
    message_lang = message.text.split()[0].upper()
    language = None
    if message_lang == "ENGLISH":
        language = 'en'
    if message_lang == "РУССКИЙ":
        language = "ru"
    db.set_language(user_id, language)
    start(message, bot)
