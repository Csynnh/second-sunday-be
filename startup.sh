#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run database migrations (if any)
# alembic upgrade head

# Start the application with Gunicorn
exec gunicorn --workers 4 --bind 0.0.0.0:80 app.main:app -k uvicorn.workers.UvicornWorker