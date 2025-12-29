from flask import Flask, request, jsonify
import razorpay
import os

app = Flask(__name__)

# Razorpay credentials from ENV
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
)

payments = {}

@app.route("/")
def home():
    return "Razorpay server is running"

@app.route("/create_payment", methods=["POST"])
def create_payment():
    data = request.json
    amount = int(data["amount"]) * 100

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    payments[order["id"]] = "created"

    return jsonify({
        "order_id": order["id"],
        "amount": amount
    })

@app.route("/check_payment", methods=["GET"])
def check_payment():
    order_id = request.args.get("order_id")

    try:
        payments_data = client.order.fetch_payments(order_id)
        for p in payments_data["items"]:
            if p["status"] == "captured":
                return jsonify({"status": "success"})
        return jsonify({"status": "pending"})
    except:
        return jsonify({"status": "error"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
