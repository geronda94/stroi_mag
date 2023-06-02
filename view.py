from flask import render_template, url_for, redirect, session, request,flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from app import app
from pg import PgConnect, PgRequest, products
from config import DB
import uuid



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
	prev_page = request.args.get('next')
	if not session.get('bag'):
		session['bag'] = dict()

	

	if request.form.get('add'):

		if session.get('history'):
			flash(message='Товар добавлен в корзину',category='success')
			return redirect(session['history'][-2])
			
		else:
			flash(message='Товар не  добавлен в корзину',category='error')
			return redirect(url_for('index'))
	
	
	elif request.form.get('buy'):
		return f"{prev_page}   now coll = {request.form.get('coll')} id = {request.form.get('product_id')}  real_ip={real_ip}  ua={user_agent}"
	













@app.before_request
def before_request():
	if not session.get('history'):
		session['history'] = list()

	link =request.path

	if 'static' not in link:
		session['history'].append(link)
		session.modified = True 
	
	
	
	