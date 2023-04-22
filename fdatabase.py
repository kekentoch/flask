import sqlite3, flask, math, time
import os


class Database:
    def __init__(self, db):

        self.__db = db
        self.__cur = db.cursor()

    def addUser(self, dict_values):

        sql = '''INSERT INTO Users (nickname, password, email, creation_date, country_id) 
                 VALUES (:nickname, :password, :email , date('now'), (SELECT country_id FROM Countries WHERE country=:country LIMIT 1));'''
        try:
            self.__cur.execute(sql, dict_values)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка " + str(e))
            return False

    def getUser(self, user_id):
        sql = ''' SELECT * FROM Users WHERE user_id =:user_id LIMIT 1 '''
        try:
            self.__cur.execute(sql, (user_id,))
            res = tuple(self.__cur.fetchone())
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False

    def getUserByEmail(self, email):
        sql = "SELECT * FROM users WHERE email = :email LIMIT 1"
        try:
            self.__cur.execute(sql, (email,))
            res = tuple(self.__cur.fetchone())
            if not res:
                print("Пользователь не найден")
                return False
            dict = {
                'id': res[0],
                'username': res[1],
                'password': res[2],
                'email': res[3],
                'creation_time': res[4],
                'country_id': res[5]
            }
            return dict
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False

    # def checkUser(self, dict_values):
    #     sql = '''SELECT password FROM Users WHERE email=:email LIMIT 1'''
    #     try:
    #         self.__cur.execute(sql, (dict_values.get('email'),))
    #         res = tuple(self.__cur.fetchone())
    #         if dict_values.get('password') == str(res[0]):
    #             return True
    #     except sqlite3.Error as e:
    #         print("Ошибка " + str(e))
    #         return False
    #     return False

    def getCountries(self):
        sql = '''SELECT country FROM countries;'''
        try:
            self.__cur.execute(sql)
            res = tuple(self.__cur.fetchall())
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addCounties(self):
        sql = '''INSERT INTO Countries (country) VALUES (?);'''
        # sqldel = '''DELETE FROm Countries '''
        # sqlreset = '''DELETE FROM sqlite_sequence where name='Countries';'''
        with open("src/result.txt", "r") as file:
            counties = file.read().split("\n")
        try:
            # self.__cur.execute(sqlreset)
            # self.__cur.execute(sqldel)
            for c in counties:
                self.__cur.execute(sql, [c])
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка " + str(e))
            return False
        return True
