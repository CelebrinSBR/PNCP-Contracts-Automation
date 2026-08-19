from __future__ import annotations

import time
import urllib.parse
from subprocess import CREATE_NO_WINDOW

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
        
        # Previne que o Chrome trave quando compilarmos a versão invisível
        service.creation_flags = CREATE_NO_WINDOW

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

        print(f"[{phone}] Abrindo WhatsApp Web...")
        self.driver.get(url)

        # Aumentamos para 90 segundos para dar tempo de você ler o QR Code na primeira vez
        wait = WebDriverWait(
            self.driver,
            90,
        )

        print(f"[{phone}] Aguardando a tela do WhatsApp carregar (Leia o QR Code se necessário)...")

        try:
            # NOVO XPATH: Busca qualquer caixa de texto editável dentro do rodapé (footer) do chat
            textbox = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//footer//div[@contenteditable="true"]',
                    )
                )
            )

            print(f"[{phone}] Caixa de texto encontrada! Disparando a mensagem...")
            textbox.send_keys(
                Keys.ENTER
            )

            # Aguarda a mensagem ser efetivamente enviada antes de pular pro próximo número
            time.sleep(3)
            
            print(f"[{phone}] Mensagem enviada com sucesso!")
            return True

        except Exception as e:
            # Se der erro (ex: número não tem WhatsApp), ele captura, avisa e segue a vida
            print(f"[{phone}] FALHA AO ENVIAR: O número pode ser inválido ou o tempo esgotou.")
            return False