@echo off
echo Starting Intelligent Feedback Analysis System...
echo =============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install requirements if they don't exist
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Streamlit application...
echo Open your browser to http://localhost:8501
echo Press Ctrl+C to stop the application
echo.

REM Start the Streamlit app
streamlit run ui_app.py --server.port 8501 --server.headless true

pause