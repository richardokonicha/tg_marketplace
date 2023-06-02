from telebot import TeleBot
from telebot.types import Message
from tgbot import config
from tgbot.utils.messages import messages
# from tgbot.utils.buttons import confirm_order
from tgbot.models import db


def enter_address(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_id = message.message_id + 1
    fcx_user = db.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    amount = message.text
    try:
        amount = Decimal(amount)
        if amount > balance:
            insufficient_funds = messages["insufficient_funds"][lang]
            bot.send_message(
                chat_id,
                text=insufficient_funds,
                parse_mode="html",
                reply_markup=force_r
            )
            bot.register_for_reply_by_message_id(
                message_id,
                enter_address
            )
        else:
            try:
                set_wallet_address_text = messages["set_wallet_address_text"][lang]

                bot.send_message(
                    chat_id,
                    text=set_wallet_address_text,
                    parse_mode="html",
                    reply_markup=force_r
                )
                bot.register_for_reply_by_message_id(
                    message_id,
                    withdrawal_confirmation,
                    (amount)
                )
            except KeyError:
                bot.send_message(
                    chat_id, text="Invalid wallet address", parse_mode="html")
                set_wallet_address(message)
    except (ValueError, InvalidOperation) as e:
        invalid_amount = messages["invalid_amount"][lang]
   
        bot.send_message(
            chat_id,
            text=invalid_amount,
            parse_mode="html",
            reply_to_message_id=message.message_id,
            reply_markup=force_r
        )
        bot.register_for_reply_by_message_id(
            message_id,
            enter_address
        )


def withdrawal_confirmation(message, amount):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    wallet_address = message.text
    regex_filter = '^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
    if re.match(regex_filter, wallet_address):
        withdraw_address_confirmation = messages["withdraw_address_confirmation"][lang].format(
            amount=amount,
            wallet_address=wallet_address
        )

        bot.send_message(
            chat_id, text=withdraw_address_confirmation, parse_mode="html", reply_markup=confirm_order[lang])
    else:
        invalid_address = messages["invalid_address"][lang]
   
        bot.send_message(
            chat_id,
            text=invalid_address,
            reply_markup=dashboard[lang],
            parse_mode="html"
        )

def withdrawal(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_id = message.message_id + 2
    fcx_user = db.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    withdrawal_minimum_amount = config.WITHDRAWAL_MINIMUM_AMOUNT
    withdrawal_amount_text = messages["withdrawal_amount_text"][lang]
    withdrawal_info = messages["withdrawal_info"][lang]
    insufficient_funds = messages["insufficient_funds"][lang]
    
    if balance < withdrawal_minimum_amount:
        bot.send_message(
            chat_id, text=withdrawal_info + insufficient_funds,
            reply_markup=dashboard[lang], parse_mode="html"
        )
    else:
        bot.send_message(
            chat_id,  reply_to_message_id=message.message_id,
            text=withdrawal_info,
            # reply_markup=force_r,
            parse_mode="html"
        )
        bot.send_message(
            chat_id,
            text=withdrawal_amount_text,
            parse_mode="html",
            reply_markup=force_r
        )
        bot.register_for_reply_by_message_id(message_id, enter_address)
