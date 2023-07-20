import logging
from decimal import Decimal, InvalidOperation
from telebot.types import InputMediaPhoto
from telebot.apihelper import ApiException
from tgbot.models import db
from tgbot.utils import buttons
from tgbot import config
from tgbot.payments import payment_client
from tgbot.config import logger

def confirm_payment_method(call, bot, user):
    chat_id = call.message.chat.id
    message_id = call.message.id
    product_id = call.data.split(":")[1]
    product = db.get_product_by_id(product_id)
    
    if product is None:
        logger.warning("Product unavailable")
        return bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    
    keyboard = buttons.payment_method(product, user)
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)

def pay_vendor_from_crypto(product, purchase):
    vendor_id = product.vendor_id
    vendor = db.get_user(user_id=vendor_id)
    total_amount = product.price
    vendor.account_balance += total_amount
    vendor.save()
    return True

def purchase_payment_continue(product, purchase, user, bot, message_id, status=None):
    if status == "processing":
        try:
            bot.edit_message_reply_markup(
                chat_id=user.user_id,
                message_id=message_id,
                reply_markup=buttons.edited_reply("Confirming")
            )
            return
        except Exception as e:
            logger.error("Could not edit message", exc_info=True)
        return True
        
    try:
        
        stock_item = product.description.pop()
        
        purchase.description = stock_item
        purchase.status = "completed"
        purchase.save()
        product.save()
        
        
        message_text, keyboard = buttons.order_placed_markup(product, purchase, user, stock_item)
        vendor_id = product.vendor_id

        try:
            bot.edit_message_text(
                text=message_text,
                chat_id=user.user_id,
                message_id=message_id,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        
        except Exception as e:
            logger.error("Could not edit message", exc_info=True)
            pass

        notification_text = buttons.vendor_notification(user, product, stock_item)
        bot.send_message(text=notification_text, chat_id=vendor_id)
        
        quantity = len(product.description)
        if quantity == 0:
            product.delete()
            bot.send_message(text="Product {product.name} is exhausted", chat_id=vendor_id)

        logger.info("Purchase payment handled successfully")
        return True
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        return False

def pay_vendor_with_crypto(user, product, bot, purchase, message_id):
    vendor_id = product.vendor_id
    bot.send_chat_action(user.user_id, action="typing")

    try:
        amount = Decimal(product.price)
        invoice = payment_client.create_invoice(
            amount=amount,
            user_id=vendor_id,
            currency=config.FIAT_CURRENCY,
            description=f"Purchase of {product.name} {amount} {config.FIAT_CURRENCY} from {user.name}",
        )

        if 'code' in invoice and invoice['code'] == 'generic-error':
            raise ValueError

        purchase_text, keyboard = buttons.purchase_address_markup(user, purchase, invoice)
        dmessage = bot.send_message(
            user.user_id,
            text=purchase_text,
            reply_markup=keyboard
        )

        db.create_deposit(
            user=user,
            invoice_id=invoice['id'],
            invoice_type="purchase",
            user_id=user.user_id,
            message_id=dmessage.id,
            amount=invoice['amount'],
            event_type=invoice['type'],
            status=invoice['status'],
            purchase_id=purchase.id,
        )
    except (ValueError, InvalidOperation):
        bot.send_message(
            user.user_id,
            text="Invalid amount",
        )

    return True

def pay_vendor_from_balance(user, product, bot, call, purchase):
    vendor_id = product.vendor_id
    vendor = db.get_user(user_id=vendor_id)
    total_amount = product.price

    if user.account_balance >= total_amount:
        user.account_balance -= total_amount
        vendor.account_balance += total_amount
        user.save()
        vendor.save()
        return True
    else:
        try:
            insufficient = f"Insufficient balance to make the payment: {str(user.account_balance)}"
            bot.send_message(text=insufficient, chat_id=user.user_id)
            bot.answer_callback_query(call.id, text=insufficient)
        except Exception as e:
            logger.error("An error occurred while sending insufficient balance message", exc_info=True)
            pass

        return False

def vendor_purchase_orders(call, bot):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    user = db.get_user(user_id)
    products = db.get_products_by_vendor(vendor_id=user_id)
    media, keyboard = buttons.all_products_markup(products, user)
    bot.edit_message_media(
        chat_id=chat_id,
        message_id=message_id,
        media=media,
        reply_markup=keyboard,
    )

def view_purchase(call, bot):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    purchase_id = call.data.split(":")[1]
    purchase = db.get_purchase_by_id(purchase_id)
    user = db.get_user(user_id)

    if purchase is None:
        logger.warning("Purchase not found")
        return bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)

    message_text, keyboard = buttons.view_purchase_markup(purchase, user)
    bot.send_message(
        chat_id=chat_id,
        text=message_text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )

def buy_product(call, bot):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    user = db.get_user(user_id)
    data, payment_type, product_id = call.data.split(":")
    product = db.get_product_by_id(product_id)

    if product is None:
        bot.answer_callback_query(user.user_id, text=f"Product Unavailable {product.name}")
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        return bot.answer_callback_query(call.id, text="Product Not Available")

    purchase = db.create_purchase(
        user_id=user_id,
        buyer_username=user.username,
        buyer_id=user_id,
        vendor_id=product.vendor_id,
        vendor_username=product.vendor_username,
        product_id=product.id,
        product_name=product.name,
        address=user.address,
        price=product.price,
        # description=product.description,
        status="incomplete"
    )
    
    status = False

    if payment_type == "pay_from_balance":
        status = pay_vendor_from_balance(user, product, bot, call, purchase)
        if status:
            status_pay = purchase_payment_continue(product, purchase, user, bot, message_id)
            bot.answer_callback_query(call.id, text="Purchase successful")
        else:
            logger.info("Purchase Failed")
            

    elif payment_type == "pay_with_crypto":
        status = pay_vendor_with_crypto(user, product, bot, purchase, message_id)

    if status is not True and purchase.status != "complete":
        return
