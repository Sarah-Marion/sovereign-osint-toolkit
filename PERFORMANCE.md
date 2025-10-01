# ⚡ Performance Optimization

## Caching Strategy

### Redis Setup
Redis is already configured in `docker-compose.yml`. To use it in your application:

```python
import redis
import json

# Connect to Redis
r = redis.Redis(host='redis', port=6379, db=0)

# Cache OSINT query results
def cache_osint_query(query_key, results, ttl=3600):
    r.setex(f"osint:{query_key}", ttl, json.dumps(results))

def get_cached_osint(query_key):
    cached = r.get(f"osint:{query_key}")
    return json.loads(cached) if cached else None