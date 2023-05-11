import sqlite3, flask, math, time
import os


class Database:
    def __init__(self, db):

        self.__db = db
        self.__cur = db.cursor()

    def addUser(self, dict_values):

        sql = '''INSERT INTO Users (nickname, password, email, creation_date, country_id) 
                 VALUES (:nickname, :password, :email , date('now'), :country);'''
        try:
            self.__cur.execute(sql, dict_values)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка " + str(e))
            return False

    def CheckUser(self, email):
        sql = "SELECT EXISTS (SELECT email FROM users WHERE email LIKE :email LIMIT 1)"
        try:
            self.__cur.execute(sql, (email,))
            res = self.__cur.fetchone()
            if not res[0]:
                print("Пользователь не найден")
                return False
            return True
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

    def getUser(self, user_id):
        sql = ''' SELECT * FROM Users WHERE user_id = :user_id LIMIT 1 '''
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

    def getCountries(self):
        sql = '''SELECT * FROM countries;'''
        try:
            self.__cur.execute(sql)
            fromdb = self.__cur.fetchall()
            res = []
            try:
                for i in fromdb:
                    res.append(tuple(i))
            except:
                print("Ошибка парсинга данных")
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addCounties(self):
        sql = '''INSERT INTO Countries (country) VALUES (?);'''
        with open("src/result.txt", "r") as file:
            counties = file.read().split("\n")
        try:
            for c in counties:
                self.__cur.execute(sql, [c])
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка " + str(e))
            return False
        return True
