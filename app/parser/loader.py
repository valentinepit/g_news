import os
import pickle
from datetime import datetime
from random import randint
from time import sleep

from selenium import webdriver
from selenium.common import InvalidCookieDomainException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy.orm import Session

from app.db.db import new_session
from app.db.models import Cookies, Profile


class NewsViewer:
    model_cls = Cookies
    base_url = "https://news.google.com/"

    def __init__(self, url: str, num: int):
        self.driver = None
        self.record = None
        self.domain = ""
        self.url = url
        self.num = num

    def load(self):
        with new_session() as session:
            self.record = session.query(Profile).filter(Profile.id == self.num).one()
            self.navigation(session)

    def get_cookies(self, session: Session) -> list[dict]:
        cookies = session.query(Cookies).filter(Cookies.profile_id == self.num).filter(
            Cookies.domain == self.domain).all()
        if cookies:
            return pickle.loads(cookies[0].cookie)
        return []

    def add_cookies(self, cookie: list[dict]) -> None:
        for item in cookie:
            try:
                self.driver.add_cookie(item)
            except InvalidCookieDomainException as e:
                print(f"{self.domain}\n{e}")

    def get_domain(self, url):
        self.driver.get(url)
        self.domain = self.driver.current_url.split("/")[2]

    def navigation(self, session: Session) -> None:
        url = self.base_url + self.url.lstrip("./")
        # s = Service(os.environ["CHROMEDRIVER_PATH"])
        options = webdriver.ChromeOptions()
        options.add_argument('disable_infobars')
        # options.add_argument("headless")
        options.add_argument("window-size=1920x935")
        options.add_argument("--kiosk")
        options.add_argument("--log-level=3")
        try:
            self.driver = webdriver.Chrome(chrome_options=options)
            self.get_domain(url)
            cookie = self.get_cookies(session)
            self.add_cookies(cookie)
            self.driver.get(url)
            self.news_viewer()
            self.update_cookies(session)
        finally:
            self.driver.close()

    def news_viewer(self) -> None:
        scroll_position = 0
        self.driver.implicitly_wait(15)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, ("onetrust-accept-btn-handler")))).click()
        except TimeoutException:
            pass
        page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        while scroll_position <= page_height:
            self.driver.execute_script(f"window.scrollTo(0, {scroll_position})")
            sleep(randint(0, 5))
            scroll_position += 400

    def update_cookies(self, session) -> None:
        ck = pickle.dumps(self.driver.get_cookies())
        now = datetime.now()
        self.record.counter = self.record.counter + 1
        self.record.last_update = now
        cookies = self.get_cookies(session)
        if not cookies:
            cookies_instance = Cookies(
                cookie=ck,
                domain=self.domain,
                profile_id=self.record.id
            )
            session.add(cookies_instance)
        else:
            cookies.cookie = ck
