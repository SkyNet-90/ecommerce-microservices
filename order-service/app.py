import requests
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
        user_id = data.get("user_id")

        # Interact with Product Service to check product availability
        try:
            product_response = requests.get(f"http://product-service/product/{product_id}")
            product_response.raise_for_status()
            product_data = product_response.json()
        except requests.exceptions.RequestException as e:
            return {"error": "Failed to connect to Product Service"}, 500

        # Create order
        order = {
            "id": str(len(list(container.read_all_items())) + 1),
            "user_id": user_id,
            "product_id": product_id,
            "product_name": product_data["name"],
            "price": product_data["price"],
            "quantity": data.get("quantity", 1)
        }

        container.create_item(body=order)
        return order, 201

    def delete(self, order_id):
        try:
            container.delete_item(item=str(order_id), partition_key=str(order_id))
            return {"message": f"Order with id {order_id} deleted."}, 200
        except exceptions.CosmosResourceNotFoundError:
            return {"error": "Order not found"}, 404

api.add_resource(Order, "/order/<int:order_id>", "/order")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
