from .coinpayment import CoinPayments
from tgbot import config

payment_client = CoinPayments(
    config.MERCHANT_PBKEY,
    config.MERCHANT_PKEY,
    ipn_url=config.IPN_URL + "pay",
    proxy=config.PROXY
)

# response = payment_client.irequest('post', **params)
