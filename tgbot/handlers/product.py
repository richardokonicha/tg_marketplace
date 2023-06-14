from tgbot.models import db
from tgbot.utils import buttons
from tgbot import config
from telebot.types import InputMediaPhoto
from decimal import Decimal, InvalidOperation
from telebot.apihelper import ApiException
from tgbot.payments import payment_client


def delete_product(call, bot):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    product_id = call.data.split(":")[1]
    product = db.get_product_by_id(product_id)
    
    if product is None:
        return bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    
    if product.vendor_id != user_id:
        return
    
    db.delete_product(product_id)
    bot.delete_message(chat_id=chat_id, message_id=message_id)


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


def view_product(call, bot):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user = db.get_user(user_id)
    product_id = call.data.split(":")[1]
    product = db.get_product_by_id(product_id)
    
    if product is None:
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
                chat_id=chat_id, text="Invalid Price. Enter digits only.")
    
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
