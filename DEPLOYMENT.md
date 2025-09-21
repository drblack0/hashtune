# Hashtune Deployment Guide

This guide explains how to deploy the Hashtune application using Docker.

## Prerequisites

- Docker and Docker Compose installed
- API keys for Apify and Google Gemini

## Environment Setup

1. Create a `.env` file in the backend directory (`hashtune/`) with the following variables:

```env
# Apify API Key for web scraping
APIFY_KEY=your_apify_api_key_here

# Google Gemini API Key for AI responses
GEMINI_API_KEY=your_gemini_api_key_here

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
```

## Deployment

### Option 1: Using Docker Compose (Recommended)

1. Navigate to the backend directory:
   ```bash
   cd hashtune
   ```

2. Start both services:
   ```bash
   docker-compose up -d
   ```

3. Check the status:
   ```bash
   docker-compose ps
   ```

4. View logs:
   ```bash
   docker-compose logs -f
   ```

### Option 2: Building Images Separately

1. Build the backend image:
   ```bash
   cd hashtune
   docker build -t hashtune-backend .
   ```

2. Build the frontend image:
   ```bash
   cd hashtune-frontend
   docker build -t hashtune-frontend .
   ```

3. Run the containers:
   ```bash
   # Backend
   docker run -d --name hashtune-backend -p 5000:5000 --env-file .env hashtune-backend

   # Frontend
   docker run -d --name hashtune-frontend -p 80:80 hashtune-frontend
   ```

## Accessing the Application

- **Frontend**: http://localhost
- **Backend API**: http://localhost:5000

## Services

### Backend (Flask + ASGI)
- **Port**: 5000
- **Health Check**: http://localhost:5000/
- **Endpoints**:
  - `POST /scrape-hashtags-and-posts` - Scrape hashtags and profiles
  - `POST /get-post-ideas` - Generate post ideas

### Frontend (React + Nginx)
- **Port**: 80
- **Health Check**: http://localhost/
- **Features**: 
  - React SPA with routing
  - Nginx reverse proxy to backend
  - Gzip compression

## Data Persistence

The following files are mounted as volumes for data persistence:
- `output.csv` - Scraped data output
- `hashtag_stats.csv` - Hashtag statistics
- `posts.csv` - Scraped posts data

## Troubleshooting

### Check Container Logs
```bash
docker-compose logs backend
docker-compose logs frontend
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild Images
```bash
docker-compose up --build
```

### Clean Up
```bash
# Stop and remove containers
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove volumes
docker-compose down -v
```

## Production Considerations

1. **Environment Variables**: Ensure all required environment variables are set
2. **API Keys**: Keep your API keys secure and never commit them to version control
3. **SSL/TLS**: Consider adding SSL certificates for production deployment
4. **Monitoring**: Set up monitoring and logging for production use
5. **Scaling**: Use Docker Swarm or Kubernetes for production scaling

## Development

For development, you can run the services individually:

```bash
# Backend
cd hashtune
python -m uvicorn app.main:asgi_app --host 0.0.0.0 --port 5000 --reload

# Frontend
cd hashtune-frontend
npm start
```

