from __future__ import annotations

import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.paths import DRIVER_PATH, WHATSAPP_SESSION_PATH


class WhatsAppClient:

    def __init__(self) -> None:
        self.driver = None


    def _initialize_driver(self) -> None:

        if self.driver is not None:
            return

        options = Options()

        options.add_argument(
            f"user-data-dir={WHATSAPP_SESSION_PATH}"
        )

        options.add_argument(
            "--disable-gpu"
        )

        options.add_argument(
            "--no-sandbox"
        )

        service = Service(
            executable_path=str(DRIVER_PATH)
        )

        self.driver = webdriver.Chrome(
            service=service,
            options=options,
        )


    def send_message(
        self,
        phone: str,
        message: str,
    ) -> bool:

        self._initialize_driver()

        url = (
            "https://web.whatsapp.com/send?"
            f"phone={phone}&"
            f"text={urllib.parse.quote(message)}"
        )

        self.driver.get(url)

        wait = WebDriverWait(
            self.driver,
            40,
        )

        textbox = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//div[@contenteditable="true"][@data-tab="10"]',
                )
            )
        )

        textbox.send_keys(
            Keys.ENTER
        )

        time.sleep(3)

        return True