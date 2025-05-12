import os
import sys
import docx
import mariadb


import mariadb, datetime

DB_CFG = dict(
    host="localhost", port=3306, user="newuser",
    password="852456qaz", database="IB", autocommit=True
)

def _conn():
    return mariadb.connect(**DB_CFG)

def create_tables():

    try:
        conn = mariadb.connect(
            host="localhost",
            port=3306,
            user="newuser",
            password="852456qaz",
            database="IB",
            autocommit=True
        )
        cur = conn.cursor()

        table_queries = [
            """
            CREATE TABLE IF NOT EXISTS License (
                ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                number TEXT,
                name_of_soft VARCHAR(100),
                number_lic TEXT,
                scop_using TEXT,
                fullname TEXT,
                name_apm TEXT,
                date DATE,
                fullname_it TEXT,
                status TINYINT(1),
                input_mark TEXT,
                input_date TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS SCZY (
                ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name_of_SCZY VARCHAR(100),
                sczy_type TEXT,
                number_SCZY TEXT,
                date DATE,
                number_license TEXT,
                location TEXT,
                location_TOM_text TEXT,
                owner TEXT,
                date_and_number TEXT,
                contract TEXT,
                fullname_owner TEXT,
                owners TEXT,
                buss_proc TEXT,
                additional TEXT,
                note TEXT,
                number_certificate TEXT,
                date_expired DATE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS KeysTable (
                ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                status TEXT,
                type TEXT,
                cert_serial_le TEXT,
                owner TEXT,
                scope_using TEXT,
                owner_fullname TEXT,
                VIP_Critical TEXT,
                start_date DATE,
                date_end DATE,
                additional TEXT,
                number_request TEXT,
                note TEXT
            )
            """,
            """
        CREATE TABLE IF NOT EXISTS CBR (
                    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    number TEXT,
                    status TEXT,
                    number_serial TEXT,
                    number_key TEXT,
                    owner TEXT,
                    scope_using TEXT,
                    fullname_owner TEXT,
                    date_start DATE,
                    date_end DATE,
                    additional TEXT,
                    note TEXT
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS TLS (
                    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    number TEXT,          -- Номер заявки
                    date DATE,            -- Дата согласования заявки
                    environment TEXT,   -- Среда (тест/продуктив) - кодируется числом
                    access TEXT,    -- Доступ (внешний/внутренний) - кодируется числом
                    issuer TEXT,          -- Выдавший УЦ
                    initiator TEXT,       -- Инициатор
                    owner TEXT,           -- Владелец АС
                    algorithm TEXT, -- Алгоритм (RSA/ГОСТ) - кодируется числом
                    scope TEXT,           -- Область действия / наименование ЭДО
                    DNS TEXT,             -- DNS
                    resolution TEXT,-- резолюция ИБ (уточнение/согласовано/отказано) - кодируется числом
                    note TEXT             -- Примечания
                )
                """,
            """
               CREATE TABLE IF NOT EXISTS keying (
               ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
               number TEXT,
               date DATE,
               status BOOLEAN
               )
               """
            ]

        for query in table_queries:
            cur.execute(query)
            conn.commit()
        conn.close()

    except mariadb.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
        sys.exit(1)


