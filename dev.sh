#!/bin/bash
echo "Setting virtual environment."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists."
    source .venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi

echo "Development environment set up."
if [ -f .env ]; then
    echo ".env file already exists."
    echo "Starting the application..."
    cd src/
    exec uvicorn main:app --reload
else
    cp .env.example .env
    echo ".env file created from example."
fi
