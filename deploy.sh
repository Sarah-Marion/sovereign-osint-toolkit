#!/bin/bash

echo "🚀 Deploying Sovereign OSINT Toolkit..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Build and start containers
echo "📦 Building Docker images..."
docker-compose build

echo "🔧 Starting services..."
docker-compose up -d

echo "✅ Deployment complete!"
echo "📚 API Documentation: http://localhost:8000/api/docs"
echo "🔗 GraphQL Endpoint: http://localhost:8000/graphql"
echo "💡 Check logs with: docker-compose logs -f"