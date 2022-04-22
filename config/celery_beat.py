from celery.schedules import crontab


def setup_periodic_tasks(app):
    app.conf.beat_schedule = {
        'delete_messages': {
            'task': 'message.tasks.delete_messages',
            'schedule': 60
        },
        'delete_user': {
            'task': 'users.tasks.delete_user',
            'schedule': crontab(minute=0, hour=0)
        },
        'expired-ad': {
            'task': 'ads.tasks.expired_ad',
            'schedule': crontab(minute=0, hour='*/1')
        },
    }
