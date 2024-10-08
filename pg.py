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

def datetime_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #return datetime.now().strftime('%d-%m-%Y %H:%M:%S')

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


    def execute(self, request, params=None):
        with self.__db as conn:
            with conn.cursor() as cur:
                cur.execute(request, params)
                return cur.fetchone()[0]



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
    
    def select_loaders(self):
        return self.__request.selectd("SELECT * FROM load_price ORDER BY order_num DESC;")
    

    def select_delivery(self):
        return self.__request.selectd("SELECT * FROM delivery_price ORDER BY order_num;")


    

    def new_order(self, 
                  session_id=None, 
                  ip_address='127.0.0.1',
                  location = None,
                  address = None,
                  full_price = None,
                  phone=None,
                  product_price = None,
                  delivery_price = None,
                  load_price = None,
                  driver_id = None,
                  loader_id = None,
                  order_status='posted'
                  
                  ):
        if str(ip_address.strip()) == "":
            ip_address = '127.0.0.1'
            
        query = """
                    INSERT INTO order_info(session_id, ip_addres, location, address, full_price, 
                                        phone, product_price, delivery_price, load_price, 
                                          driver_id, loader_id, date_time, order_status)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """
        return  self.__request.execute(query,
                                       (session_id, ip_address, location, address,
                                        full_price, phone,  product_price, delivery_price,
                                        load_price,  driver_id, loader_id, 
                                        datetime_now(), order_status))
    

    def products_to_order(self, order_id: int = None, product_lst: list = []):
        query = """INSERT INTO order_products(order_id, product_id, product_name,coll, price, total_price, seller_id) 
                    VALUES"""
        
        products_id = ','.join([str(x.get('product_id')) for x in product_lst])
        
        products = self.__request.selectd(f'SELECT id,seller_id, name FROM product WHERE id IN({products_id})')
        

        for i in product_lst:
            pid = i.get('product_id')
            pdict = next(filter(lambda x: int(x.get('id')) == int(pid), products), {})

            pname = pdict.get('name')
            sid = pdict.get('seller_id')
            if i.get('sale') != '-':
                price = i.get('sale')
            else:
                price = i.get('price')

            query += f"('{order_id}','{pid}', '{pname}', '{i.get('coll')}', '{price}', '{i.get('total')}', '{sid}')"
            if i != product_lst[-1]:
                query +=', '
            else:
                query +=';'
            
        try:
            self.__request.insert(query)
            return True
        except Exception as ex:
            print(ex)
            return False

    
    def delivery_order(self,order_id: int = None, delivery_dict: dict = None, address: str = None):
        delivery_id = delivery_dict.get('value')
        name = delivery_dict.get('name')
        need_ride = delivery_dict.get('need_ride')
        price = delivery_dict.get('price_for_once')
        total_price = delivery_dict.get('total_price')
        weight = delivery_dict.get('total_weight')
        max_weight = delivery_dict.get('max_weight')
        


        try:
            self.__request.insert("""
                INSERT INTO order_delivery (order_id, delivery_id,delivery_name, need_ride, 
                delivery_price, total_price, products_weight, max_weight, delivery_address) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (order_id, delivery_id, name,need_ride,
                    price, total_price, weight, max_weight, address))

            return True
        
        except Exception as ex:
            print(ex)
            return False
        
    def load_order(self, order_id: int =None, order_list: list = None, load_name:str = None):
        query = """INSERT INTO order_loaders(order_id, load_id, load_name, load_weight, 
        coll, price, total_price) VALUES"""

        for i in order_list:
            load_id = i.get('price_id')
            load_name = load_name
            load_weight = i.get('weight')
            coll = i.get('coll')
            price = i.get('price')
            total_price = i.get('total_price')


            query += f"""('{order_id}', '{load_id}', '{load_name}', '{load_weight}', '{coll}', '{price}', '{total_price}')"""
            if i == order_list[-1]:
                query += ';'
            else:
                query +=','


        try:
            self.__request.insert(query)
            return True
        except Exception as ex:
            print(ex)
            return False



class Orders:
    def __init__(self, request: PgRequest):
        self.__request = request


#Для телеграм бота
    def get_orders(self):
        return self.__request.selectd('SELECT * FROM order_info WHERE order_status = %s ORDER BY id;',('posted',))


    def order_status(self, order_id, status='in process'):
        try:
            self.__request.insert("UPDATE order_info SET order_status=%s WHERE id = %s;", (status, order_id))
            return True
        except Exception as ex:
            print(ex)
            return False

    def get_products(self, order_id):
        try:
            return self.__request.selectd("SELECT * FROM order_products WHERE order_id = %s;", (order_id,))
        except Exception as ex:
            print(ex)

    def get_delivery(self, order_id):
        try:
            return self.__request.selectd("SELECT * FROM order_delivery WHERE order_id = %s;", (order_id,))
        except Exception as ex:
            print(ex)

    def get_loaders(self, order_id):
        try:
            return self.__request.selectd("SELECT * FROM order_loaders WHERE order_id = %s;", (order_id,))
        except Exception as ex:
            print(ex)



#Для списка заявок в кабинете пользователя
    def orders_for_user(self, session_id:str = None):
        res =  self.__request.selectd('SELECT * FROM order_info WHERE session_id = %s ORDER BY date_time DESC',(session_id,))
        new_list = []
        for item in res:
            if len(item)>0:
                new_list.append({
                    'id':item.get('id'),
                    'date':item.get('date_time').strftime('%d/%m/%Y'),
                    'time':item.get('date_time').strftime('%H:%M'),
                    'full_price':item.get('full_price'),
                    'product_price':item.get('product_price'),
                    'delivery_price':item.get('delivery_price'),
                    'load_price':item.get('load_price')
                })
        return new_list


    def products_for_orders(self, orders_list:str):
        return self.__request.selectd(f'SELECT * FROM order_products WHERE order_id IN({orders_list})')
    
    def loaders_for_orders(self, orders_list:str):        
        return self.__request.selectd(f'SELECT * FROM order_loaders WHERE order_id IN({orders_list})')
    
    def delivery_for_orders(self, orders_list:str):
        return self.__request.selectd(f'SELECT * FROM order_delivery WHERE order_id IN({orders_list})')
    
        











connect = PgConnect(host=DB.host, port=DB.port, database=DB.database, user=DB.user, password=DB.password)
request_db = PgRequest(connect)

products = Products(request_db)
orders = Orders(request_db)



