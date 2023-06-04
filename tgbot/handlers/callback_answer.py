import logging
from tgbot.utils.buttons import product_menu_markup
from tgbot.utils import buttons
from tgbot.utils.messages import messages
from tgbot.models import db
from tgbot import config
from tgbot.handlers.product import save_product_value, buy_product, delete_product, view_product, view_all_products, view_vendor_products
from telebot.types import InputMediaPhoto
from tgbot.handlers.menu import back_to_menu, exit_view

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def callback_answer(call, **kwargs):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    message = call.message
    user = db.get_user(user_id)
    lang = user.language
    bot = kwargs.get('bot')
    markup_balances = messages["markup_balances"][lang].format(
        account_balance=user.account_balance)

    if call.data == "products":
        logger.info(f"User {user_id} requested to view products")
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(config.MENU_PHOTO, caption=markup_balances),
            reply_markup=product_menu_markup,
        )
    elif call.data == "continue_shopping":
        exit_view(call, bot)

    elif call.data == "back_to_menu":
        logger.info(f"Back to Menu")
        back_to_menu(call, bot)

    elif call.data == "all_products":
        logger.info(f"User {user_id} requested to view all products")
        view_all_products(call, bot)

    elif call.data == "vendor_products":
        logger.info(f"User {user_id} requested to view vendor products")
        view_vendor_products(call, bot)

    elif call.data.startswith("view_product:"):
        logger.info(f"User {user_id} requested to view a product")
        view_product(call, bot)

    elif call.data.startswith("buy_product:"):
        logger.info(f"User {user_id} requested to buy a product")
        buy_product(call, bot)
        bot.answer_callback_query(call.id, text="Purchase successful")

    elif call.data.startswith("delete_product:"):
        logger.info(f"User {user_id} requested to Delete a product")
        delete_product(call, bot)
        bot.answer_callback_query(call.id, text="Product deleted")

    elif call.data == "create_product":
        logger.info(f"User {user_id} requested to create a new product")
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(
                config.MENU_PHOTO, caption="Create New Product"),
            reply_markup=buttons.get_create_product_keyboard(),
        )
    elif call.data.startswith("create_product:"):
        fields = {}
        field_name = call.data.split(":")[1]
        enter_field_value = bot.send_message(
            chat_id=chat_id, text=f"Enter {field_name}", reply_markup=buttons.force_reply)
        bot.register_next_step_handler(
            enter_field_value, save_product_value, call=call, fields=fields, create_product_id=message_id, value=field_name, bot=bot)
