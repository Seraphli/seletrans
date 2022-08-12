import codecs
from .base import *
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup


class DeepL(Base):
    URL = "https://www.deepl.com/translator"

    def __init__(self, debug=False):
        super().__init__(debug)
        self.url_map = {
            ("jsonrpc",): Handlers(self._get_simple_result, self._debug_save_json),
            ("dict.deepl.com",): Handlers(
                self._get_dict_result, lambda x, y: self._debug_save_raw(x, y, "html")
            ),
        }

    def set_source_lang(self, source):
        elem = self.driver.find_element(
            By.XPATH, "//button[@dl-test='translator-source-lang-btn']"
        )
        elem.click()
        WebDriverWait(self.driver, self.TIMEOUT_MAX).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@dl-test='translator-lang-option-auto']")
            )
        )
        elem = self.driver.find_element(
            By.XPATH, f"//button[@dl-test='translator-lang-option-{source}']"
        )
        elem.click()

    def set_target_lang(self, target):
        elem = self.driver.find_element(
            By.XPATH, "//button[@dl-test='translator-target-lang-btn']"
        )
        elem.click()
        WebDriverWait(self.driver, self.TIMEOUT_MAX).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@dl-test='translator-lang-option-en-US']")
            )
        )
        elem = self.driver.find_element(
            By.XPATH, f"//button[@dl-test='translator-lang-option-{target}']"
        )
        elem.click()

    def _get_simple_result(self, body):
        resp = json.loads(body)
        if not resp["result"] or (
            resp["result"] and "translations" not in resp["result"]
        ):
            return False
        translations = resp["result"]["translations"][0]["beams"]
        self.result = [t["sentences"][0]["text"] for t in translations]
        return True

    def _get_dict_result(self, body):
        soup = BeautifulSoup(body, features="html.parser")
        wmeans = soup.select("a[class*='dictLink']")
        if len(wmeans) == 0:
            self.dict_result = ""
            return False
        wtypes = soup.select("span[class*='type']")
        words = zip([i.text for i in wmeans], [i.text for i in wtypes])
        dict_result = []
        for wmean, wtypes in words:
            if self.text in wmean:
                dict_result.append({"type": wtypes, "means": []})
                continue
            dict_result[-1]["means"].append(wmean)
        self.dict_result = dict_result
        return True

    def play_sound(self, check_interval=0.1):
        elem = self.driver.find_element(
            By.XPATH, f"//button[@dl-test='translator-speaker-source']"
        )
        class_attr = elem.get_attribute("class")
        elem.click()
        while True:
            _attr = elem.get_attribute("class")
            if _attr == class_attr:
                break
            time.sleep(check_interval)
        time.sleep(check_interval)

    def wait_for_response(self, text):
        super().wait_for_response(text)
        while True:
            self._get_net_logs()
            flag = False
            for log in self.net_logs:
                log_json = json.loads(log["message"])["message"]
                if log_json["method"] != "Network.responseReceived":
                    continue
                url = log_json["params"]["response"]["url"]
                if self.check_url(("dict.deepl.com", ), url):
                    flag = True
                    print("flag dict")
                    break
            if flag:
                break
            time.sleep(0.1)
