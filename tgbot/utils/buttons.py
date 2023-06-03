from telebot import types, TeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import sys
import os

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
