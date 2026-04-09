import psycopg2


def get_plan(sql_text: str) -> str:
    """
    Получает план выполнения SQL-запроса через EXPLAIN.

    :param sql_text: SQL-запрос
    :return: текст плана выполнения (как строка)
    """
    # подключение к базе
    conn = psycopg2.connect(
        host="localhost", port=5432, dbname="mydb", user="postgres", password="1234"
    )

    try:
        with conn.cursor() as cur:
            # получаем план выполнения запроса
            cur.execute("EXPLAIN " + sql_text)

            # забираем результат построчно
            rows = cur.fetchall()

            # собираем план в одну строку с переносами
            return "\n".join(row[0] for row in rows)
    finally:
        # закрываем соединение в любом случае
        conn.close()
