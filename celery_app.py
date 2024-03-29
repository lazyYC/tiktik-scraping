from celery import Celery
from celery.schedules import crontab

app = Celery('tiktok_scraping', broker='redis://localhost:6379/0')
app.conf.result_backend = 'redis://localhost:6379/0'
app.autodiscover_tasks(['crawler.tasks'], force=True)
app.conf.beat_schedule = {
    'exec-crawler-every-hour': {
        'task': 'crawler.tasks.exec_crawler_task',  
        'schedule': crontab(minute='0'),
    },
}

app.conf.timezone = 'Asia/Taipei'
