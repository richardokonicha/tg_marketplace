from models import User
import asyncio
import logging
from datetime import datetime
import os
import re
from flask import Flask, request
from datetime import date
import telebot
from pymongo import MongoClient
from telebot import types

from dotenv import load_dotenv
load_dotenv()


user = User


# Logging Setup
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv('TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
database_client = MongoClient(DATABASE_URL)

DEBUG = True
SERVER_URL = os.getenv("SERVER_URL")
ADMIN = os.getenv("ADMIN")

bot = telebot.TeleBot(token=TOKEN)
app = Flask(__name__)

handler_state = {}
