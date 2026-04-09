import os
from db_runner import get_plan
from parse_plan import find_operations, find_tables, find_costs
from build_report import build_markdown_report


def load_sql(path: str) -> str:
    """
    Загружает SQL-запрос из файла.

    :param path: путь к .sql файлу
    :return: текст SQL-запроса
    """
    # читаем sql из файла
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def process_query_file(file_path: str, output_dir: str):
    """
    Обрабатывает один SQL-файл:
    получает план, парсит его и сохраняет отчет.

    :param file_path: путь к SQL-файлу
    :param output_dir: папка для сохранения отчета
    """
    # загружаем текст запроса
    sql_text = load_sql(file_path)

    # получаем план выполнения
    plan_text = get_plan(sql_text)

    # вытаскиваем из плана нужные данные
    operations = find_operations(plan_text)
    tables = find_tables(plan_text)
    costs = find_costs(plan_text)

    # собираем итоговый отчет
    report = build_markdown_report(
        plan_name=os.path.basename(file_path),
        operations=operations,
        tables=tables,
        costs=costs,
    )

    # имя итогового файла
    output_file = os.path.join(
        output_dir, os.path.basename(file_path).replace(".sql", "_summary.md")
    )

    # сохраняем отчет
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Готово: {output_file}")


def main():
    """
    Основная функция:
    проходит по всем SQL-файлам и запускает обработку.
    """
    input_dir = "queries"
    output_dir = "output"

    # создаем папку под результаты
    os.makedirs(output_dir, exist_ok=True)

    # обрабатываем все query_*.sql
    for file_name in os.listdir(input_dir):
        if file_name.startswith("query_") and file_name.endswith(".sql"):
            file_path = os.path.join(input_dir, file_name)
            process_query_file(file_path, output_dir)


if __name__ == "__main__":
    main()
