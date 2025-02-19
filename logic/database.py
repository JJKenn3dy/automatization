import os
import sqlite3


def database(self):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    # Создаем таблицу Лицензии
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS License (
                Application INTEGER PRIMARY KEY,
                Software TEXT NOT NULL,
                License TEXT NOT NULL,
                Scope TEXT NOT NULL,
                Fullname TEXT NOT NULL,
                Name TEXT NOT NULL,
                Date TEXT NOT NULL,
                FullnameIT TEXT NOT NULL,
                Status TEXT NOT NULL
                )
                ''')

    # Создаем таблицу СКЗИ
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS CIPF (
                    Number INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Version TEXT NOT NULL,
                    Date TEXT NOT NULL,
                    NumberRegistr TEXT NOT NULL,
                    Owner TEXT NOT NULL,
                    DateNumber TEXT NOT NULL,
                    FullNameBussiness TEXT NOT NULL,
                    Note TEXT NOT NULL,
                    Additionally TEXT NOT NULL,
                    NumberSert TEXT NOT NULL,
                    DateExpired TEXT NOT NULL,
                    Checpoint1 TEXT NOT NULL,
                    Checpoint2 TEXT NOT NULL
                    )
                    ''')

    # Создаем таблицу УКЭП
    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS EQES (
                        Status TEXT NOT NULL,
                        Type TEXT NOT NULL,
                        Number TEXT NOT NULL,
                        NumberSertif TEXT NOT NULL,
                        OutputOwner TEXT NOT NULL,
                        ScopeUsing TEXT NOT NULL,
                        FullName TEXT NOT NULL,
                        VIPOrNo TEXT NOT NULL,
                        DateStart TEXT NOT NULL,
                        DateExp TEXT NOT NULL,
                        DaysLeft TEXT NOT NULL,
                        Additionally TEXT NOT NULL,
                        NumberAppl TEXT NOT NULL,
                        Note TEXT NOT NULL
                        )
                        
                        ''')

    # Создаем таблицу CBR
    cursor.execute('''
                           CREATE TABLE IF NOT EXISTS CBR (
                           Number INTEGER PRIMARY KEY,
                           Status TEXT NOT NULL,
                           Device TEXT NOT NULL,
                           NumberKey TEXT NOT NULL,
                           Owner TEXT NOT NULL,
                           ScopeUsing TEXT NOT NULL,
                           FullName TEXT NOT NULL,
                           DateStart TEXT NOT NULL,
                           DateExp TEXT NOT NULL,
                           DaysLedr TEXT NOT NULL,
                           Additionally TEXT NOT NULL,
                           Note TEXT NOT NULL
                           )

                           ''')

    # Создаем таблицу TLS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TLS (
        Number INTEGER PRIMARY KEY,
        DateApplic TEXT NOT NULL,
        Scope TEXT NOT NULL,
        Access TEXT NOT NULL,
        Owner TEXT NOT NULL,
        Initiator TEXT NOT NULL,
        OwnerAC TEXT NOT NULL,
        Algorithm TEXT NOT NULL,
        ScopeName TEXT NOT NULL,
        DNS TEXT NOT NULL,
        Resolution TEXT NOT NULL,
        Additionally TEXT NOT NULL
        )

        ''')

    if os.path.exists('my_database.db'):
        try:
            # Начинаем транзакцию
            cursor.execute('BEGIN')

            # Выполняем операции
            cursor.execute('INSERT INTO Users (fullname, fullnameIT) VALUES (?, ?)', ('Петров Пётр Петрович',
                                                                                      'Иван Иванович Петрович '))
            cursor.execute('INSERT INTO Users (fullname, fullnameIT) VALUES (?, ?)', ('Гений Генивочи',
                                                                                      'Захар Якуба'))

            # Подтверждаем изменения
            cursor.execute('COMMIT')

        except:
            # Отменяем транзакцию в случае ошибки
            cursor.execute('ROLLBACK')

    # Закрываем соединение
    connection.commit()
    connection.close()
