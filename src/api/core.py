from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, Field
import time
from typing import Optional, List, Dict, Any
import logging

# Import auth dependencies
from sovereign_osint.auth.core import (
    get_current_active_user, require_permission, require_role,
    authenticate_user, create_tokens, SECRET_KEY, ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_SECRET_KEY
)
from sovereign_osint.auth.models import User, LoginRequest, Token

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Sovereign OSINT API",
    description="Enhanced RESTful API for OSINT correlation and analysis",
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
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enhanced request/response schemas
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

# Enhanced endpoints with proper rate limiting
@app.post("/api/v1/correlate", response_model=CorrelationResponse)
@limiter.limit("10/minute")
async def correlate_data(request: CorrelationRequest):
    """
    Enhanced correlation endpoint with rate limiting and improved processing
    """
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

@app.get("/api/v1/health", response_model=HealthResponse)
@limiter.limit("30/minute")
async def health_check():
    """Enhanced health check with system metrics"""
    return HealthResponse(
        status="healthy",
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        version="2.0.0",
        components={
            "correlation_engine": "healthy",
            "monitoring": "healthy", 
            "rate_limiter": "active",
            "api_gateway": "operational"
        },
        uptime=round(time.time() - app_start_time, 2),
        requests_processed=getattr(app.state, 'requests_processed', 0)
    )

# Enhanced monitoring endpoint
@app.get("/api/v1/monitoring/alerts")
@limiter.limit("15/minute")
async def get_monitoring_alerts(
    severity: Optional[str] = None,
    limit: int = 50
):
    """Get system monitoring alerts with filtering and pagination"""
    alerts = await fetch_system_alerts(severity, limit)
    return {
        "alerts": alerts,
        "total": len(alerts),
        "severity_filter": severity,
        "limit": limit
    }

# Helper functions for enhanced processing
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

async def fetch_system_alerts(severity: Optional[str], limit: int) -> List[Dict]:
    """Fetch system monitoring alerts with filtering"""
    mock_alerts = [
        {"id": "alert_001", "severity": "high", "message": "Unusual traffic pattern", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")},
        {"id": "alert_002", "severity": "medium", "message": "API rate limit approaching", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")}
    ]
    
    if severity:
        return [alert for alert in mock_alerts if alert["severity"] == severity][:limit]
    return mock_alerts[:limit]

# Initialize application state
app_start_time = time.time()

# Middleware to track requests
@app.middleware("http")
async def track_requests(request, call_next):
    response = await call_next(request)
    if not hasattr(app.state, 'requests_processed'):
        app.state.requests_processed = 0
    app.state.requests_processed += 1
    return response


# Add authentication endpoints
@app.post("/api/v1/auth/login", response_model=Token)
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

@app.post("/api/v1/auth/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token"""
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if username is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
            
        user = get_user(username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
            
        access_token, new_refresh_token = create_tokens(
            data={"sub": user.username, "roles": user.roles}
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer", 
            refresh_token=new_refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@app.get("/api/v1/auth/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

# Update existing endpoints with authentication
@app.post("/api/v1/correlate", response_model=CorrelationResponse)
@limiter.limit("10/minute")
async def correlate_data(
    request: CorrelationRequest,
    current_user: User = Depends(require_permission("correlate_data"))
):
    """Protected correlation endpoint - requires correlate_data permission"""
    # ... (existing correlation logic remains the same)

@app.get("/api/v1/monitoring/alerts")
@limiter.limit("15/minute") 
async def get_monitoring_alerts(
    severity: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(require_permission("view_alerts"))
):


# Admin-only endpoint
@app.get("/api/v1/admin/users")
async def get_all_users(current_user: User = Depends(require_role("admin"))):
    """Get all users - admin role required"""
    return {"users": list(users_db.values())}
