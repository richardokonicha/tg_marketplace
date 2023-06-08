from .btcpay import BtcPay
from tgbot import config

payment_client = BtcPay(
    config.BTCPAY_STORE_ID,
    config.BTCPAY_TOKEN
)
