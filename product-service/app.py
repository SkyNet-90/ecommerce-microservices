import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

# Set up Azure Key Vault client
key_vault_name = "ecommercekv1"
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_uri, credential=credential)

# Retrieve Cosmos DB secrets from Key Vault
COSMOS_DB_URL = client.get_secret("CosmosDBUrl").value
COSMOS_DB_KEY = client.get_secret("CosmosDBKey").value
DATABASE_NAME = "ecommerce-db"
CONTAINER_NAME = "products"

# Set up the Cosmos client
cosmos_client = CosmosClient(COSMOS_DB_URL, COSMOS_DB_KEY)
database = cosmos_client.create_database_if_not_exists(DATABASE_NAME)
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import uuid

app = Flask(__name__)
api = Api(app)

# Set up Azure Key Vault client
key_vault_name = "ecommercekv1"
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_uri, credential=credential)

# Retrieve Cosmos DB secrets from Key Vault
COSMOS_DB_URL = client.get_secret("CosmosDBUrl").value
COSMOS_DB_KEY = client.get_secret("CosmosDBKey").value
DATABASE_NAME = "ecommerce-db"
CONTAINER_NAME = "products"

# Set up the Cosmos client
cosmos_client = CosmosClient(COSMOS_DB_URL, COSMOS_DB_KEY)
database = cosmos_client.create_database_if_not_exists(DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME, 
    partition_key=PartitionKey(path="/category")
)

class Product(Resource):
    def get(self, product_id):
        try:
            response = container.read_item(item=str(product_id), partition_key=str(product_id))
            return response, 200
        except exceptions.CosmosResourceNotFoundError:
            return {"error": "Product not found"}, 404

    def post(self):
        data = request.get_json()
        product = {
            "id": str(uuid.uuid4()),  # Generate a unique ID
            "name": data.get("name"),
            "category": data.get("category"),
            "price": data.get("price"),
            "quantity": data.get("quantity"),
        }
        try:
            container.create_item(body=product)
            return product, 201
        except exceptions.CosmosHttpResponseError as e:
            return {"error": str(e)}, 500

api.add_resource(Product, "/product/<string:product_id>", "/product")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME, 
    partition_key=PartitionKey(path="/category")
)

class Product(Resource):
    def get(self, product_id):
        try:
            response = container.read_item(item=str(product_id), partition_key=str(product_id))
            return response, 200
        except exceptions.CosmosResourceNotFoundError:
            return {"error": "Product not found"}, 404

    def post(self):
        data = request.get_json()
        product = {
            "id": str(data.get("id")),
            "name": data.get("name"),
            "category": data.get("category"),
            "price": data.get("price"),
            "quantity": data.get("quantity"),
        }
        container.create_item(body=product)
        return product, 201

    def delete(self, product_id):
        try:
            container.delete_item(item=str(product_id), partition_key=str(product_id))
            return {"message": f"Product with id {product_id} deleted."}, 200
        except exceptions.CosmosResourceNotFoundError:
            return {"error": "Product not found"}, 404

api.add_resource(Product, "/product/<int:product_id>", "/product")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
