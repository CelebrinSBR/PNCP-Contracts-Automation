import tkinter as tk
from tkinter import ttk

def __init__(self) -> None:

    self.service = Notification_Service()

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