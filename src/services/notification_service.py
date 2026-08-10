from __future__ import annotations
from datetime import datetime

from clients.pncp_client import PNCPClient
from clients.whatsapp_client import WhatsAppClient

from repositories.contract_repository import ContractRepository
from repositories.settings_repository import SettingsRepository  # NOVO REPOSITÓRIO

from models.contract import Contract


class NotificationService:

    def __init__(self) -> None:
        self.client = PNCPClient()
        self.repository = ContractRepository()
        self.settings = SettingsRepository()  # INICIALIZANDO O REPOSITÓRIO DE CONFIGURAÇÕES
        self.whatsapp = WhatsAppClient()

    def get_pending_contracts(self) -> list[Contract]:
        pending_contracts: list[Contract] = []

        for contract in self.client.get_contracts():
            if not self._is_pending(contract):
                continue
            pending_contracts.append(contract)

        return pending_contracts

    def send_notifications(self) -> None:
        print("BUSCANDO CONTRATOS PENDENTES")
        contracts = self.get_pending_contracts()
        print(f"CONTRATOS ENCONTRADOS: {len(contracts)}")
        
        sent_contracts: list[Contract] = []

        for contract in contracts:
            print(f"ENVIANDO CONTRATO: {contract.numero}")
            
            is_sent = self.send_notification(contract)
            
            if is_sent:
                sent_contracts.append(contract)

        if sent_contracts:
            self._send_commander_report(sent_contracts)

    def send_notification(self, contract: Contract) -> bool:
        print(f"PROCESSANDO {contract.numero}")
        print(f"PREFIXO DA UNIDADE: [{contract.prefixo_unidade}]")

        phone = self.repository.get_phone_by_unit(contract.prefixo_unidade)

        if phone is None:
            print(f"Telefone não encontrado para {contract.prefixo_unidade}")
            return False

        message = self._build_message(contract)

        self.whatsapp.send_message(phone, message)

        self.repository.mark_as_notified(
            contract.numero,
            str(contract.data_atualizacao),
        )
        
        return True

    def _is_pending(self, contract: Contract) -> bool:
        return not self.repository.was_notified(contract.numero)

    def _build_message(self, contract: Contract) -> str:
        return (
            "Olá, essa é uma mensagem automática do CAE.\n\n"
            "Foi identificada uma atualização de contrato no PNCP.\n\n"
            f"Unidade: {contract.prefixo_unidade}\n"
            f"Número PNCP: {contract.numero}\n"
            f"Objeto: {contract.objeto}"
        )

    def _send_commander_report(self, sent_contracts: list[Contract]) -> None:
        
        # BUSCANDO O TELEFONE DIRETO DO BANCO DE DADOS
        commander_phone = self.settings.get_commander_phone()
        
        # Caso o banco de dados ainda não tenha o telefone cadastrado
        if not commander_phone:
            print("Telefone do comandante não configurado. O relatório não pôde ser enviado.")
            return
        
        hoje = datetime.now().strftime("%d/%m/%Y")
        total = len(sent_contracts)

        report_message = (
            f"Olá comandante, essa é uma mensagem automática.\n"
            f"Um novo relatório de contratos enviados foi criado!\n"
            f"Hoje, {hoje}, foram atualizados e enviados recentemente {total} contratos:\n\n"
        )

        for contract in sent_contracts:
            report_message += (
                f"🔹 Unidade: {contract.prefixo_unidade}\n"
                f"   Número PNCP: {contract.numero}\n"
                f"   Objeto: {contract.objeto}\n\n"
            )

        report_message += "Essa é uma mensagem automática, caso precise de ajuda confira informações com a ASSGOV do CAE."

        self.whatsapp.send_message(commander_phone, report_message)
        print(f"RELATÓRIO ENVIADO AO COMANDANTE: {total} contratos reportados.")