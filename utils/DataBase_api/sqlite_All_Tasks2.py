import sqlite3
import time

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
        self.create_table_of_Day_Tasks()

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
        comment_to_task varchar,
        telegram_id_of_users_who_request_this_task varchar,

        PRIMARY KEY (instagram_link)
        );
        """
        self.execute(sql, commit=True)

    def add_Day_Task(self, instagram_link, creator_telegram_id, task_status, created_time, comment_to_task):
        instagram_link = str(instagram_link)
        creator_telegram_id = int(creator_telegram_id)
        task_status = str(task_status)
        created_time = str(created_time)
        comment_to_task = str(comment_to_task)

        # список пользователей, которые запроси задание.
        # Пополняется по мере того, как пользователи запрашивают задания
        telegram_id_of_users_who_request_this_task = '1:2'

        result = self.select_day_Task(instagram_link=instagram_link)
        if result is not None:
            print('Задание с такой ссылкой уже существует, его нельзя добавить!')
            return 'Задание с такой ссылкой уже существует, его нельзя добавить!'

        sql = "INSERT INTO Day_Tasks(instagram_link, creator_telegram_id, task_status, created_time, comment_to_task, telegram_id_of_users_who_request_this_task) VALUES(?, ?, ?, ?, ?, ?)"
        parameters = (instagram_link, creator_telegram_id, task_status, created_time, comment_to_task, telegram_id_of_users_who_request_this_task)
        self.execute(sql, parameters=parameters, commit=True)

    def delete_day_Task_by_instagram_link(self, instagram_link):
        sql = "DELETE FROM Day_Tasks WHERE instagram_link=?"
        parameters = (instagram_link,)
        self.execute(sql, parameters=parameters, commit=True)

    def delete_all_day_Tasks(self, confirm=False):
        if confirm:
            self.execute("DELETE FROM Day_Tasks WHERE True", commit=True)

    def select_all_day_Task(self):
        sql = 'SELECT * FROM Day_Tasks'
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' AND '.join([
            f"{item} = ?" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_day_Task(self, **kwargs):
        # '''возвращает одно дневное задание'''
        sql = 'SELECT * FROM Day_Tasks WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def count_day_Tasks(self):
        return self.execute("SELECT COUNT(*) FROM Day_Tasks;", fetchone=True)

    def update_any_info_about_day_Task_by_instagram_link(self, instagram_link, thing_to_change, new_data):
        result = self.select_day_Task(instagram_link=instagram_link)
        if result is None:
            print('Пользователя не существует, проверьте правильность id')
            return 'Пользователя не существует, проверьте правильность id'

        sql = f"UPDATE Day_Tasks SET {thing_to_change}=? WHERE instagram_link=?"
        self.execute(sql, parameters=(new_data, instagram_link), commit=True)

    @staticmethod
    def return_task_text(url, task_description):
        text = url + '\n' + task_description
        return text


    def give_actual_task_to_User(self, user_telegram_id):
        '''
        Возвращает новое задание для пользователя, которое он ещё не запрашивал.
        + Добавляет телеграм id пользователя в информацию о заданиии,
        таким образом пользователь больше не получит такого задания.
        '''
        all_task = self.select_all_day_Task()
        text_response = 'Сейчас нет доступных заданий'
        task_number = -1
        for i in range(len(all_task)):
            task = all_task[i]
            if user_telegram_id not in task[5]:
                text_response = self.return_task_text(task[0], task[4])
                task_number = i
                break

        if task_number == -1:
            return text_response

        # обновляем информацию о запросах задания
        my_task = all_task[task_number]
        instagram_link = my_task[0]
        telegram_id_of_users_who_request_this_task = my_task[5]

        new_telegram_id_of_users_who_request_this_task = telegram_id_of_users_who_request_this_task + ':' + user_telegram_id
        self.update_any_info_about_day_Task_by_instagram_link(instagram_link=instagram_link,
                                                              thing_to_change='telegram_id_of_users_who_request_this_task',
                                                              new_data=new_telegram_id_of_users_who_request_this_task)

        return text_response


#
# b1 = DatabaseOfDayTasks()
# b1.create_table_of_Day_Tasks()
#
