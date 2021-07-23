import sqlite3
from utils.DataBase_api.sqlite_tasks import DatabaseTasks
db = DatabaseTasks()


def logger(statement):
    print(f"""
--------------------------------------------------------------------1
Executing: 

{statement}
--------------------------------------------------------------------2
""")


class DatabaseActiveTasks:
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

    def create_table_active_tasks(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Active_Tasks (
        id int NOT NULL,
        src varchar(255) NOT NULL,
        balance int NOT NULL,
        users_which_done_post varchar,
        limit1 int NOT NULL,
        author_comment varchar(1024),
        PRIMARY KEY (id)
        );
        """
        self.execute(sql, commit=True)

    def add_active_task_from_task(self, id: int):
        result = self.select_active_task(id=id)
        if result is not None:
            print('Активное задание уже существует')
            return

        sql = "INSERT INTO Active_Tasks(id, src, balance, users_which_done_post, limit1, author_comment) VALUES(?, ?, ?, ?, ?, ?)"
        task = db.select_task(id=id)
        id, src, balance, users_which_done_post, limit, author_comment = task[0], task[1], task[2], task[4], task[2], task[5]
        parameters = (id, src, balance, users_which_done_post, limit, author_comment)
        if int(balance) > 0:
            self.execute(sql, parameters=parameters, commit=True)

    def add_active_task_from_values(self, id: int, src: str, balance: int, users_which_done_post: str, author_comment: str):
        result = self.select_active_task(id=id)
        if result is not None:
            print('Активное задание уже существует')
            return

        sql = "INSERT INTO Active_Tasks(id, src, balance, users_which_done_post, limit1, author_comment) VALUES(?, ?, ?, ?, ?, ?)"
        limit1 = balance
        parameters = (id, src, balance, users_which_done_post, limit1, author_comment)
        if int(balance) > 0:
            self.execute(sql, parameters=parameters, commit=True)

    def delete_active_task(self, id: int):
        sql = "DELETE FROM Active_Tasks WHERE id=?"
        parameters = (id,)
        self.execute(sql, parameters=parameters, commit=True)

    def update_active_balance(self, id: int, change_to: int):
        result = self.select_active_task(id=id)
        if result is None:
            print('Задания не существует, проверьте правильность id')
            return
        balance = result[2]
        balance = int(balance) + int(change_to)

        sql = "UPDATE Active_Tasks SET balance=? WHERE id=?"
        self.execute(sql, parameters=(balance, id), commit=True)

    def zero_active_balance(self, id):
        result = self.select_active_task(id=id)
        if result is None:
            print('Задания не существует, проверьте правильность id')
            return
        balance = int(result[2])
        if balance < 0:
            balance = 0
        sql = "UPDATE Active_Tasks SET balance=? WHERE id=?"
        self.execute(sql, parameters=(balance, id), commit=True)

    def select_all_active_tasks(self):
        sql = 'SELECT * FROM Active_Tasks'
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' AND '.join([
            f"{item} = ?" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_active_task(self, **kwargs):
        # '''возвращает одного пользователя'''
        sql = 'SELECT * FROM Active_Tasks WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def count_tasks(self):
        return self.execute("SELECT COUNT(*) FROM Active_Tasks;", fetchone=True)

    def update_user_which_done_active_post(self, id: int, user_id: int):
        result = self.select_active_task(id=id)
        if result is None:
            print('Задания не существует, проверьте правильность id')
            return

        users_which_done_post = result[4]
        users_which_done_post = str(users_which_done_post) + ':' + str(user_id)

        sql = "UPDATE Active_Tasks SET users_which_done_post=? WHERE id=?"
        self.execute(sql, parameters=(users_which_done_post, id), commit=True)

    @staticmethod
    def format_done_task(sql, parameters):
        # используется для создания sql команды с нужными параметрами для команды ниже
        posts = parameters.split(':')
        posts = [int(i) for i in posts]

        sql += ' AND '.join([
            f"id != ?" for item in posts
        ])
        return sql, tuple(posts)

    def select_all_active_tasks_which_user_not_done(self, done_posts: str = '1:2'):
        # '''возвращает много заданий'''
        sql = 'SELECT * FROM Active_Tasks WHERE '
        sql, parameters = self.format_done_task(sql, done_posts)
        return self.execute(sql, parameters, fetchall=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def select_active_task_which_user_not_done(self, done_posts: str = '1:2'):
        # '''возвращает одного пользователя'''
        sql = 'SELECT * FROM Active_Tasks WHERE '
        sql, parameters = self.format_done_task(sql, done_posts)
        return self.execute(sql, parameters, fetchone=True)

    def update_active_limit1(self, id: int, change_to: int):
        result = self.select_active_task(id=id)
        if result is None:
            print('Задания не существует, проверьте правильность id')
            return
        limit1 = result[4]
        limit1 = int(limit1) + change_to

        sql = "UPDATE Active_Tasks SET limit1=? WHERE id=?"
        self.execute(sql, parameters=(limit1, id), commit=True)


