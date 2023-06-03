from tgbot.models import db


newuser = db.create_user("777", "Pascal")


old_user = db.get_user("777")

print(old_user)