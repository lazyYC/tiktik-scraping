import time
import json
import crud
from datetime import datetime
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs


class TiktokCrawler:

    def __init__(
        self, session, channel_name: str, tracing_onset: datetime = datetime.now()
    ):
        self.scraping_channel = channel_name
        self.channel_url = f"https://www.tiktok.com/@{self.scraping_channel}"
        self.tracing_onset = tracing_onset
        self.options = ChromeOptions()
        # self.options.binary_location = '/usr/bin/google-chrome'
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = Chrome(options=self.options)
        self.session = session

    def exec_crawler(self):
        try:
            bulk = []
            self.visit_main_page()
            while True:
                response = self.scroll_page()
                cursor = response["cursor"] 
                bulk.extend(self.get_post_stats(response))                   
                if cursor != 0 and datetime.fromtimestamp(cursor / 1000) < self.tracing_onset:
                    break
            crud.create_bulk_posts(self.session, bulk)
        except Exception as e:
            print(e)
            raise
        finally:
            self.driver.quit()


    def visit_main_page(self):
        self.driver.get(self.channel_url)
        try:
            guest_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[class*="DivGuestModeContainer"]')
                )
            )
            guest_btn.click()
        except Exception as e:
            print("No guest mode button found.")

    def scroll_page(self) -> dict:
        time.sleep(10)
        logs = self.driver.get_log("performance")
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        for entry in logs:
            if response := self.is_item_list(entry):
                return response

    def is_item_list(self, entry) -> dict:
        try:
            log = json.loads(entry["message"])["message"]
            if "Network.requestWillBeSent" == log["method"]:
                url = log["params"]["request"]["url"]
                if "post/item_list" in url:
                    body = self.get_body(log, self.driver)
                    cursor = float(
                        parse_qs(urlparse(url).query).get("cursor", [0])[0])
                    body["cursor"] = cursor
                    return body
                else:
                    return None
                
        except Exception as e:
            print(e)
            return None

    def get_body(self, log, driver) -> dict:
        request_id = log.get("params").get("requestId")
        driver.execute_cdp_cmd("Network.getResponseBody", {
                               "requestId": request_id})
        response_dict = driver.execute_cdp_cmd(
            "Network.getResponseBody", {"requestId": request_id}
        )
        body = response_dict.get("body")
        jres = json.loads(body)
        return jres

    def get_post_stats(self, response: dict) -> list:
        data = []
        for post in response["itemList"]:
            if datetime.fromtimestamp(float(post["createTime"])) < self.tracing_onset:
                break
            data.append(
                dict(
                    post_tiktok_id=post["id"],
                    content=post["desc"],
                    collect_count=int(post["stats"]["collectCount"]),
                    digg_count=int(post["stats"]["diggCount"]),
                    share_count=int(post["stats"]["shareCount"]),
                    comment_count=int(post["stats"]["commentCount"]),
                    play_count=int(post["stats"]["playCount"]),
                    post_created_time=datetime.fromtimestamp(
                        post["createTime"]),
                    scraped_time=datetime.now(),
                    )
                )
        return data
