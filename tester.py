from tgbot.models import db
create_deposit_wdata = {
    'deliveryId': 'Fic6rdCgX1VncwR3jeLwqg', 
    'webhookId': '5v3gDCaXtGZtGKsJNvFmRZ', 'originalDeliveryId': 'Fic6rdCgX1VncwR3jeLwqg', 'isRedelivery': False, 'type': 'InvoiceCreated',
                        'timestamp': 1686532511, 'storeId': 'AZ2LDwZ8LEad4ctEgny89qnG1hEe2Dp4KSKcvm4bMY6K', 'invoiceId': 'GN8wcvB1mk2JyzHknxpspA', 'metadata': {'description': 'Deposit of 1.2e-05 BTC from Richard', 'user_id': 1053579181}}

invoice = {
    'id': 'GGmZvF3UkpZU899dyCwere',
    'storeId': 'AZ2LDwZ8LEad4ctEgny89qnG1hEe2Dp4KSKcvm4bMY6K',
    'amount': '0.000015',
    'checkoutLink': 'https://testnet.demo.btcpayserver.org/i/GGmZvF3UkpZU899dyCwere',
    'status': 'New',
    'additionalStatus': 'None',
    'monitoringExpiration': 1686526301,
    'expirationTime': 1686520901,
    'createdTime': 1686515501,
    'availableStatusesForManualMarking': ['Settled', 'Invalid'],
    'archived': False,
    'type': 'Standard',
    'currency': 'BTC',
    'metadata': {
        'description': 'Deposit of 1.5e-05 BTC from Richard',
        'user_id': 1053579181},

    'checkout': {
        'speedPolicy': 'HighSpeed',
        'paymentMethods': ['BTC'], 'defaultPaymentMethod': 'BTC', 'expirationMinutes': 90, 'monitoringMinutes': 90, 'paymentTolerance': 100.0, 'redirectURL': None, 'redirectAutomatically': True, 'requiresRefundEmail': True, 'defaultLanguage': 'en', 'checkoutType': None, 'lazyPaymentMethods': None},
    'receipt': {'enabled': True, 'showQR': None, 'showPayments': None}
}

db.create_deposit(
    invoice_id=invoice.id,
    user_id=invoice['metadata']['user_id'],
    message_id=message_id,
    amount=invoice.amount,
    event_type=invoice.type,
    status=invoice.status,
    created_at=invoice.created_time,
)

db.update_deposit(
    invoice_id=invoice.id,
    amount_recieved=invoice.payment['value'],
    event_type=invoice.type,
    status=invoice.payment['status'],
)

creat = {
    'deliveryId': 'WwoC135rVXDzLDgvB39bGV',
    'webhookId': '5v3gDCaXtGZtGKsJNvFmRZ',
    'originalDeliveryId': 'WwoC135rVXDzLDgvB39bGV',
    'isRedelivery': False,
    'type': 'InvoiceCreated',
    'timestamp': 1686515502,
    'storeId': 'AZ2LDwZ8LEad4ctEgny89qnG1hEe2Dp4KSKcvm4bMY6K',
    'invoiceId': 'GGmZvF3UkpZU899dyCwere',
    'metadata': {
        'description': 'Deposit of 1.5e-05 BTC from Richard',
        'user_id': 1053579181
    }
}

data = {
    'afterExpiration': False,
    'paymentMethod': 'BTC',
    'payment': {
        'id': 'ff9e795615fc9b2b062e655149a8892d1bda5d242e80d8a24d49c72aa5206f08-0',
        'receivedDate': 1686499519,
        'value': '0.00001',
        'fee': '0.0',
        'status': 'Settled',
        'destination': 'tb1qfcaq9836p0cx0zvs68rx5e0a0nvzncdlvnacyd'
    },
    'overPaid': False,
    'deliveryId': 'LL9CG96BBJTZSD5SEFN5v9',
    'webhookId': '5v3gDCaXtGZtGKsJNvFmRZ',
    'originalDeliveryId': 'LL9CG96BBJTZSD5SEFN5v9',
    'isRedelivery': False,
    'type': 'InvoicePaymentSettled',
    'timestamp': 1686500285,
    'storeId': 'AZ2LDwZ8LEad4ctEgny89qnG1hEe2Dp4KSKcvm4bMY6K',
    'invoiceId': 'DHuq7Cx5jhNYp47PoiGi18',
    'metadata':
        {
            'user_id': 1053579181,
            'description': 'Deposit of 1e-05 BTC from Richard'
    }
}


def handle_invoice_paid_webhook(data, bot=None):
    invoice_id = data['invoiceId']
    message = f"Payment received for invoice {invoice_id}!"
    try:
        user_id = data['metadata']['user_id'] or None
        bot.send_message(user_id, message)
        return bot.answer_callback_query(user_id, text=f"Invoice Created: {invoice_id}")
    except:
        print('No user id linked to this webhook, ignoring')
        return


# invoice = payment_client.create_invoice(
#     amount=amount,
#     user_id=user_id,
#     description=f"Deposit of {amount} {config.CURRENCY} from {user.name}",
# )
