from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Dict, Type, Iterable, List

import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import codecs
import json
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import urllib.parse
from dataclasses import dataclass
import time
from seletrans.util import get_path


@dataclass
class Handlers:
    process: List[Callable[[str], bool]] | None = None
    debug: Callable[[str, str]] | None = None


class Base:
    NAME = "base"
    URL = ""
    TIMEOUT_MAX = 60
    url_map: Dict[Iterable[str], Type(Handlers)]

    def __init__(self, debug=False) -> None:
        self.debug = debug
        chromedriver_autoinstaller.install()
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        if not debug:
            options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.url_map = {}
        self.net_logs = []

    def check_url(self, parts, url):
        for part in parts:
            if part in url:
                return True
        return False

    def close(self):
        self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def preprocess(self):
        pass

    def set_source_lang(self, source_lang):
        pass

    def set_target_lang(self, target_lang):
        pass

    def get_textarea(self):
        elem = self.driver.find_element(By.CSS_SELECTOR, "textarea")
        return elem

    def wait_for_response(self, text):
        self._wait_for_url_change(text)
        self._wait_for_network_idle()

    def _wait_for_url_change(self, text):
        WebDriverWait(self.driver, self.TIMEOUT_MAX).until(
            EC.url_contains(urllib.parse.quote(text))
        )

    def _wait_for_network_idle(self, check_time=0.2):
        st = time.time()
        logs = self._get_net_logs()
        while len(logs) != 0:
            time.sleep(check_time)
            if time.time() - st > self.TIMEOUT_MAX:
                return False
            logs = self._get_net_logs()
        return True

    def _handle_pattern(self, log_json, handler):
        requestId = log_json["params"]["requestId"]
        try:
            response_body = self.driver.execute_cdp_cmd(
                "Network.getResponseBody", {"requestId": requestId}
            )
            body = response_body["body"]
            if handler.process:
                if callable(handler.process):
                    flag = handler.process(body)
                else:
                    flag = any([p(body) for p in handler.process])
            else:
                flag = True
            if flag and self.debug:
                fn = f"{self.__class__.__name__}_{requestId}"
                if handler.debug:
                    handler.debug(fn, body)
                else:
                    self._debug_save_raw(fn, body)
        except WebDriverException:
            pass
        except:
            import traceback

            traceback.print_exc()

    def _handle_patterns(self, log_json):
        url = log_json["params"]["response"]["url"]
        for pattern, handler in self.url_map.items():
            if self.check_url(pattern, url):
                self._handle_pattern(log_json, handler)

    def _debug_save_json(self, fn, body):
        resp = json.loads(body)
        with codecs.open(f"{get_path('tmp', parent=True)}/{fn}.json", "w", "utf8") as f:
            json.dump(resp, f, ensure_ascii=False, indent=2)

    def _debug_save_raw(self, fn, body, suffix="body"):
        with codecs.open(
            f"{get_path('tmp', parent=True)}/{fn}.{suffix}", "w", "utf8"
        ) as f:
            f.write(body)

    def _clear_net_logs(self):
        self.net_logs = []

    def _get_net_logs(self):
        logs = self.driver.get_log("performance")
        self.net_logs.extend(logs)
        return logs

    def query(self, text, source="auto", target="zh"):
        self.text = text
        self.driver.get(self.URL)
        self.preprocess()
        self.set_source_lang(source)
        self.set_target_lang(target)
        self._get_net_logs()
        self._clear_net_logs()
        elem = self.get_textarea()
        elem.send_keys(self.text)
        self.wait_for_response(self.text)
        self._get_net_logs()
        self.result = ""
        for log in self.net_logs:
            log_json = json.loads(log["message"])["message"]
            if log_json["method"] != "Network.responseReceived":
                continue
            self._handle_patterns(log_json)
        return self
