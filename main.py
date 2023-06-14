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
register_handlers(bot, server)
bot.register_middleware_handler(antispam_func, update_types=['message'])
bot.add_custom_filter(AdminFilter())


@server.route('/' + config.TOKEN, methods=['POST', 'GET'])
def checkWebhook():
    bot.process_new_updates(
        [telebot_types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Your bot application is still active!", 200
# server.add_url_rule()

@server.route('/users')
@server.route('/dashboard')
def dashboard(name=None):
    action = request.args.get('action')
    user_id = request.args.get('user_id')

    if action == 'switch_role' and user_id:
        db.update_user(user_id=user_id, is_vendor=not db.get_user(user_id).is_vendor)
        print(f"Action performed for User ID: {user_id}")

    users = db.get_all_users()
    return render_template('users.html', users=users)

@server.route('/products')
def allProducts():
    action = request.args.get('action')
    product_id = request.args.get('product_id')

    # import pdb; pdb.set_trace()

    if action == 'delete_item' and product_id:
        db.delete_product(product_id=product_id)
        print(f"Product deleted with ID: {product_id}")

    products = db.get_all_products()
    return render_template('products.html', data=products)


@server.route('/orders')
def purchases():
    orders = db.get_all_purchases()
    return render_template('orders.html', data=orders)


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
