import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

required_variables = ['TOKEN', 'WEBHOOK_URL', 'BTCPAY_STORE_ID', 'BTCPAY_TOKEN']

for variable in required_variables:
    if variable not in os.environ:
        sys.exit(f'Missing environment variable: {variable}')

TOKEN = os.getenv('TOKEN', '545261****:AAFTdbRVxudUWM4k2OeF-Avkvvk7*******')
DEBUG = os.getenv('DEBUG', 'True')
PORT = os.getenv('PORT', 5001)

WEBHOOKMODE = os.getenv('WEBHOOKMODE', 'True')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://5001-richardokon-upgradedfcx-82z3zmfnasf.ws-eu97.gitpod.io')

DATABASE_URL = os.getenv('DATABASE_URL', "mongodb+srv://******:******@cluster0.vexqcep.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.getenv('DB_NAME', 'raznesi_bot')
GROUP_URL = os.getenv('GROUP_URL', 'https://t.me/followfootprintchat')
ADMIN_USER = os.getenv('ADMIN_USER', "https://t.me/@markyoku")
WEBSITE_URL = os.getenv('WEBSITE_URL', "https://queen.fugoku.com")
CURRENCY = os.getenv('CURRENCY', "BTC")
FIAT_CURRENCY = os.getenv('FIAT_CURRENCY', "USD")

MAX_CALLBACK_AGE_MINUTES = 1
MAX_MESSAGE_AGE_MINUTES = 1
ADMIN_ID = os.getenv('ADMIN_ID', 1053579181)
INVOICE_EXPIRATION_MINUTES = os.getenv('INVOICE_EXPIRATION_MINUTES', 90)

MENU_PHOTO = os.getenv('MENU_PHOTO', "https://mybestwine.ch/wp-content/uploads/2015/07/2015-07-b-.jpg-1200-x-400.jpg")
BTCPAY_STORE_ID = os.getenv('BTCPAY_STORE_ID', '4sfUtKnNNDvXzKEsyNyy5nrPe6WF31KL**********')
BTCPAY_TOKEN = os.getenv('BTCPAY_TOKEN', 'cf34fe5713d7e4988d871df0f0621**********')
BTCPAY_SERVER = os.getenv('BTCPAY_SERVER', 'https://testnet.demo.btcpayserver.org')

if not TOKEN:
    sys.exit('Missing environment variable TOKEN')
