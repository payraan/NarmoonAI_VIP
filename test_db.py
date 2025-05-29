import asyncio
from database import init_db
from config import *

async def test_database():
    """تست اتصال و ساخت دیتابیس"""
    try:
        await init_db()
        print("✅ Database created successfully!")
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    asyncio.run(test_database())
