import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

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
DATABASE_NAME = "ecommercedb"
CONTAINER_NAME = "Orders"

# Set up the Cosmos client
cosmos_client = CosmosClient(COSMOS_DB_URL, COSMOS_DB_KEY)
database = cosmos_client.create_database_if_not_exists(DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME, 
    partition_key=PartitionKey(path="/user_id")
)

class Order(Resource):
    def get(self, order_id):
        try:
            response = container.read_item(item=str(order_id), partition_key=str(order_id))
            return response
        except exceptions.CosmosResourceNotFoundError:
            return {"error": "Order not found"}, 404

    def post(self):
        data = request.get_json()
        product_id = data.get("product_id")

        # Interact with Product Service to check product availability
        try:
            product_response = requests.get(f"http://product-service/product/{product_id}")
            product_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": "Failed to connect to Product Service"}, 500

        order = {
            "id": str(len(orders) + 1),  # Ensure ID is a string for Cosmos DB
            "user_id": str(data.get("user_id")),
            "product_id": product_id,
            "quantity": data.get("quantity"),
            "status": "pending"
        }
        container.create_item(order)
        return order, 201

api.add_resource(Order, "/order/<int:order_id>", "/order")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
