#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Pulling default model..."
ollama pull llama3.1:8b

echo "Setup complete."
