from flask import Flask, request, jsonify
import razorpay
import os

app = Flask(__name__)

client = razorpay.Client(auth=(
    os.getenv("RAZORPAY_KEY_ID"),
    os.getenv("RAZORPAY_KEY_SECRET")
))

@app.route("/")
def home():
    return "Razorpay server is running"

@app.route("/create_payment_link", methods=["POST"])
def create_payment_link():
    data = request.json
    amount = int(data.get("amount", 1)) * 100

    payment_link = client.payment_link.create({
        "amount": amount,
        "currency": "INR",
        "description": "Water Vending Machine Payment",
        "customer": {
            "name": "Customer"
        },
        "notify": {
            "sms": False,
            "email": False
        }
    })

    return jsonify({
        "payment_link_id": payment_link["id"],
        "payment_url": payment_link["short_url"],
        "amount": payment_link["amount"],
        "status": payment_link["status"]
    })

@app.route("/check_payment_link", methods=["GET"])
def check_payment_link():
    payment_link_id = request.args.get("payment_link_id")

    payment_link = client.payment_link.fetch(payment_link_id)

    return jsonify({
        "status": payment_link["status"]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
