import sqlite3


def logger(statement):
    print(f"""
--------------------------------------------------------------------1
Executing: 

{statement}
--------------------------------------------------------------------2
""")


class DatabaseTasks:
    def __init__(self, path_to_db="data/task.db"):
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

    def create_table_tasks(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Task (
        id int NOT NULL,
        src varchar(255),
        balance int NOT NULL,
        author int NOT NULL,
        users_which_done_post varchar,
        author_comment varchar(1024),
        PRIMARY KEY (id)
        );
        """
        self.execute(sql, commit=True)

    def add_task(self, id: int, src: str, balance: int, author: int, users_which_done_post: str, author_comment: str):
        result = self.select_task(id=id)
        if result is not None:
            print('Задание уже существует, его нельзя добавить!')
            return

        sql = "INSERT INTO Task(id, src, balance, author, users_which_done_post, author_comment) VALUES(?, ?, ?, ?, ?, ?)"
        parameters = (id, src, balance, author, users_which_done_post, author_comment)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_tasks(self):
        sql = 'SELECT * FROM Task'
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' AND '.join([
            f"{item} = ?" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_task(self, **kwargs):
        # '''возвращает одного пользователя'''
        sql = 'SELECT * FROM Task WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def count_tasks(self):
        return self.execute("SELECT COUNT(*) FROM Task;", fetchone=True)

    def update_balance(self, id: int, change_to: int):
        result = self.select_task(id=id)
        if result is None:
            print('Задания не существует, проверьте правильность id')
            return
        balance = result[2]
        balance = balance + change_to

        sql = "UPDATE Task SET balance=? WHERE id=?"
        self.execute(sql, parameters=(balance, id), commit=True)

    def zero_balance(self, id):
        result = self.select_task(id=id)
        if result is None:
            print('Задания не существует, проверьте правильность id')
            return
        balance = result[2]
        if balance < 0:
            balance = 0
        sql = "UPDATE Task SET balance=? WHERE id=?"
        self.execute(sql, parameters=(balance, id), commit=True)

    def update_user_which_done_post(self, id: int, user_id: int):
        result = self.select_task(id=id)
        if result is None:
            print('Задания не существует, проверьте правильность id')
            return

        users_which_done_post = result[4]
        users_which_done_post = users_which_done_post + ':' + str(user_id)

        sql = "UPDATE Task SET users_which_done_post=? WHERE id=?"
        self.execute(sql, parameters=(users_which_done_post, id), commit=True)
