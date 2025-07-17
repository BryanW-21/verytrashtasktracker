from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from models import create_user, get_user_by_email, get_user_by_username

bcrypt = Bcrypt()

def register_user(data):
    """Handles user registration, ensuring unique usernames and emails."""
    if not all(k in data for k in ("username", "email", "password")):
        return {"error": "Missing required fields"}, 400

    # Check for existing username
    if get_user_by_username(data["username"]):
        return {"error": "Username already taken. Please choose another one."}, 400

    # Check for existing email
    if get_user_by_email(data["email"]):
        return {"error": "Email already registered. Try logging in instead."}, 400

    # Hash the password and create the user
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    create_user(data["username"], data["email"], hashed_password)

    return {"message": "User registered successfully"}, 201
def login_user(data):
    user = get_user_by_email(data["email"])
    if not user or not bcrypt.check_password_hash(user.password_hash, data["password"]):
        return {"error": "Invalid email or password"}, 401

    access_token = create_access_token(identity=user.userId)
    return {"message": "Login successful", "access_token": access_token}, 200