def enter_TLS(
    request_number,  # number
    date_str,        # date
    env,             # (будет записан в scope_using)
    access,          # access
    issuer,          # give_ac
    initiator,       # initiator
    owner,           # owner_ac
    algo,            # algorithm
    scope,           # scope
    dns,             # DNS
    resolution,      # resolution
    note             # additional
):
    """
    Сохраняет данные о TLS-заявке в таблицу TlsTable в правильном порядке:
    (number, date, scope, access, give_ac, initiator, owner_ac, algorithm,
     scope_using, DNS, resolution, additional).

    Параметры:
      request_number: номер (column 'number')
      date_str: дата в формате 'YYYY-MM-DD' (column 'date')
      env: среда (тест/прод), мы используем её как scope_using
      access: внешний/внутренний (column 'access')
      issuer: выдающий УЦ (column 'give_ac')
      initiator: инициатор (column 'initiator')
      owner: владелец АС (column 'owner_ac')
      algo: алгоритм (column 'algorithm')
      scope: область действия (column 'scope')
      dns: DNS (column 'DNS')
      resolution: резолюция ИБ (column 'resolution')
      note: дополнительная информация (column 'additional')
    """

    try:
        conn = mariadb.connect(
            host="localhost",
            port=3306,
            user="newuser",
            password="852456qaz",
            database="IB",
            autocommit=True
        )
        cur = conn.cursor()

        insert_query = """
            INSERT INTO TLS (
                number,
                date,
                environment,
                access,
                issuer,
                initiator,
                owner,
                algorithm,
                scope,
                DNS,
                resolution,
                note
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # ВАЖНО: порядок аргументов строго соответствует порядку столбцов
        cur.execute(insert_query, (
            request_number,  # number
            date_str,  # date
            env,  # (будет записан в scope_using)
            access,  # access
            issuer,  # give_ac
            initiator,  # initiator
            owner,  # owner_ac
            algo,  # algorithm
            scope,  # scope
            dns,  # DNS
            resolution,  # resolution
            note  # additional
        ))

        conn.commit()
        conn.close()

    except mariadb.Error as e:
        print(f"Ошибка вставки записи в TLS: {e}")

def enter_license(enter_number, combobox, enter_key, scope, input_fio_user, name_apm, dateedit, user, status,
                  input_mark, input_date):
    try:
        conn = mariadb.connect(
            host="localhost",
            port=3306,
            user="newuser",
            password="852456qaz",
            database="IB",
            autocommit=True
        )
        cur = conn.cursor()

        insert_query = """
            INSERT INTO License 
                (number, name_of_soft, number_lic, scop_using, fullname, name_apm, date, fullname_it, status, input_mark, input_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cur.execute(insert_query, (
        enter_number, combobox, enter_key, scope, input_fio_user, name_apm, dateedit, user, status, input_mark,
        input_date))

        conn.commit()
        conn.close()
    except mariadb.Error as e:
        print(f"Ошибка вставки записи в License: {e}")

def enter_sczy(name, sczy_type, version, date_, reg_num,
               location, location_tom, from_whom, doc_info,
               contract, owner_fio, owners, buss_proc,
               additional, note, cert_num, date_extra):
    q = """INSERT INTO SCZY
           (name_of_SCZY, sczy_type, number_SCZY, date, number_license,
            location, location_TOM_text, owner, date_and_number, contract,
            fullname_owner, owners, buss_proc, additional, note,
            number_certificate, date_expired)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    with _conn() as c:
        c.cursor().execute(q, (name, sczy_type, version, date_, reg_num,
                               location, location_tom, from_whom, doc_info,
                               contract, owner_fio, owners, buss_proc,
                               additional, note, cert_num, date_extra))
def enter_keys(
    status_cb,
    nositel_type_cb,
    cert_serial_le,
    issuer_cb,
    scope_cb,
    owner_cb,
    vip_cb,
    dateedit_str,
    dateedit2_str,
    additional_cb,
    request_let,
    note_le
):
    try:
        conn = mariadb.connect(
            host="localhost",
            port=3306,
            user="newuser",
            password="852456qaz",
            database="IB",
            autocommit=True
        )
        cur = conn.cursor()

        insert_query = """
            INSERT INTO KeysTable (
                status,
                type,
                cert_serial_le,
                owner,
                scope_using,
                owner_fullname,
                VIP_Critical,
                start_date,
                date_end,
                additional,
                number_request,
                note
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Аргументы должны строго соответствовать порядку столбцов
        cur.execute(insert_query, (
            status_cb,
            nositel_type_cb,
            cert_serial_le,
            issuer_cb,
            scope_cb,
            owner_cb,
            vip_cb,
            dateedit_str,
            dateedit2_str,
            additional_cb,
            request_let,
            note_le
        ))

        conn.commit()
        conn.close()

    except mariadb.Error as e:
        print(f"Ошибка вставки записи в KEYS: {e}")


def enter_CBR(request_le, nositel_cb, nositel_serial_cb, key_number_le, issuer_cb, scope_cb, owner_cb, dateedit_str, dateedit2_str, additional1_le, additional2_le):
    try:
        conn = mariadb.connect(
            host="localhost",
            port=3306,
            user="newuser",
            password="852456qaz",
            database="IB",
            autocommit=True
        )
        cur = conn.cursor()

        insert_query = """
               INSERT INTO CBR (
                   number,
                   status,
                   number_serial,
                   number_key,
                   owner,
                   scope_using,
                   fullname_owner,
                   date_start,
                   date_end,
                   additional,
                   note
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           """

        # Аргументы должны строго соответствовать порядку столбцов
        cur.execute(insert_query, (
            request_le,  # name_of_SCZY
            nositel_cb,  # sczy_type
            nositel_serial_cb,  # number_SCZY
            key_number_le,  # date
            issuer_cb,  # number_license
            scope_cb,  # owner
            owner_cb,  # date_and_number
            dateedit_str,  # fullname_owner
            dateedit2_str,  # note
            additional1_le,  # number_certificate
            additional2_le,  # date_expired
        ))

        conn.commit()
        conn.close()

    except mariadb.Error as e:
        print(f"Ошибка вставки записи в CBR: {e}")





# по ейспейпу назад

