from telebot import types, TeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import sys
import os
from telebot.types import InputMediaPhoto
from tgbot import config


force_reply = types.ForceReply(input_field_placeholder="Enter value")


def purchase_markup(user, purchases):
    lang = user.language
    translations = {
        "en": {
            "vendor_user": "Vendor" if user.is_vendor else "User",
            "activity": "Your Purchase Activity",
            "active": "♻️",
            "inactive": "✔️",
            "back_to_menu": "<<"
        },
        "ru": {
            "vendor_user": "Продавец" if user.is_vendor else "Пользователь",
            "activity": "Ваша активность покупок",
            "active": "♻️",
            "inactive": "✔️",
            "back_to_menu": "<<"
        }
    }

    translation = translations[lang] if lang in translations else translations["en"]

    media = InputMediaPhoto(
        config.MENU_PHOTO, caption=f"{translation['vendor_user']}: {translation['activity']}")

    keys = []

    for purchase in purchases:
        status = translation['active'] if purchase.active else translation['inactive']
        button_text = f"{purchase.get_created_at()}: {purchase.product_name} {status}"
        keys.append([InlineKeyboardButton(
            button_text, callback_data=f"purchase:{purchase.id}")])

    keys.append([InlineKeyboardButton(
        translation['back_to_menu'], callback_data="back_to_menu")])

    keyboard = InlineKeyboardMarkup(keys)
    return media, keyboard


def view_product_markup(product, user):
    lang = user.language
    user_id = user.user_id
    translations = {
        "en": {
            "mine": "My",
            "view": "View",
            "product_name": "Product Name:",
            "price": "Price:",
            "description": "Description:",
            "delete": "Delete",
            "buy": "Buy",
            "cancel": "Cancel"
        },
        "ru": {
            "mine": "Моё" if user_id == product.vendor_id else "Просмотр",
            "view": "Просмотр",
            "product_name": "Название продукта:",
            "price": "Цена:",
            "description": "Описание:",
            "delete": "Удалить",
            "buy": "Купить",
            "cancel": "Отмена"
        }
    }

    translation = translations[lang] if lang in translations else translations["en"]

    is_mine = user_id == product.vendor_id
    message_text = f"""
        {translation['mine']} Product:
        
        <b>{translation['product_name']}</b> {product.name}
        
        💰 <b>{translation['price']}</b> {product.price}
        
        📝 <b>{translation['description']}</b>
        {product.description}
    """

    button_text = translation['delete'] if is_mine else translation['buy']
    button_callback = f"delete_product:{product.id}" if is_mine else f"buy_product:{product.id}"

    keyboard = [[
        InlineKeyboardButton(button_text, callback_data=button_callback),
        InlineKeyboardButton(translation['cancel'], callback_data="cancel")
    ]]

    return message_text, InlineKeyboardMarkup(keyboard)


def order_placed_markup(product, purchase, user):
    lang = user.language
    translations = {
        "en": {
            "order_placed": "Your order has been placed successfully! Thank you for shopping with us",
            "order_id": "Order ID:",
            "purchase_status": "Purchase Status:",
            "product_name": "Product Name:",
            "price": "Price:",
            "description": "Description:",
            "continue_shopping": "Continue Shopping"
        },
        "ru": {
            "order_placed": "Ваш заказ успешно размещен! Спасибо за покупку",
            "order_id": "ID заказа:",
            "purchase_status": "Статус покупки:",
            "product_name": "Название продукта:",
            "price": "Цена:",
            "description": "Описание:",
            "continue_shopping": "Продолжить покупки"
        }
    }

    translation = translations[lang] if lang in translations else translations["en"]

    message_text = f"""
        {translation['order_placed']}
        
        📦 <b>{translation['order_id']}</b> {purchase.id}
        
        📝 <b>{translation['purchase_status']}</b> {purchase.status}

        <b>{translation['product_name']}</b> {product.name}
        
        💰 <b>{translation['price']}</b> {product.price}

        📝 <b>{translation['description']}</b>
        {product.description}
    """

    continue_button = InlineKeyboardButton(
        translation['continue_shopping'], callback_data="continue_shopping")
    keyboard = [[continue_button]]
    return message_text, InlineKeyboardMarkup(keyboard)


