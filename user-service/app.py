import os
import uuid
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from werkzeug.security import generate_password_hash
import logging

app = Flask(__name__)
api = Api(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

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
        except Exception as e:
            logging.error(f"Error retrieving user: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

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
            logging.error(f"Error creating user: {e}")
            return jsonify({"error": "Internal Server Error"}), 500
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

api.add_resource(User, '/user', '/user/<string:username>')

if __name__ == '__main__':
    app.run(debug=True)