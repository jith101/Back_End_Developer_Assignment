@echo off
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Running migrations...
python manage.py migrate

echo Creating superuser...
python manage.py createsuperadmin

echo Setup complete! Run 'python manage.py runserver' to start the development server.
pause
