import pickle
import selenium.webdriver

driver = selenium.webdriver.Firefox()
driver.get("http://www.google.com")
cookies = pickle.dumps(driver.get_cookies())


# cookies = pickle.load(open("cookies.pkl", "rb"))
# for cookie in cookies:
#     driver.add_cookie(cookie)