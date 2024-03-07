from celery import shared_task
# from celery.utils.log import get_task_logger
from .crawler import TiktokCrawler
from database.session import get_db_session
from datetime import datetime
from selenium.common.exceptions import TimeoutException

# logger = get_task_logger(__name__)

@shared_task(autoretry_for=(TimeoutException, KeyError, TypeError), retry_backoff=True, retry_backoff_max=180, max_retries=3)
def exec_crawler_task():
    channel_name = 'geevideo'
    with get_db_session() as session:
        crawler = TiktokCrawler(session, channel_name, datetime(2024, 3, 1, 0, 0, 0))
        crawler.exec_crawler()