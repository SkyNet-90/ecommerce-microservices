from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)
api = Api(app)

users = []

class User(Resource):
    def get(self, username):
        for user in users:
            if user["username"] == username:
                return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404

    def post(self):
        data = request.get_json()
        username = data.get("username")
        if any(user["username"] == username for user in users):
            return jsonify({"error": "User already exists"}), 400
        user = {
            "id": str(uuid.uuid4()),  # Generate a unique ID
            "username": username,
            "password": generate_password_hash(data.get("password")),  # Hash the password
            "email": data.get("email"),
        }
        users.append(user)
        return jsonify(user), 201

api.add_resource(User, "/user/<string:username>", "/user")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
