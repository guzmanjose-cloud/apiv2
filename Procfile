release: export CORALOGIX_SUBSYSTEM=release; python manage.py migrate && python manage.py create_academy_roles && python manage.py set_permissions
celeryworker: export CORALOGIX_SUBSYSTEM=celeryworker; export CELERY_WORKER_RUNNING=True; celery -A breathecode.celery worker --loglevel=INFO --concurrency 2
web: export CORALOGIX_SUBSYSTEM=web; gunicorn breathecode.wsgi --timeout 29
