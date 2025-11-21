@echo off
REM Setup script for QR Attendance System (Windows)

echo ================================
echo QR Attendance System Setup
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Virtual environment created
echo.

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

echo Dependencies installed
echo.

REM Run migrations
echo Setting up database...
python manage.py migrate

echo Database configured
echo.

REM Create superuser
echo Creating superuser account...
python manage.py createsuperuser

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo To start the server, run:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Then visit:
echo   http://localhost:8000/
echo.
pause
