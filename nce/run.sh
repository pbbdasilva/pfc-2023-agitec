#!/bin/bash

# Run the parse_nces.py script with Python 3
echo "Running parse_nces.py..."
python3 -W ignore parse_nces.py

# Check if parse_nces.py exited successfully
if [ $? -eq 0 ]; then
    echo "parse_nces.py completed successfully."
else
    echo "parse_nces.py encountered an error."
    exit 1
fi

# Run the store_nces.py script with Python 3
echo "Running store_nces.py..."
python3 store_nces.py

# Check if store_nces.py exited successfully
if [ $? -eq 0 ]; then
    echo "store_nces.py completed successfully."
else
    echo "store_nces.py encountered an error."
    exit 1
fi
