import urllib.request
import urllib.parse
import urllib.error
import hmac
import hashlib
import json
import requests

class CoinPayments():
    def __init__(self, public_key, private_key, ipn_url=None, proxy=None):
        self.url = 'https://www.coinpayments.net/api.php'
        self.public_key = public_key
        self.private_key = private_key
        self.ipn_url = ipn_url
        self.format = 'json'
        self.version = 1
        self.proxy = proxy


    def create_hmac(self, **params):
        encoded = urllib.parse.urlencode(params).encode('utf-8')
        return encoded, hmac.new(bytearray(self.private_key, 'utf-8'), encoded, hashlib.sha512).hexdigest()

    def irequest(self, request_method, **params):
        encoded, sig = self.create_hmac(**params)
        headers = {'hmac': sig}
        proxies = {'http': self.proxy, 'https': self.proxy} if self.proxy else None
        try:
            if request_method == 'get':
                reqs = requests.get(self.url, headers=headers, proxies=proxies, timeout=1000)
            elif request_method == 'post':
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                reqs = requests.post(self.url, data=encoded, headers=headers, proxies=proxies, timeout=1000)
            response_body = reqs.text
        except requests.exceptions.RequestException as error:
            response_body = str(error)
        return json.loads(response_body)

    def create_transaction(self, params=None):
        """
        Creates a transaction to give to the purchaser
        https://www.coinpayments.net/apidoc-create-transaction
        """
        if params is None:
            params = {}
        if self.ipn_url:
            params.update({'ipn_url': self.ipn_url})
        params.update({'cmd': 'create_transaction',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def get_basic_info(self, params=None):
        """
        Gets merchant info based on API key (callee)
        https://www.coinpayments.net/apidoc-get-basic-info
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_basic_info',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def rates(self, params=None):
        """
        Gets current rates for currencies
        https://www.coinpayments.net/apidoc-rates
        """
        if params is None:
            params = {}
        params.update({'cmd': 'rates',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def balances(self, params=None):
        """
        Get current wallet balances
        https://www.coinpayments.net/apidoc-balances
        """
        if params is None:
            params = {}
        params.update({'cmd': 'balances',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def get_deposit_address(self, params=None):
        """
        Get address for personal deposit use
        https://www.coinpayments.net/apidoc-get-deposit-address
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_deposit_address',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def get_callback_address(self, params=None):
        """
        Get a callback address to recieve info about address status
        https://www.coinpayments.net/apidoc-get-callback-address
        """
        if params is None:
            params = {}
        if self.ipn_url:
            params.update({'ipn_url': self.ipn_url})
        params.update({'cmd': 'get_callback_address',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def create_transfer(self, params=None):
        """
        Not really sure why this function exists to be honest, it transfers
        coins from your addresses to another account on coinpayments using
        merchant ID
        https://www.coinpayments.net/apidoc-create-transfer
        """
        if params is None:
            params = {}
        params.update({'cmd': 'create_transfer',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def create_withdrawal(self, params=None):
        """
        Withdraw or masswithdraw(NOT RECOMMENDED) coins to a specified address,
        optionally set a IPN when complete.
        https://www.coinpayments.net/apidoc-create-withdrawal
        """
        if params is None:
            params = {}
        params.update({'cmd': 'create_withdrawal',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def convert_coins(self, params=None):
        """
        Convert your balances from one currency to another
        https://www.coinpayments.net/apidoc-convert
        """
        if params is None:
            params = {}
        params.update({'cmd': 'convert',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def get_withdrawal_history(self, params=None):
        """
        Get list of recent withdrawals (1-100max)
        https://www.coinpayments.net/apidoc-get-withdrawal-history
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_withdrawal_history',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def get_withdrawal_info(self, params=None):
        """
        Get information about a specific withdrawal based on withdrawal ID
        https://www.coinpayments.net/apidoc-get-withdrawal-info
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_withdrawal_info',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def get_conversion_info(self, params=None):
        """
        Get information about a specific withdrawal based on withdrawal ID
        https://www.coinpayments.net/apidoc-get-conversion-info
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_conversion_info',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)

    def get_tx_info_multi(self, params=None):
        """
        Get tx info (up to 25 ids separated by | )
        https://www.coinpayments.net/apidoc-get-tx-info
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_tx_info_multi',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.irequest('post', **params)
