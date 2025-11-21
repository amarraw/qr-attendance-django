#!/bin/bash
# Setup script for QR Attendance System

echo "================================"
echo "QR Attendance System Setup"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "✓ Virtual environment created"
echo ""

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Run migrations
echo "Setting up database..."
python manage.py migrate

echo "✓ Database configured"
echo ""

# Create superuser
echo "Creating superuser account..."
python manage.py createsuperuser

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit:"
echo "  http://localhost:8000/"
echo ""
