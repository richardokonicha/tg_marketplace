from telebot import TeleBot
from telebot.types import Message
from tgbot.models import db
from tgbot.utils.buttons import list_menu_keys
from tgbot import config
from tgbot.utils.messages import messages


def menu(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = db.get_user(user_id)
    lang = user.language

    markup_balances = messages["markup_balances"][lang].format(account_balance=user.account_balance)

    bot.send_photo(
        chat_id=chat_id,
        photo=config.MENU_PHOTO,
        reply_markup=list_menu_keys,
        caption=markup_balances
    )