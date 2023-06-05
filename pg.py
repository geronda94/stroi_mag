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






class Products:
    def __init__(self, request: PgRequest):
        self.__request = request

    
    def select_categories(self):
        return self.__request.selectd('SELECT * FROM categories ORDER BY order_num;')

    def select_4_for_category(self):
        return self.__request.selectd("""SELECT
                                        c.id AS category_id,
                                        p.id AS product_id,
                                        p.name AS product_name,
                                        p.ava_link,
                                        p.description,
                                        p.link,
                                        p.seller_id,
                                        p.price,
                                        p.price2,
                                        p.price3,
                                        p.sale_for1,
                                        p.sale_for2,
                                        p.comission,
                                        p.order_num,
                                        p.sold
                                        FROM (
                                        SELECT
                                            cp.category_id,
                                            cp.product_id,
                                            ROW_NUMBER() OVER (PARTITION BY cp.category_id ORDER BY p.order_num) AS row_num
                                        FROM cat_prod cp
                                        JOIN product p ON cp.product_id = p.id
                                        ) AS subquery
                                        JOIN categories c ON subquery.category_id = c.id
                                        JOIN product p ON subquery.product_id = p.id
                                        WHERE subquery.row_num <= 4
                                        ORDER BY c.order_num, subquery.category_id, p.order_num""")





    def select_product_for_cat(self, category_link):
        return self.__request.selectd("""SELECT
                                        c.id AS category_id,
                                        p.id AS product_id,
                                        p.name AS product_name,
                                        p.ava_link,
                                        p.description,
                                        p.link,
                                        p.seller_id,
                                        p.price,
                                        p.price2,
                                        p.price3,
                                        p.sale_for1,
                                        p.sale_for2,
                                        p.comission,
                                        p.order_num,
                                        p.sold
                                    FROM (
                                        SELECT
                                            cp.category_id,
                                            cp.product_id,
                                            ROW_NUMBER() OVER (PARTITION BY cp.category_id ORDER BY p.order_num) AS row_num
                                        FROM cat_prod cp
                                        JOIN product p ON cp.product_id = p.id
                                        JOIN categories c ON cp.category_id = c.id
                                        WHERE c.link = %s
                                    ) AS subquery
                                    JOIN categories c ON subquery.category_id = c.id
                                    JOIN product p ON subquery.product_id = p.id
                                    
                                    ORDER BY c.order_num, subquery.category_id, p.order_num

                                    """,(category_link,))


    def cat_info(self, category_link):
        return self.__request.selectd("SELECT * FROM categories WHERE link = %s;",(category_link,))


    def product_for_link(self, link):
        return self.__request.selectd("""SELECT
                                        c.id AS category_id,
                                        p.id AS product_id,
                                        p.name AS product_name,
                                        p.ava_link,
                                        p.description,
                                        p.link,
                                        p.seller_id,
                                        p.price,
                                        p.price2,
                                        p.price3,
                                        p.sale_for1,
                                        p.sale_for2,
                                        p.comission,
                                        p.order_num,
                                        p.weight,
                                        p.sold
                                    FROM (
                                        SELECT
                                            cp.category_id,
                                            cp.product_id,
                                            ROW_NUMBER() OVER (PARTITION BY cp.category_id ORDER BY p.order_num) AS row_num
                                        FROM cat_prod cp
                                        JOIN product p ON cp.product_id = p.id
                                        JOIN categories c ON cp.category_id = c.id
                                        WHERE p.link = %s
                                    ) AS subquery
                                    JOIN categories c ON subquery.category_id = c.id
                                    JOIN product p ON subquery.product_id = p.id
                                    
                                    ORDER BY c.order_num, subquery.category_id, p.order_num

                                    """,(link,))


    def in_cart(self, lst):
        query = """SELECT
                        c.id AS category_id,
                        p.id AS product_id,
                        p.name AS product_name,
                        p.ava_link,
                        p.link,
                        p.seller_id,
                        p.price,
                        p.price2,
                        p.price3,
                        p.sale_for1,
                        p.sale_for2,
                        p.comission,
                        p.weight,
                        p.sold
                    FROM (
                        SELECT
                            cp.category_id,
                            cp.product_id,
                            ROW_NUMBER() OVER (PARTITION BY cp.category_id ORDER BY p.order_num) AS row_num
                        FROM cat_prod cp
                        JOIN product p ON cp.product_id = p.id
                        JOIN categories c ON cp.category_id = c.id
                        WHERE p.id IN %(ids)s
                    ) AS subquery
                    JOIN categories c ON subquery.category_id = c.id
                    JOIN product p ON subquery.product_id = p.id
                    ORDER BY c.order_num, subquery.category_id, p.order_num
                    """
        params = {'ids': tuple(lst)}
        return self.__request.selectd(query, params)





connect = PgConnect(host=DB.host, port=DB.port, database=DB.database, user=DB.user, password=DB.password)
request_db = PgRequest(connect)
products = Products(request_db)

