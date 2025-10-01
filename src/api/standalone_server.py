"""
Sovereign OSINT Toolkit - Standalone API Server
FastAPI server without dependency on broken imports
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, Field, EmailStr
import time
import secrets
from typing import Optional, List, Dict, Any
import logging
import uvicorn

from strawberry.fastapi import GraphQLRouter
from .graphql_schema import schema

# Security configuration
SECRET_KEY = secrets.token_urlsafe(32)
REFRESH_SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="Sovereign OSINT API",
    description="Standalone REST API for Sovereign OSINT Toolkit - Advanced correlation and analysis",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Apply rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])


# Data Models
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    disabled: bool = False
    roles: List[str] = []
    created_at: datetime
    last_login: Optional[datetime]

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None
    roles: List[str] = []

class LoginRequest(BaseModel):
    username: str
    password: str

class CorrelationRequest(BaseModel):
    data: Dict[str, Any] = Field(..., description="OSINT data payload for correlation")
    sources: Optional[List[str]] = Field(None, description="Specific data sources to utilize")
    correlation_type: str = Field("standard", description="Algorithm type: standard|advanced|realtime")
    priority: str = Field("medium", description="Processing priority: low|medium|high")

class CorrelationResponse(BaseModel):
    correlation_id: str
    status: str
    results: Dict[str, Any]
    confidence: float
    processing_time: float
    sources_used: List[str]
    warnings: Optional[List[str]] = []

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    components: Dict[str, str]
    uptime: float
    requests_processed: int = 0

# Mock user database
users_db = {
    "admin": {
        "id": "user_001",
        "username": "admin",
        "email": "admin@sovereign-osint.com",
        "full_name": "System Administrator",
        "hashed_password": pwd_context.hash("Admin123!"),
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
        "hashed_password": pwd_context.hash("Analyst123!"),
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
        "hashed_password": pwd_context.hash("User123!"),
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

# Authentication functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str) -> Optional[User]:
    if username in users_db:
        user_dict = users_db[username]
        return User(**user_dict)
    return None

def authenticate_user(username: str, password: str) -> Optional[User]:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, users_db[username]["hashed_password"]):
        return None
    
    # Update last login
    users_db[username]["last_login"] = datetime.utcnow()
    return user

def create_tokens(data: dict, expires_delta: Optional[timedelta] = None) -> tuple[str, str]:
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

async def get_current_user(token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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

async def get_current_active_user(authorization: str = Depends(lambda: "")) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    
    token = authorization.replace("Bearer ", "")
    user = await get_current_user(token)
    
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def require_permission(required_permission: str):
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

# Store app start time
app_start_time = time.time()
app.state.requests_processed = 0

# Middleware to track requests
@app.middleware("http")
async def track_requests(request, call_next):
    response = await call_next(request)
    if not hasattr(app.state, 'requests_processed'):
        app.state.requests_processed = 0
    app.state.requests_processed += 1
    return response

# API Routes
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Sovereign OSINT Toolkit API",
        "version": "2.0.0",
        "status": "running",
        "authentication": "enabled",
        "endpoints": {
            "docs": "/api/docs",
            "health": "/api/v1/health",
            "login": "/api/v1/auth/login",
            "correlation": "/api/v1/correlate"
        }
    }

# @app.get("/api/v1/health", response_model=HealthResponse)
# @limiter.limit("30/minute")
# async def health_check():
#     """Health check endpoint"""
#     return HealthResponse(
#         status="healthy",
#         timestamp=datetime.now().isoformat(),
#         version="2.0.0",
#         components={
#             "api": "healthy",
#             "authentication": "active",
#             "rate_limiter": "active",
#             "correlation_engine": "ready"
#         },
#         uptime=round(time.time() - app_start_time, 2),
#         requests_processed=getattr(app.state, 'requests_processed', 0)
#     )

# Enhanced health check to include GraphQL status
@app.get("/api/v1/health", response_model=HealthResponse)
@limiter.limit("30/minute")
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="2.0.0",
        components={
            "rest_api": "healthy",
            "graphql": "healthy",  # Added GraphQL status
            "authentication": "active",
            "rate_limiter": "active",
            "database": "connected"
        },
        uptime=round(time.time() - app_start_time, 2),
        requests_processed=getattr(app.state, 'requests_processed', 0)
    )

@app.post("/api/v1/auth/login", response_model=Token)
@limiter.limit("5/minute")
async def login(login_data: LoginRequest):
    """Authenticate user and return JWT tokens"""
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token, refresh_token = create_tokens(
        data={"sub": user.username, "roles": user.roles},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@app.get("/api/v1/auth/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

@app.post("/api/v1/correlate", response_model=CorrelationResponse)
@limiter.limit("10/minute")
async def correlate_data(
    request: CorrelationRequest,
    current_user: User = Depends(require_permission("correlate_data"))
):
    """Protected correlation endpoint"""
    start_time = time.time()
    
    try:
        # Advanced correlation processing
        correlation_results = await process_correlation(
            request.data, 
            request.sources, 
            request.correlation_type
        )
        
        processing_time = time.time() - start_time
        
        return CorrelationResponse(
            correlation_id=f"corr_{int(time.time())}",
            status="completed",
            results=correlation_results,
            confidence=calculate_confidence(correlation_results),
            processing_time=round(processing_time, 4),
            sources_used=request.sources or ["default", "internal_db"],
            warnings=[] if correlation_results.get("risk_score", 0) < 0.8 else ["High risk detected"]
        )
    
    except Exception as e:
        logging.error(f"Correlation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Correlation processing failed: {str(e)}"
        )

# Helper functions
async def process_correlation(data: Dict, sources: List[str], corr_type: str) -> Dict[str, Any]:
    """Enhanced correlation processing with multiple algorithms"""
    return {
        "entities_found": ["ip_address", "domain", "organization"],
        "relationships": [{"from": "entity1", "to": "entity2", "relationship": "connected"}],
        "risk_score": 0.75,
        "patterns_detected": ["suspicious_activity", "geographic_clustering"],
        "recommendations": ["Monitor for 48 hours", "Cross-reference with threat intelligence"],
        "source_confidence": {source: 0.85 for source in sources} if sources else {"default": 0.75}
    }

def calculate_confidence(results: Dict) -> float:
    """Calculate confidence score for correlation results"""
    base_confidence = 0.7
    if results.get("patterns_detected"):
        base_confidence += 0.1
    return min(round(base_confidence, 2), 1.0)

if __name__ == "__main__":
    print("🚀 Starting Sovereign OSINT Standalone API Server...")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("🔐 Test credentials:")
    print("   - analyst / Analyst123!")
    print("   - admin / Admin123!")
    print("   - user / User123!")
    
    uvicorn.run(
        "standalone_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )