from decimal import Decimal
from telebot import TeleBot
from telebot.types import Message
from tgbot.models import db
from tgbot.payments import payment_client
from tgbot.utils.messages import messages
from .language import show_language
from .start import start

def promo(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = db.get_user(user_id)
    balance = user.account_balance
    lang = user.language
    promo = message.text.split(" ")[-1]

    amount = float(promo)
    invoice = payment_client.create_invoice(
        amount=amount,
        description="Deposit of {amount} USD from {user.name}"
    )

    try:
        promo = Decimal(promo)
        new_balance = user.account_balance + promo
        db.update_user(user_id=user_id, account_balance=new_balance)

        bot.send_message(
            chat_id,
            text=f"You've deposited {promo}",
        )
    except ValueError:
        bot.send_message(
            chat_id,
            text="INVALID PROMO CODE",
        )
