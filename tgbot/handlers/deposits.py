from decimal import Decimal, InvalidOperation
from telebot import TeleBot
from telebot.types import Message
from tgbot.models import db
from tgbot.payments import payment_client
from tgbot.utils.messages import messages
from .language import show_language
from .start import start
from tgbot import config
from tgbot.utils import buttons


def generate_address(message, bot, **kwargs):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.send_chat_action(chat_id, action="typing")
    user = db.get_user(user_id)
    promo = message.text.split(" ")[-1]
    try:
        amount = float(promo)
        invoice = payment_client.create_invoice(
            amount=amount,
            user_id=user_id,
            description=f"Deposit of {amount} {config.CURRENCY} from {user.name}",
        )

        deposit_text, keyboard = buttons.deposit_address_markup(user, invoice)
        bot.send_message(
            chat_id,
            text=deposit_text,
            reply_markup=keyboard
        )
    except (ValueError, InvalidOperation):
        bot.send_message(
            chat_id,
            text="Invalid amount",
            reply_markup=buttons.menu_markup(user)
        )


def deposit(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = db.get_user(user_id)
    balance = user.account_balance
    lang = user.language
    message_id = message.message_id
    deposit_text, keyboard = buttons.deposit_markup(user)

    enter_field_value = bot.send_message(
        chat_id=chat_id, text=deposit_text, parse_mode="html", reply_markup=keyboard)

    return bot.register_next_step_handler(
        enter_field_value, generate_address, bot=bot)


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
