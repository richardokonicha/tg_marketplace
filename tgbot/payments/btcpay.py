import urllib.request
import urllib.parse
import urllib.error
import hmac
import hashlib
import json
import requests
from tgbot import config


class BtcPay():
    def __init__(self, store_id, token):
        self.store_id = store_id
        self.token = token
        self.url = 'https://mainnet.demo.btcpayserver.org'

    
    def create_invoice(self, amount: float, description: str) -> dict | None:
        "Creates a new btcpay invoice"

        try:
        
            checkout_data = {
                'metadata': {
                    'description': description
                },
                'checkout': {
                    'speedPolicy': "HighSpeed",
                    'paymentMethods': ["LTC"],
                    'defaultPaymentMethod': "LTC",
                    'expirationMinutes': 90,
                    'monitoringMinutes': 90,
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
                'amount': amount,
                'currency': 'USD',
            }

            # import pdb; pdb.set_trace()


            headers = {
                "Content-Type": "application/json",
                "Authorization": f"token {self.token}"
            }
            url = self.url + f'/api/v1/stores/{self.store_id}/invoices'

            req = requests.post(url=url, data=checkout_data, headers=headers, **kwargs)
            
            print(req)
            print("New invoice created")

            return req


        
        except Exception as e:
            print(e)
            return "Error creating an invoice"





    def get_invoice(self, invoice_id: str) -> dict | None:
        "Fetch a specific invoice"
        pass







