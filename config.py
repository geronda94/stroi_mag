
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
				'1 Этаж': 1,
				'2 Этаж': 2,
				'Можно поднять лифтом': 2,
				'3 Этаж': 4,
				'5 Этаж': 5,
				'6 Этаж': 6,
				'7 Этаж': 7,
				'8 Этаж': 8,
				'9 Этаж': 9,
				'По земле до 3 метров': 0.4,
				'По земле до 15 метров': 1,
				'По земле от 15 до 30 метров': 2,
				'По земле от 30 до 45 метров': 3,
				'По земле от 45 до 60 метров': 4,
			}


