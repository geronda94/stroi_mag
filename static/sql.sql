CREATE DATABASE stroimarket;

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name varchar(50),
    description varchar(150)
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
    link text,
    seller_id INT REFERENCES seller (id),
    price numeric(5, 2),
    price2 numeric(5, 2),
    price3 numeric(5, 2),
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
    link text
);




INSERT INTO seller(name, description,address,phone,telegram, email) VALUES
('self', 'self', 'aval', '77553291', '15444654565', 'iiiliev.igor@gmail.com'),
('Аваль', 'Цемент Песок Гравий', 'Мегатранс', '77782349', '15444654565', 'iiiliev.igor@gmail.com');



INSERT INTO categories(name, description) VALUES
('Цемент и наполнители', 'Цемент М400, М500, М550, Белый цемент, Песок мытый, Песок сеянный, Гравий, Мелуза молотая(отсев).'),
('Кирпичи, фортан и блоки', 'Кирпичи: Полнотелые, Щелевые, Полуторные, Огнеупорные, Декоративные, Клинкерные. Фортан, Газоблоки, Пеноблоки.'),
('Плитка, бордюры и прочие изделия', 'Тротуарная плитка, Коньки и крышки для заборов, Бордюры, Водостоки'),
('Камины и печи', 'Дверцы печные, Жаровые Решетки, Дымоходные затворы, Клей огнеупорный'),
('Клей, шпатлевка и сетка', 'Клей 333, Шпатлевка первичная и вторичная. Армирующая сетка 1*2м с ячейкой: 100*100мм, 150*150мм.');


INSERT INTO product(name, description, link, seller_id, price, price2, price3, comission, sold, order_num)VALUES
('Цемент М 400', 'Цемент марки 400 рыбницкого завода', 'cement-m400', '2','85', '84','83','0','0','1'),
('Цемент М 500', 'Цемент марки 500 рыбницкого завода', 'cement-m500', '2','90', '89','88','0','0','2'),
('Цемент М 550', 'Цемент марки 550 рыбницкого завода', 'cement-m550', '2','90', '89','88','0','0',NULL),
('Песок сеянный', 'Цемент сеянный с содержанием глины подходит для кладки и штукатурки', 'pesok-1', '2','13', '0','0','0','0',NULL),
('Песок Мытый', 'Цемент мытый, без глины', 'pesok-2', '2','14', '0','0','0','0','3'),
('Гравий', 'Гравий среднего размера', 'gravii', '2','18', '0','0','0','0','4'),
('Мелуза', 'Мелуза или известковый отсев. Молотая, отлично подходит для добавки в штукатурные смеси, фасадной отделки и для добавления в корм животных', 'meluza', '2','25', '0','0','0','0','5');


INSERT INTO cat_prod(category_id, product_id) VALUES
('1','1'),
('1','2'),
('1','3'),
('1','4'),
('1','5'),
('1','6'),
('1','7');
