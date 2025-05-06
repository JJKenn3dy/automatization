import os
from datetime import datetime
from typing import Dict, List, Any

import pandas as pd
import mariadb

# ──────────────────
# ПАРАМЕТРЫ ПОДКЛЮЧЕНИЯ К БД
# ──────────────────
DB_CFG: Dict[str, Any] = dict(
    host="localhost",
    port=3306,
    user="newuser",
    password="852456qaz",
    database="IB",
    autocommit=True,  # автокоммит оставляем включённым – удобно для импорта
)

# ──────────────────
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ──────────────────

def _conn():
    """Единая точка подключения к MariaDB."""
    return mariadb.connect(**DB_CFG)


def convert_date(value):
    """Приведение даты к ISO‑формату YYYY‑MM‑DD или None."""
    if pd.isna(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        for fmt in ("%d.%m.%Y", "%Y-%m-%d"):  # пробуем DD.MM.YYYY, затем ISO
            try:
                return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        # последний шанс – доверяем pandas
        date_obj = pd.to_datetime(value, errors="coerce")
        return None if pd.isna(date_obj) else date_obj.strftime("%Y-%m-%d")
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.strftime("%Y-%m-%d")
    return value


def remove_unwanted_whitespace(cell):
    """Удаляет повторяющиеся/концевые пробелы и невидимые символы."""
    if pd.isna(cell):
        return None
    if isinstance(cell, str):
        return " ".join(cell.split())
    return cell


def filter_existing_rows(
    df: pd.DataFrame,
    table: str,
    key_columns: List[str],
    connection,
) -> pd.DataFrame:
    """Возвращает только новые строки, отсутствующие в *table* по ключу key_columns."""
    if df.empty:
        return df

    cols_sql = ", ".join(key_columns)
    with connection.cursor(dictionary=True) as cur:
        cur.execute(f"SELECT {cols_sql} FROM {table}")
        existing_keys = {
            tuple(row[col] for col in key_columns)
            for row in cur.fetchall()
        }

    df["_key"] = df.apply(lambda r: tuple(r[c] for c in key_columns), axis=1)
    df_new = df.loc[~df["_key"].isin(existing_keys)].drop(columns=["_key"])
    return df_new

# ──────────────────
# ГЛАВНАЯ УНИВЕРСАЛЬНАЯ ФУНКЦИЯ ИМПОРТА
# ──────────────────

def import_excel_to_table(
    excel_file: str,
    table: str,
    column_mapping: Dict[str, str],
    key_columns: List[str],
    date_columns: List[str] | None = None,
):
    """Читает *excel_file*, приводит столбцы к формату таблицы *table* и
    добавляет только уникальные записи (по *key_columns*).

    :param excel_file:   путь к *.xlsx*
    :param table:        таблица назначения (License, SCZY, …)
    :param column_mapping:  Excel‑колонка → колонка БД
    :param key_columns:  колонки‑ключи в БД, определяющие уникальность
    :param date_columns: список колонок, которые нужно привести к ISO‑дат
    """

    if date_columns is None:
        date_columns = []

    if not os.path.exists(excel_file):
        raise FileNotFoundError(excel_file)

    # ── 1. Загружаем Excel и оставляем/переименовываем нужные столбцы ──
    df = pd.read_excel(excel_file, header=0)
    cols_in_xls = set(df.columns)
    cols_needed = [c for c in column_mapping if c in cols_in_xls]
    df = df[cols_needed].rename(columns=column_mapping)

    # ── 2. Приводим даты и чистим пробелы ──
    for col in date_columns:
        if col in df.columns:
            df[col] = df[col].apply(convert_date)
    for col in df.columns:
        df[col] = df[col].apply(remove_unwanted_whitespace)

    # ── 3. Подключаемся к БД и отбрасываем дубликаты ──
    with _conn() as conn:
        df = filter_existing_rows(df, table, key_columns, conn)
        if df.empty:
            print(f"[{table}] новых строк нет – импорт пропущен.")
            return 0

        # ── 4. Массовая вставка ──
        cols_sql = ", ".join(f"`{c}`" for c in df.columns)
        placeholders = ", ".join(["?"] * len(df.columns))
        insert_q = f"INSERT INTO {table} ({cols_sql}) VALUES ({placeholders})"

        # executemany ждёт список кортежей
        payload = [
            tuple(None if pd.isna(v) else v for v in row)
            for row in df.itertuples(index=False, name=None)
        ]
        with conn.cursor() as cur:
            cur.executemany(insert_q, payload)
            print(f"[{table}] добавлено строк: {cur.rowcount}")
        return len(payload)

# ──────────────────
# ОПИСАНИЯ КОЛОНОК ДЛЯ КАЖДОЙ ТАБЛИЦЫ
# ──────────────────

LICENSE_MAPPING = {
    "№ Заявки": "number",
    "Наименование ПО СКЗИ": "name_of_soft",
    "№ лицензии": "number_lic",
    "Область применения / наименование ЭДО": "scop_using",
    "Ф.И.О. пользователя": "fullname",
    "Имя АРМ/IP": "name_apm",
    "Дата установки": "date",
    "Ф.И.О. сотрудника ИТ": "fullname_it",
    "статус": "status",
    "Отметка об изъятии/ уничтожении/ вывода из эксплуатации": "input_mark",
    "Дата, расписка, номер акта об уничтожении": "input_date",
}

SCZY_MAPPING = {
    "Наименование СКЗИ": "name_of_SCZY",
    "Тип ПО/ПАК": "sczy_type",
    "Версия СКЗИ": "number_SCZY",
    "Дата получения": "date",
    "Регистрационный (серийный) номер": "number_license",
    "Местонахождение": "location",
    "Местонахождение ТОМ (текст)": "location_TOM_text",
    "От кого получены": "owner",
    "Дата и номер документа, сопроводительного письма": "date_and_number",
    "Договор": "contract",
    "ФИО владельца, бизнес процесс в рамках которого используется": "fullname_owner",
    "Владельцы": "owners",
    "Бизнес процессы": "buss_proc",
    "Примечание": "additional",
    "Дополнительно": "note",
    "Сертификат": "number_certificate",
    "Срок": "date_expired",
}

KEYS_MAPPING = {
    "Статус да/нет": "status",
    "Носитель (Серийный номер)": "type",
    "Серийный номер сертификата": "cert_serial_le",
    "ФИО владельца": "owner",
    "Область действия / наименование ЭДО": "scope_using",
    "Владелец ключа (ФИО)": "owner_fullname",
    "VIP/ Critical": "VIP_Critical",
    "Срок начала действия": "start_date",
    "Срок окончания действия": "date_end",
    "Дополнительно": "additional",
    "Заявка/номер обращения": "number_request",
    "Примечание": "note",
}

CBR_MAPPING = {
    "Заявка/номер обращения": "number",
    "Осталось дней": "status",
    "Носитель (Серийный номер)": "number_serial",
    "Номер ключа": "number_key",
    "ФИО владельца": "fullname_owner",
    "Выдавший УЦ": "owner",
    "Область действия / наименование ЭДО": "scope_using",
    "Срок начала действия": "date_start",
    "Срок окончания действия": "date_end",
    "Дополнительно": "additional",
    "Примечание": "note",
}

TLS_MAPPING = {
    "номер заявки": "number",
    "Дата согласования заявки": "date",
    "Среда": "environment",
    "Доступ": "access",
    "Выдавший УЦ": "issuer",
    "Инициатор": "initiator",
    "Владелец АС": "owner",
    "тип сертификата": "algorithm",
    "Область действия / наименование ЭДО": "scope",
    "Сервис": "DNS",
    "резолюция ИБ": "resolution",
    "примечание (описание)": "note",
}

# ──────────────────
# ПРИМЕР ИСПОЛЬЗОВАНИЯ (можно вызвать из GUI, скрипта, etc.)
# ──────────────────
if __name__ == "__main__":
    # 1. Лицензии
    import_excel_to_table(
        excel_file="Лицензии.xlsx",
        table="License",
        column_mapping=LICENSE_MAPPING,
        key_columns=["number_lic", "name_of_soft"],
        date_columns=["date"],
    )

    # 2. СКЗИ
    import_excel_to_table(
        excel_file="СКЗИ.xlsx",
        table="SCZY",
        column_mapping=SCZY_MAPPING,
        key_columns=["number_license"],
        date_columns=["date", "date_expired"],
    )

    # 3. Ключи (УКЭП)
    import_excel_to_table(
        excel_file="УКЭП.xlsx",
        table="KeysTable",
        column_mapping=KEYS_MAPPING,
        key_columns=["cert_serial_le"],
        date_columns=["start_date", "date_end"],
    )

    # 4. CBR
    import_excel_to_table(
        excel_file="CBR.xlsx",
        table="CBR",
        column_mapping=CBR_MAPPING,
        key_columns=["number_serial", "number_key"],
        date_columns=["date_start", "date_end"],
    )

    # 5. TLS
    import_excel_to_table(
        excel_file="TLS.xlsx",
        table="TLS",
        column_mapping=TLS_MAPPING,
        key_columns=["number", "DNS"],
        date_columns=["date"],
    )
