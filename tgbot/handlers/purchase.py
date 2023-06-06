from tgbot.models import db
from tgbot.utils import buttons
from tgbot import config


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
    if purchase == None:
        return bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    message_text, keyboard = buttons.view_purchase_markup(
        purchase, user)
    bot.send_message(
        chat_id=chat_id,
        text=message_text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )
