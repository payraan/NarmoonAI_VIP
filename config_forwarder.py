import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

# تنظیمات Telegram API (همان اطلاعات قبلی)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# کانال‌های مبدا
SOURCE_CHANNELS = [
    "klondikeai",  # بدون @
]

# کانال مقصد
TARGET_CHANNEL = "NarmoonAI_VIP"  # بدون @

# متن فارسی اضافی
PERSIAN_TEMPLATE = """

🔥 تحلیل فوری هوش مصنوعی

💡 این سیگنال از منابع معتبر جمع‌آوری و برای شما ارسال شده است.

📈 برای دریافت سایر تحلیل‌ها در کانال ما همراه باشید.

🤖 @NarmoonAI_VIP"""

# کلمات برای حذف (برندینگ کانال اصلی) 
WORDS_TO_REMOVE = [
    "@KlondikeAI",
    "KlondikeAI",
    "klondike", 
    "Klondike",
]
