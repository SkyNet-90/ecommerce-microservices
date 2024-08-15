import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
api = Api(app)

# Retrieve the Product Service URL from environment variable
product_service_url = os.getenv("PRODUCT_SERVICE_URL", "http://product-service")

orders = []

class Order(Resource):
    def get(self, order_id):
        for order in orders:
            if order["id"] == order_id:
                return order, 200
        return "Order not found", 404

    def post(self):
        data = request.get_json()

        # Example interaction with Product Service to check product availability
        product_id = data.get("product_id")
        try:
            product_response = requests.get(f"{product_service_url}/product/{product_id}")
            product_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": "Failed to connect to Product Service"}, 500

        order = {
            "id": len(orders) + 1,
            "user_id": data.get("user_id"),
            "product_id": product_id,
            "quantity": data.get("quantity"),
            "status": "pending"
        }
        orders.append(order)
        return order, 201

    def delete(self, order_id):
        global orders
        orders = [order for order in orders if order["id"] != order_id]
        return f"Order with id {order_id} deleted.", 200

api.add_resource(Order, "/order/<int:order_id>", "/order")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
