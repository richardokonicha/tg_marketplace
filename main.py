import os
from flask import Flask, request, render_template
from telebot import TeleBot, apihelper, types as telebot_types
from tgbot import config
from tgbot.filters.admin_filter import AdminFilter

from tgbot.handlers import register_handlers
from tgbot.middlewares.antiflood_middleware import antispam_func
from tgbot.models import db


apihelper.ENABLE_MIDDLEWARE = True

server = Flask(__name__, template_folder='tgbot/templates')
bot = TeleBot(config.TOKEN, num_threads=5)


@bot.message_handler(commands=['test'])
def test(message):
    """
    You can create a function and use parameter pass_bot.
    """
    bot.send_message(message.chat.id, "Hello, testing !")


register_handlers(bot)

bot.register_middleware_handler(antispam_func, update_types=['message'])
bot.add_custom_filter(AdminFilter())


@server.route('/' + config.TOKEN, methods=['POST', 'GET'])
def checkWebhook():
    bot.process_new_updates(
        [telebot_types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Your bot application is still active!", 200


@server.route('/dashboard/')
@server.route('/dashboard/<name>')
def dashboard(name=None):
    users = db.get_all_users()
    return render_template('dashboard.html', name=name, users=users)


@server.route("/")
def webhook():
    bot.remove_webhook()
    hook = f'{config.WEBHOOK_URL}/{config.TOKEN}'
    bot.set_webhook(url=hook)
    return f'Application running! <br/> TG Listening {hook} <br/> Webhook set to {config.WEBHOOK_URL}', 200


def run_web():
    if __name__ == "__main__":
        server.run(
            host="0.0.0.0",
            threaded=True,
            port=int(os.environ.get('PORT', 5001)),
        )


def run_poll():
    webhook_info = bot.get_webhook_info()
    if webhook_info.url:
        bot.delete_webhook()
    bot.infinity_polling()
    print("Bot polling!")


if config.WEBHOOKMODE == "False":
    run_poll()
else:
    run_web()
