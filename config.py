import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

# تنظیمات Telegram API
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
SESSION_NAME = "telegram_monitor"

# تنظیمات دیتابیس
DATABASE_URL = os.getenv("DATABASE_URL")

# نمایش تنظیمات (بدون نمایش کلیدهای حساس)
print("✅ Config loaded successfully!")
print(f"📱 Phone: {PHONE_NUMBER}")
print(f"📢 Channel: {CHANNEL_USERNAME}")
