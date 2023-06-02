from telebot import TeleBot
from telebot.types import Message
from tgbot.models import db
from tgbot.utils.messages import messages
# from tgbot.utils.buttons import dashboard

def transaction(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    transactions = db.get_transactions(user_id)

    deposits = []
    payouts = []
    reinvestments = []
    commissions = []

    for value in transactions:
        if value.transaction_type == "deposit" and value.status == "Completed":
            deposits.append(f"{value.date.split('T')[0]}   {value.amount} BTC")
        elif value.transaction_type == "withdrawal":
            payouts.append(f"{value.date.split('T')[0]}   {value.amount} BTC")
        elif value.transaction_type == "reinvestment":
            reinvestments.append(f"{value.date.split('T')[0]}   {value.amount} BTC")
        elif value.transaction_type == "commissions":
            commissions.append(f"{value.date.split('T')[0]}   {value.amount} BTC")

    text_deposit = '\n'.join(deposits)
    text_reinvestments = '\n'.join(reinvestments)
    text_payout = '\n'.join(payouts)
    text_commissions = '\n'.join(commissions)

    transaction_text_info = messages["transaction_text_info"][lang]
    transaction_text_info_data = transaction_text_info.format(
        text_deposit=text_deposit,
        text_payout=text_payout,
        text_reinvestments=text_reinvestments,
        text_commissions=text_commissions
    )

    fcx_markup_balances = messages["fcx_markup_balances"][lang]
    fcx_markup_balances_lang = fcx_markup_balances.format(account_balance=fcx_user.account_balance)
    dashboard[lang].keyboard[0][0] = fcx_markup_balances_lang

    try:
        bot.send_message(
            chat_id,
            text=transaction_text_info_data,
            reply_markup=dashboard.get(lang),
            parse_mode="html"
        )
    except TypeError:
        bot.send_message(
            chat_id,
            text="No Transactions yet",
            reply_markup=dashboard.get(lang),
            parse_mode="html"
        )
