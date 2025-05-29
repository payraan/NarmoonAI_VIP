from telethon import TelegramClient, events
from datetime import datetime, timedelta
import asyncio
from sqlalchemy import select
from database import AsyncSessionLocal
from models import TelegramPost
from config import API_ID, API_HASH, PHONE_NUMBER, SESSION_NAME, CHANNEL_USERNAME
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChannelMonitor:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        
    async def start(self):
        await self.client.start(phone=PHONE_NUMBER)
        logger.info("Client started successfully")
        
        # اولین بار: دریافت پست‌های 24 ساعت گذشته
        await self.fetch_recent_posts(hours=24)
        
        # شروع monitoring real-time
        await self.setup_handlers()
        
    async def fetch_recent_posts(self, hours=24):
        """دریافت پست‌های چند ساعت اخیر"""
        try:
            channel = await self.client.get_entity(CHANNEL_USERNAME)
            after_date = datetime.now() - timedelta(hours=hours)
            
            messages = []
            async for message in self.client.iter_messages(
                channel,
                offset_date=datetime.now(),
                reverse=False
            ):
                if message.date.replace(tzinfo=None) < after_date:
                    break
                messages.append(message)
            
            logger.info(f"Found {len(messages)} messages from last {hours} hours")
            
            # ذخیره در دیتابیس
            async with AsyncSessionLocal() as db:
                for msg in messages:
                    await self.save_message(db, msg, CHANNEL_USERNAME)
                await db.commit()
                
        except Exception as e:
            logger.error(f"Error fetching recent posts: {e}")
            
    async def save_message(self, db, message, channel_username):
        """ذخیره پیام در دیتابیس با ذخیره تصویر"""
        try:
            media_path = None
            # اگر پیام مدیا دارد (عکس/ویدیو)
            if message.media:
                media_folder = 'media'
                os.makedirs(media_folder, exist_ok=True)
                filename = f"{message.id}.jpg"
                media_path = os.path.join(media_folder, filename)
                # دانلود فقط اگر قبلاً دانلود نشده
                if not os.path.exists(media_path):
                    await self.client.download_media(message, media_path)
            
            stmt = select(TelegramPost).where(
                TelegramPost.message_id == message.id,
                TelegramPost.channel_username == channel_username
            )
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                existing.views = getattr(message, 'views', 0) or 0
                existing.forwards = getattr(message, 'forwards', 0) or 0
                if media_path:
                    existing.media_path = media_path
            else:
                post = TelegramPost(
                    message_id=message.id,
                    channel_username=channel_username,
                    content=message.text or message.message,
                    date=message.date.replace(tzinfo=None),
                    views=getattr(message, 'views', 0) or 0,
                    forwards=getattr(message, 'forwards', 0) or 0,
                    has_media=bool(message.media),
                    media_type=type(message.media).__name__ if message.media else None,
                    media_path=media_path
                )
                db.add(post)
                
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            
    async def setup_handlers(self):
        """تنظیم handler برای پیام‌های جدید"""
        @self.client.on(events.NewMessage(chats=CHANNEL_USERNAME))
        async def new_message_handler(event):
            logger.info(f"New message: {event.message.id}")
            async with AsyncSessionLocal() as db:
                await self.save_message(db, event.message, CHANNEL_USERNAME)
                await db.commit()
                
        logger.info(f"Monitoring channel: {CHANNEL_USERNAME}")
        
    async def run_forever(self):
        """اجرای دائمی monitor"""
        await self.start()
        logger.info("Bot is running... Press Ctrl+C to stop")
        await self.client.run_until_disconnected()
