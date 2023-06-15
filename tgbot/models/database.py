import mongoengine
import certifi
from tgbot.models.model import User, Product, Purchase, Deposit, Category, Categoryy
from tgbot import config
from typing import List
from decimal import Decimal
from datetime import datetime
from mongoengine import ObjectIdField
from typing import Optional

mongoengine.connect(db=config.DB_NAME,
                    host=config.DATABASE_URL, tlsCAFile=certifi.where())

class Database:
    @staticmethod
    def get_user(user_id):
        return User.objects(user_id=user_id).first()

    @staticmethod
    def create_user(user_id, name, username: str, language=None, address=None, is_vendor=False):
        user = User(
            user_id=user_id,
            name=name,
            username=username,
            is_vendor=is_vendor,
            address=address,
            language=language
        )
        user.save()
        return user

    @staticmethod
    def set_language(user_id, language):
        user = User.objects(user_id=user_id).first()
        if user:
            user.language = language
            user.save()
            return user
        return None
    
    @staticmethod
    def update_balance(user_id, payment):
        user = User.objects(user_id=user_id).first()
        new_balance = user.account_balance + payment
        if user:
            user.account_balance = new_balance
            user.save()
            return user
        return None

    @staticmethod
    def update_user(user_id, **kwargs):
        user = User.objects(user_id=user_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.save()
            return user
        return None

    @staticmethod
    def delete_user(user_id):
        user = User.objects(user_id=user_id).first()
        if user:
            user.delete()
            return True
        return False

    @staticmethod
    def get_all_users():
        return User.objects()

    @staticmethod
    def get_products_by_vendor(vendor_id: str) -> List[Product]:
        products = Product.objects(vendor_id=vendor_id)
        return products

    @staticmethod
    
    def create_product(name: str, description: str, price: Decimal, vendor_id: int, vendor_username: str, category: str = None,) -> Product:
        product = Product(name=name, description=description,
                          price=price, category=category, vendor_id=vendor_id, vendor_username=vendor_username)
        product.save()
        return product

    @staticmethod
    def delete_product(product_id):
        product = Product.objects(id=product_id).first()
        if product:
            product.delete()
            return True
        return False

    @staticmethod
    def get_product_by_id(product_id: str) -> Product:
        product = Product.objects(id=product_id).first()
        return product

    @staticmethod
    def update_product(product: Product, **kwargs) -> Product:
        for key, value in kwargs.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def get_all_products() -> List[Product]:
        products = Product.objects()
        return products
    
    @staticmethod
    def get_all_product_category(category_name: str) -> List[Product]:
        products = Product.objects(category=category_name.lower())
        return products
    
    
    @staticmethod
    def get_all_categories_set() -> set:
        categories = Category.objects()
        category_set = set(category.category_name for category in categories)
        return category_set

    
    @staticmethod
    def get_all_categories() -> List[Category]:
        categories = Category.objects()
        return categories
    
    @staticmethod
    def get_category(category_name) -> Category:
        category = Category.objects(category_name=category_name.lower()).first()
        if category:
            return category
        return False
    
    
    @staticmethod
    def create_category(category_name: str) -> Category:
        try:
            category = Category(category_name=category_name.lower())
            category.save()
            return category
        except Exception as e:
            print("An error occurred:", e)
            return False
        
    @staticmethod
    def create_purchase(user_id: int, buyer_username: str, buyer_id: int, vendor_id: int, vendor_username: str, product_id: str, product_name: str, address: str, price: Decimal, description: str, status: str) -> Purchase:
        purchase = Purchase(
            user_id=user_id,
            buyer_username=buyer_username,
            buyer_id=buyer_id,
            vendor_id=vendor_id,
            vendor_username=vendor_username,
            product_id=product_id,
            product_name=product_name,
            address=address,
            price=price,
            description=description,
            status=status
        )
        purchase.save()
        return purchase

    @staticmethod
    def get_purchase_by_id(purchase_id: int) -> Purchase:
        purchase = Purchase.objects(id=purchase_id).first()
        return purchase

    @staticmethod
    def get_active_purchases() -> List[Purchase]:
        purchases = Purchase.objects(active=True)
        return purchases

    @staticmethod
    def get_purchases_by_vendor(vendor_id) -> List[Purchase]:
        purchases = Purchase.objects(vendor_id=vendor_id)
        return purchases

    @staticmethod
    def get_purchases_by_user(user_id) -> List[Purchase]:
        purchases = Purchase.objects(user_id=user_id)
        return purchases

    @staticmethod
    def update_purchase(purchase: Purchase, **kwargs) -> Purchase:
        for key, value in kwargs.items():
            setattr(purchase, key, value)
        purchase.save()
        return purchase

    @staticmethod
    def create_deposit(user: User,  invoice_id: str, invoice_type: str, user_id: int, message_id: str, amount: Decimal, event_type: str, status: str, purchase_id: Optional[ObjectIdField] = None) -> Deposit:
        deposit = Deposit(
            user=user,
            invoice_id=invoice_id,
            invoice_type=invoice_type,
            user_id=user_id,
            message_id=message_id,
            amount=amount,
            event_type=event_type,
            status=status,
            purchase_id=purchase_id
        )
        deposit.save()
        return deposit

    @staticmethod
    def update_deposit(deposit: Deposit, **kwargs) -> Deposit:
        for key, value in kwargs.items():
            setattr(deposit, key, value)
        deposit.save()
        return deposit

    @staticmethod
    def update_deposit_by_invoice_id(invoice_id: str, **kwargs) -> Deposit:
        deposit = Deposit.objects(invoice_id=invoice_id).first()
        if deposit:
            for key, value in kwargs.items():
                if key == 'updated_at':
                    value = datetime.fromtimestamp(value / 1000)
                setattr(deposit, key, value)
            deposit.save()
        return deposit
    
    @staticmethod
    def get_deposit_by_invoice_id(invoice_id: str) -> Deposit:
        deposit = Deposit.objects(invoice_id=invoice_id).first()
        return deposit
