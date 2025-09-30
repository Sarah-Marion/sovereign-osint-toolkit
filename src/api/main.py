"""
Sovereign OSINT Toolkit - REST API
FastAPI-based RESTful API for correlation and analysis endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import sys
import os

# Add project root to path for proper imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# Import existing Sovereign components
try:
    from src.analyzers.sovereign_correlator import SovereignCorrelator
    from src.monitoring.sovereign_monitor import SovereignMonitor
except ImportError:
    # Fallback import
    from analyzers.sovereign_correlator import SovereignCorrelator
    from monitoring.sovereign_monitor import SovereignMonitor

# Initialize FastAPI app
app = FastAPI(
    title="Sovereign OSINT API",
    description="REST API for Sovereign OSINT Toolkit - Advanced correlation and analysis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
correlator = SovereignCorrelator()
monitor = SovereignMonitor(correlator)

# Pydantic Models for API
class CorrelationRequest(BaseModel):
    data_sources: List[Dict[str, Any]]
    advanced_analysis: bool = True
    correlation_threshold: float = 0.6

class CorrelationResponse(BaseModel):
    correlation_id: str
    timestamp: datetime
    confidence_score: float
    entity_count: int
    correlation_count: int
    insights: List[str]
    status: str = "completed"

class EntityRequest(BaseModel):
    entities: List[str]
    depth: int = 2

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    components: Dict[str, str]

# API Routes
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Sovereign OSINT Toolkit API",
        "version": "1.0.0",
        "endpoints": {
            "correlation": "/api/v1/correlate",
            "entities": "/api/v1/entities/analyze",
            "monitoring": "/api/v1/monitoring/alerts",
            "health": "/api/v1/health"
        }
    }

@app.post("/api/v1/correlate", response_model=CorrelationResponse)
async def correlate_data(request: CorrelationRequest):
    """
    Run correlation analysis on provided data sources
    """
    try:
        # Run correlation analysis
        result = correlator.correlate_data(
            request.data_sources, 
            advanced=request.advanced_analysis
        )
        
        # Extract key metrics
        confidence = result.get('confidence_synthesis', {}).get('overall_confidence', 0)
        entity_count = result.get('graph_analysis', {}).get('entity_count', 0)
        correlation_count = result.get('multi_modal_correlation', {}).get('correlation_network_size', 0)
        insights = result.get('advanced_insights', [])
        
        return CorrelationResponse(
            correlation_id=f"corr_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            confidence_score=confidence,
            entity_count=entity_count,
            correlation_count=correlation_count,
            insights=insights
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Correlation failed: {str(e)}")

@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for API status"""
    components_status = {}
    
    try:
        # Test correlation component
        test_data = [{"title": "test", "content": "test content", "source": "test"}]
        correlator.correlate_data(test_data, advanced=False)
        components_status["correlation_engine"] = "healthy"
    except Exception as e:
        components_status["correlation_engine"] = f"unhealthy: {str(e)}"
    
    components_status["monitoring"] = "healthy"
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0",
        components=components_status
    )

@app.get("/api/v1/monitoring/alerts")
async def get_monitoring_alerts(limit: int = 10):
    """Get current monitoring alerts"""
    try:
        # Mock alerts
        mock_alerts = [
            {
                "id": 1,
                "timestamp": datetime.now().isoformat(),
                "level": "HIGH",
                "type": "Pattern Detection",
                "message": "Unusual correlation pattern detected",
                "entities": ["nairobi", "development"],
                "confidence": 0.85
            }
        ]
        
        return {"alerts": mock_alerts[:limit], "total": len(mock_alerts)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alerts: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)