#### Intro
- 使用 celery 進行排程
- celery 觸發 crawler.tasks.exec_crawler_task
- 實體化 TiktokCrawler 並執行 TiktokCrawler.exec_crawler()
- 用 selenium 的 log 捕獲非同步請求及其回應
- 解析回應並 bulk insert 到 postgreSQL