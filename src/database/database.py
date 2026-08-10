from __future__ import annotations

import sqlite3

from utils.paths import DATABASE_PATH

def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    return sqlite3.connect(
        DATABASE_PATH
    )

def initialize_database() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS configuracao_unidades (
                prefixo TEXT PRIMARY KEY,
                nome_da_unidade TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS contratos_notificados (
                numero_pncp TEXT PRIMARY KEY,
                data_ultima_atualizacao TEXT
            )
        """)

        # NOVA TABELA PARA GUARDAR O TELEFONE DO COMANDANTE E OUTRAS CONFIGURAÇÕES
        conn.execute("""
            CREATE TABLE IF NOT EXISTS configuracoes_gerais (
                chave TEXT PRIMARY KEY,
                valor TEXT NOT NULL
            )
        """)