from mongoengine import Document, StringField, DecimalField, BooleanField, DateTimeField, IntField
from datetime import datetime

class User(Document):
    user_id = IntField(unique=True)
    name = StringField(required=True)
    is_vendor = BooleanField(default=False)
    language = StringField(default="en")
    address = StringField()
    registered_date = DateTimeField(default=datetime.now)
    is_new_user = BooleanField(default=True)
    last_visited = DateTimeField()
    account_balance = DecimalField(precision=6, default=0.00)

    def exists(self):
        return User.objects(user_id=self.user_id).first() is not None

    def set_last_visited(self):
        self.last_visited = datetime.now()
        self.save()


class Order(Document):
    """
    Bot Order Model
    """
    buyer = StringField(default="")
    from_id = IntField(default=0)
    vendor = StringField(default="")
    message_id = IntField(default=0)
    item = StringField(default="")
    address = StringField(default="")
    active = BooleanField(default=True)
    status = StringField(default="new")
    created_at = DateTimeField()
