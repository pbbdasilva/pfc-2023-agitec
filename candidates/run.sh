#!/bin/bash

# Run the fetch_candidates.py script with Python 3
echo "Running fetch_candidates.py..."
python3 fetch_candidates.py --month 01 --year 2023

# Check if fetch_candidates.py exited successfully
if [ $? -eq 0 ]; then
    echo "fetch_candidates.py completed successfully."
else
    echo "fetch_candidates.py encountered an error."
    exit 1
fi

# Run the fetch_ids.py script with Python 3
echo "Running fetch_ids.py..."
python3 fetch_ids.py

# Check if fetch_ids.py exited successfully
if [ $? -eq 0 ]; then
    echo "fetch_ids.py completed successfully."
else
    echo "fetch_ids.py encountered an error."
    exit 1
fi

# All scripts have completed successfully
echo "Both fetch_candidates.py and fetch_ids.py have completed successfully."
