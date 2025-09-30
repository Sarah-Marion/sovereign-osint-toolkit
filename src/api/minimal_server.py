"""
Sovereign OSINT Toolkit - Minimal API Server
No external dependencies beyond FastAPI
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import time
from typing import Optional, List, Dict, Any
import uvicorn

# Simple token-based auth (no JWT dependencies)
API_TOKENS = {
    "admin": "admin_token_123",
    "analyst": "analyst_token_456", 
    "user": "user_token_789"
}

# Initialize FastAPI app
app = FastAPI(
    title="Sovereign OSINT API",
    description="Minimal REST API for Sovereign OSINT Toolkit",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_role: str

class CorrelationRequest(BaseModel):
    data: Dict[str, Any] = Field(..., description="OSINT data payload for correlation")
    sources: Optional[List[str]] = Field(None, description="Specific data sources to utilize")
    correlation_type: str = Field("standard", description="Algorithm type: standard|advanced|realtime")

class CorrelationResponse(BaseModel):
    correlation_id: str
    status: str
    results: Dict[str, Any]
    confidence: float
    processing_time: float
    sources_used: List[str]

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    uptime: float

# Simple user validation
def verify_user(username: str, password: str) -> Optional[str]:
    """Simple user verification"""
    users = {
        "admin": "Admin123!",
        "analyst": "Analyst123!",
        "user": "User123!"
    }
    
    if username in users and users[username] == password:
        return username
    return None

def get_user_role(token: str) -> Optional[str]:
    """Get user role from token"""
    for role, api_token in API_TOKENS.items():
        if api_token == token:
            return role
    return None

async def verify_token(authorization: str = Header(None)) -> str:
    """Verify API token with proper header handling"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication scheme. Use 'Bearer <token>'")
    
    token = authorization.replace("Bearer ", "").strip()
    user_role = get_user_role(token)
    
    if not user_role:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_role

# Store app start time
app_start_time = time.time()

# API Routes
@app.get("/")
async def root():
    return {
        "message": "Sovereign OSINT Toolkit API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/api/docs",
            "health": "/api/v1/health",
            "login": "/api/v1/auth/login",
            "correlation": "/api/v1/correlate",
            "test_auth": "/api/v1/auth/test"
        }
    }

@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        version="2.0.0",
        uptime=round(time.time() - app_start_time, 2)
    )

@app.post("/api/v1/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """Simple login endpoint"""
    user_role = verify_user(login_data.username, login_data.password)
    if not user_role:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return LoginResponse(
        access_token=API_TOKENS[user_role],
        user_role=user_role
    )

@app.post("/api/v1/correlate", response_model=CorrelationResponse)
async def correlate_data(
    request: CorrelationRequest,
    user_role: str = Depends(verify_token)
):
    """Protected correlation endpoint"""
    start_time = time.time()
    
    try:
        # Mock correlation processing
        correlation_results = {
            "entities_found": ["ip_address", "domain", "organization"],
            "relationships": [{"from": "entity1", "to": "entity2", "relationship": "connected"}],
            "risk_score": 0.75,
            "patterns_detected": ["suspicious_activity"],
            "recommendations": ["Monitor for 48 hours"]
        }
        
        processing_time = time.time() - start_time
        
        return CorrelationResponse(
            correlation_id=f"corr_{int(time.time())}",
            status="completed",
            results=correlation_results,
            confidence=0.85,
            processing_time=round(processing_time, 4),
            sources_used=request.sources or ["default"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Correlation failed: {str(e)}")

@app.get("/api/v1/auth/test")
async def test_auth(user_role: str = Depends(verify_token)):
    """Test authentication endpoint"""
    return {
        "message": "Authentication successful",
        "user_role": user_role,
        "status": "authenticated"
    }

@app.get("/api/v1/debug/tokens")
async def debug_tokens():
    """Debug endpoint to show available tokens"""
    return {
        "available_tokens": API_TOKENS,
        "test_users": {
            "admin": "Admin123!",
            "analyst": "Analyst123!", 
            "user": "User123!"
        }
    }

if __name__ == "__main__":
    print("🚀 Starting Sovereign OSINT Minimal API Server...")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("🔐 Test credentials:")
    print("   - Username: analyst, Password: Analyst123!")
    print("   - Username: admin, Password: Admin123!")
    print("   - Username: user, Password: User123!")
    print("\n🔑 After login, use the provided token in Authorization header:")
    print("   Authorization: Bearer <token_from_login>")
    print("\n🔍 Debug endpoint: http://localhost:8000/api/v1/debug/tokens")
    
    uvicorn.run(
        "minimal_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )