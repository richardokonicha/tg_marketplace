import requests
from tgbot import config
from decimal import Decimal

class BtcPay:
    def __init__(self, store_id, token):
        self.store_id = store_id
        self.token = token
        self.url = config.BTCPAY_SERVER

    def create_invoice(self, 
                       amount: Decimal, 
                       description: str, 
                       user_id: str, 
                       currency: str = config.CURRENCY, 
                       **kwargs) -> dict | None:
        "Creates a new btcpay invoice"
        try:
            checkout_data = {
                'metadata': {
                    'description': description,
                    'user_id': user_id,
                },
                'checkout': {
                    'speedPolicy': "HighSpeed",
                    'paymentMethods': [config.CURRENCY],
                    'defaultPaymentMethod': config.CURRENCY,
                    'expirationMinutes': config.INVOICE_EXPIRATION_MINUTES,
                    'monitoringMinutes': config.INVOICE_EXPIRATION_MINUTES,
                    'paymentTolerance': 100,
                    'redirectAutomatically': True,
                    'requiresRefundEmail': True,
                    'checkoutType': None,
                    'defaultLanguage': "en",
                },
                'receipt': {
                    'enabled': True,
                    'showQR': None,
                    'showPayments': None,
                },
                'amount': float(amount),
                'currency': currency,
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"token {self.token}"
            }
            url = f'{self.url}/api/v1/stores/{self.store_id}/invoices'

            req = requests.post(url=url, json=checkout_data,
                                headers=headers, **kwargs)
            print(req)
            print("New invoice created")
            return req.json()
        except Exception as e:
            print(e)
            return "Error creating an invoice"

    def get_invoice(self, invoice_id: str) -> dict | None:
        "Fetch a specific invoice"
        pass
