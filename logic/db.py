import os
import sys
import mariadb


def enterData(cur):
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
        autocommit=True)

    cur = conn.cursor()
    # Retrieve Contacts

    cur.execute("""
        CREATE TABLE IF NOT EXISTS License (
            ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name_of_soft TINYINT,
            number_lic TINYTEXT,
            scop_using TEXT,
            fullname TINYTEXT,
            name_apm TEXT,
            date DATE,
            fullname_it TINYTEXT,
            status TINYINT(1)
        )
    """)
    conn.commit()  # Добавь коммит после изменений в БД

    cur.execute("""
            CREATE TABLE IF NOT EXISTS SCZY (
                ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name_of_SCZY TINYINT,
                number_SCZY TINYINT(100),
                date DATE,
                number_license TINYTEXT,
                owner TINYTEXT,
                date_and_number TINYTEXT,
                fullname_owner TINYTEXT,
                additional TEXT,
                note TEXT,
                number_certificate TINYTEXT,
                date_expired DATE,
                remove INT,
                date_number_act INT
            )
        """)
    conn.commit()  # Добавь коммит после изменений в БД

    cur.execute("""
                CREATE TABLE IF NOT EXISTS KeysTable (
                    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    status TINYINT(1),
                    type TINYTEXT,
                    number_soft TINYTEXT,
                    owner TINYTEXT,
                    scope_using TEXT,
                    owner_fullname TINYTEXT,
                    VIP_Critical TINYINT(1),
                    start_date DATE,
                    date_end DATE,
                    expired INT,
                    additional TEXT,
                    number_reques INT,
                    note TEXT
                )
            """)
    conn.commit()  # Добавь коммит после изменений в БД

    cur.execute("""
                        CREATE TABLE IF NOT EXISTS CBR (
                            ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            number TINYTEXT,
                            status TINYINT(1),
                            number_serial TINYTEXT,
                            number_key TINYTEXT,
                            owner TINYTEXT,
                            scope_using TEXT,
                            fullname_owner TINYTEXT,
                            date_start DATE,
                            date_end DATE,
                            expired INT,
                            additional TEXT,
                            note TEXT
                        )
                    """)
    conn.commit()  # Добавь коммит после изменений в БД

    cur.execute("""
                CREATE TABLE IF NOT EXISTS TLS (
                    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    number TINYTEXT,
                    date DATE,
                    scope TINYINT(1),
                    access TINYINT(1),
                    give_ac TINYTEXT,
                    iniciator TINYTEXT,
                    owner_ac TINYTEXT,
                    algorithm TINYINT(1),
                    scope_using TEXT,
                    DNS TEXT,
                    resolution TINYINT(1),
                    additional TEXT
                )
            """)
    conn.commit()  # Добавь коммит после изменений в БД
except mariadb.Error as e:
      print(f"Error connecting to the database: {e}")
      sys.exit(1)

def enter_fio (text):
    try:
        conn = mariadb.connect(
            host="localhost",
            port=3306,
            user="newuser",
            password="852456qaz",
            database="IB",
            autocommit=True)
    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

    cur = conn.cursor()

    insert_movies_query = f"""
    INSERT INTO License (fullname)
    VALUES ('{text}');
    """
    with conn.cursor() as cursor:
        cursor.execute(insert_movies_query)
        conn.commit()







