# 🔐 Password-Protected QR Code Generator

A simple web-based QR Code Generator that allows users to create QR codes for any URL, with an optional password protection layer.  
When password protection is enabled, the QR code points to a secure unlock page that asks for a password before redirecting to the original URL.

---

## ✨ Features

- Generate QR codes for any valid URL
- Optional password protection for QR links
- Clean and minimal UI
- Download QR code as an image
- Lightweight and fast
- No database required (token-based flow)

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Node.js (Express)
- **QR Generation:** `qrcode` npm package
- **Security:** Token-based password verification

---

## 📂 Project Structure

qr-password-generator/
│
├── public/
│ ├── index.html
│ ├── style.css
│ └── script.js
│
├── server.js
├── package.json
├── README.md
└── .gitignore

yaml
Copy code

---

## 🚀 How It Works

1. User enters a URL
2. (Optional) User enables password protection and sets a password
3. Server generates:
   - A secure token containing the URL and password hash
   - A QR code pointing to an unlock route
4. On scan:
   - User is asked to enter the password
   - On success, user is redirected to the original URL

---

## ▶️ Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/qr-password-generator.git
cd qr-password-generator
2️⃣ Install dependencies
bash
Copy code
npm install
3️⃣ Start the server
bash
Copy code
node server.js
4️⃣ Open in browser
arduino
Copy code
http://localhost:3000
🔒 Security Notes
Passwords are never stored in plain text

Tokens can be configured to expire

No database dependency

🧪 Future Enhancements
Token expiration timer

Scan analytics

Custom QR styling

Rate limiting

Mobile-friendly unlock page

📜 License
This project is open-source and free to use for educational and hackathon purposes.