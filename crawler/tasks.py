from celery import shared_task
# from celery.utils.log import get_task_logger
from .crawler import TiktokCrawler
from database.session import get_db_session
from datetime import datetime

# logger = get_task_logger(__name__)

@shared_task
def exec_crawler_task():
    channel_name = 'geevideo'
    with get_db_session() as session:
        crawler = TiktokCrawler(session, channel_name, datetime(2024, 3, 5, 0, 0, 0))
        crawler.exec_crawler()