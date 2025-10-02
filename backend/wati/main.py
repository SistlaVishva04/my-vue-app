from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from .database import database
from .routes import user, broadcast, contacts, auth, woocommerce, integration, wallet, analytics
from .services import dramatiq_router
from . import oauth2
from wati.models.ChatBox import Last_Conversation
from .models import ChatBox
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

# ---------------- Gemini import ----------------
import os
import google.generativeai as genai
from pydantic import BaseModel

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ------------------------------------------------

app = FastAPI()
scheduler = AsyncIOScheduler()
scheduler_started = False


# ---------------- Database setup ----------------
async def create_db_and_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_db_and_tables()

    global scheduler_started
    if not scheduler_started:
        scheduler.add_job(close_expired_chats, 'interval', minutes=1)
        scheduler.start()
        scheduler_started = True
        print("Scheduler started.")


@app.on_event("shutdown")
async def shutdown_event():
    global scheduler_started
    if scheduler_started:
        scheduler.shutdown(wait=False)
        scheduler_started = False
        print("Scheduler shut down.")


# ---------------- Routers ----------------
app.include_router(broadcast.router)
app.include_router(contacts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(oauth2.router)
app.include_router(dramatiq_router.router)
app.include_router(woocommerce.router)
app.include_router(integration.router)
app.include_router(analytics.router)


# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- Scheduler task ----------------
async def close_expired_chats() -> None:
    try:
        async for session in database.get_db():
            now = datetime.now()
            result = await session.execute(
                select(ChatBox.Last_Conversation).where(
                    ChatBox.Last_Conversation.active == True,
                    now - ChatBox.Last_Conversation.last_chat_time > timedelta(minutes=1440)
                )
            )
            expired_conversations = result.scalars().all()

            for conversation in expired_conversations:
                conversation.active = False

            await session.commit()
            print(f"Successfully closed {len(expired_conversations)} expired chats.")
            break
    except Exception as e:
        print(f"Error in close_expired_chats: {e}")


