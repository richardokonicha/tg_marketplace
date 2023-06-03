from telebot import TeleBot
from telebot.types import Message
from tgbot.utils.messages import messages
# from tgbot.utils.buttons import dashboard
from .start import start
from .language import show_language
from tgbot.models import db


def balance(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.get_user(user_id)
    if fcx_user is None: return start(message, bot)
    if fcx_user.language not in ["en", "it"]: return show_language(message, bot)
    lang = fcx_user.language
    
    try:
        balance_msg = messages["balance_msg"][lang].format(
            balance=fcx_user.account_balance, 
            active_investment=fcx_user.active_investment, 
            active_reinvestment=fcx_user.active_reinvestment, 
            pending_investment=fcx_user.pending_investment
        )
        
        fcx_markup_balances = messages["fcx_markup_balances"]
        dashboard[lang].keyboard[0][0] = fcx_markup_balances[lang].format(account_balance=fcx_user.account_balance)

        if fcx_user.account_balance == 0 and fcx_user.active_investment == 0 and fcx_user.active_reinvestment == 0 and fcx_user.pending_investment == 0:
            no_balance_text = messages["no_balance_text"]
            bot.send_message(chat_id, text=no_balance_text[lang], reply_markup=dashboard.get(lang), parse_mode="html")
        else:
            bot.send_message(chat_id, text=balance_msg, reply_markup=dashboard.get(lang), parse_mode="html")

    except Exception as e:
        error_msg = f"An error occurred: {type(e).__name__}"
        bot.send_message(chat_id, text=error_msg, parse_mode="html")
