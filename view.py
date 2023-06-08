from flask import render_template, url_for, redirect, session, request,flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from app import app
from pg import PgConnect, PgRequest, products
from config import DB, load_cof
import uuid
from func import return_next, coll_to_int, bag_construct
import math


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
		
		next_url = request.args.get('next')
		if next_url is None:
			next_url = 'index'
		return redirect(url_for(next_url))
					
		
	
	elif request.form.get('buy'):
		flash(message=f'Оформляем покупку:     {request.form.get("product_name")} * {coll} шт. ',category='cart')
		return redirect(return_next(session['history']))
	



@app.route('/bag')
def get_bag():
	cart = session.get('bag')
	total_price = 0
	total_weight = 0



	if cart:
		new_bag = bag_construct(cart)
		bag_refactored = new_bag[0]
		total_price = new_bag[1]
		total_weight = new_bag[2]

		

	else:
		bag_refactored = False

	

	return render_template('bag.html', title='Корзина', menu=menu, cart=bag_refactored,\
							total=total_price, weight=session['delivery']['total_weight'])



@app.route('/edit_bag', methods=['POST'])
def edit_bag():
	if request.method == 'POST':
		coll = coll_to_int(request.form.get('coll'))
		product_id = request.form.get('product_id')
		product_name = request.form.get('product_name')

		if request.form.get('minus'):
			session['bag'][product_id] -= coll
			if session['bag'][product_id] < 1:
				del session['bag'][product_id]
			flash(message=f'Убрали из корзины {coll} шт. {product_name}', category='success')

		if request.form.get('plus'):
			session['bag'][product_id] += coll
			flash(message=f'Добавили в корзину {coll} шт. {product_name}', category='success')
	
	return redirect(url_for('get_bag'))


@app.route('/drop_bag')
def drop_bag():
	session['bag'] = dict()
	del session['bag_refactored']
	del session['loaders_calc']
	session['delivery']['total_weight'] = 0
	session['delivery']['total_price'] = 0
	flash(message=f'Корзина очищена',category='success')

	return redirect(url_for('get_bag'))



@app.route('/delivery', methods=['GET', 'POST'])
def set_delivery():
	total_weight = session.get('delivery').get('total_weight')
	total_price = session.get('delivery').get('price')
	bag_refactored = session.get('bag_refactored')
	bag = session.get('bag')
	loaders_calc = session.get('loaders_calc')
	
	

	if total_weight and int(total_weight) > 0:
		if (bag_refactored and bag) and (bag_refactored ==  bag):
			delivery_options = products.select_delivery()
			loaders_options = products.select_loaders()



			if  request.method == 'POST':
				delivery_value = int(request.form.get('delivery'))
				load_coficient = float(request.form.get('load_coficient'))
				
				delivery_dict = None
				load_list = None
				if load_coficient > 0:
					load_list = []
					for i in loaders_options:
						for weight, num in loaders_calc.items():
							if float(weight) == float(i.get('weight')):
								load_list.append({
									'weight':float(weight),
									'coll':num,
									'price': float(i.get('price')) * float(load_coficient),
									'total_price': num * float(i.get('price'))* float(load_coficient)
									})
								
				
				if delivery_value > 1:
					delivery_option = next(filter(lambda i: int(i.get('id')) == int(delivery_value), delivery_options), {})

					if len(delivery_option) > 0:
						delivery_name = delivery_option.get('name')
						max_weight = float(delivery_option.get('max_weight'))
						total_weight = float(total_weight)
						price_for_once = float(delivery_option.get('price'))
						need_ride =  math.ceil(float(total_weight) / float(delivery_option.get('max_weight')))
						total_price = need_ride* price_for_once
						
						delivery_dict = {
										'value': delivery_value,
										'name':delivery_name,
										'max_weight':max_weight,
										'total_weight': total_weight ,
										'price_for_once': price_for_once,
										'need_ride':need_ride,
										'total_price':total_price
										}

						

				return render_template('delivery_order.html', title='Способ доставки и разгрузки', menu=menu,
										total_weight=total_weight, total_price=total_price, delivery=delivery_options,
										loaders=loaders_options, load_cof=load_cof, delivery_value=int(delivery_value),
										load_coficient=float(load_coficient), load_list=load_list, delivery_dict=delivery_dict,
										)

			


			return render_template('delivery_order.html', title='Способ доставки и разгрузки', menu=menu,
			  total_weight=total_weight, total_price=total_price, delivery=delivery_options,\
				loaders=loaders_options, load_cof=load_cof)
		
		else:
			return redirect(url_for('get_bag'))
	else:
		return redirect(url_for('get_bag'))
	













@app.before_request
def before_request():
	if not session.get('history'):
		session['history'] = list()

	link =request.path

	if 'static' not in link and 'bag' not in link:
		session['history'].append(link)
		session.modified = True
	
	
	
	