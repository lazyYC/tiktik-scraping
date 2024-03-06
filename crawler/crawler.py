import random, time, json
import crud
from datetime import datetime
from undetected_chromedriver import Chrome, ChromeOptions
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from urllib.parse import urlparse, parse_qs

# TODO: exception handling (retry, timeout, etc.)

class TiktokCrawler:
    
    def __init__(self, session, channel_name: str, tracing_onset: datetime = datetime.now()):
        self.scraping_channel = channel_name
        self.channel_url = f'https://www.tiktok.com/@{self.scraping_channel}'
        self.tracing_onset = tracing_onset
        self.options = ChromeOptions()
        self.options.add_argument("--headless")
        self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = Chrome(options=self.options, browser_executable_path=r"/usr/bin/chromium")
        # self.driver = Chrome(options=self.options)
        self.session = session

    def exec_crawler(self):
        self.visit_main_page()
        urls = self.scroll_page_handler()
        self.requests_api(urls)
        # self.driver.quit()

    def visit_main_page(self):
        self.driver.get(self.channel_url)
        try:
            guest_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="DivGuestModeContainer"]'))
                )
            guest_btn.click()
        except TimeoutException:
            pass
        
    def scroll_page_handler(self):
        urls = []
        keep_scrolling = True
        while keep_scrolling:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            if url := self.parse_urls_from_logs():
                urls.extend(url)
                # 因為一定會捲動至少一次，所以可以確定 cursor != 0
                cursor = float(parse_qs(urlparse(urls[-1]).query).get('cursor', [0])[0])
                if datetime.fromtimestamp(cursor/1000) < self.tracing_onset:
                    keep_scrolling = False  
                    # urls 中最後一筆 url 會爬到包含一部分 onset 之前的 post
                    # 解析之後再刪除
        return urls
        
    def parse_urls_from_logs(self) -> list:
        logs = self.driver.get_log('performance')
        urls = []
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if "Network.requestWillBeSent" == log["method"]:
                url = log["params"]["request"]["url"]
                if "item_list" in url and url not in urls:
                    urls.append(url)
        return urls

    def requests_api(self, urls: list):
        for url in urls:
            time.sleep(random.randint(1, 3))
            self.driver.get(url)
            stats = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "pre"))
            )
            response = json.loads(stats.text)
            
            for post in response["itemList"]:
                if datetime.fromtimestamp(float(post["createTime"])) < self.tracing_onset:
                   break
                data = dict(
                    post_tiktok_id = post["id"],
                    content = post["desc"],
                    collect_count = int(post["stats"]["collectCount"]),
                    digg_count =int( post["stats"]["diggCount"]),
                    share_count = int(post["stats"]["shareCount"]),
                    comment_count = int(post["stats"]["commentCount"]),
                    play_count = int(post["stats"]["playCount"]),
                    post_created_time = datetime.fromtimestamp(post["createTime"]),
                    scraped_time = datetime.now()
                )
                crud.insert_post_stats_record(self.session, data)
                