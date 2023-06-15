import logging
from tgbot.utils.buttons import product_menu_markup
from tgbot.utils import buttons
from tgbot.utils.messages import messages
from tgbot.models import db
from tgbot import config
from tgbot.config import logger
from tgbot.handlers.deposits import deposit
from tgbot.handlers.product import save_product_value, delete_product, view_product, view_all_products, view_all_categories, view_vendor_products, view_category
from telebot.types import InputMediaPhoto
from tgbot.handlers.menu import back_to_menu, exit_view
from tgbot.handlers.purchase import view_purchase, confirm_payment_method, buy_product
from tgbot.handlers.start import start


def callback_answer(call, **kwargs):
    bot = kwargs.get('bot')
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    message = call.message
    user = db.get_user(user_id)
    if user is None:
        return start(message, bot)

    if call.data == "products":
        logger.info(f"User {user_id} requested to view products")
        media, keyboard = buttons.product_menu_markup(user)
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=media,
            reply_markup=keyboard,
        )
    elif call.data == "create_deposit":
        deposit(call.message, bot)

    elif call.data == "continue_shopping":
        exit_view(call, bot)

    elif call.data == "back_to_menu":
        logger.info(f"Back to Menu")
        back_to_menu(call, bot)
        
    elif call.data == "all_categories":
        logger.info(f"User {user_id} requested to view all categories")
        view_all_categories(call, bot)
    
    elif call.data.startswith("view_category:"):
        logger.info(f"Category {call.data} requested to view a category")
        view_category(call, bot)

    elif call.data == "all_products":
        logger.info(f"User {user_id} requested to view all products")
        view_all_products(call, bot)
        

    elif call.data == "vendor_products":
        logger.info(f"User {user_id} requested to view vendor products")
        view_vendor_products(call, bot)
        

    elif call.data.startswith("view_product:"):
        logger.info(f"User {user_id} requested to view a product")
        view_product(call, bot)

    elif call.data.startswith("confirm_payment:"):
        logger.info(f"User {user_id} requested to confirm payment method")
        confirm_payment_method(call, bot, user)

    elif call.data.startswith("buy_product:"):
        logger.info(f"User {user_id} requested to buy a product {call.data}")
        buy_product(call, bot)

    elif call.data.startswith("delete_product:"):
        logger.info(f"User {user_id} requested to delete a product")
        delete_product(call, bot)
        bot.answer_callback_query(call.id, text="Product deleted")

    elif call.data == "create_product":
        logger.info(f"User {user_id} requested to create a new product")
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(
                config.MENU_PHOTO, caption="Create New Product"),
            reply_markup=buttons.get_create_product_keyboard(user),
        )

    elif call.data.startswith("create_product:"):
        fields = {}
        field_name = call.data.split(":")[1]
        enter_field_value = bot.send_message(
            chat_id=chat_id, text=f"Enter {field_name}", reply_markup=buttons.force_reply)
        bot.register_next_step_handler(
            enter_field_value, save_product_value, call=call, fields=fields, create_product_id=message_id, bot=bot, user=user, value=field_name)

    elif call.data == "purchase":
        logger.info(f"User {user_id} requested to view purchases")
        purchases = db.get_purchases_by_vendor(user_id) if user.is_vendor else db.get_purchases_by_user(user_id)
        media, keyboard = buttons.purchase_markup(user, purchases)
        bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=media,
            reply_markup=keyboard,
        )

    elif call.data.startswith("purchase:"):
        logger.info(f"User {user_id} requested to view a purchase")
        view_purchase(call, bot)

    elif call.data == "cancel":
        try:
            bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        except Exception as e:
            logger.error(f"Failed to delete message: {e}")

    return
