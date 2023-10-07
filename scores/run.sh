#!/bin/bash

# Run the main.py script with Python 3
echo "Running main.py..."
python3 -W ignore main.py

# Check if main.py exited successfully
if [ $? -eq 0 ]; then
    echo "main.py completed successfully."
else
    echo "main.py encountered an error."
    exit 1
fi

