import sqlite3


def logger(statement):
    print(f"""
--------------------------------------------------------------------1
Executing: 

{statement}
--------------------------------------------------------------------2
""")


class Accounts:
    def __init__(self, path_to_db="data/accounts.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()

        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    def create_table_accounts(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Accounts (
        account_name varchar(255) NOT NULL,
        account_password varchar(255) NOT NULL,
        proxy varchar(255) NOT NULL,
        position varchar(255) NOT NULL,
        valid int,
        PRIMARY KEY (account_name)
        );
        """
        self.execute(sql, commit=True)

    def add_account(self, account_name: str, account_password: str, proxy: str, position: str, valid: int = 1):
        result = self.select_account(account_name=account_name)
        if result is not None:
            print(f'Аккаун {account_name} уже существует')
            return

        sql = "INSERT INTO Accounts(account_name, account_password, proxy, position, valid) VALUES(?, ?, ?, ?, ?)"
        parameters = (account_name, account_password, proxy, position, valid)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_accounts(self):
        sql = 'SELECT * FROM Accounts'
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' AND '.join([
            f"{item} = ?" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_account(self, **kwargs):
        # '''возвращает одного пользователя'''
        sql = 'SELECT * FROM Accounts WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def count_accounts(self):
        return self.execute("SELECT COUNT(*) FROM Accounts;", fetchone=True)

    def update_account(self, account_name: str, account_password=None, proxy=None, position=None, valid=None):
        result = self.select_account(account_name=account_name)
        if result is None:
            print('Аккаунта не существует, проверьте правильность account_name')
            return

        if not account_password is None:
            sql = "UPDATE Accounts SET account_password=? WHERE account_name=?"
            self.execute(sql, parameters=(account_password, account_name), commit=True)

        if not proxy is None:
            sql = "UPDATE Accounts SET proxy=? WHERE account_name=?"
            self.execute(sql, parameters=(proxy, account_name), commit=True)

        if not position is None:
            sql = "UPDATE Accounts SET position=? WHERE account_name=?"
            self.execute(sql, parameters=(position, account_name), commit=True)

        if not valid is None:
            sql = "UPDATE Accounts SET valid=? WHERE account_name=?"
            self.execute(sql, parameters=(account_password, account_name), commit=True)

    def delete_all_accounts(self, confirm=False):
        if confirm:
            self.execute("DELETE FROM Accounts WHERE True", commit=True)
