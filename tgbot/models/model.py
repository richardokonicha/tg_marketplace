from mongoengine import Document, StringField, DecimalField, BooleanField, DateTimeField, IntField, ObjectIdField, ReferenceField
from datetime import datetime
from decimal import Decimal


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
    account_balance = DecimalField(precision=2, rounding='ROUND_HALF_UP', default=Decimal('0.00'))

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
    price = DecimalField(precision=2, rounding='ROUND_HALF_UP', default=Decimal('0.00'))
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
    price = DecimalField(precision=2, rounding='ROUND_HALF_UP', default=Decimal('0.00'))
    category = StringField(default="General")
    vendor_id = IntField(required=True)
    vendor_username = StringField(default="")

    meta = {
        'collection': 'products'
    }
    

class Category(Document):
    category_name = StringField(required=True, unique=True)
    meta = {
        'collection': 'categoryi'
    }

    def save(self, *args, **kwargs):
        # Check if category name already exists
        existing_category = Category.objects(category_name=self.category_name).first()
        if existing_category:
            raise ValueError(f"Category '{self.category_name}' already exists.")
        
        super(Category, self).save(*args, **kwargs)

    
class Categoryy(Document):
    category_name = StringField(required=True, unique=True)
    meta = {
        'collection': 'categoryy'
    }


class Deposit(Document):
    user = ReferenceField('User', required=True)
    invoice_id = StringField(unique=True)
    purchase_id = ObjectIdField(default=None, null=True)
    invoice_type = StringField(default="deposit")
    user_id = IntField(default="created")
    message_id = IntField(default="0") 
    amount = DecimalField(precision=2, rounding='ROUND_HALF_UP', default=Decimal('0.00'))
    amount_received = DecimalField(precision=2, rounding='ROUND_HALF_UP', default=Decimal('0.00'))
    event_type = StringField(default="created")
    status = StringField(default="none")
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'deposits',
        'datetime_format': 'iso8601'
    }
