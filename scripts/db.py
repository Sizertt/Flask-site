import mysql.connector


class DB:

    def __init__(self) -> None:
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="building_shop"
        )

    # --- All ---

    def get_all_from_table(self, table_name) -> list:
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM `{table_name}`;")
        return cursor.fetchall()

    # --- Users ---

    # Show
    def get_user_by_id(self, id) -> tuple:
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM `auth` WHERE id = {id};")
        return cursor.fetchone()

    # Delete
    def delete_user_by_id(self, id) -> None:
        cursor = self.db.cursor()
        cursor.execute(f"DELETE FROM `auth` WHERE id = {id};")
        self.db.commit()
        return
    
    def AddUser(self, name, email, hash):
        try:
            print(name, email, hash )
            cursor = self.db.cursor()
            cursor.execute(f"SELECT COUNT('email') as 'count' FROM auth WHERE email LIKE '{email}';")
            res = cursor.fetchone()
            print(res)
            if res[0] > 0:
                print("Пользователь с таким эмаилом существует")
                return True
            cursor.execute(f"INSERT INTO auth (name, email, password_hash , created_at) VALUES('{name}', '{email}', '{hash}', now())") 
            self.db.commit()
        except:
            print("Получилось")
        return []

    def getUser(self, user_id):
        try:
            cursor = self.db.cursor()
            cursor.execute(f"SELECT * FROM auth WHERE id = '{user_id}' LIMIT 1")
            print('Отработало!!!')
            res = cursor.fetchone()
            if not res:
                print("Пользователь не найден!")
                return False
            return res
        except:
            print('Ошибка получения данных из Бд')
            return False

    def getUserByEmail(self , email):
        try:
            cur = self.db.cursor()
            cur.execute(f"SELECT * FROM auth WHERE email = '{email}' LIMIT 1")
            res = cur.fetchall()
            # print(email)
            if  not res:
                print("Пользователь не найден")
                return False
            return res
        except:
            print("Ошибка получения данных из бд!")
            return False