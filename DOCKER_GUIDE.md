# Docker Setup for Vedantu Chat Dashboard

## Overview
This guide explains how to build, run, and deploy the Vedantu Chat Dashboard application using Docker.

## Prerequisites
- Docker (v20.10+)
- Docker Compose (v1.29+)
- Port 5000 available on your machine

## Files
- `Dockerfile` - Container image definition
- `docker-compose.yml` - Multi-container orchestration (for development)
- `.dockerignore` - Files to exclude from Docker build

---

## Quick Start (Recommended)

### Using Docker Compose (Development)

```bash
# Navigate to project directory
cd vedantu

# Build and start the container
docker-compose up --build

# Access the application
# http://localhost:5000
```

To stop:
```bash
docker-compose down
```

---

## Manual Docker Commands

### Build the Image

```bash
# Build the Docker image
docker build -t vedantu-chat:latest .

# Or with specific version tag
docker build -t vedantu-chat:1.0 .
```

### Run the Container

```bash
# Run the container (development mode with hot reload)
docker run -p 5000:5000 -v $(pwd):/app vedantu-chat:latest

# Or on Windows PowerShell:
docker run -p 5000:5000 -v ${PWD}:/app vedantu-chat:latest

# Run in background (detached mode)
docker run -d -p 5000:5000 --name vedantu-app vedantu-chat:latest

# Run with environment variables
docker run -p 5000:5000 \
  -e FLASK_ENV=development \
  -e FLASK_DEBUG=1 \
  vedantu-chat:latest
```

### View Logs

```bash
# View logs from running container
docker logs vedantu-app

# Follow logs in real-time
docker logs -f vedantu-app
```

### Stop and Remove Container

```bash
# Stop the running container
docker stop vedantu-app

# Remove the container
docker rm vedantu-app

# Remove the image
docker rmi vedantu-chat:latest
```

---

## Environment Variables

The app supports these environment variables:

```env
FLASK_ENV=production          # or 'development'
FLASK_DEBUG=0                 # or '1' for debug mode
PYTHONUNBUFFERED=1            # Ensure Python output is logged
```

### Production Example

```bash
docker run -d -p 5000:5000 \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=0 \
  --name vedantu-prod \
  vedantu-chat:latest
```

---

## Docker Compose Usage

### Common Commands

```bash
# Start services (build if needed)
docker-compose up -d

# View running services
docker-compose ps

# View service logs
docker-compose logs vedantu-chat
docker-compose logs -f vedantu-chat

# Rebuild the image
docker-compose build

# Restart services
docker-compose restart

# Stop services
docker-compose stop

# Stop and remove everything
docker-compose down

# Remove volumes too (warning: data loss)
docker-compose down -v
```

---

## Dockerfile Breakdown

### Base Image
```dockerfile
FROM python:3.12-slim
```
- Uses official Python 3.12 slim image (lightweight)
- Reduces image size by ~200MB vs full Python image

### Dependencies Installation
```dockerfile
RUN apt-get update && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt
```
- Installs system dependencies (gcc for compiled packages)
- Uses `--no-cache-dir` to reduce image size
- Cleans apt cache after installation

### Volumes
```dockerfile
COPY app.py .
COPY static/ ./static/
COPY templates/ ./templates/
```
- Copies application code into container
- Organizes files in working directory

### Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3
```
- Container automatically checks if app is running
- Docker can restart unhealthy containers
- Useful for orchestration platforms (Kubernetes, Swarm)

---

## Image Size Optimization

### Current Size
```
vedantu-chat:latest    ~500MB (includes Python 3.12, dependencies)
```

### Multi-Stage Build (Optional)
For smaller production images:

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
COPY static/ ./static/
COPY templates/ ./templates/
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["python", "app.py"]
```

Reduces final image to ~450MB.

---

## Deployment Scenarios

### Local Development
```bash
docker-compose up --build
```

### Testing/Staging
```bash
docker build -t vedantu-chat:staging .
docker run -p 5000:5000 vedantu-chat:staging
```

### Production
```bash
# Build optimized image
docker build --no-cache -t vedantu-chat:1.0 .

# Tag for registry
docker tag vedantu-chat:1.0 your-registry/vedantu-chat:1.0

# Push to registry
docker push your-registry/vedantu-chat:1.0

# Run in production
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=0 \
  --restart always \
  your-registry/vedantu-chat:1.0
```

---

## Docker Hub Registry

### Login
```bash
docker login
```

### Tag Image
```bash
docker tag vedantu-chat:latest your-username/vedantu-chat:latest
docker tag vedantu-chat:latest your-username/vedantu-chat:1.0
```

### Push
```bash
docker push your-username/vedantu-chat:latest
docker push your-username/vedantu-chat:1.0
```

### Pull
```bash
docker pull your-username/vedantu-chat:latest
```

---

## Kubernetes Deployment

### Create Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vedantu-chat
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vedantu-chat
  template:
    metadata:
      labels:
        app: vedantu-chat
    spec:
      containers:
      - name: vedantu-chat
        image: your-registry/vedantu-chat:1.0
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: production
        - name: FLASK_DEBUG
          value: "0"
        livenessProbe:
          httpGet:
            path: /api/auth/check
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /api/auth/check
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: vedantu-chat-service
spec:
  type: LoadBalancer
  selector:
    app: vedantu-chat
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
```

### Deploy
```bash
kubectl apply -f deployment.yaml
```

---

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker logs vedantu-app

# Check image
docker images vedantu-chat

# Inspect container
docker inspect vedantu-app
```

### Port Already in Use
```bash
# Use different port
docker run -p 8080:5000 vedantu-chat:latest

# Or find and stop existing container
docker ps
docker stop <container-id>
```

### Health Check Failing
```bash
# Check if app is responding
curl http://localhost:5000/api/auth/check

# View health check details
docker inspect vedantu-app | grep -A 10 "Health"
```

### Volumes Not Mounting
```bash
# Use absolute paths
docker run -v /full/path/to/vedantu:/app vedantu-chat:latest

# Or use bind mounts
docker run --mount type=bind,source=/full/path,target=/app vedantu-chat:latest
```

---

## Security Best Practices

### 1. Use Non-Root User
```dockerfile
RUN useradd -m appuser
USER appuser
```

### 2. Read-Only File System
```bash
docker run --read-only vedantu-chat:latest
```

### 3. Resource Limits
```bash
docker run -m 512m --cpus="1" vedantu-chat:latest
```

### 4. Network Security
```bash
docker run --network private vedantu-chat:latest
```

### 5. Secrets Management
```bash
docker run --secret google_sheets_id vedantu-chat:latest
```

---

## Performance Tips

### 1. Layer Caching
Order Dockerfile commands by change frequency:
```dockerfile
FROM python:3.12-slim
COPY requirements.txt .           # Changes less frequently
RUN pip install ...              # Can be cached
COPY app.py .                    # Changes frequently
COPY static/ ./static/
COPY templates/ ./templates/
```

### 2. Minimize Layers
Combine RUN commands:
```dockerfile
RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*
```

### 3. Use .dockerignore
Exclude unnecessary files to reduce build context.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-20 | Initial Docker setup |

---

## Support

For issues or questions:
1. Check container logs: `docker logs vedantu-app`
2. Verify image: `docker inspect vedantu-chat:latest`
3. Test manually: `docker run -it vedantu-chat:latest /bin/bash`

---

**Last Updated**: December 20, 2025
