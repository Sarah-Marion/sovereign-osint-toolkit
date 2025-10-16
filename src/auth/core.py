from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
import logging

from .models import User, TokenData, LoginRequest

# Security configuration
SECRET_KEY = secrets.token_urlsafe(32)
REFRESH_SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Mock user database (replace with real database in production)
users_db: Dict[str, Dict[str, Any]] = {
    "admin": {
        "id": "user_001",
        "username": "admin",
        "email": "admin@sovereign-osint.com",
        "full_name": "System Administrator",
        "hashed_password": pwd_context.hash("DemoAdmin123!"),
        "disabled": False,
        "roles": ["admin", "analyst", "user"],
        "created_at": datetime.utcnow(),
        "last_login": None
    },
    "analyst": {
        "id": "user_002", 
        "username": "analyst",
        "email": "analyst@sovereign-osint.com",
        "full_name": "OSINT Analyst",
        "hashed_password": pwd_context.hash("DemoAnalyst123!"),
        "disabled": False,
        "roles": ["analyst", "user"],
        "created_at": datetime.utcnow(),
        "last_login": None
    },
    "user": {
        "id": "user_003",
        "username": "user",
        "email": "user@sovereign-osint.com", 
        "full_name": "Standard User",
        "hashed_password": pwd_context.hash("DemoUser123!"),
        "disabled": False,
        "roles": ["user"],
        "created_at": datetime.utcnow(),
        "last_login": None
    }
}

# Role permissions configuration
ROLE_PERMISSIONS = {
    "admin": ["*"],
    "analyst": ["correlate_data", "view_alerts", "export_data", "manage_queries"],
    "user": ["correlate_data", "view_alerts"]
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def get_user(username: str) -> Optional[User]:
    """Get user from database"""
    if username in users_db:
        user_dict = users_db[username]
        return User(**user_dict)
    return None

def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate user credentials"""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, users_db[username]["hashed_password"]):
        return None
    
    # Update last login
    users_db[username]["last_login"] = datetime.utcnow()
    return user

def create_tokens(data: dict, expires_delta: Optional[timedelta] = None) -> tuple[str, str]:
    """Create access and refresh tokens"""
    to_encode = data.copy()
    
    # Access token
    if expires_delta:
        access_expire = datetime.utcnow() + expires_delta
    else:
        access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": access_expire, "type": "access"})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Refresh token
    refresh_expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": refresh_expire, "type": "refresh"})
    refresh_token = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    
    return access_token, refresh_token

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if username is None or token_type != "access":
            raise credentials_exception
            
        token_data = TokenData(username=username, roles=payload.get("roles", []))
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_permission(required_permission: str):
    """Dependency to check user permissions"""
    def permission_checker(current_user: User = Depends(get_current_active_user)):
        user_permissions = set()
        
        # Collect all permissions from user roles
        for role in current_user.roles:
            if role in ROLE_PERMISSIONS:
                if ROLE_PERMISSIONS[role] == ["*"]:  # Admin has all permissions
                    return current_user
                user_permissions.update(ROLE_PERMISSIONS[role])
        
        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {required_permission} required"
            )
            
        return current_user
    return permission_checker

def require_role(required_role: str):
    """Dependency to check user role"""
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if required_role not in current_user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {required_role} required"
            )
        return current_user
    return role_checker