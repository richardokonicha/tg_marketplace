from telebot import TeleBot
from telebot.types import Message
from tgbot.models import db
from tgbot.utils.messages import messages
from tgbot.utils.buttons import lang_keys, passive_menu


def start(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name
    user = db.get_user(user_id)
    select_preferred_lang = messages["select_preferred_lang"]
    welcome_text = messages["welcome_text"]

    if user is not None:
        lang = user.language
        if lang == None or lang not in ['en', 'it']:
            bot.send_message(
                chat_id,
                text=select_preferred_lang,
                reply_markup=lang_keys,
                parse_mode="HTML"
            )
        else:
            bot.send_message(
                chat_id,
                text=welcome_text[lang],
                reply_markup=passive_menu[lang],
                parse_mode="HTML"
            )
    else:
        user = db.create_user(
            name=name,
            user_id=user_id,
            username=username
        )
        bot.send_message(
            chat_id,
            text=select_preferred_lang,
            reply_markup=lang_keys,
            parse_mode="HTML"
        )
