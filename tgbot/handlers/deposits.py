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
from telebot.apihelper import ApiException
from tgbot.handlers.menu import show_menu



def handle_invoice_created_webhook(data, bot):
    deposit = db.update_deposit_by_invoice_id(invoice_id=data['invoiceId'], event_type=data['type'], status="created", updated_at=data['timestamp'])
    try:
        print('created webhook')

    except KeyError:
        print('No user id linked to this webhook, ignoring')
    except Exception as e:
        print(f"An error occurred: {e}")


def handle_invoice_paid_webhook(data, bot):
    deposit = db.update_deposit_by_invoice_id(
        invoice_id=data['invoiceId'], 
        event_type=data['type'], 
        status="settled", 
        updated_at=data['timestamp'],
        )
    if deposit.event_type == 'InvoicePaymentSettled':
        payment = Decimal(data['payment']['value'])
        user = db.update_balance(user_id=deposit.user_id, payment=deposit.amount)
        show_menu(user, bot)
    try:
        bot.edit_message_reply_markup(chat_id=deposit.user_id, message_id=deposit.message_id, reply_markup=buttons.editted_reply("Settled"))
    except:
        print('No user id linked to this webhook, ignoring')
        return

def handle_payment_recieved_webhook(data, bot):
    deposit = db.update_deposit_by_invoice_id(
        invoice_id=data['invoiceId'], 
        event_type=data['type'], 
        status="recieved", 
        amount_recieved=data['payment']['value'],  
        updated_at=data['timestamp'],
        )
    try:
        bot.edit_message_reply_markup(chat_id=deposit.user_id, message_id=deposit.message_id, reply_markup=buttons.editted_reply("Confirming"))
    except:
        print('No user id linked to this webhook, ignoring')
        return

def handle_invoice_expired_webhook(data, bot):
    deposit = db.update_deposit_by_invoice_id(invoice_id=data['invoiceId'], event_type=data['type'], updated_at=data['timestamp'])
    try:
        bot.edit_message_reply_markup(chat_id=deposit.user_id, message_id=deposit.message_id, reply_markup=buttons.editted_reply("Expired"))
    except KeyError:
        print('No user id linked to this webhook, ignoring')
    except Exception as e:
        print(f"An error occurred: {e}")


def generate_address(message, bot, **kwargs):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.send_chat_action(chat_id, action="typing")

    user = db.get_user(user_id)
    promo = message.text.split(" ")[0]

    try:
        amount = Decimal(promo)
        invoice = payment_client.create_invoice(
            amount=amount,
            user_id=user_id,
            currency=config.FIAT_CURRENCY,
            description=f"Deposit of {amount} {config.FIAT_CURRENCY} from {user.name}",
        )

        if 'code' in invoice and invoice['code'] == 'generic-error':
            raise ValueError

        deposit_text, keyboard = buttons.deposit_address_markup(user, invoice)
        dmessage = bot.send_message(
            chat_id,
            text=deposit_text,
            reply_markup=keyboard
        )

        db.create_deposit(
            user=user,
            invoice_id=invoice['id'],
            user_id=user_id,
            message_id=dmessage.id,
            amount=invoice['amount'],
            event_type=invoice['type'],
            status=invoice['status']
        )
    except (ValueError, InvalidOperation):
        bot.send_message(
            chat_id,
            text="Invalid amount",
            # reply_markup=buttons.passive_menu(user.language)
        )


def deposit(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = db.get_user(user_id)
    if user == None:
        return start(message, bot)
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

    amount = Decimal(promo)
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
