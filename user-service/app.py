from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

users = []

class User(Resource):
    def get(self, username):
        for user in users:
            if user["username"] == username:
                return user, 200
        return "User not found", 404

    def post(self):
        data = request.get_json()
        username = data.get("username")
        if any(user["username"] == username for user in users):
            return "User already exists", 400
        user = {
            "username": username,
            "password": data.get("password"),
            "email": data.get("email"),
        }
        users.append(user)
        return user, 201

api.add_resource(User, "/user/<string:username>", "/user")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
