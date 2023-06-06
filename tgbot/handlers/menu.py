from tgbot.utils import buttons
from telebot import TeleBot
from telebot.types import Message
from tgbot.models import db
from tgbot.utils.buttons import list_menu_keys
from tgbot import config
from tgbot.utils.messages import messages
from tgbot.handlers.start import start


def menu(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = db.get_user(user_id)
    if user == None:
        return start(message, bot)
    media, keyboard = buttons.menu_markup(user)

    bot.send_photo(chat_id=chat_id, photo=media.media,
                   caption=media.caption, reply_markup=keyboard)


def back_to_menu(call, bot):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    user = db.get_user(user_id)
    if user == None:
        return start(call.message, bot)
    media, keyboard = buttons.menu_markup(user)
    bot.edit_message_media(
        chat_id=chat_id,
        message_id=message_id,
        media=media,
        reply_markup=keyboard
    )


def exit_view(call, bot):
    message_id = call.message.message_id
    chat_id = call.message.chat.id
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass
