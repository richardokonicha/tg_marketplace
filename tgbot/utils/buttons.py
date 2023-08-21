from telebot import types, TeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import sys
import os
from telebot.types import InputMediaPhoto
from tgbot import config


force_reply = types.ForceReply(input_field_placeholder="Enter value")

expired_reply = InlineKeyboardMarkup([[InlineKeyboardButton(text="Invoice Expired", callback_data="expired")]])
created_reply = InlineKeyboardMarkup([[InlineKeyboardButton(text="Invoice Created", callback_data="created")]])

def edited_reply(text):
    return InlineKeyboardMarkup(
        [
        [InlineKeyboardButton(text=f"{text}", callback_data=f"{text}")] 
        ]
    )
    

def vendor_notification(user, product, stock_item):
    lang = user.language
    translations = {
        "en": {
            "vendor_notification_text": """
The buyer has paid {price}{fiat} for the product {product_name}.

From User {user_name}
Address:  {address}
UserId:   {user_id}
Username:  @{user_username}
    
New Order:  {product_name} 
Price:       {price} {fiat}
Stock Item: {stock_item}
            """,
        },
        "ru": {
             "vendor_notification_text": """
The buyer has paid {price}{fiat} to for the product {product_name}.

From User {user_name}
Address:  {address}
UserId:   {user_id}
Username:  @{user_username}
    
New Order:  {product_name} 
Price:       {price} {fiat}
Stock Item: {stock_item}
            """,
        }
    }
    translation = translations.get(lang, translations["en"])
    data = {
        'price': product.price,
        'fiat': config.FIAT_CURRENCY,
        'product_name': product.name,
        'address':user.address,
        'user_id':user.user_id,
        'user_name': user.name,
        'user_username': user.username,
        'description': product.description,
        'stock_item': stock_item
    }
    notification_text = translation['vendor_notification_text'].format(**data)
    return notification_text

def purchase_address_markup(user, purchase, invoice, state=None):
    lang = user.language
    invoice_link = invoice['checkoutLink']
    translations = {
        "en": {
            "purchase_address_text": """
Invoice for {product_name} Purchase
InvoiceId: {invoice_id}

You're purchasing {product_name}
Cost: {invoice_amount} {invoice_currency}
Please proceed with the payment by clicking Pay Now

Make sure to complete the payment of {invoice_amount} {invoice_currency} within the provided expiration time.
                """,
            "purchase_address_processing": "Payment is currently being processed for {product_name}.",
            "purchase_address_settled": "Payment has been settled for {product_name}.",
            "back_to_menu": "<<",
            "pay": "💰Pay now",
            "processing": "Processing Payment",
            "settled": "Payment Settled"
        },
        "ru": {
            "purchase_address_text": """
Счет-фактура создан: {invoice_id}

Вы вносите {invoice_amount} {invoice_currency}
Пожалуйста, продолжите оплату, нажав «Оплатить сейчас»

Убедитесь, что вы завершили платеж {invoice_amount} {invoice_currency} в течение указанного срока действия.
                """,
            "purchase_address_processing": "Оплата в настоящее время обрабатывается для {product_name}.",
            "purchase_address_settled": "Оплата прошла успешно для {product_name}.",
            "back_to_menu": "<<",
            "pay": "💰Оплатить сейчас",
            "processing": "Обработка оплаты",
            "settled": "Оплата завершена"
        }
    }

    translation = translations.get(lang, translations["en"])
    keyboard = []
    data = {
        'product_name': purchase.product_name,
        'invoice_id': invoice['id'],
        'invoice_amount': invoice['amount'],
        'invoice_currency': invoice['currency']
    }
    if state is None:
        purchase_text = translation['purchase_address_text'].format(**data)
        keyboard.append(InlineKeyboardButton(translation['pay'], url=invoice_link))
    elif state == "processing":
        purchase_text = translation['purchase_address_processing'].format(**data)
        keyboard.append(InlineKeyboardButton(translation['processing'], url=invoice_link))
    elif state == "settled":
        purchase_text = translation['purchase_address_settled'].format(**data)
        keyboard.append(InlineKeyboardButton(translation['settled'], url=''))
    keyboard.append(InlineKeyboardButton("Cancel", callback_data="cancel"))
    return purchase_text, InlineKeyboardMarkup([keyboard])


def deposit_address_markup(user, invoice):
    lang = user.language
    invoice_link = invoice['checkoutLink']

    translations = {
        "en": {
            "deposit_address_text": """
Invoice Created: {invoice_id}

You're depositing {invoice_amount} {invoice_currency}
Please proceed with the payment by clicking Pay now

Make sure to complete the payment of {invoice_amount} {invoice_currency} within the provided expiration time.
                """,
            "back_to_menu": "<<",
            "pay": "💰Pay now"
        },
        "ru": {
            "deposit_address_text": """
Счет-фактура создан: {invoice_id}

Вы вносите {invoice_amount} {invoice_currency}
Пожалуйста, продолжите оплату, нажав «Оплатить сейчас»

Убедитесь, что вы завершили платеж {invoice_amount} {invoice_currency} в течение указанного срока действия.
                """,
            "back_to_menu": "<<",
            "pay": "💰Оплатить сейчас"
        }
    }

    translation = translations.get(lang, translations["en"])

    data = {
        'invoice_id': invoice['id'],
        'invoice_amount': invoice['amount'],
        'invoice_currency': invoice['currency']
    }

    deposit_text = translation['deposit_address_text'].format(**data)

    keyboard = [
        [
            InlineKeyboardButton(translation['pay'], url=invoice_link),
            InlineKeyboardButton("Cancel", callback_data="cancel")
        ]
    ]

    return deposit_text, InlineKeyboardMarkup(keyboard)


def deposit_markup(user):
    lang = user.language
    translations = {
        "en": {
            "balance_text": "Wallet Balance is {account_balance}",
            "deposit_text": """<b>Enter the amount you wish to deposit (min: 10 {fiat} max: 5,000,000 {fiat})</b>""",
            "back_to_menu": "<<",
            "input_holder": "Enter value"
        },
        "ru": {
            "balance_text": "Wallet Balance is {account_balance}",
            "deposit_text": """Введите сумму, которую вы хотите внести (мин.: 10 {fiat} max: 5,000,000 {fiat} )""",
            "back_to_menu": "<<",
            "input_holder": "Enter value"
        }
    }
    data = {
        'account_balance': user.account_balance,
        'fiat': config.FIAT_CURRENCY,
    }
    translation = translations.get(lang, translations["en"])
    force_reply = types.ForceReply(input_field_placeholder=translation['input_holder'])
    deposit_text = translation['deposit_text'].format(**data)
    return deposit_text, force_reply



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
            "view_product_text": """
{owner} Product:

<b>Product Name:</b> {name}

<b>Category:</b> {category}

<b>Stock:</b> {description}x
{stock_list}

💰 <b>Price:</b> {price} {fiat}

    """,
            "delete": "Delete",
            "buy": "Buy",
            "cancel": "Cancel",
            "mine": "Vendor: My",
            "view": "View"
        },
        "ru": {
            "view_product_text": """
{owner} Product:

<b>Product Name:</b> {name}

<b>Category:</b> {category}

<b>Stock:</b> {description}x
{stock_list}

💰 <b>Price:</b> {price} {fiat}

    """,
            "delete": "Delete",
            "buy": "Buy",
            "cancel": "Cancel",
            "mine": "Vendor: Моё",
            "view": "view"
        },
    }

    translation = translations.get(lang, translations["en"])
    
    stock_list = ''.join([f"{i} \n" for i in product.description])

    data = {
        'name': product.name,
        'price': product.price,
        'fiat': config.FIAT_CURRENCY,
        'description': len(product.description),
        'stock_list': stock_list if user_id == product.vendor_id else " ",
        'category': product.category,
        'owner': translation['mine'] if user_id == product.vendor_id else translation['view']
    }

    view_product_text = translation['view_product_text'].format(**data)
    
    key = [
        InlineKeyboardButton(translation['delete'], callback_data=f"delete_product:{product.id}")
    ] if user_id == product.vendor_id else [
        InlineKeyboardButton(translation['buy'], callback_data=f"confirm_payment:{product.id}")
    ]
    key.append(InlineKeyboardButton(translation['cancel'], callback_data="cancel"))
    
    return view_product_text, InlineKeyboardMarkup([key])


