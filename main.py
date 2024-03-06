from database.session import get_db_session
from crawler.crawler  import TiktokCrawler  # 确保从您的爬虫文件导入TiktokCrawler
from datetime import datetime

if __name__ == "__main__":
    channel_name = "geevideo"
    with get_db_session() as session:
        crawler = TiktokCrawler(
            session=session, channel_name=channel_name, tracing_onset=datetime(2024, 2, 27, 0, 0, 0)
            )
        crawler.exec_crawler()