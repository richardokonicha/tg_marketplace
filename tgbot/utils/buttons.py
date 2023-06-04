from telebot import types, TeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import sys
import os
from telebot.types import InputMediaPhoto
from tgbot import config


force_reply = types.ForceReply(input_field_placeholder="Enter value")


def purchase_markup(user, purchases):
    media = InputMediaPhoto(
        config.MENU_PHOTO, caption=f"{'Vendor' if user.is_vendor else 'User'}:Your Purchase Activity")

    keys = []

    for purchase in purchases:
        button_text = f"{purchase.get_created_at()}: {purchase.product_name} {'♻️' if purchase.active else '✔️'}"
        keys.append(
            [InlineKeyboardButton(
                button_text, callback_data=f"purchase:{purchase.id}")]
        )
    keys.append(
        [InlineKeyboardButton("<<", callback_data="back_to_menu")])
    keyboard = InlineKeyboardMarkup(keys)
    return media, keyboard


def menu_markup(user):
    media = InputMediaPhoto(
        config.MENU_PHOTO, caption=f"🏦 Balance: {user.account_balance} BTC")
    list_menu_keys = [
        [InlineKeyboardButton(
            "Products 🧶", callback_data="products")],
        [InlineKeyboardButton(
            "Website 🪐", url="https://queen.fugoku.com")],
        [InlineKeyboardButton(
            "Group 👥", url="https://t.me/followfootprintchat")],
        [InlineKeyboardButton(
            "Admin 👩‍🚀", url="https://t.me/@markyoku")],
        [InlineKeyboardButton(
            "Purchase 🪺", callback_data="purchase")]
    ]
    keyboard = InlineKeyboardMarkup(list_menu_keys)
    return media, keyboard


def view_product_markup(product, user_id):
    is_mine = user_id == product.vendor_id
    message_text = f"""
        {'My' if is_mine else 'View'} Product:
        
        <b>Product Name:</b> {product.name}
        
        💰 <b>Price:</b> {product.price}
        
        📝 <b>Description:</b>
        {product.description}
    """

    button_text = "Delete" if is_mine else "Buy"
    button_callback = f"delete_product:{product.id}" if is_mine else f"buy_product:{product.id}"

    keyboard = [[
        InlineKeyboardButton(button_text, callback_data=button_callback),
        InlineKeyboardButton("Cancel", callback_data="cancel")
    ]]

    return message_text, InlineKeyboardMarkup(keyboard)


def view_purchase_markup(purchase, user):
    is_vendor = user.is_vendor
    message_text = f"""
        {'View Orders' if is_vendor else 'My Orders'}:
        
        <b>User Name:</b> {purchase.buyer_username}
        <b>User ID:</b> {purchase.buyer_id}
        
        <b>Vendor ID:</b> {purchase.vendor_id}
        <b>Vendor Username:</b> @{purchase.vendor_username}
        
        <b>User Address:</b> {purchase.address}
        
        <b>Product Name:</b> {purchase.product_name}
        
        💰 <b>Price:</b> {purchase.price}
        
        📝 <b>Description:</b>
        {purchase.description}
    """

    if is_vendor:
        button_text = "Completed"
        button_callback = f"complete_purchase:{purchase.id}"
        keyboard = [
            [InlineKeyboardButton(button_text, callback_data=button_callback)],
            [InlineKeyboardButton("Cancel", callback_data="cancel")]
        ]
    else:
        button_text = "Cancel"
        button_callback = "cancel"
        keyboard = [[InlineKeyboardButton(
            button_text, callback_data=button_callback)]]

    return message_text, InlineKeyboardMarkup(keyboard)


def order_placed_markup(product, purchase):
    message_text = f"""
        Your order has been placed successfully! Thank you for shopping with us
        
      📦 <b>Order ID:</b> {purchase.id}
      
      📝 <b>Purchase Status:</b> {purchase.status}

      <b>Product Name:</b> {product.name}
      
      💰 <b>Price:</b> {product.price}

      📝 <b>Description:</b>
      {product.description}
    """
    continue_button = InlineKeyboardButton(
        "Continue Shopping", callback_data="continue_shopping")
    keyboard = [[continue_button]]
    return message_text, InlineKeyboardMarkup(keyboard)


def all_products_markup(products, user):
    all_products_markup = []
    media = InputMediaPhoto(
        config.MENU_PHOTO, caption=f"🏦 Balance  {user.account_balance} BTC")
    for product in products:
        all_products_markup.append(
            [InlineKeyboardButton(
                f'{product.name}', callback_data=f"view_product:{product.id}")]
        )
    all_products_markup.append(
        [InlineKeyboardButton("<<", callback_data="back_to_menu")])
    return media, InlineKeyboardMarkup(all_products_markup)


def get_create_product_keyboard(fields=None):
    name = fields.get('name', 'Enter name') if fields else 'Enter name'
    description = fields.get(
        'description', 'Enter description') if fields else 'Enter description'
    price = fields.get('price', 'Enter price') if fields else 'Enter price'
    create_product_keyboard = [
        [InlineKeyboardButton(
            f"Name: {name}", callback_data="create_product:name")],
        [InlineKeyboardButton(
            f"Description: {description}", callback_data="create_product:description")],
        [InlineKeyboardButton(
            f"Price: {price}", callback_data="create_product:price")],
        [InlineKeyboardButton("<<", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(create_product_keyboard)


# ---------
product_keyboard = [
    [InlineKeyboardButton("All Products 🧶", callback_data="all_products")],
    [InlineKeyboardButton("Vendor Products", callback_data="vendor_products")],
    [InlineKeyboardButton("Create New Product",
                          callback_data="create_product")],
    [InlineKeyboardButton("<<", callback_data="back_to_menu")]
]
product_menu_markup = InlineKeyboardMarkup(product_keyboard)
# ---------------

# -----------
products_button = InlineKeyboardButton("Products 🧶", callback_data="products")
admin_button = InlineKeyboardButton("Admin 👩‍🚀", url="https://t.me/@markyoku")
clearnet_button = InlineKeyboardButton(
    "Website 🪐", url="https://queen.fugoku.com")
group_chat_button = InlineKeyboardButton(
    "Group 👥", url="https://t.me/followfootprintchat")
purchase_button = InlineKeyboardButton("Purchase 🪺", callback_data="purchase")

inline_keyboard = [
    [products_button],
    [clearnet_button],
    [group_chat_button],
    [admin_button],
    [purchase_button]
]
list_menu_keys = InlineKeyboardMarkup(inline_keyboard)

# ---------


# ----- Menu Button
passive_markup = {
    "en": [
        ["𓀉 Menu"],
    ],
    "it": [
        ["𓀉 Menu"],
    ]
}
en_passive_keys = types.ReplyKeyboardMarkup(
    resize_keyboard=True, input_field_placeholder="View Menu")
it_passive_keys = types.ReplyKeyboardMarkup(
    resize_keyboard=True, input_field_placeholder="View Menu")
passive_menu = {
    "en": en_passive_keys,
    "it": it_passive_keys
}
en_passive_keys.keyboard = passive_markup.get("en")
it_passive_keys.keyboard = passive_markup.get("it")

# -----


# ------- Language
select_lang_markup = [
    ["English  🇬🇧", "Italiano  🇮🇹"]
]
lang_keys = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
)
lang_keys.keyboard = select_lang_markup

# --------
