from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

products = []

class Product(Resource):
    def get(self, product_id):
        for product in products:
            if product["id"] == product_id:
                return product, 200
        return "Product not found", 404

    def post(self):
        data = request.get_json()
        product = {
            "id": len(products) + 1,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": data.get("quantity"),
        }
        products.append(product)
        return product, 201

    def delete(self, product_id):
        global products
        products = [product for product in products if product["id"] != product_id]
        return f"Product with id {product_id} deleted.", 200

api.add_resource(Product, "/product/<int:product_id>", "/product")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
