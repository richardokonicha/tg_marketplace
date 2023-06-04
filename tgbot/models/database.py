import mongoengine
import certifi
from tgbot.models.model import User, Product, Purchase
from tgbot import config
from typing import List

mongoengine.connect(db=config.DB_NAME,
                    host=config.DATABASE_URL, tlsCAFile=certifi.where())


class Database:
    @staticmethod
    def get_user(user_id):
        return User.objects(user_id=user_id).first()

    @staticmethod
    def create_user(user_id, name, language=None, address=None, is_vendor=False):
        user = User(
            user_id=user_id,
            name=name,
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
    def get_products_by_vendor(vendor: str) -> List[Product]:
        products = Product.objects(vendor=vendor)
        return products

    @staticmethod
    def create_product(name: str, description: str, price: str, vendor: int, category: str = None,) -> Product:
        product = Product(name=name, description=description,
                          price=price, category=category, vendor=vendor)
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

    # Purchase ------------------------

    @staticmethod
    def create_purchase(user_id: int, vendor: int, product_id: str, address: str) -> Purchase:
        purchase = Purchase(
            user_id=user_id,
            vendor=vendor,
            product_id=product_id,
            address=address
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
        purchases = Purchase.objects(vendor=vendor_id)
        return purchases

    @staticmethod
    def get_purchases_by_buyer(buyer_id) -> List[Purchase]:
        purchases = Purchase.objects(buyer=buyer_id)
        return purchases

    @staticmethod
    def update_purchase(purchase: Purchase, **kwargs) -> Purchase:
        for key, value in kwargs.items():
            setattr(purchase, key, value)
        purchase.save()
        return purchase
