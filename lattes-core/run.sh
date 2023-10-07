#!/bin/bash

# Run the store_cvs.py script with Python 3
echo "Running store_cvs.py..."
python3 store_cvs.py

# Check if store_cvs.py exited successfully
if [ $? -eq 0 ]; then
    echo "store_cvs.py completed successfully."
else
    echo "store_cvs.py encountered an error."
    exit 1
fi
