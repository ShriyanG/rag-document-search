#!/bin/bash
# Deployment script for RAG Document Search

set -e

echo "🚀 Starting deployment..."

# Build images
echo "📦 Building Docker images..."
docker-compose -f docker-compose.yml build

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.yml down

# Start services
echo "▶️  Starting services..."
docker-compose -f docker-compose.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check health
echo "🏥 Checking service health..."
curl -f http://localhost:8000/health || echo "⚠️  Backend not ready"
curl -f http://localhost:8501/ || echo "⚠️  Frontend not ready"

echo "✅ Deployment complete!"
echo "Frontend: http://localhost:8501"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
