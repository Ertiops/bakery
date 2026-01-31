from typing import Final

from bakery.application.entities import UNSET, Unset

_EMPTY: Final[str] = ""
UNSET_MARK: Final[str] = "__UNSET__"


def normalize_text(text: str | None) -> str:
    if text == UNSET_MARK:
        return _EMPTY
    return (text or _EMPTY).strip()


def extract_value(value: str | Unset | None) -> str | Unset:
    if isinstance(value, Unset) or value == UNSET_MARK:
        return UNSET
    return normalize_text(value)


def display_text(value: str | Unset | None) -> str:
    if isinstance(value, Unset) or value == UNSET_MARK:
        return _EMPTY
    return normalize_text(value)
