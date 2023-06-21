from flask import render_template, url_for, redirect, session, request,flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from app import app
from pg import PgConnect, PgRequest, products, orders
from config import DB, load_cof
import uuid
from func import coll_to_int, bag_construct, clear_bag, number_validator, string_validator
import math
from datetime import datetime

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
		clear_bag()

	if session['bag'].get(product_id):
		session['bag'][product_id] += coll
	else:
		session['bag'][product_id] = coll


		
	if request.form.get('add'):		
		anchor = request.form.get('anchor')
		flash(message=f'В корзину добавлен товар: {product_name} * {coll} шт. ',category='cart')
		
		next_url = request.args.get('next')
		if next_url is None:
			next_url = 'index'
		return redirect(request.referrer+'#'+str(anchor))
					
		
	
	elif request.form.get('buy'):
		return redirect(url_for('get_bag'))
	



@app.route('/bag')
def get_bag():
	cart = False
	if not session.get('bag'):
		clear_bag()
	else:
		cart = session.get('bag')

	if cart:
		bag_refactored = bag_construct(cart)
		

		return render_template('bag.html', title='Корзина', menu=menu, cart=bag_refactored,\
							total=session['product']['total_price'], weight=session['product']['total_weight'])


	else:
		bag_refactored = False

		return render_template('bag.html', title='Корзина', menu=menu)

	


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
	clear_bag()
	flash(message=f'Корзина очищена',category='success')

	return redirect(url_for('get_bag'))



@app.route('/delivery', methods=['GET', 'POST'])
def set_delivery():
	total_weight = session.get('product').get('total_weight')
	total_price = session.get('product').get('price')
	bag_refactored = session.get('bag_refactored')
	bag = session.get('bag')
	weight_calc = session.get('weight_calc')
	
	

	if total_weight and int(total_weight) > 0:
		if (bag_refactored and bag) and (bag_refactored ==  bag):
			delivery_options = products.select_delivery()
			loaders_options = products.select_loaders()



			if  request.method == 'POST':
				delivery_value = int(request.form.get('delivery'))
				load_name = request.form.get('load_coficient')
				load_coficient = float(load_cof.get(load_name))
				
				delivery_dict = None
				load_list = None
				total_load_price = 0
				total_delivery_price = 0


				if load_coficient > 0:
					load_list = []
					for i in loaders_options:
						for weight, num in weight_calc.items():
							if float(weight) == float(i.get('weight')):
								price = float(i.get('price')) * float(load_coficient)
								price_id = i.get('id')
								total_price = price * num
								total_load_price += total_price

								load_list.append({
									'weight':float(weight),
									'coll':num,
									'price': round(price,2),
									'price_id':price_id,
									'total_price': num * float(i.get('price'))* float(load_coficient)
									})
					session['load_list'] = load_list
					session['load_name'] = load_name
					session['total_load_price'] = total_load_price
				else:
					session['load_list'] = []
					session['load_name'] = ''
					session['total_load_price'] = 0
								
				
				if delivery_value > 1:
					delivery_option = next(filter(lambda i: int(i.get('id')) == int(delivery_value), delivery_options), {})

					if len(delivery_option) > 0:
						delivery_name = delivery_option.get('name')
						max_weight = float(delivery_option.get('max_weight'))
						total_weight = float(total_weight)
						price_for_once = float(delivery_option.get('price'))
						need_ride =  math.ceil(float(total_weight) / float(delivery_option.get('max_weight')))
						total_price = need_ride* price_for_once
						delivery_location = delivery_option.get('location')

						delivery_dict = {
										'value': delivery_value,
										'name':delivery_name,
										'location':delivery_location,
										'max_weight':max_weight,
										'total_weight': total_weight ,
										'price_for_once': price_for_once,
										'need_ride':need_ride,
										'total_price':total_price
										}
						
						session['delivery_dict'] = delivery_dict
						session['total_delivery_price'] = total_price
						
					
				else:
					session['delivery_dict'] = dict()
					session['total_delivery_price'] = 0
					
				if request.form.get('send_order'):
						return redirect(url_for('complete_order'))			
				
				return render_template('delivery_order.html', title='Способ доставки и разгрузки', menu=menu,
										total_weight=total_weight, total_price=total_price, delivery=delivery_options,
										loaders=loaders_options, load_cof=load_cof, delivery_value=int(delivery_value),
										load_name=load_name, load_list=load_list, delivery_dict=delivery_dict,
										total_load_price = total_load_price, anchor='1', all_total_price = total_load_price+total_delivery_price
										)

			

			return render_template('delivery_order.html', title='Способ доставки и разгрузки', menu=menu,
			  total_weight=total_weight, total_price=total_price, delivery=delivery_options,\
				loaders=loaders_options, load_cof=load_cof)
		
		else:
			return redirect(url_for('get_bag'))
	else:
		return redirect(url_for('get_bag'))
	




