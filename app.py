from flask import Flask, request, jsonify
import razorpay
import os

app = Flask(__name__)

# ✅ Keys sirf Environment se aayengi (code me nahi likhni)
client = razorpay.Client(auth=(
    os.getenv("RAZORPAY_KEY_ID"),
    os.getenv("RAZORPAY_KEY_SECRET")
))

@app.route("/")
def home():
    return "Razorpay server is running"

# ✅ API 1: Order Create
@app.route("/create_order", methods=["POST"])
def create_order():
    data = request.json
    amount = int(data.get("amount", 1)) * 100  # Rs → paise

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return jsonify({
        "order_id": order["id"],
        "amount": order["amount"]
    })

# ✅ API 2: Payment Status Check
@app.route("/check_payment", methods=["GET"])
def check_payment():
    order_id = request.args.get("order_id")

    payments = client.order.payments(order_id)

    if payments["count"] > 0:
        payment = payments["items"][0]
        return jsonify({
            "status": payment["status"]
        })

    return jsonify({"status": "pending"})

# ✅ Render ke liye port setup
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
