from flask import Flask, render_template, request, jsonify
import qrcode
import base64
from io import BytesIO
from urllib.parse import urlparse

app = Flask(__name__)


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

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    return jsonify({
        "qr_base64": img_base64
    })


if __name__ == "__main__":
    app.run(debug=True)
