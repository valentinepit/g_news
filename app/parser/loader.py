import pickle
from datetime import datetime
from random import randint
from time import sleep

import selenium.webdriver
from selenium.common import InvalidCookieDomainException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from app.db.db import new_session
from app.db.models import Cookies


class NewsViewer:
    model_cls = Cookies

    def __init__(self, url: str, num: int = 2):
        self.driver = None
        self.record = None
        self.url = url
        self.num = num

    def load(self):
        with new_session() as session:
            cookie, counter = self.get_cookies(session)
            self.get_webdriver(cookie, counter)


    def get_cookies(self, session):
        self.record = session.query(Cookies).filter(Cookies.id == self.num).one()
        return pickle.loads(self.record.cookie), self.record.counter

    def add_cookies(self, cookie):
        for item in cookie:
            try:
                self.driver.add_cookie(item)
            except InvalidCookieDomainException:
                print("No cookie")

    def get_webdriver(self, cookie, counter):
        try:
            self.driver = selenium.webdriver.Firefox()
            self.add_cookies(cookie)
            self.driver.get(self.url)
            self.news_viewer()
            self.update_cookies(counter)
        finally:
            self.driver.close()

    def news_viewer(self):
        scroll_position = 0
        page_height = self.driver.execute_script("return document.body.scrollHeight")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, ("onetrust-accept-btn-handler")))).click()
        while scroll_position <= page_height / 4: #TODO:  remove 4
            self.driver.implicitly_wait(10)
            self.driver.execute_script(f"window.scrollTo(0, {scroll_position})")
            sleep(randint(0, 5))
            scroll_position += 200

    def update_cookies(self, counter):
        ck = pickle.dumps(self.driver.get_cookies())
        now = datetime.now()
        self.record.cookie = ck
        self.record.counter = counter + 1
        self.record.last_update = now
        # instance = Cookies(
        #     cookie=ck,
        #     last_start_time=now,
        #     counter=
        # )


# with new_session() as session:
# now = datetime.now()
# instance = Cookies(
#     id=1,
#     created_at=now,
#     last_start_time=now,
#     counter=1
# )
# session.add(instance)
# ck = session.query(Cookies).all()
# ck = session.query(Cookies).all()
# print()

_url = "https://news.google.com/articles/CBMiWmh0dHBzOi8vd3d3Lndhc2hpbmd0b25wb3N0LmNvbS93b3JsZC8yMDIzLzA0LzIyL3N1ZGFuLWV2YWN1YXRpb25zLXVzLWJyaXRhaW4tZnJhbmNlLXNhdWRpL9IBAA?hl=en-US&gl=US&ceid=US%3Aen"
dr = NewsViewer(_url)
dr.load()
