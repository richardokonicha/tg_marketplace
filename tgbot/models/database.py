import mongoengine
import certifi
from tgbot.models.model import User
from tgbot import config

# Connect to MongoDB
mongoengine.connect(db=config.DB_NAME, host=config.DATABASE_URL, tlsCAFile=certifi.where())

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
