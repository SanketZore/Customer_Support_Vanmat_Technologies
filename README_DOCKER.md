# Docker Setup for Customer Support Application

This guide explains how to run the Customer Support application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually included with Docker Desktop)

## Quick Start

1. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys:
   # GROK_API_KEY=your-grok-api-key
   # GEMINI_API_KEY=your-gemini-api-key
   ```

2. **Build and run the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   Open your browser and go to `http://localhost:8000`

## Docker Commands

### Build the image
```bash
docker-compose build
```

### Start the application
```bash
docker-compose up
```

### Start in detached mode
```bash
docker-compose up -d
```

### Stop the application
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs
```

### Run database migrations
```bash
docker-compose exec web python manage.py migrate
```

### Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### Run tests
```bash
docker-compose exec web python manage.py test
```

## Environment Variables

The following environment variables can be set in your `.env` file:

- `GROK_API_KEY`: Your Grok API key for AI responses
- `GEMINI_API_KEY`: Your Gemini API key (alternative AI service)
- `SECRET_KEY`: Django secret key (generated automatically if not set)
- `DEBUG`: Set to `False` for production

## Production Deployment

For production deployment, consider:

1. Using a proper database (PostgreSQL) instead of SQLite
2. Setting `DEBUG=False` in environment variables
3. Using a proper WSGI server (Gunicorn) instead of Django development server
4. Setting up proper static file serving with Nginx or similar
5. Using environment-specific settings

## Troubleshooting

### Port already in use
If port 8000 is already in use, change the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"
```

### Database issues
Run migrations if you see database-related errors:
```bash
docker-compose exec web python manage.py migrate
```

### Static files not loading
Collect static files:
```bash
docker-compose exec web python manage.py collectstatic
