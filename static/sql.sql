-- CREATE DATABASE stroimarket;


CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name varchar(50),
    link TEXT,
    description varchar(150),
    order_num INT
);




CREATE TABLE IF NOT EXISTS seller(
    id SERIAL PRIMARY KEY,
    name varchar(50),
    description text,
    address varchar(50),
    phone varchar(10),
    telegram varchar(40),
    email varchar(40),
    logo text,
    avatar text
);



CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    name varchar(50),
    description text,
    ava_link text,
    link text,
    seller_id INT REFERENCES seller (id),
    price numeric(5, 2),
    price2 numeric(5, 2),
    price3 numeric(5, 2),
    sale_for1 INT,
    sale_for2 INT,
    weight DECIMAL,
    comission numeric(5, 2),
    order_num INT,
    sold INT
);


CREATE TABLE IF NOT EXISTS cat_prod(
    category_id INT REFERENCES categories (id),
    product_id INT REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS product_img(
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES product(id),
    link text, 
    order_num INT 
);




INSERT INTO seller(name, description,address,phone,telegram, email) VALUES
('self', 'self', 'aval', '77553291', '15444654565', 'iiiliev.igor@gmail.com'),
('Аваль', 'Цемент Песок Гравий', 'Мегатранс', '77782349', '15444654565', 'iiiliev.igor@gmail.com'),
('Кирпичок', 'Кирпичи, бетонные изделия, печное оборудование', 'Мегатранс', '77782349', '15444654565', 'nikolay@gmail.com');



INSERT INTO categories(name, link, description, order_num) VALUES
('Цемент и наполнители', 'cement','Цемент М400, М500, М550, Белый цемент, Песок мытый, Песок сеянный, Гравий, Мелуза молотая(отсев).','1'),
('Кирпичи, фортан и блоки', 'chirpich','Кирпичи: Полнотелые, Щелевые, Полуторные, Огнеупорные, Декоративные, Клинкерные. Фортан, Газоблоки, Пеноблоки.', NULL),
('Плитка, бордюры и прочие изделия', 'plitka','Тротуарная плитка, Коньки и крышки для заборов, Бордюры, Водостоки',NULL),
('Камины и печи', 'kamini', 'Дверцы печные, Жаровые Решетки, Дымоходные затворы, Клей огнеупорный','2'),
('Клей, шпатлевка и сетка', 'klei', 'Клей 333, Шпатлевка первичная и вторичная. Армирующая сетка 1*2м с ячейкой: 100*100мм, 150*150мм.', NULL);


INSERT INTO product(name, description,  ava_link, link, seller_id, price, price2, price3, sale_for1,sale_for2, weight, comission, sold, order_num)VALUES
('Цемент М 400', 'Цемент марки 400 рыбницкого завода', 'cement_m400.png', 'cement-m400', '2','85', '84','83','6','25','40','0','0','1'),
('Цемент М 500', 'Цемент марки 500 рыбницкого завода', 'cement_m500.png','cement-m500', '2','90', '89','88','6','25','40','0','0','2'),
('Цемент М 550', 'Цемент марки 550 рыбницкого завода', 'cement_m550.png','cement-m550', '2','93', '92','91','6','25','40','0','0',NULL),
('Песок сеянный', 'Цемент сеянный с содержанием глины подходит для кладки и штукатурки', 'pesok.jpg', 'pesok-1', '2','13', '0','0', Null,'40', NULL,'0','0',NULL),
('Песок Мытый', 'Цемент мытый, без глины', 'pesok.jpg','pesok-2', '2','14', '0','0',NULL, NULL,'40','0','0','3'),
('Гравий', 'Гравий среднего размера', 'gravii.webp', 'gravii', '2','18', '0','0',NULL, NULL,'40','0','0','4'),
('Мелуза', 'Мелуза или известковый отсев. Молотая, отлично подходит для добавки в штукатурные смеси, фасадной отделки и для добавления в корм животных', 'meluza.jpg','meluza', '2','25', '0','0',NULL, '40',NULL,'0','0','5'),
('Кирпич полнотелый', 'Полнотелый кирпич','poln_kirpich.jpg', 'kirpich_poln', '3','4', '0','0',NULL, NULL,'3.5','0','0','1'),
('Кирпич полый', 'Полый кирпич','polii_kirpich.jpeg','kirpich_polii', '3','3.8', '0','0',NULL,NULL,'3.5','0','0','2'),
('Кирпич полуторный', 'Полый кирпич','polutor_kirpich.jpg', 'kirpich_polutor', '3','4.5', '0','0',NULL, NULL,'3.5', '0','0',NULL),
('Кирпич Огнеупорный', 'Огнеупорный кирпич', 'ogneupor_kirpich.jpeg','kirpich_ogneupor', '3','45', '0','0', NULL, NULL,'3.5', '0','0','3')
;








INSERT INTO cat_prod(category_id, product_id) VALUES
('1','1'),
('1','2'),
('1','3'),
('1','4'),
('1','5'),
('1','6'),
('1','7'),
('2','8'),
('2','9'),
('2','10'),
('2','11')
;

CREATE TABLE IF NOT EXISTS load_price(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    descriprion VARCHAR(150),
    price DECIMAL,
    weight DECIMAL,
    order_num INT
);

INSERT INTO load_price(name, descriprion,price, weight, order_num) VALUES
('Мешок 40 кг.', 'Мешки по 40 кг. по 5 рублей за этаж или каждые 15 метров', '5', '40','1'),
('Мешок 25 кг.', 'Мешки по 25 кг. по 3.5 рубля за этаж или каждые 15 метров', '3.5', '25','2'),
('Кирпичи.', 'Кирпичи по 3.5 рубля за 5 кирпичей этаж или каждые 15 метров', '0.75', '3.5','3'),
('Фортан и Пеноблоки маленькие(до 10 кг).', 'Блоки по 1 рублю до 10кг за этаж или каждые 15 метров', '1', '10','4'),
('Фортан и Пеноблоки крупные(от 10 кг).', 'Блоки по 1.5 рублей от 10кг за этаж или каждые 15 метров', '1.5', '10','5')
;