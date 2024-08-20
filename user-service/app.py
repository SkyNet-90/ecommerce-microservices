from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import jwt
import datetime
import os
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

# Set up Azure Key Vault client
key_vault_name = os.getenv("KEY_VAULT_NAME", "ecommercekv1")
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_uri, credential=credential)

# Retrieve Cosmos DB secrets from Key Vault
COSMOS_DB_URL = client.get_secret("CosmosDBUrl").value
COSMOS_DB_KEY = client.get_secret("CosmosDBKey").value
DATABASE_NAME = "ecommerce-db"
CONTAINER_NAME = "users"

# Set up the Cosmos client
cosmos_client = CosmosClient(COSMOS_DB_URL, COSMOS_DB_KEY)
database = cosmos_client.create_database_if_not_exists(DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME, 
    partition_key=PartitionKey(path="/username")
)

# Secret key for JWT
SECRET_KEY = client.get_secret("JWT").value

class User(Resource):
    def get(self, username):
        try:
            response = container.read_item(item=username, partition_key=username)
            return jsonify(response), 200
        except exceptions.CosmosResourceNotFoundError:
            return jsonify({"error": "User not found"}), 404

    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        hashed_password = generate_password_hash(password, method='sha256')
        user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "password": hashed_password
        }

        try:
            container.create_item(body=user)
            return jsonify({"message": "User created successfully"}), 201
        except exceptions.CosmosHttpResponseError as e:
            return jsonify({"error": str(e)}), 500

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        try:
            user = container.read_item(item=username, partition_key=username)
            if check_password_hash(user["password"], password):
                token = jwt.encode({
                    "username": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                }, SECRET_KEY, algorithm="HS256")
                return jsonify({"token": token}), 200
            else:
                return jsonify({"error": "Invalid credentials"}), 401
        except exceptions.CosmosResourceNotFoundError:
            return jsonify({"error": "User not found"}), 404

api.add_resource(User, "/user/<string:username>")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)