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
    category_id INT REFERENCES categories (id),
    seller_id INT REFERENCES seller (id),
    price numeric(5, 2),
    price2 numeric(5, 2),
    price3 numeric(5, 2),
    comission numeric(5, 2),
    sold INT
);


INSERT INTO product(name, description, link, category_id, seller_id, price, price2, price3, comission, sold)
VALUES('Цемент М400', '')

CREATE TABLE IF NOT EXISTS product_img(
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES product(id),
    link text
);



INSERT INTO seller(name, description,address,phone,telegram, email)
VALUES('self', 'self', 'aval', '77553291', '15444654565', 'iiiliev.igor@gmail.com'),
('Аваль', 'Цемент Песок Гравий', 'Мегатранс', '77782349', '15444654565', 'iiiliev.igor@gmail.com');



INSERT INTO categories(name, description) VALUES
('Цемент и наполнители', 'Цемент М400, М500, М550, Белый цемент, Песок мытый, Песок сеянный, Гравий, Мелуза молотая(отсев).'),
('Кирпичи, фортан и блоки', 'Кирпичи: Полнотелые, Щелевые, Полуторные, Огнеупорные, Декоративные, Клинкерные. Фортан, Газоблоки, Пеноблоки.'),
('Плитка, бордюры и прочие изделия', 'Тротуарная плитка, Коньки и крышки для заборов, Бордюры, Водостоки'),
('Камины и печи', 'Дверцы печные, Жаровые Решетки, Дымоходные затворы, Клей огнеупорный'),
('Клей, шпатлевка и сетка', 'Клей 333, Шпатлевка первичная и вторичная. Армирующая сетка 1*2м с ячейкой: 100*100мм, 150*150мм.');