from enum import StrEnum, unique


@unique
class BuildingTitle(StrEnum):
    FORT_DIALOG = "ФОРТ-ДИАЛОГ"
    TZ_FONTAN = "ТЦ ФОНТАН"
    TEST = "ТЕСТ"