def order_placed_markup(product, purchase, user, stock_item):
    lang = user.language
    
    translations = {
        "en": {
            "order_placed_text": """
    You have successfully paid {price} {fiat} for the product {name}.

    📦 <b>Order ID:</b> {purchase_id}

    📝 <b>Purchase Status:</b> {status}

    <b>Product Name:</b> {name}

    💰 <b>Price:</b> {price} {fiat}

    📝 <b>Stock Item:</b>
    {stock_item}
    """,
            "continue_shopping": "Continue Shopping"
        },
        "ru": {
            "order_placed_text": """
    Вы успешно оплатили {price} {fiat} с вашего баланса за товар {name}.

    📦 <b>Номер заказа:</b> {purchase_id}

    📝 <b>Статус заказа:</b> {status}

    <b>Название товара:</b> {name}

    💰 <b>Цена:</b> {price} {fiat}

    📝 <b>Stock Item:</b>
    {stock_item}
    """,
            "continue_shopping": "Продолжить покупки"
        }
    }

    translation = translations.get(lang, translations["en"])

    data = {
        'name': product.name,
        'description': product.description,
        'status': purchase.status,
        'purchase_id': purchase.id,
        'fiat': config.FIAT_CURRENCY,
        'price': product.price,
        'stock_item': stock_item
    }
    order_placed_text = translation['order_placed_text'].format(**data)

    continue_button = InlineKeyboardButton(
        translation['continue_shopping'], callback_data="continue_shopping")
    keyboard = [[continue_button]]
    return order_placed_text, InlineKeyboardMarkup(keyboard)


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


def all_categories_markup(categories, user):
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

    all_categories_markup = []
    media = InputMediaPhoto(config.MENU_PHOTO, caption=translation['balance'])
    for category in categories:
        all_categories_markup.append([
            InlineKeyboardButton(
                category.category_name.capitalize(), callback_data=f"view_category:{category.category_name}")
        ])
    all_categories_markup.append([
        InlineKeyboardButton(
            translation['back_to_menu'], callback_data="back_to_menu")
    ])
    return media, InlineKeyboardMarkup(all_categories_markup)
    


