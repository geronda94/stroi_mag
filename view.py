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
	'Главная страница':'index',
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


		
	if request.form.get('add'):		
		flash(message=f'В корзину добавлен товар: {product_name} * {coll} шт. ',category='cart')
		return redirect(return_next(session['history']))
			
		
	
	
	elif request.form.get('buy'):
		flash(message=f'Оформляем покупку:     {request.form.get("product_name")} * {coll} шт. ',category='cart')
		return redirect(return_next(session['history']))
	



@app.route('/bag')
def get_bag():
	cart = session.get('bag')
	total_price = 0
	total_weight = 0


	if cart:
		prod_id = [x[0] for x in cart]
		product_list = products.in_cart(prod_id)
		
		bag_refactored= []
		for i in product_list:
			
			for key, value in cart.items():
				product_id = int(i.get('product_id'))
				cart_id = int(key)
				if product_id ==cart_id:
					sale = 0
					price = int(i.get('price'))
					price2 = i.get('price2')
					price3 = i.get('price3')
					condition1 = i.get('sale_for1')
					condition2 = i.get('sale_for2')
					coll = int(value)
					weight = float(i.get('weight'))

					if (condition1 and price2) or (condition2 and price3):
						if coll >= condition1 :
							sale = int(price2)

						elif coll >=  condition2:
							sale = int(price3)

						else:
							sale = price
					else:
						sale = int(price)

					total = int(sale)*int(coll)
					total_price+=total
					sum_weight = int(weight*int(coll))
					total_weight += sum_weight

					if sale == price:
						sale = '-'

					bag_refactored.append({
						'product_id':i.get('product_id'),
						'product_name':i.get('product_name'),
						'product_ava':i.get('ava_link'),
						'coll':coll,
						'weight':sum_weight,
						'price':price,
						'sale':sale,
						'total':total,
						'link':i.get('link')
					})

				else:
					continue

	else:
		bag_refactored = False


	return render_template('bag.html', title='Корзина', menu=menu, cart=bag_refactored,\
							total=total_price, weight=total_weight)



@app.route('/edit_bag', methods=['POST'])
def edit_bag():
	if request.method == 'POST':
		coll = coll_to_int(request.form.get('coll'))
		product_id = request.form.get('product_id')
		product_name = request.form.get('product_name')

		if request.form.get('minus'):
			session['bag'][product_id] -= coll
			flash(message=f'Убрали из корзины {coll} шт. {product_name}', category='cart')

		if request.form.get('plus'):
			session['bag'][product_id] += coll
			flash(message=f'Добавили в корзину {coll} шт. {product_name}', category='cart')
	
	return redirect(url_for('get_bag'))







@app.before_request
def before_request():
	if not session.get('history'):
		session['history'] = list()

	link =request.path

	if 'static' not in link and 'bag' not in link:
		session['history'].append(link)
		session.modified = True
	
	
	
	