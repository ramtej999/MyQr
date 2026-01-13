from flask import Flask, render_template, request, jsonify, redirect
import qrcode
import base64
from io import BytesIO
from urllib.parse import urlparse
import uuid
import time
import hashlib

app = Flask(__name__)

# In-memory store (auto-clears on restart)
QR_STORE = {}
EXPIRY_SECONDS = 10 * 60  # 10 minutes


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate-qr", methods=["POST"])
def generate_qr():
    data = request.get_json()
    url = data.get("url", "").strip()
    password = data.get("password")

    if not url or not is_valid_url(url):
        return jsonify({"error": "Invalid URL"}), 400

    token = uuid.uuid4().hex

    QR_STORE[token] = {
        "url": url,
        "password": hash_password(password) if password else None,
        "created": time.time()
    }

    protected_url = request.host_url + f"q/{token}"

    qr = qrcode.make(protected_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return jsonify({"qr_base64": img_base64})


@app.route("/q/<token>", methods=["GET", "POST"])
def unlock_qr(token):
    entry = QR_STORE.get(token)

    if not entry or time.time() - entry["created"] > EXPIRY_SECONDS:
        return "<h2>QR expired or invalid</h2>"

    if entry["password"] is None:
        return redirect(entry["url"])

    if request.method == "POST":
        user_pass = request.form.get("password", "")
        if hash_password(user_pass) == entry["password"]:
            return redirect(entry["url"])
        return render_template("unlock.html", error="Wrong password")

    return render_template("unlock.html")


if __name__ == "__main__":
    app.run(debug=True)
