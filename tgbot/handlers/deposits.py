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
    fcx_user = db.get_user(user_id)
    
    if not fcx_user: return start(message, bot)
    if fcx_user.language not in ["en", "it"]: return show_language(message, bot)

    balance = fcx_user.account_balance
    lang = fcx_user.language
    fcx_markup_balances = messages["fcx_markup_balances"]
    
    try:
        amount = Decimal(message.text)

        dashboard[lang].keyboard[0][0] = fcx_markup_balances[lang].format(account_balance=fcx_user.account_balance)
        # dashboard[lang].keyboard[0][0] = f"Balances  {fcx_user.account_balance} BTC"
        arrival_text = messages["arrival_text"][lang]
        duration_text = messages["duration_text"][lang]

        if amount < 5:
            bot.send_chat_action(chat_id, action="typing")
            bot.send_message(chat_id, text=arrival_text)

            try:
                payment_details = payment_client.create_transaction({"amount":amount, "currency1":"LTCT", "currency2":"LTCT"})

                pd = payment_details["result"]
                fcx_dp = db.Transactions(
                    user_id=fcx_user.user_id,
                    transaction_type="deposit",
                    amount=pd["amount"]
                )
                fcx_dp.dp_txn_id = pd["txn_id"]
                fcx_dp.dp_address_timeout = pd["timeout"]
                fcx_dp.dp_qrcode_url = pd["qrcode_url"]
                fcx_dp.dp_status = pd["status_url"]
                fcx_dp.dp_address = pd["address"]
                fcx_dp.status = "0"
                fcx_dp.commit()

                bot.send_message(chat_id, text=f"<strong>{pd['address']}</strong>", parse_mode="html")
                bot.send_photo(chat_id, photo=fcx_dp.dp_qrcode_url, caption="Scan QR")
                bot.send_message(chat_id, text=duration_text, reply_markup=dashboard.get(lang))
            
            except TypeError:
                bot.send_message(chat_id, text="An error occurred. You'll be contacted by support to assist you.", reply_markup=dashboard.get(lang))
                bot.send_message(ADMIN_ID, text=f"<strong>{payment_details['error']} for fcx server</strong>", parse_mode="html")
        
        else:
            max_amount_text = messages["max_amount_text"][lang]
            bot.send_message(chat_id, text=max_amount_text, reply_markup=dashboard.get(lang))
    
    except (ValueError):
        bot.send_message(chat_id, text="Invalid amount", reply_markup=dashboard.get(lang))
    except requests.exceptions.ProxyError as e:
        error_message = str(e)
        bot.send_message(
            ADMIN_ID,
            text=f"<strong>Proxy Error:</strong> {error_message}",
            parse_mode="html"
        )

#######################################DEPOSIT HANDLERS ##############################################

def deposit(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    fcx_user = db.get_user(user_id)
    lang = fcx_user.language
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


### Promo code section
def promo(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    fcx_user = db.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    fcx_markup_balances = messages["fcx_markup_balances"]
    dashboard[lang].keyboard[0][0] = fcx_markup_balances[lang].format(account_balance=fcx_user.account_balance)
    promo = message.text.split(" ")[-1]
    try:
        promo = Decimal(promo)
        fcx_user.account_balance += promo
        
        fcx_transact = db.create_transact(
            user_id=fcx_user.user_id,
            transaction_type="deposit",
            amount=promo,
            status="Completed",
            balance=fcx_user.account_balance
        )
        
        db.commit()
        
        dashboard[lang].keyboard[0][0] = fcx_markup_balances[lang].format(account_balance=fcx_user.account_balance)
        bot.send_message(
            chat_id,
            text=f"You've been gifted {promo} virtual btc to test other features",
            reply_markup=dashboard.get(lang)
        )
    except ValueError:
        bot.send_message(
            chat_id,
            text="INVALID PROMO CODE",
            reply_markup=dashboard.get(lang)
        )
