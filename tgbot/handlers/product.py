from tgbot.models import db
from tgbot.utils import buttons
from tgbot import config
from telebot.types import InputMediaPhoto


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
    product_id = call.data.split(":")[1]
    product = db.get_product_by_id(product_id)
    if product == None:
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
        description=product.description
    )

    message_text, keyboard = buttons.order_placed_markup(
        product, purchase, user)

    vender_id = product.vendor_id

    bot.edit_message_text(
        text=message_text,
        chat_id=chat_id,
        message_id=message_id,
        parse_mode="HTML",
        reply_markup=keyboard,
    )

    vendor_alert = f"""```
    From User {user.name}
    Address:  {user.address}
    UserId:   {user.user_id}
    Username:  @{user.username}
        
    New Order:  {product.name} 
    Price:       {product.price}
    Description: {product.description}
    ```
    """
    bot.send_message(text=vendor_alert, chat_id=vender_id)


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
    create_product_id = kwargs.get("create_product_id")
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id

    fields[value] = message.text
    bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=create_product_id,
        reply_markup=buttons.get_create_product_keyboard(fields),
    )

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
            call=call
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
            call=call
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
            call=call
        )
    else:
        name = fields["name"]
        description = fields["description"]
        price = fields["price"]
        vendor_id = user_id
        vendor_username = username

        db.create_product(name, description, price, vendor_id, vendor_username)
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=create_product_id,
            media=InputMediaPhoto(
                config.MENU_PHOTO, caption="Create New Product Created"),
            reply_markup=buttons.get_create_product_keyboard(fields),
        )
        view_vendor_products(call, bot)
