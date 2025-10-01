# --- Stub for /broadcast ---
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Body, Request
from pydantic import BaseModel
import random
from ..models import User
from ..Schemas import user
from ..database import database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import hashing
from ..oauth2 import get_current_user
import secrets
import requests
import mimetypes

# Single router declaration at the top
router = APIRouter(tags=['User'])


# --- Stub for /broadcast ---
@router.get("/broadcast")
async def get_broadcasts(limit: int = 10, offset: int = 0, statusfilter: str = None):
    return {"broadcasts": [], "total": 0}

# --- Stub for /template ---
@router.get("/template")
async def get_templates():
    # Return a structure matching frontend expectations
    return {"data": []}




# Message Generator Endpoint (robust, handles missing prompt)
@router.post("/generate-message", tags=["Message Generator"])
async def generate_message(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        name = data.get("name", "Friend")
        if not prompt:
            return {"generated_message": "Please enter a prompt to generate a message."}
        templates = {
            "diwali": [
                "Hello {name}, Diwali greetings! We wish you a joyful holiday. Namaste!",
                "Dear {name}, may this Diwali bring light, love, and happiness!"
            ],
            "new year": [
                "Happy New Year {name}! Wishing you success and happiness ahead.",
                "Cheers to 2025, {name}! May this year be full of new opportunities."
            ],
            "default": [
                "Hello {name}, sending you our best wishes!",
                "Hi {name}, we appreciate you and wish you well!"
            ]
        }
        prompt_lower = prompt.lower()
        if "diwali" in prompt_lower:
            message = random.choice(templates["diwali"])
        elif "new year" in prompt_lower:
            message = random.choice(templates["new year"])
        else:
            message = random.choice(templates["default"])
        message = message.replace("{name}", name)
        return {"generated_message": message}
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))





# ---------------- Update WhatsApp Business Profile ----------------
@router.post("/update-profile", status_code=200)
def update_profile(
    request: user.BusinessProfile,
    get_current_user: user.newuser = Depends(get_current_user)
):
    """
    Updates the WhatsApp Business Profile using the provided JSON payload.
    """
    # Commented out WhatsApp API integration for now
    # WHATSAPP_API_URL = f"https://graph.facebook.com/v20.0/{get_current_user.Phone_id}/whatsapp_business_profile"
    # headers = {
    #     "Authorization": f"Bearer {get_current_user.PAccessToken}",
    #     "Content-Type": "application/json",
    # }
    # response = requests.post(WHATSAPP_API_URL, json=request.dict(), headers=headers)
    # if response.status_code != 200:
    #     raise HTTPException(status_code=response.status_code, detail=response.json())
    # return {"message": "Business profile updated successfully", "data": response.json()}

    # For now, just return the payload
    return {"message": "Business profile endpoint is disabled (no API key)", "data": request.dict()}


# ---------------- Resumable Upload ----------------
@router.post("/resumable-upload/")
async def resumable_upload(file: UploadFile, get_current_user: user.newuser = Depends(get_current_user)):
    # Commented out WhatsApp upload for now
    # BASE_URL = "https://graph.facebook.com/v20.0"
    # ACCESS_TOKEN = get_current_user.PAccessToken
    # ...
    return {"message": "Resumable upload endpoint is disabled (no API key)"}


# ---------------- Get WhatsApp Business Profile ----------------
@router.get("/get-business-profile/")
def get_business_profile(get_current_user: user.newuser = Depends(get_current_user)):
    # Commented out WhatsApp API integration for now
    # BASE_URL = "https://graph.facebook.com/v17.0"
    # ACCESS_TOKEN = get_current_user.PAccessToken
    # PHONE_NUMBER_ID = get_current_user.Phone_id
    # url = f"{BASE_URL}/{PHONE_NUMBER_ID}/whatsapp_business_profile?fields=about,address,description,email,profile_picture_url,websites,vertical"
    # headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    # response = requests.get(url, headers=headers)
    # if response.status_code != 200:
    #     raise HTTPException(status_code=response.status_code, detail=response.json())
    # return response.json()
    return {"message": "Get business profile endpoint is disabled (no API key)"}


# ---------------- Subscribe Customer ----------------
# Commented out because requires Facebook client_id and secret
# @router.post("/subscribe_customer")
# async def process_responses(
#     payload: dict,
#     db: AsyncSession = Depends(database.get_db),
#     get_current_user: user.newuser = Depends(get_current_user),
# ):
#     return {"message": "Subscribe customer endpoint disabled (requires Facebook credentials)"}
