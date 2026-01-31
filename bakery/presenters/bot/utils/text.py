from collections.abc import Sequence
from typing import Final

from bakery.application.entities import UNSET, Unset

_EMPTY: Final[str] = ""
UNSET_MARK: Final[str] = "__UNSET__"


def normalize_text(text: str | None) -> str:
    if text == UNSET_MARK:
        return _EMPTY
    return (text or _EMPTY).strip()


def extract_text(value: str | Unset | None) -> str | Unset:
    if isinstance(value, Unset) or value == UNSET_MARK:
        return UNSET
    return normalize_text(value)


def extract_list(value: Sequence[str] | Unset | None) -> list[str] | Unset:
    if isinstance(value, Unset) or value == UNSET_MARK:
        return UNSET
    if value is None:
        return []
    return _normalize_list(value)


def display_text(value: str | Unset | None) -> str:
    if isinstance(value, Unset) or value == UNSET_MARK:
        return _EMPTY
    return normalize_text(value)


def display_list(value: Sequence[str] | Unset | None) -> str:
    if isinstance(value, Unset) or value == UNSET_MARK:
        return _EMPTY
    if value is None:
        return _EMPTY
    if isinstance(value, str):
        return normalize_text(value)
    return ", ".join(_normalize_list(value))


def split_items(value: str | None) -> list[str]:
    if not value:
        return []
    normalized = value.replace(",", "\n")
    return [
        item for item in (normalize_text(v) for v in normalized.splitlines()) if item
    ]


def _normalize_list(value: Sequence[str] | None) -> list[str]:
    if value is None:
        return []
    return [item for item in (normalize_text(v) for v in value) if item]
