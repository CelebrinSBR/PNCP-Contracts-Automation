from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from database.database import get_connection
# IMPORTANDO O NOSSO NOVO REPOSITÓRIO
from repositories.settings_repository import SettingsRepository


class ContactsWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Gerenciamento de Contatos e Configurações"
        )

        self.window.geometry(
            "800x650"  # Aumentei um pouco a altura para caber o novo bloco
        )

        self.window.resizable(
            True,
            True,
        )
        
        # Instancia o repositório de configurações
        self.settings_repo = SettingsRepository()

        self.create_table()
        self.create_form()
        self.create_commander_form()  # NOVO: Cria o bloco do comandante

        self.load_contacts()
        self.load_commander_phone()   # NOVO: Carrega o número salvo ao abrir


    # =========================================================
    # TABELA
    # =========================================================

    def create_table(self):

        columns = (
            "prefixo",
            "nome_da_unidade",
            "telefone",
        )

        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings",
        )

        self.tree.heading("prefixo", text="Prefixo")
        self.tree.heading("nome_da_unidade", text="Nome da Unidade")
        self.tree.heading("telefone", text="Telefone")

        self.tree.column("prefixo", width=150, anchor="center")
        self.tree.column("nome_da_unidade", width=400, anchor="w")
        self.tree.column("telefone", width=180, anchor="center")

        self.tree.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10,
        )


    # =========================================================
    # FORMULÁRIO DE UNIDADES
    # =========================================================

    def create_form(self):

        frame = tk.LabelFrame(
            self.window,
            text="Cadastro de Contato (Unidades)",
            padx=10,
            pady=10,
        )

        frame.pack(
            fill=tk.X,
            padx=10,
            pady=5,
        )

        # PREFIXO
        tk.Label(frame, text="Prefixo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.prefixo = tk.Entry(frame, width=25)
        self.prefixo.grid(row=0, column=1, padx=5, pady=5)

        # NOME DA UNIDADE
        tk.Label(frame, text="Nome da Unidade:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.nome_da_unidade = tk.Entry(frame, width=50)
        self.nome_da_unidade.grid(row=1, column=1, padx=5, pady=5)

        # TELEFONE
        tk.Label(frame, text="Telefone:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.telefone = tk.Entry(frame, width=25)
        self.telefone.grid(row=2, column=1, padx=5, pady=5)

        # BOTÕES
        buttons_frame = tk.Frame(frame)
        buttons_frame.grid(row=0, column=2, rowspan=3, padx=20)

        tk.Button(buttons_frame, text="Adicionar / Salvar", width=18, command=self.save_contact).pack(pady=5)
        tk.Button(buttons_frame, text="Limpar", width=18, command=self.clear_form).pack(pady=5)
        tk.Button(buttons_frame, text="Excluir selecionado", width=18, command=self.delete_contact).pack(pady=5)

        self.tree.bind("<Double-1>", self.select_contact)


    # =========================================================
    # FORMULÁRIO DO COMANDANTE (NOVO)
    # =========================================================
    
    def create_commander_form(self):
        
        commander_frame = tk.LabelFrame(
            self.window,
            text="Configuração de Relatórios (Comandante)",
            padx=10,
            pady=10,
        )

        commander_frame.pack(
            fill=tk.X,
            padx=10,
            pady=10,
        )

        tk.Label(
            commander_frame, 
            text="Telefone do Comandante:",
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.telefone_comandante = tk.Entry(
            commander_frame, 
            width=25,
        )
        self.telefone_comandante.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            commander_frame, 
            text="Salvar Comandante", 
            width=18, 
            command=self.save_commander_phone,
        ).grid(row=0, column=2, padx=20, pady=5)


    # =========================================================
    # CARREGAR E SALVAR COMANDANTE (NOVO)
    # =========================================================

    def load_commander_phone(self):
        phone = self.settings_repo.get_commander_phone()
        
        if phone:
            self.telefone_comandante.delete(0, tk.END)
            self.telefone_comandante.insert(0, phone)

    def save_commander_phone(self):
        phone = self.telefone_comandante.get().strip()
        
        if not phone:
            messagebox.showwarning(
                "Atenção",
                "Informe o telefone do comandante.",
            )
            return
            
        try:
            self.settings_repo.update_commander_phone(phone)
            messagebox.showinfo(
                "Sucesso",
                "Telefone do comandante salvo com sucesso!",
            )
        except Exception as error:
            messagebox.showerror(
                "Erro",
                f"Não foi possível salvar o telefone do comandante:\n\n{error}",
            )


    # =========================================================
    # CARREGAR CONTATOS (UNIDADES)
    # =========================================================

    def load_contacts(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT
                    prefixo,
                    nome_da_unidade,
                    telefone
                FROM configuracao_unidades
                ORDER BY nome_da_unidade
                """
            ).fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)


    # =========================================================
    # SALVAR CONTATO (UNIDADES)
    # =========================================================

    def save_contact(self):

        prefixo = self.prefixo.get().strip().upper()
        nome_da_unidade = self.nome_da_unidade.get().strip().upper()
        telefone = self.telefone.get().strip()

        if not prefixo:
            messagebox.showwarning("Atenção", "Informe o prefixo da unidade.")
            return

        if not nome_da_unidade:
            messagebox.showwarning("Atenção", "Informe o nome da unidade.")
            return

        if not telefone:
            messagebox.showwarning("Atenção", "Informe o telefone.")
            return

        try:
            with get_connection() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO configuracao_unidades
                    (
                        prefixo,
                        nome_da_unidade,
                        telefone
                    )
                    VALUES (?, ?, ?)
                    """,
                    (prefixo, nome_da_unidade, telefone,),
                )

            messagebox.showinfo("Sucesso", "Contato salvo com sucesso!")
            self.clear_form()
            self.load_contacts()

        except Exception as error:
            messagebox.showerror("Erro", f"Não foi possível salvar o contato:\n\n{error}")


    # =========================================================
    # SELECIONAR CONTATO
    # =========================================================

    def select_contact(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item.get("values", [])

        if len(values) != 3:
            return

        prefixo = values[0]
        nome_da_unidade = values[1]
        telefone = values[2]

        self.prefixo.delete(0, tk.END)
        self.prefixo.insert(0, prefixo)

        self.nome_da_unidade.delete(0, tk.END)
        self.nome_da_unidade.insert(0, nome_da_unidade)

        self.telefone.delete(0, tk.END)
        self.telefone.insert(0, telefone)


    # =========================================================
    # EXCLUIR CONTATO
    # =========================================================

    def delete_contact(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Atenção", "Selecione um contato para excluir.")
            return

        item = self.tree.item(selected[0])
        values = item.get("values", [])

        if not values:
            return

        prefixo = values[0]
        nome = values[1]

        confirmation = messagebox.askyesno(
            "Confirmar exclusão",
            (
                "Deseja realmente excluir este contato?\n\n"
                f"Prefixo: {prefixo}\n"
                f"Unidade: {nome}"
            ),
        )

        if not confirmation:
            return

        try:
            with get_connection() as conn:
                conn.execute(
                    """
                    DELETE FROM configuracao_unidades
                    WHERE prefixo = ?
                    """,
                    (prefixo,),
                )

            messagebox.showinfo("Sucesso", "Contato excluído.")
            self.clear_form()
            self.load_contacts()

        except Exception as error:
            messagebox.showerror("Erro", f"Não foi possível excluir o contato:\n\n{error}")


    # =========================================================
    # LIMPAR FORMULÁRIO
    # =========================================================

    def clear_form(self):

        self.prefixo.delete(0, tk.END)
        self.nome_da_unidade.delete(0, tk.END)
        self.telefone.delete(0, tk.END)
        self.prefixo.focus()