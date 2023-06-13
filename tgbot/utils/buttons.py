from telebot import types, TeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import sys
import os
from telebot.types import InputMediaPhoto
from tgbot import config


force_reply = types.ForceReply(input_field_placeholder="Enter value")

expired_reply = InlineKeyboardMarkup([[InlineKeyboardButton(text="Invoice Expired", callback_data="expired")]])
created_reply = InlineKeyboardMarkup([[InlineKeyboardButton(text="Invoice Created", callback_data="created")]])

def editted_reply(text):
    return InlineKeyboardMarkup(
        [
        [InlineKeyboardButton(text=f"Invoice {text}", callback_data=f"{text}")] 
        ]
    )

def deposit_address_markup(user, invoice):
    lang = user.language
    invoice_id = invoice['id']
    invoice_link = invoice['checkoutLink']
    invoice_amount = invoice['amount']
    invoice_currency = invoice['currency']
    # qr_code = invoice['receipt']['showQR']
    translations = {
        "en": {
            "deposit_address_text": f"""
Invoice Created: {invoice_id}

You're depositing {invoice_amount} {invoice_currency}
Please proceed with the payment by clicking Pay now

Make sure to complete the payment of {invoice_amount} {invoice_currency} within the provided expiration time.
                """,
            "back_to_menu": "<<",
            "pay": "💰Pay now"
        },
        "ru": {
            "deposit_address_text": f"""
Счет-фактура создан: {invoice_id}

Вы вносите {invoice_amount} {invoice_currency}
Пожалуйста, продолжите оплату, нажав «Оплатить сейчас»

Убедитесь, что вы завершили платеж {invoice_amount} {invoice_currency} в течение указанного срока действия.
                """,
            "back_to_menu": "<<",
            "pay": "💰Оплатить сейчас"
        }
    }
    translation = translations[lang] if lang in translations else translations["en"]
    deposite_text = translation['deposit_address_text']
    keyboard = [[
        InlineKeyboardButton(translation['pay'], url=invoice_link),
        InlineKeyboardButton("Cancel", callback_data="cancel"),
    ]]
    return deposite_text, InlineKeyboardMarkup(keyboard)


def deposit_markup(user):
    lang = user.language
    translations = {
        "en": {
            "balance_text": f"Wallet Balance is {user.account_balance}",
            "deposit_text": f"""<b>Enter the amount you wish to deposit (min: 10 {config.FIAT_CURRENCY} max: 5,000,000 {config.FIAT_CURRENCY})</b>""",
            "back_to_menu": "<<",
            "inputholder": "Enter value"
        },
        "ru": {
            "balance_text": f"Wallet Balance is {user.account_balance}",
            "deposit_text": f"""Введите сумму, которую вы хотите внести (мин.: 10 {config.FIAT_CURRENCY} max: 5,000,000 {config.FIAT_CURRENCY} )""",
            "back_to_menu": "<<",
            "inputholder": "Enter value"
        }
    }
    translation = translations[lang] if lang in translations else translations["en"]
    force_reply = types.ForceReply(
        input_field_placeholder=translation['inputholder'])
    deposite_text = translation['deposit_text']
    return deposite_text, force_reply


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


def payment_method(product, user):
    lang = user.language
    translations = {
        "en": {
            "cancel": "Cancel",
            "pay_from_balance": "Pay from Balance",
            "pay_with_crypto": "Pay with Crypto"
        },
        "ru": {
            "cancel": "Отмена",
            "pay_from_balance": "Оплатить с баланса",
            "pay_with_crypto": "Оплатить с помощью криптовалюты"
        },
        "ge": {
            "cancel": "გაუქმება",
            "pay_from_balance": "გადახდა ბალანსიდან",
            "pay_with_crypto": "გადახდა კრიპტოვალუტით"
        }
    }
    translation = translations.get(lang, translations["en"])
    pay_from_wallet = InlineKeyboardButton(translation['pay_from_balance'], callback_data=f"buy_product:pay_from_balance:{product.id}")
    pay_direct = InlineKeyboardButton(translation['pay_with_crypto'], callback_data=f"buy_product:pay_with_crypto:{product.id}")
    cancel = InlineKeyboardButton(translation['cancel'], callback_data="cancel")
    keyboard = [[pay_from_wallet, pay_direct], [cancel]]
    return InlineKeyboardMarkup(keyboard)


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
            "cancel": "Cancel",
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

    message_text = f"""
{translation['mine']} Product:

<b>{translation['product_name']}</b> {product.name}

💰 <b>{translation['price']}</b> {product.price} {config.FIAT_CURRENCY}

📝 <b>{translation['description']}</b>
{product.description}
    """
    is_mine = user_id == product.vendor_id
    key = []
    if is_mine:
        key.append(InlineKeyboardButton(translation['delete'], callback_data=f"delete_product:{product.id}"))
    else:
        key.append(InlineKeyboardButton(translation['buy'], callback_data=f"confirm_payment:{product.id}"))
    key.append(InlineKeyboardButton(translation['cancel'], callback_data="cancel"))
    return message_text, InlineKeyboardMarkup([key])


