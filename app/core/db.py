from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=True,  
    poolclass=QueuePool,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    session = SessionLocal()
    try:
        yield session
        await session.commit()  
    except Exception:  
        await session.rollback()
        raise
    finally:
        await session.close()

@event.listens_for(Engine, "connect")
def receive_connect(dbapi_connection, connection_record):
    connection_record.info['start_time'] = time.time()

@event.listens_for(Engine, "close")
def receive_close(dbapi_connection, connection_record):
    total_time = time.time() - connection_record.info['start_time']
    if total_time > 0.5: 
        logger.warning(f"Database connection held for {total_time:.3f} seconds")