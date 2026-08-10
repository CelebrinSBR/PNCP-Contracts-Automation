from __future__ import annotations

import time
from datetime import date, timedelta
import urllib.request
from urllib.parse import urlparse
from tkinter import simpledialog

import requests

from config.settings import (
    CNPJ_ORGAO,
    PAGE_SIZE,
)

from models.contract import Contract


class PNCPClient:

    BASE_URL = (
        "https://pncp.gov.br/api/consulta/v1/contratos"
    )

    def __init__(self) -> None:

        self.headers = {
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "Chrome/138.0"
            ),
        }
        
        # Memória temporária para não pedir a senha a cada página raspada
        self.proxy_auth = None

    def _get_proxy_credentials(self) -> dict | None:
        """Lê o proxy do Windows e pede a senha ao usuário na tela."""
        
        # Se as credenciais já foram digitadas, reaproveita
        if self.proxy_auth is not None:
            return self.proxy_auth

        # Tenta pegar o proxy configurado no Windows
        windows_proxies = urllib.request.getproxies()
        base_proxy = windows_proxies.get('http') or windows_proxies.get('https')

        # Se a rede não tiver proxy, retorna None e segue a vida
        if not base_proxy:
            return None

        # Janelas para solicitar credenciais
        usuario = simpledialog.askstring(
            "Autenticação de Rede", 
            "O Firewall da rede bloqueou o acesso.\n\nDigite seu USUÁRIO de rede:"
        )
        
        if not usuario:
            return None

        senha = simpledialog.askstring(
            "Autenticação de Rede", 
            "Digite sua SENHA de rede:", 
            show='*'  
        )

        if not senha:
            return None

        # Monta a URL do proxy com o usuário e senha injetados
        parsed = urlparse(base_proxy)
        proxy_url_com_senha = f"http://{usuario}:{senha}@{parsed.netloc}"

        # Guarda na memória da classe
        self.proxy_auth = {
            "http": proxy_url_com_senha,
            "https": proxy_url_com_senha,
        }

        return self.proxy_auth

    def get_contracts(self) -> list[Contract]:

        contracts: list[Contract] = []

        page = 1

        while True:

            data = self._fetch_page(page)

            if not data:
                break

            for item in data:

                contract = Contract.from_api(
                    item
                )

                contracts.append(contract)

            if len(data) < PAGE_SIZE:
                break

            page += 1

        return contracts

    def _fetch_page(
        self,
        page: int,
    ) -> list[dict]:

        params = self._build_params(page)
        
        # Busca as credenciais de rede do chefe antes de disparar a requisição
        credenciais = self._get_proxy_credentials()

        for attempt in range(3):

            try:

                response = requests.get(
                    self.BASE_URL,
                    params=params,
                    headers=self.headers,
                    proxies=credenciais,  # <--- Injetando o proxy aqui
                    timeout=30,
                )

                if response.status_code == 400:

                    if "inexistente" in (
                        response.text.lower()
                    ):
                        return []

                if response.status_code == 503:

                    time.sleep(
                        3 * (attempt + 1)
                    )

                    continue

                response.raise_for_status()

                payload = response.json()

                if isinstance(payload, dict):

                    return payload.get(
                        "data",
                        [],
                    )

                return payload

            except requests.exceptions.Timeout:

                time.sleep(3)

        raise Exception(
            "API PNCP indisponível após múltiplas tentativas."
        )

    def _build_params(
        self,
        page: int,
    ) -> dict:

        today = date.today()

        return {
            "dataInicial": (
                today - timedelta(days=5)
            ).strftime("%Y%m%d"),

            "dataFinal": (
                today + timedelta(days=1)
            ).strftime("%Y%m%d"),

            "cnpjOrgao": CNPJ_ORGAO,

            "pagina": page,

            "tamanhoPagina": PAGE_SIZE,
        }