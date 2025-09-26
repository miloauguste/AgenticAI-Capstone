#!/bin/bash

echo "Starting Intelligent Feedback Analysis System..."
echo "============================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# Install requirements
echo "Installing dependencies..."
pip3 install -r requirements.txt

echo
echo "Starting Streamlit application..."
echo "Open your browser to http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo

# Start the Streamlit app
streamlit run ui_app.py --server.port 8501 --server.headless true