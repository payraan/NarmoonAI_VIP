from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TelegramPost(Base):
    __tablename__ = 'telegram_posts'
    
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, unique=True, nullable=False)
    channel_username = Column(String(100), nullable=False)
    content = Column(Text)
    date = Column(DateTime, nullable=False)
    views = Column(Integer, default=0)
    forwards = Column(Integer, default=0)
    has_media = Column(Boolean, default=False)
    media_type = Column(String(50))
    media_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'message_id': self.message_id,
            'content': self.content,
            'date': self.date.isoformat(),
            'views': self.views,
            'forwards': self.forwards,
            'has_media': self.has_media,
            'media_type': self.media_type,
            'media_path': self.media_path
        }
