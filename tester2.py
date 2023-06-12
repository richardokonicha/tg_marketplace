from tgbot.models.model import Deposit
from tgbot.models import db
from datetime import datetime



old_user = db.get_user(1053579181)

deposit = Deposit(
    user=old_user,
    invoice_id="your_invoice_id",
    user_id=12345,
    message_id=67890,
    amount=100.0,
    amount_received="123.45",
    event_type="created",
    status="pending",
    updated_at=datetime.fromtimestamp(1686537280 / 1000)
)
deposit.save()

# Retrieve deposits
all_deposits = Deposit.objects()
