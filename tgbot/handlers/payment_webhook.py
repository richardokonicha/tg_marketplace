from werkzeug.exceptions import UnsupportedMediaType
from flask import request


def process_merchant_webhook(bot):
    try:
        data = request.json
        event_type = data['type']
    except UnsupportedMediaType:
        return 'Unsupported Media Type: request payload must be in JSON format', 415

    if event_type == 'InvoiceCreated':
        handle_invoice_created_webhook(data, bot)

    elif event_type == 'InvoicePaymentSettled' or event_type == 'InvoiceSettled':
        handle_invoice_paid_webhook(data, bot)

    elif event_type == 'InvoiceExpired':
        handle_invoice_expired_webhook(data, bot)

    return '', 200


def handle_invoice_created_webhook(data, bot):
    invoice_id = data['invoiceId']
    message = f"Invoice created for invoice {invoice_id} \n awaiting payment!"
    try:
        user_id = data['metadata']['user_id'] or None
        return bot.send_message(user_id, message)
    except:
        print('No user id linked to this webhook, ignoring')
        return


def handle_invoice_paid_webhook(data, bot):
    invoice_id = data['invoiceId']
    message = f"Payment received for invoice {invoice_id}!"
    try:
        user_id = data['metadata']['user_id'] or None
        bot.send_message(user_id, message)
        return bot.answer_callback_query(user_id, text=f"Invoice Created: {invoice_id}")
    except:
        print('No user id linked to this webhook, ignoring')
        return


def handle_invoice_expired_webhook(data, bot):
    invoice_id = data['invoiceId']
    message = f"Invoice Id {invoice_id} has expired!"
    try:
        user_id = data['metadata']['user_id'] or None
        bot.send_message(user_id, message)
        return bot.answer_callback_query(user_id, text=f"Invoice Created: {invoice_id}")
    except:
        print('No user id linked to this webhook, ignoring')
        return
