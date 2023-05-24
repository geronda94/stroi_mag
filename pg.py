from datetime import datetime
import re
import psycopg2
from psycopg2 import pool
from config import DB
import math
from flask import url_for
import re


def pagintaion(pages_total, page_current):
        prev = page_current-1
        nextp = page_current +1

        pages_dict = dict()
        if page_current > 1:
            pages_dict.update({f'<': prev})

        for i in range(1, pages_total+1):
            if i in range(page_current-3, page_current)\
                  or i==page_current or i in range(page_current+1, page_current+4):
                pages_dict.update({f'{i}': i})

        if pages_total >= nextp:
            pages_dict.update({'>': nextp})
        
        return pages_dict

def slugify(s):
    return re.sub(r'[^\w+]', '-', s)

def generate_slug(title):
    return str(slugify(title))

def time():
    return datetime.now().strftime('%H:%M:%S')

def today():
    return datetime.now().strftime('%Y-%m-%d')


def refactor_img(text):
    base = url_for('static', filename='html_img/') 
    return re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                  lambda match: f"{match.group('tag')}{base}{match.group('url')}>" if not match.group('url').startswith('http') else match.group(0),
                  text)



class PgConnect:
    def __init__(self, minconn=1, maxconn=10, **kwargs):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn, maxconn, **kwargs)

    def __enter__(self):
        self.conn = self.connection_pool.getconn()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.connection_pool.putconn(self.conn)

    def execute(self, sql, params=None):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()

    def push(self, sql, params=None):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)


class PgRequest:
    def __init__(self, db: PgConnect):
        self.__db = db

    def insert(self, request, params=None):
        with self.__db as conn:
            self.__db.push(request, params)

    def select(self, request, params=None):
        with self.__db as conn:
            return self.__db.execute(request, params)
        
    def selectd(self, request, params=None):
        with self.__db as conn:
            with conn.cursor() as cur:
                cur.execute(request, params)
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]


class Posts:
    def __init__(self, request: PgRequest, table: str):
        self.__request = request
        self.__table = table

    def add_post(self, title, text):
        try:
                       
            self.__request.insert(f"INSERT INTO {self.__table}(title, text, url, time, date) VALUES(%s, %s, %s, %s, %s)",
                 (str(title), refactor_img(text), generate_slug(title), time(), today()))
            return True

        except Exception as ex:
            print(ex)
            return False
        


    def select_all(self):
        return self.__request.selectd(f"SELECT * FROM {self.__table};")
    

    def select_for_url(self, post_url):
        try:
            post = self.__request.selectd(f"SELECT * FROM {self.__table} WHERE url='{post_url}';")[0]
            
            return post
        
        except Exception as ex:
            print(ex)
            return False

    def select_paginate(self, page, pas=5):
        page-=1
        start = page*pas
        total_posts = self.__request.select(f"SELECT COUNT(*) FROM {self.__table};")[0][0]/int(pas)
        data = self.__request.selectd(f"SELECT * FROM {self.__table} ORDER BY id DESC OFFSET {start} LIMIT {pas} ;")
        

        return (data, math.ceil(total_posts))
    


    def search_post(self, request):
        req_list = request.split(' ')
        query = f"SELECT * FROM {self.__table} WHERE "

        for i, word in enumerate(req_list):
            if i != 0:
                query += "AND "
            query += f"(LOWER(title) LIKE LOWER('%{word}%') OR LOWER(text) LIKE LOWER('%{word}%')) "

        query += ";"
        return self.__request.selectd(query)
    
    
    def update_post(self, post_url, title, body):
        try:
            self.__request.insert(f"UPDATE {self.__table} SET title = %s, text = %s WHERE url= %s;",
                                    (str(title), refactor_img(body), post_url))
            return True
        except Exception as ex:
            print(ex)
            return False
        
        
    def del_post(self, post_url):
        try:
            self.__request.insert(f"DELETE FROM {self.__table} WHERE url=%s;", (post_url,))
            return True
        except Exception as ex:
            print(ex)
            return False



class Users:
    def __init__(self, request: PgRequest, table: str):
        self.__request = request
        self.__table = table


    def new_user(self, name, email, psw):
        try:                       
            self.__request.insert(f"INSERT INTO {self.__table}(name, email, psw, time) VALUES(%s, %s, %s, %s)",
                 (name, email,psw, time()))
            return True

        except Exception as ex:
            print(ex)
            return False
        
        
    def check_email(self, email):
        result = self.__request.select('SELECT COUNT(*) FROM users WHERE email = %s;', (email,))
        if result and result[0][0] > 0:
            return True
        else:
            return False
        
        
    def select_user(self, email):
        result = self.__request.selectd('SELECT * FROM users WHERE email = %s LIMIT 1;', (email,))
        if result:
            return result[0]
        else:
            return f'ERROR to extract from DB with email: {email}'


    def get_user(self, user_id):
        return self.__request.selectd('SELECT * FROM users WHERE id = %s LIMIT 1;', (user_id,))[0]


    def UpdateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False
        
        try:
            self.__request.insert("UPDATE users SET avatar = %s WHERE id = %s", (avatar, user_id))
            
        
        except Exception as ex:
            print('Ошибка загрузки аватара')
            return False

        return True
    
    def RemoveUserAva(self, user_id):
        try:
            self.__request.insert("UPDATE users SET avatar = NULL WHERE id = %s", (user_id,))
            return True
        
        except Exception as ex:
            
            return False
        

    def select_paginate(self, page, pas=5):
        page-=1
        start = page*pas
        total_posts = self.__request.select(f"SELECT COUNT(*) FROM {self.__table};")[0][0]/int(pas)
        data = self.__request.selectd(f"SELECT * FROM {self.__table} ORDER BY id DESC OFFSET {start} LIMIT {pas} ;")
        

        return (data, math.ceil(total_posts))








connect = PgConnect(host=DB.host, port=DB.port, database=DB.database, user=DB.user, password=DB.password)
request_db = PgRequest(connect)
posts = Posts(request=request_db, table='posts')
users = Users(request=request_db, table='users')
