#!/bin/bash

echo "Setting virtual environment."

if [ -d ".venv" ]; then
    echo "Virtual environment already exists."
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activar el entorno y siempre (re)instalar dependencias
source .venv/bin/activate
echo "Installing/upgrading dependencies..."
pip install --upgrade -r requirements.txt

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

