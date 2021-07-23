import sqlite3


def logger(statement):
    print(f"""
--------------------------------------------------------------------1
Executing: 

{statement}
--------------------------------------------------------------------2
""")


class Database:
    def __init__(self, path_to_db="data/main.db"):
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

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id int NOT NULL,
        name varchar(255) NOT NULL,
        instagram_akk varchar(255),
        balance int,
        done_posts varchar,
        my_tasks varchar,
        ref_id int,
        last_activity varchar(255),
        PRIMARY KEY (id)
        );
        """
        self.execute(sql, commit=True)

    def add_user(self, id: int, name: str, instagram_akk: str = None, balance: int = 0, done_posts: str = '1:2', my_tasks: str = '', ref_id: int = None, last_activity: str = None):
        result = self.select_user(id=id)
        if result is not None:
            print('Пользователь уже существует')
            return

        sql = "INSERT INTO Users(id, name, instagram_akk, balance, done_posts, my_tasks, ref_id, last_activity) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
        parameters = (id, name, instagram_akk, balance, done_posts, my_tasks, ref_id, last_activity)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_users(self):
        sql = 'SELECT * FROM Users'
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' AND '.join([
            f"{item} = ?" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_user(self, **kwargs):
        # '''возвращает одного пользователя'''
        sql = 'SELECT * FROM Users WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_instagram_akk(self, id: int, instagram_akk: str):
        result = self.select_user(id=id)
        if result is None:
            print('Пользователя не существует, проверьте правильность id')
            return

        sql = "UPDATE Users SET instagram_akk=? WHERE id=?"
        self.execute(sql, parameters=(instagram_akk, id), commit=True)

    def update_user_balance(self, id: int, balance: int):
        result = self.select_user(id=id)
        if result is None:
            print('Пользователя не существует, проверьте правильность id')
            return

        sql = "UPDATE Users SET balance=? WHERE id=?"
        self.execute(sql, parameters=(balance, id), commit=True)

    def delete_all_users(self, confirm=False):
        if confirm:
            self.execute("DELETE FROM Users WHERE True", commit=True)

    def update_user_balance_with_const(self, id: int, change_to: int):
        result = self.select_user(id=id)
        if result is None:
            print('Пользователя не существует, обновить id невозможно!')
            return
        balance = result[3]
        balance = int(balance) + int(change_to)

        sql = "UPDATE Users SET balance=? WHERE id=?"
        self.execute(sql, parameters=(balance, id), commit=True)

    def update_user_last_activity(self, id: int, last_activity: str):
        result = self.select_user(id=id)
        if result is None:
            print('Пользователя не существует, проверьте правильность id')
            return

        sql = "UPDATE Users SET last_activity=? WHERE id=?"
        self.execute(sql, parameters=(last_activity, id), commit=True)

    def add_task_to_user_tasks(self, id: int, task):
        result = self.select_user(id=id)
        if result is None:
            print('Пользователя не существует, проверьте правильность id')
            return

        sql = "UPDATE Users SET my_tasks=? WHERE id=?"

        if result[5] == '' or result[5] is None:
            posts = result[5] + str(task)
        else:
            posts = result[5] + ':' + str(task)

        self.execute(sql, parameters=(posts, id), commit=True)


    def set_new_user_tasks(self, id: int, tasks):
        result = self.select_user(id=id)
        if result is None:
            print('Пользователя не существует, проверьте правильность id')
            return

        sql = "UPDATE Users SET my_tasks=? WHERE id=?"

        posts = tasks

        self.execute(sql, parameters=(posts, id), commit=True)

    def update_done_tasks(self, id: int, task_id: int):
        result = self.select_user(id=id)
        if result is None:
            print('Задания не существует, проверьте правильность id')
            return

        done_posts = result[4]
        if str(task_id) in done_posts.split(':'):
            return

        done_posts = done_posts + ':' + str(task_id)

        sql = "UPDATE Users SET done_posts=? WHERE id=?"
        self.execute(sql, parameters=(done_posts, id), commit=True)