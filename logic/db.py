import os
import sys
import docx
import mariadb


def enterData():
    """Retrieves the list of contacts from the database and prints to stdout"""
    # Initialize Variables
    # List Contacts

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

            doc = docx.Document("output.docx")
            fullText = "\n".join(para.text for para in doc.paragraphs)

            update_query = """
                UPDATE keying
                SET number = ?
                ORDER BY id DESC
                LIMIT 1;
            """
            cur.execute(update_query, (fullText,))
            conn.commit()
            conn.close()

            return fullText
    except mariadb.Error as e:
        print(f"Ошибка обновления ключей: {e}")
        sys.exit(1)


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
                name_of_soft VARCHAR(100),
                number_lic TEXT,
                scop_using TEXT,
                fullname TEXT,
                name_apm TEXT,
                date DATE,
                fullname_it TEXT,
                status TINYINT(1)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS SCZY (
                ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name_of_SCZY VARCHAR(100),
                number_SCZY VARCHAR(100),
                date DATE,
                number_license TEXT,
                owner TEXT,
                date_and_number TEXT,
                fullname_owner TEXT,
                additional TEXT,
                note TEXT,
                number_certificate TEXT,
                date_expired DATE,
                remove INT,
                date_number_act INT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS KeysTable (
                ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                status TINYINT(1),
                type TEXT,
                number_soft TEXT,
                owner TEXT,
                scope_using TEXT,
                owner_fullname TEXT,
                VIP_Critical TINYINT(1),
                start_date DATE,
                date_end DATE,
                expired INT,
                additional TEXT,
                number_request INT,
                note TEXT
            )
            """,
            """
        CREATE TABLE IF NOT EXISTS CBR (
                    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    number TEXT,
                    status TINYINT(1),
                    number_serial TEXT,
                    number_key TEXT,
                    owner TEXT,
                    scope_using TEXT,
                    fullname_owner TEXT,
                    date_start DATE,
                    date_end DATE,
                    expired INT,
                    additional TEXT,
                    note TEXT
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS TLS (
                    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    number TEXT,
                    date DATE,
                    scope TINYINT(1),
                    access TINYINT(1),
                    give_ac TEXT,
                    initiator TEXT,
                    owner_ac TEXT,
                    algorithm TINYINT(1),
                    scope_using TEXT,
                    DNS TEXT,
                    resolution TINYINT(1),
                    additional TEXT
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


def update_license(field, value):
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

        update_query = f"""
        UPDATE License
        SET {field} = ?
        ORDER BY id DESC
        LIMIT 1;
        """
        cur.execute(update_query, (value,))
        conn.commit()
        conn.close()
    except mariadb.Error as e:
        print(f"Ошибка обновления {field} в License: {e}")


def enter_fio(text):
    update_license("fullname", text)


def enter_variant(variant):
    update_license("name_of_soft", variant)


def create_keys_table():
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

        cur.execute("""
            CREATE TABLE IF NOT EXISTS keying (
                ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                number TEXT,
                date DATE
            )
        """)
        conn.commit()
        conn.close()
    except mariadb.Error as e:
        print(f"Ошибка при создании таблицы ключей: {e}")
        sys.exit(1)






