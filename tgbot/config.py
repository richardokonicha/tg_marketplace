import os
import sys
import logging
from dotenv import load_dotenv
load_dotenv()

# Logging Setup
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO
)

# Validate the most important variables
required_variables = ['TOKEN', 'WEBHOOK_URL']

for variable in required_variables:
    if variable not in os.environ:
        sys.exit(f'Missing environment variable: {variable}')

# Telegram Bot Configuration
TOKEN = os.getenv('TOKEN', '5452611835:AAFTdbRVxudUWM4k2OeF-Avkvvk7wAfA34E')
DEBUG = os.getenv('DEBUG', 'True')
PORT = os.getenv('PORT', 5001)

# Webhook Configuration
WEBHOOKMODE = os.getenv('WEBHOOKMODE', 'True')
WEBHOOK_URL = os.getenv(
    'WEBHOOK_URL', 'https://5001-richardokon-upgradedfcx-82z3zmfnasf.ws-eu97.gitpod.io')

# Database Configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL', "mongodb+srv://admin-user:clientdbpass@cluster0.vexqcep.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.getenv('DB_NAME', 'raznesi_bot')
GROUP_URL = os.getenv('GROUP_URL', 'https://t.me/followfootprintchat')
ADMIN_USER = os.getenv('ADMIN_USER', "https://t.me/@markyoku")
WEBSITE_URL = os.getenv('WEBSITE_URL', "https://queen.fugoku.com")


# Admin Configuration
MAX_CALLBACK_AGE_MINUTES = 1
MAX_MESSAGE_AGE_MINUTES = 1
ADMIN_ID = os.getenv('ADMIN_ID', 1053579181)
MENU_PHOTO = os.getenv(
    'MENU_PHOTO', "https://mybestwine.ch/wp-content/uploads/2015/07/2015-07-b-.jpg-1200-x-400.jpg")

# Merchant Configuration
MERCHANT_ID = os.getenv('MERCHANT_ID', "c4baf6ef23be73a2da7fa05********")
MERCHANT_PKEY = os.getenv(
    'MERCHANT_PKEY', "c68f21F77B13FE4D6617EfcD0287c036da7A3aB1A5f3e870fb179E94********")
MERCHANT_PBKEY = os.getenv(
    'MERCHANT_PBKEY', "953b0c668c9d75c2d3da984f62a00fd269dc66c6da701250a0d7e14********")

# IPN Configuration
IPN_URL = os.getenv(
    'IPN_URL', "https://5001-richardokon-upgradedfcx-82z3zmfnasf.ws-eu97.gitpod.io")
PROXY = os.getenv('PROXY', 'http://proxy_ip:proxy_port')


# Validation
if not TOKEN:
    sys.exit('Missing env variable TOKEN')
