from flask import  render_template, url_for, redirect, session
from app import app

menu = {
	'Каталог товаров':{
		'Цемент':'index',
		'Клей':'index',
		'Песок':'index'
		                },
	'Связаться с нами':'index',
	'Достава и разгрузка':'index',
	'Ваши заказы':'index',
	}
  
@app.route('/')
def index():
	return render_template('index.html', title='Главная страница', menu=menu)


