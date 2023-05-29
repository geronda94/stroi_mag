from flask import render_template, url_for, redirect, session
from app import app
from pg import PgConnect, PgRequest, products
from config import DB

menu = {
	'Каталог товаров':{
		'Цемент / Песок / Гравий':'index',
		'Клей 333 / Шпаклевка':'index',
		'Декоравтивный Кирпич':'index',
		'Кирпичи / Фортан / Пеноблоки':'index',
		'Печные дверцы / Огнеупорные смеси':'index',
		'Штукарутрная сетка':'index'
		                },
	'Связаться с нами':'index',
	'Достава и разгрузка':'index',
	'Ваши заказы':'index',
	}
  
@app.route('/')
def index():
	cats = products.select_categories()
	list_products = products.select_4_for_category()

	return render_template('index.html', title='Наш ассортимент', menu=menu, cats=cats, \
			products=list_products)


