#!/bin/bash

# Create and activate virtual environment
echo "Creating virtual environment..."
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperadmin

echo "Setup complete! Run 'python manage.py runserver' to start the development server."
