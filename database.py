from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base
from config import DATABASE_URL

# ساخت async engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# ساخت session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """ساخت جداول دیتابیس"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
