import re
from explain_terms import TERM_EXPLANATIONS


def load_plan(path: str) -> str:
    """
    Загружает текст плана выполнения из файла.

    :param path: путь к файлу
    :return: строка с планом
    """
    # читаем текст плана из файла
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def find_operations(plan_text: str) -> list[str]:
    """
    Ищет операции (Seq Scan, Hash Join и т.д.) в плане.

    :param plan_text: текст плана выполнения
    :return: список найденных операций
    """
    found = []

    # ищем названия операций в тексте плана
    for term in TERM_EXPLANATIONS:
        if term in plan_text:
            found.append(term)

    return found


# шаблоны для поиска таблиц
TABLE_PATTERNS = [
    r"Seq Scan on ([A-Za-z_][A-Za-z0-9_]*)",
    r"Index Scan using [A-Za-z_][A-Za-z0-9_]* on ([A-Za-z_][A-Za-z0-9_]*)",
    r"Index Only Scan using [A-Za-z_][A-Za-z0-9_]* on ([A-Za-z_][A-Za-z0-9_]*)",
]

# шаблон для поиска cost
COST_PATTERN = r"cost=([0-9.]+)\.\.([0-9.]+)"


def find_tables(plan_text: str) -> list[str]:
    """
    Находит названия таблиц, участвующих в плане.

    :param plan_text: текст плана выполнения
    :return: список таблиц без повторений
    """
    tables = []

    for pattern in TABLE_PATTERNS:
        matches = re.findall(pattern, plan_text)
        for match in matches:
            # добавляем только уникальные таблицы
            if match not in tables:
                tables.append(match)

    return tables


def find_costs(plan_text: str) -> list[tuple[str, str]]:
    """
    Извлекает значения cost из плана выполнения.

    :param plan_text: текст плана
    :return: список пар (start_cost, end_cost)
    """
    return re.findall(COST_PATTERN, plan_text)