def all_products_markup(products, user):
    lang = user.language

    translations = {
        "en": {
            "balance": f"🏦 Balance: {user.account_balance} BTC",
            "back_to_menu": "<<"
        },
        "ru": {
            "balance": f"🏦 Баланс: {user.account_balance} BTC",
            "back_to_menu": "<<"
        }
    }

    translation = translations[lang] if lang in translations else translations["en"]

    all_products_markup = []
    media = InputMediaPhoto(config.MENU_PHOTO, caption=translation['balance'])
    for product in products:
        all_products_markup.append([
            InlineKeyboardButton(
                product.name, callback_data=f"view_product:{product.id}")
        ])
    all_products_markup.append([
        InlineKeyboardButton(
            translation['back_to_menu'], callback_data="back_to_menu")
    ])
    return media, InlineKeyboardMarkup(all_products_markup)


def get_create_product_keyboard(user, fields=None):
    lang = user.language
    translations = {
        "en": {
            "name": "Name",
            "description": "Description",
            "price": "Price",
            "back_to_menu": "<<",
            "enter_name": "Enter name",
            "enter_description": "Enter description",
            "enter_price": "Enter price"
        },
        "ru": {
            "name": "Название",
            "description": "Описание",
            "price": "Цена",
            "back_to_menu": "<<",
            "enter_name": "Введите название",
            "enter_description": "Введите описание",
            "enter_price": "Введите цену"
        }
    }

    translation = translations[lang] if lang in translations else translations["en"]

    name = fields.get(
        'name', translation['enter_name']) if fields else translation['enter_name']
    description = fields.get(
        'description', translation['enter_description']) if fields else translation['enter_description']
    price = fields.get(
        'price', translation['enter_price']) if fields else translation['enter_price']

    create_product_keyboard = [
        [InlineKeyboardButton(
            f"{translation['name']}: {name}", callback_data="create_product:name")],
        [InlineKeyboardButton(
            f"{translation['description']}: {description}", callback_data="create_product:description")],
        [InlineKeyboardButton(
            f"{translation['price']}: {price}", callback_data="create_product:price")],
        [InlineKeyboardButton(translation['back_to_menu'],
                              callback_data="back_to_menu")]
    ]

    return InlineKeyboardMarkup(create_product_keyboard)


def product_menu_markup(user):
    translations = {
        "en": {
            "balance": "🏦 Balance",
            "all_products": "All Products 🧶",
            "vendor_products": "Vendor Products",
            "create_product": "Create New Product",
            "back_to_menu": "<<"
        },
        "ru": {
            "balance": "🏦 Баланс",
            "all_products": "Все товары 🧶",
            "vendor_products": "Товары продавца",
            "create_product": "Создать новый товар",
            "back_to_menu": "<<"
        }
    }

    # Default to English if language not available
    lang = user.language if user.language in translations else "en"
    translation = translations[lang]

    is_vendor = user.is_vendor
    media = InputMediaPhoto(
        config.MENU_PHOTO, caption=f"{translation['balance']}: {user.account_balance} BTC")

    if is_vendor:
        keys = [
            [InlineKeyboardButton(
                translation["all_products"], callback_data="all_products")],
            [InlineKeyboardButton(
                translation["vendor_products"], callback_data="vendor_products")],
            [InlineKeyboardButton(
                translation["create_product"], callback_data="create_product")],
            [InlineKeyboardButton(
                translation["back_to_menu"], callback_data="back_to_menu")]
        ]
    else:
        keys = [
            [InlineKeyboardButton(
                translation["all_products"], callback_data="all_products")],
            [InlineKeyboardButton(
                translation["back_to_menu"], callback_data="back_to_menu")]
        ]

    keyboard = InlineKeyboardMarkup(keys)
    return media, keyboard


def menu_markup(user):
    translations = {
        "en": {
            "balance": "🏦 Balance",
            "products": "Products 🧶",
            "website": "Website 🪐",
            "group": "Group 👥",
            "admin": "Admin 👩‍🚀",
            "purchase": "Purchase 🪺"
        },
        "ru": {
            "balance": "🏦 Баланс",
            "products": "Продукты 🧶",
            "website": "Сайт 🪐",
            "group": "Группа 👥",
            "admin": "Админ 👩‍🚀",
            "purchase": "Покупка 🪺"
        }
    }

    # Default to English if language not available
    lang = user.language if user.language in translations else "en"
    translation = translations[lang]

    media = InputMediaPhoto(
        config.MENU_PHOTO, caption=f"{translation['balance']}: {user.account_balance} BTC")
    list_menu_keys = [
        [InlineKeyboardButton(translation["products"],
                              callback_data="products")],
        [InlineKeyboardButton(translation["website"], url=config.WEBSITE_URL)],
        [InlineKeyboardButton(translation["group"], url=config.GROUP_URL)],
        [InlineKeyboardButton(translation["admin"], url=config.ADMIN_USER)],
        [InlineKeyboardButton(translation["purchase"],
                              callback_data="purchase")]
    ]
    keyboard = InlineKeyboardMarkup(list_menu_keys)
    return media, keyboard