@app.route('/order', methods=['GET','POST'])
def complete_order():
	bag_refactored = session.get('bag_refactored')
	bag = session.get('bag')
	number_phone = False
	address = None

	products_price = round(session.get('product').get('total_price'),2)
	delivery_price = round(session.get('total_delivery_price'),2)
	load_price = round(session.get('total_load_price'),2)
	full_price = products_price + delivery_price + load_price

	if (bag and bag_refactored) and (bag == bag_refactored):
		location = session.get('delivery_dict').get('location')

		if request.method == 'POST':
			number_phone = number_validator(request.form.get('phone'))

			if location:
				address = string_validator(request.form.get('address'))
				if not address or address == '':
					flash(message='Ошибка в адресе, введите еще раз', category='error')
					
					
					return render_template('complete_order.html', title='Отправить заказ', menu=menu,
											location=location, number_phone=number_phone, load_price=load_price, delivery_price=delivery_price,
											products_price=products_price, full_price=full_price)
			
			if number_phone in [None, False]:
				flash(message='Не правильный номер телефона', category='error')
				return render_template('complete_order.html', title='Отправить заказ', menu=menu,
				location=location, address=address, load_price=load_price, delivery_price=delivery_price,
				products_price=products_price, full_price=full_price)

		

			order_id = products.new_order(
				session_id = str(session.get('uid')),
				ip_address = request.remote_addr,
				location = location,
				address = address,
				full_price = full_price,
				phone = number_phone,
				product_price = products_price,
				delivery_price = delivery_price,
				load_price= load_price
				)
			
			order_products = products.products_to_order(order_id=order_id, product_lst=session.get('bag_list'))
			if not order_products:
				flash(message='Что-то пошло не так при оформлении заказа, попробуйте позже', category='error')
				return render_template('complete_order.html', title='Отправить заказ', menu=menu,
				location=location, address=address,load_price=load_price, delivery_price=delivery_price,
				products_price=products_price, full_price=full_price)

			
			if len(session.get('delivery_dict')) > 0:
				result = products.delivery_order(order_id=order_id, delivery_dict=session.get('delivery_dict'), address=address)
				if not result:
					flash(message='Что-то пошло не так при оформлении доставки, попробуйте позже', category='error')
					return render_template('complete_order.html', title='Отправить заказ', menu=menu,
					location=location, address=address, load_price=load_price, delivery_price=delivery_price,
					products_price=products_price, full_price=full_price)
			
			if len(session.get('load_list')):
				result =  products.load_order(order_id=order_id, order_list=session.get('load_list'),
				  			load_name=session.get('load_name'))
				if not result:
					flash(message='Что-то пошло не так при заказе услуг грузчиков, попробуйте позже', category='error')
					return render_template('complete_order.html', title='Отправить заказ', menu=menu,
					location=location, address=address, load_price=load_price, delivery_price=delivery_price,
					products_price=products_price, full_price=full_price)

			# clear_bag()

			return redirect(url_for('orders_history'))



		return render_template('complete_order.html', title='Отправить заказ', menu=menu,
				location=location, load_price=load_price, delivery_price=delivery_price,
				products_price=products_price, full_price=full_price)
	else:
		return redirect(url_for('get_bag'))




@app.route('/orders_history')
def orders_history():
	session_id = str(session.get('uid'))
	orders_list = orders.orders_for_user(session_id=session_id)
	if orders_list:
		orders_id = ', '.join(str(order_id) for order_id in [order_item.get('id') for order_item in orders_list])
		products = orders.products_for_orders(orders_id)
		delivery = orders.delivery_for_orders(orders_id)
		loaders = orders.loaders_for_orders(orders_id)
		
		return render_template('orders.html', title='История заказов', menu=menu, orders_list=orders_list,
				products=products, delivery=delivery, loaders=loaders)

	return render_template('orders.html', title='История заказов пуста', menu=menu)




















@app.before_request
def before_request():
	if request.endpoint and request.endpoint != 'static' and not request.path.startswith(url_for('static', filename='')):
		if not session.get('uid'):
			session['uid'] = uuid.uuid4()
			session['created'] = datetime.now().strftime('%Y-%m-%d %H:%M')
		
	
	
	
	