const form = document.getElementById("qr-form");
const input = document.getElementById("url-input");
const result = document.getElementById("qr-result");

// NEW
const passwordToggle = document.getElementById("password-toggle");
const passwordInput = document.getElementById("password-input");

// NEW: toggle visibility
passwordToggle.addEventListener("change", () => {
    passwordInput.style.display = passwordToggle.checked ? "block" : "none";
});

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    result.innerHTML = "";

    const url = input.value.trim();
    if (!url) return;

    // NEW
    const password = passwordToggle.checked
        ? passwordInput.value.trim()
        : null;

    try {
        const response = await fetch("/generate-qr", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url, password })
        });

        const data = await response.json();

        if (!response.ok) {
            result.innerHTML = `<p style="color:red;">${data.error}</p>`;
            return;
        }

        const imgSrc = `data:image/png;base64,${data.qr_base64}`;

        result.innerHTML = `
            <img src="${imgSrc}" alt="Generated QR Code">
            <br>
            <a href="${imgSrc}" download="my-qr.png" class="download-btn">
                Download QR
            </a>
        `;
    } catch (err) {
        result.innerHTML = "<p style='color:red;'>Server error</p>";
    }
});
