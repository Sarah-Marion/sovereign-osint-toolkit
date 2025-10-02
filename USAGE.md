# 🖥️ Sovereign OSINT Toolkit - Usage Guide

## Command Line Interface

### Using `main.py` - Primary CLI Tool
```bash
# Activate environment first
source sovereign_env/bin/activate  # Linux/Mac
# sovereign_env\Scripts\activate  # Windows

# Run main CLI
python main.py --help

# Analyze Kenyan Twitter data
python main.py --source twitter --query "Nairobi development" --output results.json

# Analyze with ethical boundaries
python main.py --source news --region kenya --ethical true --output kenya_analysis.json

# Available options:
# --source: Data source (twitter, news, social_media)
# --query: Search query or topic
# --region: Geographic region (kenya, nairobi, east_africa)
# --output: Output file path
# --ethical: Enable ethical boundaries (true/false)
```

### Using api_runner.py - REST API Server

```bash 
# Start the API server
python api_runner.py --host 0.0.0.0 --port 8080

# Or use default settings
python api_runner.py

# Server starts at: http://localhost:8080
# API documentation: http://localhost:8080/docs
```

### 🌐 API Usage Examples

Using curl with the API

```bash 
# Health check
curl http://localhost:8080/health

# Analyze Kenyan social media
curl -X POST "http://localhost:8080/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "twitter",
    "query": "Nairobi infrastructure",
    "region": "kenya",
    "ethical_boundaries": true
  }'

# Get analysis results
curl "http://localhost:8080/api/v1/results?query_id=12345"
```

### Python API Client Example

```python 
import requests

# Analyze data through API
response = requests.post("http://localhost:8080/api/v1/analyze", 
    json={
        "source": "news",
        "query": "Kenyan elections",
        "region": "nairobi",
        "ethical_boundaries": True
    }
)

results = response.json()
print(results)
```

## 🔧 Module-Specific Usage

### Direct Python Usage

```python 
from src.sovereign_osint.collectors.news_collector import NewsCollector
from src.sovereign_osint.analyzers.cultural_analyzer import CulturalAnalyzer

# Collect news data
collector = NewsCollector(region="kenya")
articles = collector.collect_news("development projects")

# Analyze with cultural context
analyzer = CulturalAnalyzer()
insights = analyzer.analyze_cultural_context(articles)

print(insights)
```

## 📊 Output Formats

### JSON Output Example

```json 
{
  "query": "Nairobi development",
  "region": "kenya",
  "results": [
    {
      "source": "twitter",
      "content": "New infrastructure project in Nairobi...",
      "cultural_context": "local_development",
      "ethical_rating": "high",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "analysis_metadata": {
    "ethical_boundaries_respected": true,
    "cultural_sensitivity_score": 0.95
  }
}
```


## 🐳 Docker Usage

Using the Dockerized Application

```bash 
# Build and run with Docker Compose
docker-compose up --build

# Or run specific services
docker-compose up api
docker-compose up redis

# Access API at: http://localhost:8080
```

## 🔒 Environment Configuration

Create .env file from template:

```bash 
cp .env.template .env
```

Edit .env with your settings:

```ini 
API_KEYS=your_twitter_api_key,your_news_api_key
REDIS_URL=redis://redis:6379
DEFAULT_REGION=kenya
ETHICAL_BOUNDARIES=true
LOG_LEVEL=INFO
```


## 🚀 Quick Start Examples

### Example 1: Basic Analysis

```bash 
python main.py --source news --query "Kenyan technology" --output tech_analysis.json
```

### Example 2: API Development

```bash 
# Terminal 1 - Start API
python api_runner.py

# Terminal 2 - Make requests
curl -X POST "http://localhost:8080/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"source": "twitter", "query": "Nairobi", "region": "kenya"}'
```

### Example 3: Cultural Context Analysis

```python 
from src.sovereign_osint import KenyanOSINTCollector

collector = KenyanOSINTCollector(ethical_boundaries=True)
results = collector.analyze_with_cultural_context(
    platform="twitter",
    query="county government",
    region="nairobi"
)
```