@echo off

REM AI-Powered Talent Scouting Agent - Startup Script

echo AI-Powered Talent Scouting Agent - Starting Up
echo ==============================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo Creating directories...
mkdir data\logs 2>nul
mkdir data\cache 2>nul

REM Start the application
echo Starting the application...
python main.py

echo Application started successfully!
pause