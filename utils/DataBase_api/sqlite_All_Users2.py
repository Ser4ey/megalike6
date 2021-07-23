import sqlite3
import data.config


def logger(statement):
    print(f"""
--------------------------------------------------------------------1
Executing: 

{statement}
--------------------------------------------------------------------2
""")


class DatabaseAllActiveUsers:
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

    def create_table_of_Active_Users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS All_Active_Users (
        telegram_id int NOT NULL,
        instagram_account_name varchar(255),
        phone_number varchar(255),
        registration_date varchar(255),
        doing_task_history varchar,
        available_links_for_today int NOT NULL,
        number_of_links_requested_today int NOT NULL,
        common_day_link_limit int NOT NULL,
        vip_status varchar(255),
        vip_bought_date varchar(255),
        special_vip_links_number int NOT NULL,
        deadline_of_common_vip varchar(255),

        PRIMARY KEY (telegram_id)
        );
        """
        self.execute(sql, commit=True)

    def add_active_User(self, telegram_id, instagram_account_name, phone_number, registration_date, doing_task_history, available_links_for_today, number_of_links_requested_today, common_day_link_limit, vip_status, vip_bought_date, special_vip_links_number, deadline_of_common_vip):
        telegram_id = int(telegram_id)
        instagram_account_name = str(instagram_account_name)
        phone_number = str(phone_number)
        registration_date = str(registration_date)
        doing_task_history = str(doing_task_history)
        available_links_for_today = int(available_links_for_today)
        number_of_links_requested_today = int(number_of_links_requested_today)
        common_day_link_limit = int(common_day_link_limit)
        vip_status = str(vip_status)
        vip_bought_date = str(vip_bought_date)
        special_vip_links_number = int(special_vip_links_number)
        deadline_of_common_vip = str(deadline_of_common_vip)

        result = self.select_active_User(telegram_id=telegram_id)
        if result is not None:
            print('Пользователь уже существует, его нельзя добавить!')
            return

        sql = "INSERT INTO All_Active_Users(telegram_id, instagram_account_name, phone_number, registration_date, doing_task_history, available_links_for_today, number_of_links_requested_today, common_day_link_limit, vip_status, vip_bought_date, special_vip_links_number, deadline_of_common_vip) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        parameters = (telegram_id, instagram_account_name, phone_number, registration_date, doing_task_history, available_links_for_today, number_of_links_requested_today, common_day_link_limit, vip_status, vip_bought_date, special_vip_links_number, deadline_of_common_vip)
        self.execute(sql, parameters=parameters, commit=True)

    def delete_active_User_by_instagram_account_name(self, instagram_account_name):
        sql = "DELETE FROM All_Active_Users WHERE instagram_account_name=?"
        parameters = (instagram_account_name,)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_active_Users(self):
        sql = 'SELECT * FROM All_Active_Users'
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
        sql = 'SELECT * FROM All_Active_Users WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def count_active_Users(self):
        return self.execute("SELECT COUNT(*) FROM All_Active_Users;", fetchone=True)

    def update_any_info_about_any_active_User(self, instagram_account_name, thing_to_change, new_data):
        result = self.select_active_User(instagram_account_name=instagram_account_name)
        if result is None:
            print('Пользователя не существует, проверьте правильность id')
            return 'Пользователя не существует, проверьте правильность id'

        sql = f"UPDATE All_Active_Users SET {thing_to_change}=? WHERE instagram_account_name=?"
        self.execute(sql, parameters=(new_data, instagram_account_name), commit=True)


class DatabaseOfHistoryOfUsers:
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

    def create_table_of_History_of_Users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS History_of_Users (
        telegram_id int NOT NULL,
        instagram_account_name varchar(255),
        registration_date varchar(255),
        delete_date varchar(255),

        PRIMARY KEY (telegram_id)
        );
        """
        self.execute(sql, commit=True)

    def add_history_User(self, telegram_id, instagram_account_name, registration_date):
        telegram_id = int(telegram_id)
        instagram_account_name = str(instagram_account_name)
        registration_date = str(registration_date)
        delete_date = 'Not-deleted'

        result = self.select_history_User(telegram_id=telegram_id)
        if result is not None:
            print('Пользователь уже существует, его нельзя добавить!')
            return 'Пользователь уже существует, его нельзя добавить!'

        sql = "INSERT INTO History_of_Users(telegram_id, instagram_account_name, registration_date, delete_date) VALUES(?, ?, ?, ?)"
        parameters = (telegram_id, instagram_account_name, registration_date, delete_date)
        self.execute(sql, parameters=parameters, commit=True)


    def select_all_history_Users(self):
        sql = 'SELECT * FROM History_of_Users'
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' AND '.join([
            f"{item} = ?" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_history_User(self, **kwargs):
        # '''возвращает одного пользователя'''
        sql = 'SELECT * FROM History_of_Users WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def count_active_Users(self):
        return self.execute("SELECT COUNT(*) FROM History_of_Users;", fetchone=True)


    def update_delete_date_of_history_User(self, instagram_account_name, new_delete_date):
        result = self.select_history_User(instagram_account_name=instagram_account_name)
        if result is None:
            print('Пользователя не существует, проверьте правильность id')
            return 'Пользователя не существует, проверьте правильность id'

        sql = f"UPDATE History_of_Users SET delete_date=? WHERE instagram_account_name=?"
        self.execute(sql, parameters=(new_delete_date, instagram_account_name), commit=True)


    def update_any_info_about_any_history_User(self, instagram_account_name, thing_to_change, new_data):
        result = self.select_history_User(instagram_account_name=instagram_account_name)
        if result is None:
            print('Пользователя не существует, проверьте правильность id')
            return 'Пользователя не существует, проверьте правильность id'

        sql = f"UPDATE History_of_Users SET {thing_to_change}=? WHERE instagram_account_name=?"
        self.execute(sql, parameters=(new_data, instagram_account_name), commit=True)



u = DatabaseOfHistoryOfUsers()
u.create_table_of_History_of_Users()
u.update_delete_date_of_history_User('@povar', '12-222-333')
r = u.select_all_history_Users()
print(r)