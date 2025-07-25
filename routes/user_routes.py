from flask import Blueprint, request, jsonify
from typing import Tuple, Any
from db import get_connection
from utils.security import hash_password, verify_password

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/')
def index() -> str:
    return "User Management API is running."

@user_routes.route('/users', methods=['GET'])
def get_all_users() -> Any:
    _, cursor = get_connection()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    return jsonify([dict(zip(["id", "name", "email"], user)) for user in users])

@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int) -> Any:
    _, cursor = get_connection()
    cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify(dict(zip(["id", "name", "email"], user)))
    return jsonify({"error": "User not found"}), 404

@user_routes.route('/users', methods=['POST'])
def create_user() -> Tuple[str, int]:
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = hash_password(data['password'])

    conn, cursor = get_connection()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    return "User created", 201

@user_routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id: int) -> Tuple[str, int]:
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    conn, cursor = get_connection()
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    conn.commit()
    return "User updated", 200

@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int) -> Tuple[str, int]:
    conn, cursor = get_connection()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return "User deleted", 200

@user_routes.route('/login', methods=['POST'])
def login() -> Any:
    data = request.get_json()
    email = data['email']
    password = data['password']

    _, cursor = get_connection()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()

    if row and verify_password(row[0], password):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid email or password"}), 401
