from telebot import TeleBot
from telebot.types import Message
from tgbot.models import db
from tgbot.utils.buttons import list_menu_keys
from tgbot import config
from tgbot.utils.messages import messages
from decimal import Decimal

def process_reinvest(message):
    pass

def verify_reinvest(message, **kwargs):
    bot = kwargs.get("bot")
    markup = kwargs.get("markup")

    user_id = message.from_user.id
    user = db.get_user(user_id)
    chat_id = message.chat.id
    reply_from = message.reply_to_message.text
    if reply_from in ["Please enter the amount to reinvest:", "Per favore inserire l'importo da reinvestire:"]:
        balance = user.account_balance
        lang = user.language
        try:
            reinvestment_amount = Decimal(message.text)
            if reinvestment_amount > balance:
                text_insufficient = messages["text_insufficient"][lang]
                bot.reply_to(
                    message,
                    text=text_insufficient,
                    reply_markup=markup
                )
            elif reinvestment_amount < 0:
                invalid_amount = messages["invalid_amount"][lang]
                bot.reply_to(
                    message,
                    text=invalid_amount,
                    reply_markup=markup
                )
            else:
                investment_confirmation = messages["investment_confirmation"][lang].format(
                    reinvestment_amount=reinvestment_amount)
                bot.send_message(
                    chat_id,
                    text=investment_confirmation,
                    reply_markup=confirm_reinvestment[lang]
                )
        except ValueError as err:
            invalid_amount = messages["invalid_amount"][lang]
            bot.reply_to(
                message,
                text=invalid_amount,
                reply_markup=dashboard[lang]
            )

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
   
    # dashboard[lang].keyboard[0][0] = markup_balances[lang].format(
    #     account_balance=user.account_balance)

    # reinvest_info = messages["reinvest_infhttps://mybestwine.ch/wp-content/uploads/2015/07/2015-07-b-.jpg-1200-x-400.jpgo"][lang]
    # reinvest_insufficient = messages["reinvest_insufficient"][lang]
    # reinvest_enter_amount = messages["reinvest_enter_amount"][lang]

    # if user.account_balance < config.WITHDRAWAL_MINIMUM_AMOUNT:
    #     bot.send_message(
    #         chat_id, text=reinvest_info + reinvest_insufficient,
    #         reply_markup=dashboard[lang], parse_mode="html"
    #     )
    # else:
    #     bot.send_message(
    #         chat_id,
    #         text=reinvest_info
    #     )
    #     bot.send_message(
    #         chat_id,
    #         text=reinvest_enter_amount,
    #         parse_mode="html",
    #         reply_markup=force_r
    #     )
    #     bot.register_next_step_handler(
    #         message, verify_reinvest, bot=bot, markup=dashboard[lang])
