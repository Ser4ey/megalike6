import sqlite3


def logger(statement):
    print(f"""
--------------------------------------------------------------------1
Executing: 

{statement}
--------------------------------------------------------------------2
""")


class DatabaseGenId:
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

    def create_table_gen_id(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Gen_id (
        id int NOT NULL,
        name varchar(255) NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def add_id(self, id: int, name: str = 'id_gen'):
        sql = "INSERT INTO Gen_id(id, name) VALUES(?, ?)"
        parameters = (id, name)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_id(self):
        sql = 'SELECT * FROM Gen_id'
        return self.execute(sql, fetchall=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Gen_id;", fetchone=True)

    def update_id(self, id: int):
        sql = "UPDATE Gen_id SET id=? WHERE name=?"
        name = 'id_gen'
        self.execute(sql, parameters=(id, name), commit=True)

    def delete_all_id(self, confirm=False):
        if confirm:
            self.execute("DELETE FROM Gen_id WHERE True", commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' AND '.join([
            f"{item} = ?" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_id(self, **kwargs):
        sql = 'SELECT * FROM Gen_id WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def gen_id(self):
        id = self.select_all_id()[0][0]
        self.update_id(id+1)
        return id
