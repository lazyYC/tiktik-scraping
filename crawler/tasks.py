from celery import shared_task
from .crawler import TiktokCrawler
from database.session import get_db_session
from datetime import datetime

@shared_task
def exec_crawler_task():
    channel_name = 'geevideo'
    with get_db_session() as session:
        crawler = TiktokCrawler(session, channel_name, datetime(2024, 3, 5, 0, 0, 0))
        crawler.exec_crawler()