def order_placed_markup(product, purchase, user):
    lang = user.language
    translations = {
        "en": {
            "order_placed": "You have successfully paid {product.price}{config.FIAT_CURRENCY} from your account balance for the product {product.name}.",
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
{translation['order_placed'].format(product=product, config=config)}

📦 <b>{translation['order_id']}</b> {purchase.id}

📝 <b>{translation['purchase_status']}</b> {purchase.status}

<b>{translation['product_name']}</b> {product.name}

💰 <b>{translation['price']}</b> {product.price} {config.FIAT_CURRENCY}

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
            "balance": f"🏦 Wallet Balance: {user.account_balance} {config.FIAT_CURRENCY}",
            "back_to_menu": "<<"
        },
        "ru": {
            "balance": f"🏦 Wallet Баланс: {user.account_balance} {config.FIAT_CURRENCY}",
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
            f"{translation['price']}: {price} {config.FIAT_CURRENCY}", callback_data="create_product:price")],
        [InlineKeyboardButton(translation['back_to_menu'],
                              callback_data="back_to_menu")]
    ]

    return InlineKeyboardMarkup(create_product_keyboard)


def product_menu_markup(user):
    translations = {
        "en": {
            "balance": "Wallet Balance 💵 ",
            "all_products": "All Products 🧶",
            "vendor_products": "Vendor Products 📙",
            "create_product": "Create New Product 🔎",
            "back_to_menu": "<<"
        },
        "ru": {
            "balance": "Wallet Баланс 💵 ",
            "all_products": "Все товары 🧶",
            "vendor_products": "Товары продавца 📙",
            "create_product": "Создать новый товар 🔎",
            "back_to_menu": "<<"
        }
    }

    lang = user.language if user.language in translations else "en"
    translation = translations[lang]

    is_vendor = user.is_vendor
    media = InputMediaPhoto(
        config.MENU_PHOTO, caption=f"{translation['balance']}: {user.account_balance} {config.FIAT_CURRENCY}")

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
            "balance": "Wallet Balance 💵 ",
            "products": "Products 🧶",
            "website": "Website 🪐",
            "group": "Group 👥",
            "admin": "Admin 👩‍🚀",
            "purchase": "Purchase 🪺",
            "deposit": "Deposit"

        },
        "ru": {
            "balance": "Wallet Баланс 💵 ",
            "products": "Продукты 🧶",
            "website": "Сайт 🪐",
            "group": "Группа 👥",
            "admin": "Админ 👩‍🚀",
            "purchase": "Покупка 🪺",
            "deposit": "Deposit"
        }
    }

    # Default to English if language not available
    lang = user.language if user.language in translations else "en"
    translation = translations[lang]

    media = InputMediaPhoto(
        config.MENU_PHOTO, caption=f"{translation['balance']}: {user.account_balance} {config.FIAT_CURRENCY}")
    list_menu_keys = [
        [InlineKeyboardButton(translation["products"],
                              callback_data="products")],
        # [InlineKeyboardButton(translation["website"], url=config.WEBSITE_URL)],
        # [InlineKeyboardButton(translation["group"], url=config.GROUP_URL)],
        [InlineKeyboardButton(translation["admin"], url=config.ADMIN_USER)],
        [InlineKeyboardButton(translation["purchase"],
                              callback_data="purchase")],
        [InlineKeyboardButton(translation["deposit"],
                              callback_data="create_deposit")]
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
        
        📦 <b>{translation['order_id']}</b> {purchase.id}
        
        <b>{translation['user_name']}</b> {purchase.buyer_username}
        <b>{translation['user_id']}</b> {purchase.buyer_id}
        
        <b>{translation['vendor_id']}</b> {purchase.vendor_id}
        <b>{translation['vendor_username']}</b> @{purchase.vendor_username}
        
        <b>{translation['user_address']}</b> {purchase.address}
        
        <b>{translation['product_name']}</b> {purchase.product_name}
        
        💰 <b>{translation['price']}</b> {purchase.price} {config.FIAT_CURRENCY}
        
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
            f"{translation['price']} {price} {config.FIAT_CURRENCY}", callback_data="create_product:price")],
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
