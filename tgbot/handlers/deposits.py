from decimal import Decimal
from telebot import TeleBot
from telebot.types import Message
from tgbot.models import db
from tgbot.payments import payment_client
# from tgbot.utils.buttons import force_r, dashboard
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

        invoice_id = invoice['id']
        invoice_link = invoice['checkoutLink']
        invoice_amount = invoice['amount']
        invoice_currency = invoice['currency']

        qr_code = invoice['receipt']['showQR']

        bot.send_message(
            chat_id,
            text=f"You're depositing {promo} {invoice_currency}.\n\n"
                 f"Please proceed with the payment by clicking the following link:\n"
                 f"{invoice_link}\n\n"
                 f"Make sure to complete the payment of {invoice_amount} {invoice_currency} within the provided expiration time."
        )

        if qr_code:
            bot.send_photo(
                chat_id,
                photo=qr_code,
                caption="Scan the QR code to make the payment."
            )

    except ValueError:
        bot.send_message(
            chat_id,
            text="INVALID PROMO CODE",
        )
