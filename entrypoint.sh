#!/bin/bash

# Default values
API_HOST="0.0.0.0"
API_PORT=${API_PORT:-8001}
APP_DEBUG=${APP_DEBUG:-false}

# Convert debug to reload flag
if [ "$APP_DEBUG" = "true" ] || [ "$APP_DEBUG" = "True" ]; then
    RELOAD_FLAG="--reload"
else
    RELOAD_FLAG=""
fi

# Start uvicorn with the app module directly
exec uvicorn app.main:app \
    --host "$API_HOST" \
    --port "$API_PORT" \
    $RELOAD_FLAG