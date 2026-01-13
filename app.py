from flask import Flask, render_template, request, jsonify, send_from_directory
import qrcode
import os
import uuid
from urllib.parse import urlparse

app = Flask(__name__)

# Configuration
QR_FOLDER = "static/qr"
os.makedirs(QR_FOLDER, exist_ok=True)


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate-qr", methods=["POST"])
def generate_qr():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url or not is_valid_url(url):
        return jsonify({"error": "Invalid URL"}), 400

    filename = f"{uuid.uuid4().hex}.png"
    file_path = os.path.join(QR_FOLDER, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

    return jsonify({
        "qr_url": f"/static/qr/{filename}"
    })


if __name__ == "__main__":
    app.run(debug=True)
