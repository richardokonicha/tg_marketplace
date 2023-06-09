# from tgbot.models import db
from tgbot.payments import payment_client


# newuser = db.create_user("777", "Pascal")


# old_user = db.get_user("777")

# print(old_user)

invoice = payment_client.create_invoice(
    amount=50,
    description="Deposit of {amount} USD from {user.name}"
)
print(invoice)
