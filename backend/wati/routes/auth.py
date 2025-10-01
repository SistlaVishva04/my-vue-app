# routes/auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import User
from ..database import database
from ..hashing import Hash
from ..Schemas.user import register_user, LoginUser
from .. import JWTtoken
import secrets

router = APIRouter(tags=["Auth"])

# ---------------- LOGIN ----------------
@router.post("/login")
async def login(user: LoginUser, db: AsyncSession = Depends(database.get_db)):
    """
    Login endpoint accepting JSON:
    {
        "username": "user@example.com",
        "password": "12345"
    }
    """
    result = await db.execute(select(User.User).filter(User.User.email == user.username))
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not Hash.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = JWTtoken.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ---------------- REGISTER ----------------
@router.post('/register')
async def register_user(request_body: register_user, db: AsyncSession = Depends(database.get_db)):
    """
    Register endpoint accepting JSON:
    {
        "username": "test",
        "email": "test@gmail.com",
        "password": "12345"
    }
    """
    # Check for existing user
    result = await db.execute(select(User.User).filter(User.User.email == request_body.email))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Account with this email already exists")
    
    # Create a new user
    api_key = secrets.token_hex(32)
    new_user = User.User(
        username=request_body.username,
        email=request_body.email,
        password_hash=Hash.bcrypt(request_body.password),
        api_key=api_key
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"success": True, "message": "Account created successfully"}
