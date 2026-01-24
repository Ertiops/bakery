from __future__ import annotations

from collections.abc import Sequence

from bakery.application.constants.common import WEEKDAYS_BASE


def normalize_and_validate_schedule(
    *,
    weekdays: Sequence[int],
    min_days_before: int,
    max_days_in_advance: int,
) -> tuple[tuple[int, ...], int, int]:
    if max_days_in_advance > min_days_before:
        raise ValueError(
            "Некорректный диапазон: max_days_in_advance должен быть <= min_days_before."
        )
    normalized: set[int] = set()
    for wd in weekdays:
        wd0 = wd - 1 if WEEKDAYS_BASE == 1 else wd
        if not 0 <= wd0 <= 6:
            raise ValueError("Дни недели должны быть в диапазоне 1..7.")
        normalized.add(wd)

    weekdays_sorted = tuple(sorted(normalized))
    return weekdays_sorted, min_days_before, max_days_in_advance
