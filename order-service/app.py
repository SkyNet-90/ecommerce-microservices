from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
api = Api(app)

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
        product_response = requests.get(f"http://product-service/product/{product_id}")
        
        if product_response.status_code != 200:
            return "Product not available", 404

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
