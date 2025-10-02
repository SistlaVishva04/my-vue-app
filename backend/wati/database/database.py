import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# For SQLite, we can keep it local or use an env variable
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./local.db")

# SQLite engine does NOT need pool_size, pool_recycle, pool_pre_ping
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)

# Create a session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for declarative models
Base = declarative_base()

# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
