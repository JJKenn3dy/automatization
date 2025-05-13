# utils.py  (можно бросить в ui/common.py — где удобно)
from datetime import datetime, date

FMT_DB   = "%Y-%m-%d"
FMT_HUM  = "%d.%m.%Y"

def to_mysql(s: str) -> str:
    """'12.07.2024' ↦ '2024-07-12'  (или вернёт уже нормализованное)"""
    for f in (FMT_HUM, FMT_DB):
        try:
            return datetime.strptime(s, f).strftime(FMT_DB)
        except ValueError:
            continue
    raise ValueError("Неверный формат даты")

def from_mysql(v) -> str:
    """date | datetime | 'YYYY-MM-DD' ↦ 'dd.MM.yyyy'"""
    if v in (None, ""):           return ""
    if isinstance(v, (date, datetime)):
        return v.strftime(FMT_HUM)
    if isinstance(v, str):
        try:
            return datetime.strptime(v, FMT_DB).strftime(FMT_HUM)
        except ValueError:
            return v        # неизвестно что пришло — оставим как есть