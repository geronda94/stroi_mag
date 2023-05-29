from flask import render_template, url_for, redirect, session
from app import app

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
	return render_template('index.html', title='Domstroi.pro - Наш ассортимент', menu=menu)


