import pyotp
import time
import qrcode

# ============ 1: 產生一次性6碼 OTP ,附加 auth URI  ============
secret = "vshcmb6x5zttkhmp" # 這個是User Key，可自己亂碼產生，也可透過微軟取得User Key

totp = pyotp.TOTP(secret)  # 用 User Key 建立Create TOTP Object

current_otp = totp.now()   # 產生 TOTP Code, 用Linux 時間混合 Key 產生 Code，可手動輸入
print(f"Current TOTP: {current_otp}")

                           # 產生 URI 以便User點連結設定 或 變成QR Code掃碼設定
uri = totp.provisioning_uri(name="deanliu@compeq.com.tw", issuer_name="COMPEQ TW")
print(f"Provisioning URI: {uri}")

# ============ 2: 由 auth URI 產生 QR Code，可簡化輸入 但非必要 ============
qr = qrcode.QRCode(version=3, box_size=5, border=2, error_correction=qrcode.constants.ERROR_CORRECT_L)
qr.add_data(uri)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("QR.png")

# ============ 3: Server 端 認證User 輸入的 6碼 OTP code ============
user_input_totp = input("輸入 6碼 TOTP 驗證: ")
# Verify the provided OTP
if totp.verify(user_input_totp):
    print("TOTP is OK valid.")
else:
    print("Invalid TOTP.")
