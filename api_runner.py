"""
Sovereign API Runner
Standalone script to run the Sovereign OSINT API
"""

import uvicorn
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )