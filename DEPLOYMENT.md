# RAG Document Search - Production Deployment Guide

## Quick Start with Docker Compose

### Development Mode

```bash
# Start both frontend and backend
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Production Mode

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Use deployment script
chmod +x deploy.sh
./deploy.sh
```

## Manual Deployment

### 1. Backend Only

```bash
docker build -t rag-backend .
docker run -d \
  --name rag-backend \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  rag-backend
```

### 2. Frontend Only

```bash
docker build -f Dockerfile.frontend -t rag-frontend .
docker run -d \
  --name rag-frontend \
  -p 8501:8501 \
  -e API_URL=http://localhost:8000 \
  rag-frontend
```

## Cloud Deployment Options

### AWS (ECS/Fargate)

1. Push images to ECR:
```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag rag-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/rag-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/rag-backend:latest
```

2. Create ECS task definitions for backend and frontend
3. Deploy to Fargate with Application Load Balancer

### Google Cloud (Cloud Run)

```bash
# Backend
gcloud run deploy rag-backend \
  --image gcr.io/<project-id>/rag-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Frontend
gcloud run deploy rag-frontend \
  --image gcr.io/<project-id>/rag-frontend \
  --platform managed \
  --region us-central1 \
  --set-env-vars API_URL=<backend-url>
```

### DigitalOcean (App Platform)

1. Push to container registry
2. Create new app in App Platform
3. Add backend and frontend as separate services
4. Configure environment variables

### Heroku

```bash
# Backend
heroku container:push web -a rag-backend
heroku container:release web -a rag-backend

# Frontend
heroku container:push web -a rag-frontend
heroku container:release web -a rag-frontend
heroku config:set API_URL=<backend-url> -a rag-frontend
```

## Environment Variables

Create `.env.production` for production:

```bash
# Required for OpenAI models
OPENAI_API_KEY=sk-...

# Required for Supabase storage
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
SUPABASE_BUCKET=rag-documents

# Configuration
DEFAULT_LLM_MODEL=google/flan-t5-small
DEFAULT_STORAGE_BACKEND=supabase
LOG_LEVEL=INFO
```

## Monitoring and Maintenance

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart Services

```bash
docker-compose restart backend
docker-compose restart frontend
```

### Update Deployment

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

## Performance Optimization

### Backend
- Use GPU for faster inference (change device to 'cuda')
- Increase workers for uvicorn
- Cache embeddings and indexes
- Use smaller LLM models for faster responses

### Frontend
- Enable Streamlit caching
- Optimize image sizes
- Use CDN for static assets

## Security Checklist

- [ ] Use HTTPS in production (configure nginx with SSL)
- [ ] Set secure environment variables
- [ ] Enable CORS restrictions
- [ ] Implement rate limiting
- [ ] Add authentication if needed
- [ ] Keep dependencies updated
- [ ] Use secrets management (AWS Secrets Manager, etc.)

## Troubleshooting

### Backend not responding
```bash
docker logs rag-backend
curl http://localhost:8000/health
```

### Frontend can't connect to backend
```bash
# Check if backend is accessible
docker exec rag-frontend curl http://backend:8000/health

# Verify network
docker network inspect rag-document-search_rag-network
```

### Out of memory
- Reduce model size
- Increase Docker memory limits
- Use smaller batch sizes
