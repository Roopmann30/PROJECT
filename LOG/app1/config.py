import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "my_secret_key")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/forumdb")
