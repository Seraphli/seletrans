from .base import *


class Baidu(Base):
    URL = "https://fanyi.baidu.com"

    def __init__(self, debug=False):
        super().__init__(debug)
        self.url_map = {
            ("v2transapi",): Handlers(self.get_result, self._debug_save_json),
        }
        self.skip_guide = False

    def preprocess(self):
        if not self.skip_guide:
            elem = self.driver.find_element(
                By.XPATH, "//span[@class='app-guide-close']"
            )
            elem.click()
            self.skip_guide = True

    def set_source_lang(self, source):
        elem = self.driver.find_element(
            By.XPATH, "//a[@class='language-btn select-from-language']"
        )
        elem.click()
        if source == "auto":
            elem = self.driver.find_element(
                By.XPATH, "//li[contains(@class,'lang-item')]"
            )
            elem.click()
        else:
            elem = self.driver.find_element(By.XPATH, "//input[@class='search-input']")
            elem.send_keys(source)
            elem = self.driver.find_element(
                By.XPATH, "//div[@class='search-result-item']"
            )
            elem.click()

    def set_target_lang(self, target):
        elem = self.driver.find_element(
            By.XPATH, "//a[@class='language-btn select-to-language']"
        )
        elem.click()
        elem = self.driver.find_element(By.XPATH, "//input[@class='search-input']")
        elem.send_keys(target)
        elem = self.driver.find_element(By.XPATH, "//div[@class='search-result-item']")
        elem.click()

    def get_result(self, body):
        resp = json.loads(body)
        self.result = resp["trans_result"]["data"][0]["dst"]
        return True
