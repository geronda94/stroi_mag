
class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://geronda:1994@localhost/self'
    sqlalchemy_track_modifications = False 
    SECRET_KEY = 'hfsjfksd$%&2323#klds'


class DB:
    host="localhost"
    port='5432'
    database="stroimarket"
    user="geronda"
    password="1994"


load_cof = {'Грузчики не нужны': 0,
				'Выгрузка на  1 Этаж': 1,
				'Подъем на  2 Этаж': 2,
				'Подъем лифтом': 2,
				'Подъем на  3 Этаж': 4,
				'Подъем на  5 Этаж': 5,
				'Подъем на  6 Этаж': 6,
				'Подъем на  7 Этаж': 7,
				'Подъем на  8 Этаж': 8,
				'Подъем на  9 Этаж': 9,
				'Выгрузка рядом с машиной до 3 метров': 0.4,
				'Пронести от машины 15 метров': 1,
				'Пронести от машины от 15 до 30 метров': 2,
				'Пронести от машины 30 до 45 метров': 3,
				'Пронести от машины от 45 до 60 метров': 4,
			}




