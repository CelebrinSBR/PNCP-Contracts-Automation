from database.database import get_connection


with get_connection() as conn:

    result = conn.execute(
        """
        SELECT *
        FROM configuracao_unidades
        """
    )

    for row in result.fetchall():
        print(row)