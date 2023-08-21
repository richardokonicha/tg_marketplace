from decimal import Decimal
from flask import request
from telebot import TeleBot
from telebot.apihelper import ApiException
from werkzeug.exceptions import UnsupportedMediaType
from tgbot.models import db
from tgbot.payments import payment_client
from tgbot.utils import buttons
from tgbot.utils.messages import messages
from tgbot.handlers.menu import show_menu
from .language import show_language
from .purchase import purchase_payment_continue, pay_vendor_from_crypto
from tgbot.config import logger

def handle_purchase_payment(deposit, bot):
    purchase = db.get_purchase_by_id(purchase_id=deposit.purchase_id)
    product = db.get_product_by_id(product_id=purchase.product_id)
    user = db.get_user(user_id=deposit.user_id)
    message_id = deposit.message_id
    
    if product is None:
        logger.warning("Product unavailable")
        return False
    
    try:
        if deposit.status == "settled" and product is not None:
           
            ress = pay_vendor_from_crypto(product, purchase)
            res = purchase_payment_continue(product, purchase, user, bot, message_id)
            
            bot.edit_message_reply_markup(
                chat_id=deposit.user_id,
                message_id=deposit.message_id,
                reply_markup=buttons.edited_reply("Settled")
            )
            
            return True
    except Exception as e:
        logger.error("An error occurred in handle_purchase_payment", exc_info=True)
        return False


def handle_invoice_created_webhook(data, bot):
    deposit = db.update_deposit_by_invoice_id(
        invoice_id=data['invoiceId'],
        event_type=data['type'],
        status="created",
        updated_at=data['timestamp']
    )
    try:
        print('Created webhook')
    except KeyError:
        print('No user ID linked to this webhook, ignoring')
    except Exception as e:
        print(f"An error occurred: {e}")


def handle_invoice_paid_webhook(data, bot):
    deposit = db.update_deposit_by_invoice_id(
        invoice_id=data['invoiceId'],
        event_type=data['type'],
        status="settled",
        updated_at=data['timestamp']
    )

    if deposit.event_type == 'InvoicePaymentSettled':
        payment = Decimal(data['payment']['value'])
        
    if deposit.invoice_type == "purchase":
        handle_purchase_payment(deposit=deposit, bot=bot)
    elif deposit.invoice_type == "deposit":
        user = db.update_balance(user_id=deposit.user_id, payment=deposit.amount)
        bot.edit_message_reply_markup(
            chat_id=deposit.user_id,
            message_id=deposit.message_id,
            reply_markup=buttons.edited_reply("Settled")
        )
        show_menu(user, bot)
    
    logger.info("Invoice payment webhook processed successfully")
    return True
    

def handle_payment_received_webhook(data, bot):
    deposit = db.update_deposit_by_invoice_id(
        invoice_id=data['invoiceId'],
        event_type=data['type'],
        status="received",
        amount_received=data['payment']['value'],
        updated_at=data['timestamp']
    )

    if deposit.invoice_type == "purchase":
        purchase = db.get_purchase_by_id(purchase_id=deposit.purchase_id)
        product = db.get_product_by_id(product_id=purchase.product_id)
        if product is None:
            logger.warning("Product unavailable")
            return
        user = db.get_user(user_id=deposit.user_id)
        message_id = deposit.message_id
        purchase_payment_continue(product, purchase, user, bot, message_id, status="processing")

    try:
        bot.edit_message_reply_markup(
            chat_id=deposit.user_id,
            message_id=deposit.message_id,
            reply_markup=buttons.edited_reply("Confirming")
        )
    except:
        logger.error('No user ID linked to this webhook, ignoring')
        return


def handle_invoice_expired_webhook(data, bot):
    deposit = db.update_deposit_by_invoice_id(
        invoice_id=data['invoiceId'],
        event_type=data['type'],
        updated_at=data['timestamp']
    )
    try:
        bot.edit_message_reply_markup(
            chat_id=deposit.user_id,
            message_id=deposit.message_id,
            reply_markup=buttons.edited_reply("Expired")
        )
    except KeyError:
        logger.error('No user ID linked to this webhook, ignoring')
    except Exception as e:
        logger.error(f"An error occurred: {e}")


def process_merchant_webhook(bot):
    data = request.get_json()
    if data['metadata'] is None:
        logger.info("Webhook Test")
        return 'Testing', 200
    try:
        event_type = data['type']
        logger.info(f"Webhook event from server merchant: {event_type}")
        if event_type == 'InvoiceCreated':
            handle_invoice_created_webhook(data, bot)
        if event_type == 'InvoiceReceivedPayment':
            handle_payment_received_webhook(data, bot)
        elif event_type in ['InvoicePaymentSettled']:
            handle_invoice_paid_webhook(data, bot)
        elif event_type == 'InvoiceExpired':
            handle_invoice_expired_webhook(data, bot)
    except UnsupportedMediaType:
        logger.error('Unsupported Media Type: request payload must be in JSON format')
        return 'Unsupported Media Type: request payload must be in JSON format', 200
    except KeyError:
        logger.error('Invalid request payload: missing required field')
        return 'Invalid request payload: missing required field', 200
    return '', 200
