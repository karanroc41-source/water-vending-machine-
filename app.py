from flask import Flask, request, jsonify
import razorpay
import os
import qrcode

app = Flask(__name__)

client = razorpay.Client(auth=(
    os.getenv("RAZORPAY_KEY_ID"),
    os.getenv("RAZORPAY_KEY_SECRET")
))

@app.route("/")
def home():
    return "Razorpay QR server is running"

@app.route("/create_payment_link", methods=["POST"])
def create_payment_link():
    data = request.json or {}
    amount = int(data.get("amount", 1)) * 100

    payment_link = client.payment_link.create({
        "amount": amount,
        "currency": "INR",
        "description": "Water Vending Machine Payment",
        "notify": {
            "sms": False,
            "email": False
        }
    })

    payment_url = payment_link["short_url"]

    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=2
    )
    qr.add_data(payment_url)
    qr.make(fit=True)

    matrix = qr.get_matrix()

    return jsonify({
        "payment_link_id": payment_link["id"],
        "payment_url": payment_url,
        "amount": payment_link["amount"],
        "status": payment_link["status"],
        "qr_size": len(matrix),
        "qr_matrix": matrix
    })

@app.route("/check_payment_link", methods=["GET"])
def check_payment_link():
    payment_link_id = request.args.get("payment_link_id")

    if not payment_link_id:
        return jsonify({"status": "error", "message": "payment_link_id missing"})

    payment_link = client.payment_link.fetch(payment_link_id)

    return jsonify({
        "status": payment_link["status"]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
