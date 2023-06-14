from tgbot.models import db
from tgbot.utils import buttons
from tgbot import config
from telebot.types import InputMediaPhoto
from decimal import Decimal, InvalidOperation
from telebot.apihelper import ApiException
from tgbot.payments import payment_client


def purchase_payment_continue(product, purchase, user, bot, message_id, **kwargs):
    try:
        message_text, keyboard = buttons.order_placed_markup(
            product, purchase, user)
        vendor_id = product.vendor_id
        try:
            bot.edit_message_text(
                text=message_text,
                chat_id=user.user_id,
                message_id=message_id,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        except:
            print("not edited")
            pass
        notification_text = buttons.vendor_notification(user, product)
        bot.send_message(text=notification_text, chat_id=vendor_id)
        product.delete()
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
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
        purchase.status = "completed"
        purchase.save()

        return True
    else:
        try:
            insufficient = f"Insufficient balance to make the payment: {str(user.account_balance)}"
            bot.send_message(text=insufficient, chat_id=user.user_id)
            bot.answer_callback_query(call.id, text=insufficient)
        except:
            pass
        return False




def delete_product(call, bot):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    product_id = call.data.split(":")[1]
    product = db.get_product_by_id(product_id)
    if product == None:
        return bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    if product.vendor_id != user_id:
        return
    db.delete_product(product_id)
    bot.delete_message(chat_id=chat_id, message_id=message_id)


def buy_product(call, bot):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    user = db.get_user(user_id)
    data, payment_type, product_id= call.data.split(":")
    product = db.get_product_by_id(product_id)
    
    if product == None:
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
        description=product.description,
        status="incomplete"
    )
    status = False
    if payment_type == "pay_from_balance":
        status = pay_vendor_from_balance(user, product, bot, call, purchase)
        status_pay = purchase_payment_continue(product, purchase, user, bot, message_id)
        bot.answer_callback_query(call.id, text="Purchase successful")
        
    elif payment_type == "pay_with_crypto":
        status = pay_vendor_with_crypto(user, product, bot, purchase, message_id)
        
    if status != True and purchase.status != "complete":
        return
    
    # payment_success(product, purchase, user, bot, message_id)


def view_vendor_products(call, bot):
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
    
def confirm_payment_method(call, bot, user):
    chat_id = call.message.chat.id
    # user_id = call.from_user.id
    # user = db.get_user(user_id)
    message_id = call.message.id
    product_id = call.data.split(":")[1]
    product = db.get_product_by_id(product_id)
    if product == None:
        return bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    keyboard = buttons.payment_method(product, user)
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
    
    # bot.send_message(
    #     chat_id=chat_id,
    #     text=message_text,
    #     parse_mode="HTML",
    #     reply_markup=keyboard,
    # )


def view_product(call, bot):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user = db.get_user(user_id)
    product_id = call.data.split(":")[1]
    product = db.get_product_by_id(product_id)
    if product == None:
        return bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    message_text, keyboard = buttons.view_product_markup(product, user)
    bot.send_message(
        chat_id=chat_id,
        text=message_text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


def view_all_products(call, bot):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    user = db.get_user(user_id)
    products = db.get_all_products()
    media, keyboard = buttons.all_products_markup(products, user)
    bot.edit_message_media(
        chat_id=chat_id,
        message_id=message_id,
        media=media,
        reply_markup=keyboard,
    )


def save_product_value(message, **kwargs):
    bot = kwargs.get("bot")
    markup = kwargs.get("markup")
    fields = kwargs.get("fields")
    call = kwargs.get("call")
    value = kwargs.get("value")
    user = kwargs.get("user")
    create_product_id = kwargs.get("create_product_id")
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id
    message_text = message.text
  
    if value == "price":
        try:
            quant = Decimal(message_text)
            message_text = quant.quantize(Decimal('0.00'))
        except:
            value = "error"
            bot.send_message(
                chat_id=chat_id, text="Invalid Price Enter Digits only")
    
    fields[value] = message_text
    keyboard = buttons.get_create_product_keyboard(user, fields)
    
    try:
        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=create_product_id,
            reply_markup=keyboard,
        )
    except ApiException as e:
        print(f"An error occurred: {e}")
        pass

    try:
        bot.delete_message(chat_id=chat_id, message_id=message.message_id - 1)
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    except:
        pass

    if "name" not in fields:
        enter_name = bot.send_message(
            chat_id=chat_id, text="Enter Name:", reply_markup=buttons.force_reply)
        bot.register_next_step_handler(
            enter_name,
            save_product_value,
            value="name",
            create_product_id=create_product_id,
            bot=bot,
            markup=markup,
            fields=fields,
            call=call,
            user=user
        )
    elif "description" not in fields:
        enter_description = bot.send_message(
            chat_id=chat_id, text="Enter Description:", reply_markup=buttons.force_reply)
        bot.register_next_step_handler(
            enter_description,
            save_product_value,
            value="description",
            create_product_id=create_product_id,
            bot=bot,
            markup=markup,
            fields=fields,
            call=call,
            user=user
        )
    elif "price" not in fields:
        enter_price = bot.send_message(
            chat_id=chat_id, text="Enter Price:", reply_markup=buttons.force_reply)
        bot.register_next_step_handler(
            enter_price,
            save_product_value,
            value="price",
            create_product_id=create_product_id,
            bot=bot,
            markup=markup,
            fields=fields,
            call=call,
            user=user
        )
    else:
        name = fields["name"]
        description = fields["description"]
        price = fields["price"]
        vendor_id = user_id
        vendor_username = username

        db.create_product(name, description, price, vendor_id, vendor_username)
        keyboard = buttons.get_create_product_keyboard(user, fields)
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=create_product_id,
            media=InputMediaPhoto(
                config.MENU_PHOTO, caption="Create New Product Created"),
            reply_markup=keyboard,
        )
        view_vendor_products(call, bot)
