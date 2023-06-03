from tgbot.utils import buttons
from tgbot.models import db
from tgbot import config
from telebot.types import InputMediaPhoto


def save_product_value(message, **kwargs):
    bot = kwargs.get("bot")
    markup = kwargs.get("markup")
    fields = kwargs.get("fields")
    value = kwargs.get("value")
    create_product_id = kwargs.get("create_product_id")
    user_id = message.from_user.id
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
        enter_name = bot.send_message(chat_id=chat_id, text="Enter Name:", reply_markup=buttons.force_reply)
        bot.register_next_step_handler(
            enter_name,
            save_product_value,
            value="name",
            create_product_id=create_product_id,
            bot=bot,
            markup=markup,
            fields=fields
        )
    elif "description" not in fields:
        enter_description = bot.send_message(chat_id=chat_id, text="Enter Description:", reply_markup=buttons.force_reply)
        bot.register_next_step_handler(
            enter_description,
            save_product_value,
            value="description",
            create_product_id=create_product_id,
            bot=bot,
            markup=markup,
            fields=fields
        )
    elif "price" not in fields:
        enter_price = bot.send_message(chat_id=chat_id, text="Enter Price:", reply_markup=buttons.force_reply)
        bot.register_next_step_handler(
            enter_price,
            save_product_value,
            value="price",
            create_product_id=create_product_id,
            bot=bot,
            markup=markup,
            fields=fields
        )
    else:
        name = fields["name"]
        description = fields["description"]
        price = fields["price"]
        vendor = user_id

        db.create_product(name, description, price, vendor)
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=create_product_id,
            media=InputMediaPhoto(config.MENU_PHOTO, caption="Create New Product Created"),
            reply_markup=buttons.get_create_product_keyboard(fields),
        )