def get_create_product_keyboard(user, fields=None):
    lang = user.language
    translations = {
        "en": {
            "name": "Name",
            "category": "Category",
            "description": "Description",
            "price": "Price",
            "back_to_menu": "<<",
            "enter_name": "Enter name",
            "enter_category": "Enter Category",
            "enter_description": "Enter description",
            "enter_price": "Enter price"
        },
        "ru": {
            "name": "Название",
            "category": "Category",
            "description": "Описание",
            "price": "Цена",
            "back_to_menu": "<<",
            "enter_name": "Введите название",
            "enter_category": "Enter Category",
            "enter_description": "Введите описание",
            "enter_price": "Введите цену"
        }
    }

    translation = translations[lang] if lang in translations else translations["en"]

    name = fields.get(
        'name', translation['enter_name']) if fields else translation['enter_name']
    category = fields.get(
        'category', translation['enter_category']) if fields else translation['enter_category']
    description = fields.get(
        'description', translation['enter_description']) if fields else translation['enter_description']
    price = fields.get(
        'price', translation['enter_price']) if fields else translation['enter_price']

    create_product_keyboard = [
        [InlineKeyboardButton(
            f"{translation['name']}: {name}", callback_data="create_product:name")],
        [InlineKeyboardButton(
            f"{translation['category']}: {category}", callback_data="create_product:category")],
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
            "all_categories": "All Categories",
            "vendor_products": "Vendor Products 📙",
            "create_product": "Create New Product 🔎",
            "back_to_menu": "<<"
        },
        "ru": {
            "balance": "Wallet Баланс 💵 ",
            "all_products": "Все товары 🧶",
            "all_categories": "All Categories",
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
                translation["all_categories"], callback_data="all_categories")],
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
                translation["all_categories"], callback_data="all_categories")],
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
            "view_purchase_text": """
View Orders

📦 <b>Order ID:</b> {purchase_id}

<b>User Name:</b> @{buyer_username}
<b>User ID:</b> {buyer_id}

<b>Vendor ID:</b> {vendor_id}
<b>Vendor Username:</b> @{vendor_username}

<b>User Address:</b> {address}

<b>Product Name:</b> {product_name}

💰 <b>Price:</b> {price} {fiat}

📝 <b>Stock Item:</b>
{description}
            """,
            "completed": "Completed",
            "cancel": "Cancel"
        },
        "ru": {
            "view_purchase_text": """
Просмотр заказов

📦 <b>Номер заказа:</b> {purchase_id}

<b>Имя пользователя:</b> {buyer_username}
<b>ID пользователя:</b> {buyer_id}

<b>ID продавца:</b> {vendor_id}
<b>Имя продавца:</b> @{vendor_username}

<b>Адрес пользователя:</b> {address}

<b>Название продукта:</b> {product_name}

💰 <b>Цена:</b> {price} {fiat}

📝 <b>Описание:</b>
{description}
            """,
            "completed": "Завершено",
            "cancel": "Отмена"
        }
    }
    translation = translations.get(lang, translations["en"])
    data = {
        'purchase_id': purchase.id,
        'buyer_username': purchase.buyer_username,
        'fiat': config.FIAT_CURRENCY,
        'buyer_id': purchase.buyer_id,
        'vendor_id': purchase.vendor_id,
        'vendor_username': purchase.vendor_username,
        'address': purchase.address,
        'product_name': purchase.product_name,
        'price': purchase.price,
        'description': purchase.description,
    }
    view_purchase_text = translation['view_purchase_text'].format(**data)
    # is_vendor = user.is_vendor
    # if is_vendor:
    #     button_text = translation['completed']
    #     button_callback = f"complete_purchase:{purchase.id}"
    # else:
    button_text = translation['cancel']
    button_callback = "cancel"
    keyboard = [[InlineKeyboardButton(button_text, callback_data=button_callback)]]
    return view_purchase_text, InlineKeyboardMarkup(keyboard)


def get_create_product_keyboard(user, fields=None):
    lang = user.language
    translations = {
        "en": {
            "name": "Name:",
            "category": "Categories:",
            "description": "Stock:",
            "price": "Price:",
            "back_to_menu": "<<"
        },
        "ru": {
            "name": "Название:",
            "category": "Categories:",
            "description": "Stock:",
            "price": "Цена:",
            "back_to_menu": "<<"
        }
    }

    translation = translations[lang] if lang in translations else translations["en"]
    name = fields.get(
        'name', translation['name']) if fields else translation['name']
    category = fields.get(
        'category', translation['category']) if fields else translation['category']
    description = fields.get(
        'description', translation['description']) if fields else translation['description']
    price = fields.get(
        'price', translation['price']) if fields else translation['price']
    create_product_keyboard = [
        [InlineKeyboardButton(
            f"{translation['name']} {name}", callback_data="create_product:name")],
        [InlineKeyboardButton(
            f"{translation['category']} {category}", callback_data="create_product:category")],
        [InlineKeyboardButton(
            f"{translation['description']} {len(description)}x", callback_data="create_product:description")],
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
