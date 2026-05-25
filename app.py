from flask import Flask, request, jsonify, render_template_string
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

# ✅ Order create API
@app.route("/create_order", methods=["POST"])
def create_order():
    data = request.json
    amount = int(data.get("amount", 1)) * 100

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return jsonify({
        "order_id": order["id"],
        "amount": order["amount"]
    })

# ✅ NEW: Payment Page (IMPORTANT 🔥)
@app.route("/pay")
def pay():
    order_id = request.args.get("order_id")

    html = f"""
    <html>
    <head>
        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    </head>
    <body>
        <h2>Processing Payment...</h2>
        <script>
            var options = {{
                "key": "{os.getenv("RAZORPAY_KEY_ID")}",
                "amount": "100",
                "currency": "INR",
                "name": "Water Vending Machine",
                "description": "Test Payment",
                "order_id": "{order_id}",
                "handler": function (response){{
                    alert("Payment Successful!");
                }},
                "theme": {{
                    "color": "#3399cc"
                }}
            }};
            var rzp = new Razorpay(options);
            rzp.open();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

# ✅ Payment check
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

# ✅ Render run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
