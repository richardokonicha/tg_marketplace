from telebot import types, TeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import sys
import os

force_reply = types.ForceReply(input_field_placeholder="Enter value")

def place_order_keyboard(product):
    buy_button = InlineKeyboardButton("Buy", callback_data=f"buy_product:{product.product_id}")
    return InlineKeyboardMarkup([buy_button])


def get_all_products_markup(products):
    all_products_markup = []
    for product in products:
        all_products_markup.append(
            [InlineKeyboardButton(f'{product.price} . {product.name}', callback_data=f"view_product:{product.id}")]
            )
    all_products_markup.append([InlineKeyboardButton("<<", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(all_products_markup)


def get_create_product_keyboard(fields=None):
    name = fields.get('name', 'Enter name') if fields else 'Enter name'
    description = fields.get('description', 'Enter description') if fields else 'Enter description'
    price = fields.get('price', 'Enter price') if fields else 'Enter price'
    create_product_keyboard = [
        [InlineKeyboardButton(f"Name: {name}", callback_data="create_product:name")],
        [InlineKeyboardButton(f"Description: {description}", callback_data="create_product:description")],
        [InlineKeyboardButton(f"Price: {price}", callback_data="create_product:price")],
        [InlineKeyboardButton("<<", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(create_product_keyboard)


# ---------
product_keyboard = [
    [InlineKeyboardButton("All Products 🧶", callback_data="all_products")],
    [InlineKeyboardButton("My Products", callback_data="my_products")],
    [InlineKeyboardButton("Create New Product 🧶+", callback_data="create_product")],
    [InlineKeyboardButton("<<", callback_data="back_to_menu")]
]
product_menu_markup = InlineKeyboardMarkup(product_keyboard)
# ---------------

# -----------
products_button = InlineKeyboardButton("Products 🧶", callback_data="products")
admin_button = InlineKeyboardButton("Admin 👩‍🚀", url="https://t.me/@markyoku")
clearnet_button = InlineKeyboardButton("Website 🪐", url="https://queen.fugoku.com")
group_chat_button = InlineKeyboardButton("Group 👥", url="https://t.me/followfootprintchat")
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
en_passive_keys = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="View Menu")
it_passive_keys = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="View Menu")
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
