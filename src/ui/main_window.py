from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from services.notification_service import NotificationService
from ui.contacts_window import ContactsWindow


class MainWindow:

    def __init__(self):

        self.service = NotificationService()

        self.root = tk.Tk()

        self.root.title(
            "Gestor de Notificações PNCP"
        )

        self.root.geometry(
            "1000x550"
        )

        self._create_table()

        self._create_buttons()

        self.load_contracts()


    def _create_table(self):

        columns = (
            "numero",
            "unidade",
            "objeto",
            "data",
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
        )


        self.tree.heading(
            "numero",
            text="Número PNCP",
        )

        self.tree.heading(
            "unidade",
            text="Unidade",
        )

        self.tree.heading(
            "objeto",
            text="Objeto",
        )

        self.tree.heading(
            "data",
            text="Atualização",
        )


        self.tree.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10,
        )


    def _create_buttons(self):

        frame = tk.Frame(
            self.root
        )

        frame.pack(
            fill=tk.X
        )


        tk.Button(
            frame,
            text="Gerenciar contatos",
            command=self.open_contacts,
        ).pack(
            side=tk.LEFT,
            padx=10,
            pady=10,
        )


        tk.Button(
            frame,
            text="Enviar notificações",
            command=self.send_notifications,
        ).pack(
            side=tk.LEFT,
            padx=10,
            pady=10,
        )


    def load_contracts(self):

        for item in self.tree.get_children():

            self.tree.delete(item)


        contracts = self.service.get_pending_contracts()


        for contract in contracts:

            self.tree.insert(
                "",
                tk.END,
                values=(
                    contract.numero,
                    contract.prefixo_unidade,
                    contract.objeto,
                    contract.data_formatada,
                ),
            )


    def send_notifications(self):

        print("BOTÃO DE ENVIO CLICADO")

        self.service.send_notifications()

        print("ENVIO FINALIZADO")

        self.load_contracts()


    def open_contacts(self):

        ContactsWindow(
            self.root
        )


    def run(self):

        self.root.mainloop()