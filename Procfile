web: gunicorn config.wsgi --log-file - --log-level debug
worker: celery -A config worker -events -loglevel info
beat: celery -A config beat
