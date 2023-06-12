# Using database
# from tgbot.models import db
# newuser = db.create_user("777", "Pascal")
# old_user = db.get_user("777")
# print(old_user)

# Create a new deposit
from tgbot.models.model import Deposit
from tgbot.models import db


old_user = db.get_user(1053579181)

deposit = Deposit(
    user=old_user,
    invoice_id="your_invoice_id",
    user_id=12345,
    message_id=67890,
    amount=100.0,
    amount_received="123.45",
    event_type="created",
    status="pending"
)
deposit.save()

# Retrieve deposits
all_deposits = Deposit.objects()
