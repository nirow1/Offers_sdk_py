from flask import Flask, request, jsonify
from uuid import UUID

app = Flask(__name__)
products = {}  # simple in-memory store
offers = {}    # simple in-memory offers store

@app.route("/api/v1/auth", methods=["POST"])
def auth():
    data = request.get_json() or {}
    return jsonify({"access_token": "fake-token"})

@app.route("/api/v1/products/register", methods=["POST"])
def register_product():
    data = request.get_json()
    product_id = str(data["id"])
    products[product_id] = data
    # create dummy offers for this product
    offers[product_id] = {
        "id": product_id,
        "price": 99,
        "items_in_stock": 10
    }
    return jsonify({"status": "ok", "product": data})


@app.route("/api/v1/products/<product_id>/offers", methods=["GET"])
def get_product_offers(product_id):
    if product_id not in offers:
        return jsonify({"error": "No offers found"}), 404
    return jsonify(offers[product_id])

if __name__ == "__main__":
    app.run(port=8000)