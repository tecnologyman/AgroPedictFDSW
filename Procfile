release: |
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
  python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin','admin@agropredict.cl','Admin1234')"
web: gunicorn agropredict.wsgi
