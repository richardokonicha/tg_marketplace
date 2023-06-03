from tgbot.utils.buttons import product_menu_markup
from tgbot.utils import buttons
from tgbot.utils.messages import messages
from tgbot.models import db
from tgbot import config
from tgbot.utils.helpers import save_product_value
from telebot.types import InputMediaPhoto


def callback_answer(call, **kwargs):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    message = call.message
    user = db.get_user(user_id)
    lang = user.language
    bot = kwargs.get('bot')
    markup_balances = messages["markup_balances"][lang].format(account_balance=user.account_balance)

    if call.data == "products":
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(config.MENU_PHOTO, caption=markup_balances),
            reply_markup=product_menu_markup,
        )
    elif call.data == "back_to_menu":
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(config.MENU_PHOTO, caption=markup_balances),
            reply_markup=buttons.list_menu_keys,
        )
    elif call.data == "all_products":
        products = db.get_all_products()
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(config.MENU_PHOTO, caption=markup_balances),
            reply_markup=buttons.get_all_products_markup(products),
        )
    elif call.data.startswith("view_product:"):
        product_id = call.data.split(":")[1]
        product = db.get_product_by_id(product_id)
        message_text = f"<b>{product.name}</b>: {product.price}\n\n{product.description}"
        bot.send_message(
            chat_id=chat_id,
            text=message_text,
            parse_mode="HTML",
            reply_markup=buttons.place_order_keyboard(product),
        )

        # bot.edit_message_media(
        #     chat_id=chat_id,
        #     message_id=message_id,
        #     media=InputMediaPhoto(config.MENU_PHOTO, caption=f"{product.name}:{product.price} <br/> {product.description}"),
        #     reply_markup=buttons.place_order_keyboard(product),
        # )
    elif call.data.startswith("buy_product:"):
        product_id = call.data.split(":")[1]


        pass


    elif call.data == "create_product":
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(config.MENU_PHOTO, caption="Create New Product"),
            reply_markup=buttons.get_create_product_keyboard(),
        )
    elif call.data.startswith("create_product:"):
        fields = {} 
        field_name = call.data.split(":")[1]
        enter_field_value = bot.send_message(chat_id=chat_id, text=f"Enter {field_name}",reply_markup=buttons.force_reply)
        bot.register_next_step_handler(
            enter_field_value, save_product_value, fields=fields, create_product_id=message_id ,value=field_name, bot=bot)
