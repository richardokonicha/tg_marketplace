from decimal import Decimal
from telebot import TeleBot
from telebot.types import Message
from tgbot.models import db
from tgbot.payments import payment_client
# from tgbot.utils.buttons import force_r, dashboard
from tgbot.utils.messages import messages
from .language import show_language
from .start import start


def generate_address(message, **kwargs):
    bot = kwargs.get("bot")
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = db.get_user(user_id)

    if not user:
        return start(message, bot)
    if user.language not in ["en", "it"]:
        return show_language(message, bot)

    balance = user.account_balance
    lang = user.language
    markup_balances = messages["markup_balances"]

    try:
        amount = Decimal(message.text)

        dashboard[lang].keyboard[0][0] = markup_balances[lang].format(
            account_balance=user.account_balance)
        # dashboard[lang].keyboard[0][0] = f"Balances  {user.account_balance} BTC"
        arrival_text = messages["arrival_text"][lang]
        duration_text = messages["duration_text"][lang]

        if amount < 5:
            bot.send_chat_action(chat_id, action="typing")
            bot.send_message(chat_id, text=arrival_text)

            try:
                payment_details = payment_client.create_transaction(
                    {"amount": amount, "currency1": "LTCT", "currency2": "LTCT"})

                pd = payment_details["result"]
                dp = db.Transactions(
                    user_id=user.user_id,
                    transaction_type="deposit",
                    amount=pd["amount"]
                )
                dp.dp_txn_id = pd["txn_id"]
                dp.dp_address_timeout = pd["timeout"]
                dp.dp_qrcode_url = pd["qrcode_url"]
                dp.dp_status = pd["status_url"]
                dp.dp_address = pd["address"]
                dp.status = "0"
                dp.commit()

                bot.send_message(
                    chat_id, text=f"<strong>{pd['address']}</strong>", parse_mode="html")
                bot.send_photo(chat_id, photo=dp.dp_qrcode_url,
                               caption="Scan QR")
                bot.send_message(chat_id, text=duration_text,
                                 reply_markup=dashboard.get(lang))

            except TypeError:
                bot.send_message(
                    chat_id, text="An error occurred. You'll be contacted by support to assist you.", reply_markup=dashboard.get(lang))
                bot.send_message(
                    ADMIN_ID, text=f"<strong>{payment_details['error']} for fcx server</strong>", parse_mode="html")

        else:
            max_amount_text = messages["max_amount_text"][lang]
            bot.send_message(chat_id, text=max_amount_text,
                             reply_markup=dashboard.get(lang))

    except (ValueError):
        bot.send_message(chat_id, text="Invalid amount",
                         reply_markup=dashboard.get(lang))
    except requests.exceptions.ProxyError as e:
        error_message = str(e)
        bot.send_message(
            ADMIN_ID,
            text=f"<strong>Proxy Error:</strong> {error_message}",
            parse_mode="html"
        )

####################################### DEPOSIT HANDLERS ##############################################


def deposit(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = db.get_user(user_id)
    lang = user.language
    message_id = message.message_id
    deposit_amount_text = messages["deposit_amount_text"][lang]
    bot.send_message(
        chat_id,
        text=deposit_amount_text,
        parse_mode="html",
        reply_markup=force_r
    )
    nxt = message_id + 1
    bot.register_for_reply_by_message_id(
        nxt,
        generate_address,
        bot=bot
    )


# Promo code section
def promo(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = db.get_user(user_id)
    balance = user.account_balance
    lang = user.language
    promo = message.text.split(" ")[-1]
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