def view_purchase_markup(purchase, user):
    lang = user.language

    translations = {
        "en": {
            "view_orders": "View Orders",
            "my_orders": "My Orders",
            "user_name": "User Name:",
            "user_id": "User ID:",
            "vendor_id": "Vendor ID:",
            "vendor_username": "Vendor Username:",
            "user_address": "User Address:",
            "product_name": "Product Name:",
            "price": "Price:",
            "description": "Description:",
            "completed": "Completed",
            "cancel": "Cancel"
        },
        "ru": {
            "view_orders": "Просмотр заказов",
            "my_orders": "Мои заказы",
            "user_name": "Имя пользователя:",
            "user_id": "ID пользователя:",
            "vendor_id": "ID продавца:",
            "vendor_username": "Имя пользователя продавца:",
            "user_address": "Адрес пользователя:",
            "product_name": "Название продукта:",
            "price": "Цена:",
            "description": "Описание:",
            "completed": "Завершено",
            "cancel": "Отмена"
        }
    }

    translation = translations[lang] if lang in translations else translations["en"]

    is_vendor = user.is_vendor
    message_text = f"""
        {translation['view_orders'] if is_vendor else translation['my_orders']}
        
        <b>{translation['user_name']}</b> {purchase.buyer_username}
        <b>{translation['user_id']}</b> {purchase.buyer_id}
        
        <b>{translation['vendor_id']}</b> {purchase.vendor_id}
        <b>{translation['vendor_username']}</b> @{purchase.vendor_username}
        
        <b>{translation['user_address']}</b> {purchase.address}
        
        <b>{translation['product_name']}</b> {purchase.product_name}
        
        💰 <b>{translation['price']}</b> {purchase.price}
        
        📝 <b>{translation['description']}</b>
        {purchase.description}
    """

    if is_vendor:
        button_text = translation['completed']
        button_callback = f"complete_purchase:{purchase.id}"
        keyboard = [
            [InlineKeyboardButton(button_text, callback_data=button_callback)],
            [InlineKeyboardButton(translation['cancel'],
                                  callback_data="cancel")]
        ]
    else:
        button_text = translation['cancel']
        button_callback = "cancel"
        keyboard = [[InlineKeyboardButton(
            button_text, callback_data=button_callback)]]

    return message_text, InlineKeyboardMarkup(keyboard)


def get_create_product_keyboard(user, fields=None):
    lang = user.language
    translations = {
        "en": {
            "name": "Name:",
            "description": "Description:",
            "price": "Price:",
            "back_to_menu": "<<"
        },
        "ru": {
            "name": "Название:",
            "description": "Описание:",
            "price": "Цена:",
            "back_to_menu": "<<"
        }
    }

    translation = translations[lang] if lang in translations else translations["en"]

    name = fields.get(
        'name', translation['name']) if fields else translation['name']
    description = fields.get(
        'description', translation['description']) if fields else translation['description']
    price = fields.get(
        'price', translation['price']) if fields else translation['price']
    create_product_keyboard = [
        [InlineKeyboardButton(
            f"{translation['name']} {name}", callback_data="create_product:name")],
        [InlineKeyboardButton(
            f"{translation['description']} {description}", callback_data="create_product:description")],
        [InlineKeyboardButton(
            f"{translation['price']} {price}", callback_data="create_product:price")],
        [InlineKeyboardButton(translation['back_to_menu'],
                              callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(create_product_keyboard)


def passive_menu(lang):
    passive_markup = {
        "en": [
            ["𓀉 Menu"],
        ],
        "ru": [
            ["𓀉 Меню"],
        ]
    }
    passive_keys = types.ReplyKeyboardMarkup(
        resize_keyboard=True, input_field_placeholder="View Menu")
    passive_keys.keyboard = passive_markup.get(lang, passive_markup["en"])
    return passive_keys


# ------- Language

def lang_keys():
    select_lang_markup = [
        ["English  🇬🇧", "Русский 🇷🇺"]
    ]
    lang_keys = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    lang_keys.keyboard = select_lang_markup
    return lang_keys

# --------
