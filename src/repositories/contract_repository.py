from database.database import get_connection


class ContractRepository:

    def was_notified(
        self,
        numero: str,
    ) -> bool:

        with get_connection() as conn:

            cursor = conn.execute(
                """
                SELECT 1
                FROM contratos_notificados
                WHERE numero_pncp = ?
                """,
                (numero,),
            )

            return cursor.fetchone() is not None

    def mark_as_notified(
        self,
        numero: str,
        data_atualizacao: str,
    ) -> None:

        with get_connection() as conn:

            conn.execute(
                """
                INSERT OR REPLACE INTO contratos_notificados
                (
                    numero_pncp,
                    data_ultima_atualizacao
                )
                VALUES (?, ?)
                """,
                (
                    numero,
                    data_atualizacao,
                ),
            )

    def get_phone_by_unit(
        self,
        nome_da_unidade: str,
    ) -> str | None:

        print(
            f"BUSCANDO TELEFONE PARA: "
            f"[{nome_da_unidade}]"
        )

        with get_connection() as conn:

            cursor = conn.execute(
                """
                SELECT telefone
                FROM configuracao_unidades
                WHERE nome_da_unidade = ?
                """,
                (nome_da_unidade,),
            )

            result = cursor.fetchone()

            print(
                f"RESULTADO BANCO: {result}"
            )

            if result:
                return result[0]

            return None