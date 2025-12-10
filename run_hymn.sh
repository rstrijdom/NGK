#!/bin/bash

# Bash script to run hymn_extractor.py with virtual environment

# Change these paths to match your setup
VENV_PATH="/path/to/your/venv"
SCRIPT_PATH="/path/to/hymn_extractor.py"

echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

echo "Running hymn extractor..."
python "$SCRIPT_PATH"

echo "Deactivating virtual environment..."
deactivate

echo "Done!"