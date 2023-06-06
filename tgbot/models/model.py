from mongoengine import Document, StringField, DecimalField, BooleanField, DateTimeField, IntField, ObjectIdField
from datetime import datetime


class User(Document):
    user_id = IntField(unique=True)
    name = StringField(required=True)
    username = StringField(default="unknown")
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


class Purchase(Document):
    user_id = IntField(default="")
    buyer_username = StringField(default="")
    buyer_id = IntField(default="")
    vendor_id = IntField(default="")
    vendor_username = StringField(default="")
    product_id = ObjectIdField(default="")
    product_name = StringField(default="")
    price = StringField(default="$")
    description = StringField(default="description")
    address = StringField(default="")
    active = BooleanField(default=True)
    status = StringField(default="new")
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    def get_created_at(self):
        formatted_date = self.created_at.strftime("%d %b")
        return formatted_date


class Product(Document):
    name = StringField(required=True)
    description = StringField(default="")
    price = StringField(required=True)
    category = StringField(default="General")
    vendor_id = IntField(required=True)
    vendor_username = StringField(default="")

    meta = {
        'collection': 'products'
    }
