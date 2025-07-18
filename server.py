from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Chào mừng Quý khách!"

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.json
        receiver = data.get("to")
        cc = data.get("cc")  # ✅ nhận danh sách Cc từ client
        subject = data.get("subject")
        html_content = data.get("htmlBody")
        from_name = data.get("from_name", "VNPT THU DUC - CSKH")

        # Kiểm tra thông tin bắt buộc
        if not receiver or "@" not in receiver:
            return {"status": "error", "message": "Email người nhận không hợp lệ"}, 400
        if not html_content or "<" not in html_content:
            return {"status": "error", "message": "Nội dung email không hợp lệ"}, 400

        email_password = os.environ.get("EMAIL_PASSWORD")
        if not email_password:
            return {"status": "error", "message": "EMAIL_PASSWORD chưa được thiết lập"}, 500

        # Tạo email
        msg = MIMEText(html_content, "html")
        msg["Subject"] = subject
        msg["From"] = f"{from_name} <diepttb.hcm@vnpt.vn>"
        msg["To"] = receiver

        # Xử lý Cc nếu có
        cc_list = []
        if cc:
            msg["Cc"] = cc
            cc_list = [email.strip() for email in cc.split(",") if "@" in email]

        # Gửi email
        with smtplib.SMTP("email.vnpt.vn", 587) as server:
            server.starttls()
            server.login("diepttb.hcm@vnpt.vn", email_password)
            server.sendmail(
                "diepttb.hcm@vnpt.vn",
                [receiver] + cc_list,
                msg.as_string()
            )

        # Ghi log gửi
        print(f"✅ {datetime.now()} - Đã gửi đến {receiver} | Tiêu đề: {subject}")
        return {
            "status": "success",
            "receiver": receiver,
            "cc": cc_list,
            "subject": subject,
            "from": msg["From"]
        }, 200

    except Exception as e:
        print("❌ Lỗi gửi email:", str(e))
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
