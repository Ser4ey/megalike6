import sqlite3
import data.config


def logger(statement):
    print(f"""
--------------------------------------------------------------------1
Executing: 

{statement}
--------------------------------------------------------------------2
""")


class DatabaseOfDayTasks:
    def __init__(self, path_to_db=data.config.absolute_path_to_Users_database):
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

    def create_table_of_Day_Tasks(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Day_Tasks (
        instagram_link varchar(255),
        creator_telegram_id int NOT NULL,
        task_status varchar(255),
        created_time varchar(255),
        comment_to_task varchar(255),
        telegram_id_of_users_who_request_this_task varchar,

        PRIMARY KEY (instagram_link)
        );
        """
        self.execute(sql, commit=True)

    def add_Day_Task(self, instagram_link, creator_telegram_id, task_status, created_time, comment_to_task, telegram_id_of_users_who_request_this_task):
        instagram_link = s

        result = self.select_active_User(telegram_id=telegram_id)
        if result is not None:
            print('Пользователь уже существует, его нельзя добавить!')
            return

        sql = "INSERT INTO Day_Tasks(telegram_id, instagram_account_name, phone_number, registration_date, doing_task_history, available_links_for_today, number_of_links_requested_today, common_day_link_limit, vip_status, vip_bought_date, special_vip_links_number, deadline_of_common_vip) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        parameters = (telegram_id, instagram_account_name, phone_number, registration_date, doing_task_history, available_links_for_today, number_of_links_requested_today, common_day_link_limit, vip_status, vip_bought_date, special_vip_links_number, deadline_of_common_vip)
        self.execute(sql, parameters=parameters, commit=True)

    def delete_active_User_by_instagram_account_name(self, instagram_account_name):
        sql = "DELETE FROM Day_Tasks WHERE instagram_account_name=?"
        parameters = (instagram_account_name,)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_active_Users(self):
        sql = 'SELECT * FROM Day_Tasks'
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' AND '.join([
            f"{item} = ?" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_active_User(self, **kwargs):
        # '''возвращает одного пользователя'''
        sql = 'SELECT * FROM Day_Tasks WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def count_active_Users(self):
        return self.execute("SELECT COUNT(*) FROM Day_Tasks;", fetchone=True)

    def update_any_info_about_any_active_User(self, instagram_account_name, thing_to_change, new_data):
        result = self.select_active_User(instagram_account_name=instagram_account_name)
        if result is None:
            print('Пользователя не существует, проверьте правильность id')
            return 'Пользователя не существует, проверьте правильность id'

        sql = f"UPDATE All_Active_Users SET {thing_to_change}=? WHERE instagram_account_name=?"
        self.execute(sql, parameters=(new_data, instagram_account_name), commit=True)

    def delete_all_id(self, confirm=False):
        if confirm:
            self.execute("DELETE FROM Gen_id WHERE True", commit=True)



u = DatabaseOfDayTasks()
u.create_table_of_Day_Tasks()

