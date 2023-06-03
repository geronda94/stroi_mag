from flask import render_template, url_for, redirect, session, request,flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from app import app
from pg import PgConnect, PgRequest, products
from config import DB
import uuid
from func import return_next, coll_to_int



cats = products.select_categories()
cats_submenu = dict((category.get('name'), category.get('link') )for category in products.select_categories())





menu = {
	'Каталог товаров':cats_submenu,
	'Связаться с нами':'index',
	'Достава и разгрузка':'index',
	'Ваша корзина':'get_bag',
	}


  
  
@app.route('/')
def index():
	list_products = products.select_4_for_category()

	return render_template('index.html', title='Стройматериалы в Тирасполе и ПМР', menu=menu, cats=cats, \
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
	user_agent = request.headers.get('User-Agent')
	real_ip = request.headers.get('X-Forwarded-For')
	ip_address = request.remote_addr

	coll = coll_to_int(request.form.get('coll'))
	product_id = request.form.get('product_id')
	product_name = request.form.get("product_name")

	
	if not session.get('bag'):
		session['bag'] = dict()
	
	if session['bag'].get(product_id):
		session['bag'][product_id] += coll
	else:
		session['bag'][product_id] = coll

	for i,j in session['bag'].items():
		print(i,j)
		
	if request.form.get('add'):		
		flash(message=f'В корзину добавлен товар: {product_name} * {coll} шт. ',category='cart')
		return redirect(return_next(session['history']))
			
		
	
	
	elif request.form.get('buy'):
		flash(message=f'Оформляем покупку:     {request.form.get("product_name")} * {coll} шт. ',category='cart')
		return redirect(return_next(session['history']))
	



@app.route('/bag')
def get_bag():
	cart = session.get('bag')


	return render_template('bag.html', title='Корзина', menu=menu)













@app.before_request
def before_request():
	if not session.get('history'):
		session['history'] = list()

	link =request.path

	if 'static' not in link and 'bag' not in link:
		session['history'].append(link)
		session.modified = True
	
	
	
	