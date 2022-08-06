import codecs
from .base import *
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class DeepL(Base):
    URL = "https://www.deepl.com/translator"

    def __init__(self, debug=False):
        super().__init__(debug)
        self.url_map = {
            ("jsonrpc",): Handlers(self.get_simple_result, self._debug_save_json),
            ("dict.deepl.com",): Handlers(
                None, lambda x, y: self._debug_save_raw(x, y, "html")
            ),
        }
    
    def set_source_lang(self):
        elem = self.driver.find_element(By.XPATH, "//button[@dl-test='translator-source-lang-btn']")
        elem.click()
        WebDriverWait(self.driver, self.TIMEOUT_MAX).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@dl-test='translator-lang-option-en']")
            )
        )
        elems = self.driver.find_elements(
            By.XPATH, "//button[contains(@dl-test,'translator-lang-option')]"
        )
        action = ActionChains(self.driver)
        action.move_to_element(elems[1]).click().perform()

    def set_target_lang(self):
        elem = self.driver.find_element(By.XPATH, "//button[@dl-test='translator-target-lang-btn']")
        elem.click()
        WebDriverWait(self.driver, self.TIMEOUT_MAX).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@dl-test='translator-lang-option-en']")
            )
        )
        elems = self.driver.find_elements(
            By.XPATH, "//button[contains(@dl-test,'translator-lang-option')]"
        )
        action = ActionChains(self.driver)
        action.move_to_element(elems[1]).click().perform()

    def wait_for_response(self, text):
        super().wait_for_response(text)
        # if " " in text:
        #     return
        # WebDriverWait(self.driver, self.TIMEOUT_MAX).until(
        #     EC.url_contains(text)
        #     and EC.visibility_of_element_located((By.XPATH, "//a[@class='dictLink']"))
        # )

    def get_simple_result(self, body):
        resp = json.loads(body)
        if not resp["result"] or (
            resp["result"] and "translations" not in resp["result"]
        ):
            return False
        translations = resp["result"]["translations"][0]["beams"]
        self.result = "\n".join([t["sentences"][0]["text"] for t in translations])
        return True
