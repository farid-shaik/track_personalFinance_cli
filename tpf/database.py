import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI="mongodb+srv://vangalapudisandeep22:hello@hello.tfupf.mongodb.net/?retryWrites=true&w=majority&appName=hello"

# MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vangalapudi"]
users_collection = db["vangalapudi"]
# print(users_collection)