#!/bin/bash

echo "running migration..."

alembic upgrade head

echo "Starting API..."

uvicorn main:app --host 0.0.0.0 --port $PORT 