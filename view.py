from flask import render_template, url_for, redirect, session, request
from app import app
from pg import PgConnect, PgRequest, products
from config import DB

cats = products.select_categories()
cats_submenu = dict((category.get('name'), category.get('link') )for category in products.select_categories())



menu = {
	'Каталог товаров':cats_submenu,
	'Связаться с нами':'index',
	'Достава и разгрузка':'index',
	'Ваша корзина':'index',
	}


  
  
@app.route('/')
def index():
	list_products = products.select_4_for_category()

	return render_template('index.html', title='Наш ассортимент', menu=menu, cats=cats, \
			products=list_products)


@app.route('/category/<cat>')
def category(cat):
	list_products = products.select_product_for_cat(category_link=cat)
	category_info = products.cat_info(category_link=cat)
	

	return render_template('category.html', title='Категория товаров',menu=menu, cat=category_info[0], \
							products=list_products)


@app.route('/product/<link>')
def get_product(link):
	try:
		product_info = products.product_for_link(link)[0]
	except:
		product_info = False

	if product_info:
		product_title = product_info.get("product_name")
	else:
		product_title = False

	return render_template('product.html', title=product_title, menu=menu, \
			products=product_info)


@app.route('/to_bag', methods=['POST'])
def add_to_bag():
	if request.form.get('add'):
		return f"order coll = {request.form.get('coll')} id = {request.form.get('product_id')}"
	elif request.form.get('buy'):
		return f"now coll = {request.form.get('coll')} id = {request.form.get('product_id')}"