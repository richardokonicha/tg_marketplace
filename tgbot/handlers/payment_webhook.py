from werkzeug.exceptions import UnsupportedMediaType
from flask import request
from tgbot.handlers.deposits import handle_invoice_created_webhook, handle_invoice_expired_webhook, handle_invoice_paid_webhook, handle_payment_recieved_webhook

def process_merchant_webhook(bot):
    data = request.get_json()
    if data['metadata'] == None: print("Webhook Test"); return 'Testing', 200
    try:
        event_type = data['type']
        print(event_type, "Webhook event from server merchant")
        if event_type == 'InvoiceCreated':
            handle_invoice_created_webhook(data, bot)
        if event_type == 'InvoiceReceivedPayment':
            handle_payment_recieved_webhook(data, bot)
        elif event_type in ['InvoicePaymentSettled', 'InvoiceSettled']:
            handle_invoice_paid_webhook(data, bot)
        elif event_type == 'InvoiceExpired':
            handle_invoice_expired_webhook(data, bot)
    except UnsupportedMediaType:
        return 'Unsupported Media Type: request payload must be in JSON format', 200
    except KeyError:
        return 'Invalid request payload: missing required field', 200
    return '', 200

