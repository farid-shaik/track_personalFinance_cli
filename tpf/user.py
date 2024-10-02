import bcrypt
from database import users_collection

def create_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {"username": username, "password": hashed_password}
    users_collection.insert_one(user)
    return "User created successfully!"

def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return "Authentication successful!"
    else:
        return "Invalid username or password."
