pip install -r requirements.txt &
python manage.py qcluster &
gunicorn --bind=0.0.0.0:8000 --timeout 600 OAuth.wsgi --access-logfile '-' --error-logfile '-'