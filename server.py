from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Chào mừng Quý khách!"

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.json
        receiver = data.get("to")
        subject = data.get("subject")
        html_content = data.get("htmlBody")

        if not receiver or "@" not in receiver:
            return {"status": "error", "message": "Email người nhận không hợp lệ"}, 400

        email_password = os.environ.get("EMAIL_PASSWORD")
        if not email_password:
            return {"status": "error", "message": "EMAIL_PASSWORD chưa được thiết lập"}, 500

        msg = MIMEText(html_content, "html")
        msg["Subject"] = subject
        msg["From"] = "VNPT THU DUC-CSKH"
        msg["To"] = receiver

        with smtplib.SMTP("email.vnpt.vn", 587) as server:
            server.starttls()
            server.login("thgiang.hcm@vnpt.vn", email_password)
            server.sendmail("thgiang.hcm@vnpt.vn", receiver, msg.as_string())

        print(f"✅ Đã gửi email đến {receiver} với tiêu đề: {subject}")
        return {"status": "success"}, 200

    except Exception as e:
        print("❌ Lỗi gửi email:", str(e))
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
