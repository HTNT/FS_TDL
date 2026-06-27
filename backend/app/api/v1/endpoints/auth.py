from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import create_access_token, verify_password, get_password_hash, get_current_user
from app.db.database import get_db
from app.models.user import User
from app.models.account import Account
from app.schemas.user import LoginResponse, UserCreate
from app.schemas.account import RegisterRequest
from app.utils import generate_user_id

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

@router.post("/register", response_model=LoginResponse)
def register(
    req: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Register new account and create user profile"""
    
    # Check if email exists
    existing_account = db.query(Account).filter(Account.email == req.email).first()
    if existing_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username exists
    existing_user = db.query(User).filter(User.username == req.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create account with auto-increment ID
    hashed_password = get_password_hash(req.password)
    db_account = Account(
        email=req.email,
        hashed_password=hashed_password
    )
    db.add(db_account)
    db.flush()
    
    # Create user profile with generated ID
    db_user = User(
        id=generate_user_id(),
        account_id=db_account.id,
        username=req.username
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_account.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }

@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login with email and password"""
    
    # Find account by email
    account = db.query(Account).filter(Account.email == form_data.username).first()
    if not account or not verify_password(form_data.password, account.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not account.is_active:
        raise HTTPException(status_code=400, detail="Account is inactive")
    
    # Get user profile
    user = db.query(User).filter(User.account_id == account.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": account.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

