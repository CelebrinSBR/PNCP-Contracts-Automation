from database.database import get_connection

class SettingsRepository:

    def get_commander_phone(self) -> str | None:
        """Busca o telefone do comandante no banco de dados."""
        with get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT valor
                FROM configuracoes_gerais
                WHERE chave = 'telefone_comandante'
                """
            )
            result = cursor.fetchone()
            
            if result:
                return result[0]
            
            return None

    def update_commander_phone(self, phone: str) -> None:
        """Atualiza ou insere o telefone do comandante no banco de dados."""
        with get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO configuracoes_gerais 
                (chave, valor)
                VALUES (?, ?)
                """,
                ('telefone_comandante', phone),
            )