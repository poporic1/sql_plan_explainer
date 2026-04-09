from explain_terms import TERM_EXPLANATIONS


def estimate_risk(operations: list[str], costs: list[tuple[str, str]]) -> str:
    """
    Оценивает "риск" плана выполнения на основе операций и cost.

    :param operations: список операций (Seq Scan, Join и т.д.)
    :param costs: список cost значений
    :return: уровень риска (LOW / MEDIUM / HIGH)
    """
    max_cost = 0.0

    # ищем максимальный cost
    for start_cost, end_cost in costs:
        try:
            max_cost = max(max_cost, float(end_cost))
        except ValueError:
            pass

    # если в плане сразу несколько тяжелых операций
    if (
        "Seq Scan" in operations
        and "Sort" in operations
        and "Nested Loop" in operations
    ):
        return "HIGH"

    if "Hash Join" in operations and max_cost > 2000:
        return "HIGH"

    if "Hash Join" in operations and max_cost > 1000:
        return "MEDIUM"

    if (
        "Seq Scan" in operations
        and "Sort" not in operations
        and "Hash Join" not in operations
        and "Nested Loop" not in operations
    ):
        return "MEDIUM"

    # индекс обычно означает более хороший план
    if "Index Scan" in operations or "Index Only Scan" in operations:
        return "LOW"

    return "MEDIUM"


def build_recommendations(operations: list[str], tables: list[str]) -> list[str]:
    """
    Формирует простые рекомендации по оптимизации запроса.

    :param operations: список операций
    :param tables: список таблиц
    :return: список текстовых рекомендаций
    """
    recommendations = []

    if "Seq Scan" in operations:
        if tables:
            recommendations.append(f"Проверь размер таблицы {tables[0]}.")
        recommendations.append("Посмотри, точно ли нужно читать почти всю таблицу.")

    if "Sort" in operations:
        recommendations.append("Проверь, нужна ли здесь сортировка.")

    if "Hash Join" in operations:
        recommendations.append("Посмотри, какой объем данных участвует в JOIN.")

    if "Nested Loop" in operations:
        recommendations.append(
            "Проверь, не слишком ли много строк соединяется через Nested Loop."
        )

    if "Index Scan" in operations or "Index Only Scan" in operations:
        recommendations.append("Индекс используется, это хороший признак.")

    if not recommendations:
        recommendations.append("Нужно посмотреть план вручную.")

    return recommendations


def build_markdown_report(
    plan_name: str,
    operations: list[str],
    tables: list[str],
    costs: list[tuple[str, str]],
) -> str:
    """
    Собирает markdown-отчет по плану выполнения.

    :param plan_name: имя запроса/файла
    :param operations: найденные операции
    :param tables: найденные таблицы
    :param costs: значения cost
    :return: строка с markdown отчетом
    """
    risk = estimate_risk(operations, costs)
    recommendations = build_recommendations(operations, tables)

    lines = []
    lines.append(f"# Разбор плана: {plan_name}")
    lines.append("")

    lines.append("## Найденные операции")
    if operations:
        for op in operations:
            lines.append(f"- {op}")
    else:
        lines.append("- Операции не найдены")
    lines.append("")

    lines.append("## Что означают операции")
    if operations:
        for op in operations:
            explanation = TERM_EXPLANATIONS.get(op, "Нет пояснения")
            lines.append(f"- {op}: {explanation}")
    else:
        lines.append("- Нет данных")
    lines.append("")

    lines.append("## Таблицы")
    if tables:
        for table in tables:
            lines.append(f"- {table}")
    else:
        lines.append("- Таблицы не найдены")
    lines.append("")

    lines.append("## Cost")
    if costs:
        for start_cost, end_cost in costs:
            lines.append(f"- {start_cost}..{end_cost}")
    else:
        lines.append("- Cost не найден")
    lines.append("")

    lines.append("## Оценка риска")
    lines.append(f"- {risk}")
    lines.append("")

    lines.append("## Что стоит проверить")
    for rec in recommendations:
        lines.append(f"- {rec}")

    return "\n".join(lines)
