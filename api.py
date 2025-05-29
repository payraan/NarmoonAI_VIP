from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
from sqlalchemy import select
from database import AsyncSessionLocal
from models import TelegramPost
from config import CHANNEL_USERNAME
import os

app = FastAPI()

@app.get("/posts/recent/{hours}")
async def get_recent_posts(hours: int = 6):
    if hours > 48:
        raise HTTPException(status_code=400, detail="Maximum 48 hours allowed")
    after_date = datetime.now() - timedelta(hours=hours)
    async with AsyncSessionLocal() as db:
        stmt = select(TelegramPost).where(
            TelegramPost.date >= after_date
        ).order_by(TelegramPost.date.desc())
        result = await db.execute(stmt)
        posts = result.scalars().all()
        return {
            "count": len(posts),
            "hours": hours,
            "posts": [post.to_dict() for post in posts]
        }

@app.get("/posts/latest/{count}")
async def get_latest_posts(count: int = 10):
    if count > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 posts allowed")
    async with AsyncSessionLocal() as db:
        stmt = select(TelegramPost).order_by(TelegramPost.date.desc()).limit(count)
        result = await db.execute(stmt)
        posts = result.scalars().all()
        return {
            "count": len(posts),
            "posts": [post.to_dict() for post in posts]
        }

@app.get("/{filename}")
async def get_media_file(filename: str):
    file_path = os.path.join("media", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")
