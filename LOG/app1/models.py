from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.email = user_data["email"]
        self.password_hash = user_data["password"]

    @staticmethod
    def create_user(username, email, password):
        return {
            "username": username,
            "email": email,
            "password": generate_password_hash(password),
        }

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
