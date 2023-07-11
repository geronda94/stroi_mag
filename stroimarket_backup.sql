--
-- PostgreSQL database dump
--

-- Dumped from database version 12.15 (Ubuntu 12.15-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.15 (Ubuntu 12.15-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cat_prod; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.cat_prod (
    category_id integer,
    product_id integer
);


ALTER TABLE public.cat_prod OWNER TO geronda;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(50),
    link text,
    description character varying(150),
    order_num integer
);


ALTER TABLE public.categories OWNER TO geronda;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: geronda
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO geronda;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: geronda
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: delivery_price; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.delivery_price (
    id integer NOT NULL,
    name character varying(200),
    price numeric,
    max_weight numeric,
    location text,
    comission numeric,
    order_num integer
);


ALTER TABLE public.delivery_price OWNER TO geronda;

--
-- Name: delivery_price_id_seq; Type: SEQUENCE; Schema: public; Owner: geronda
--

CREATE SEQUENCE public.delivery_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.delivery_price_id_seq OWNER TO geronda;

--
-- Name: delivery_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: geronda
--

ALTER SEQUENCE public.delivery_price_id_seq OWNED BY public.delivery_price.id;


--
-- Name: drivers; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.drivers (
    id integer NOT NULL,
    name character varying(30),
    phone character varying(13),
    email text,
    telegram text
);


ALTER TABLE public.drivers OWNER TO geronda;

--
-- Name: drivers_id_seq; Type: SEQUENCE; Schema: public; Owner: geronda
--

CREATE SEQUENCE public.drivers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.drivers_id_seq OWNER TO geronda;

--
-- Name: drivers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: geronda
--

ALTER SEQUENCE public.drivers_id_seq OWNED BY public.drivers.id;


--
-- Name: load_price; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.load_price (
    id integer NOT NULL,
    name character varying(50),
    descriprion character varying(150),
    price numeric,
    weight numeric,
    comission numeric,
    order_num integer
);


ALTER TABLE public.load_price OWNER TO geronda;

--
-- Name: load_price_id_seq; Type: SEQUENCE; Schema: public; Owner: geronda
--

CREATE SEQUENCE public.load_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.load_price_id_seq OWNER TO geronda;

--
-- Name: load_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: geronda
--

ALTER SEQUENCE public.load_price_id_seq OWNED BY public.load_price.id;


--
-- Name: loaders; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.loaders (
    id integer NOT NULL,
    name character varying(30),
    phone character varying(13),
    email text,
    telegram text
);


ALTER TABLE public.loaders OWNER TO geronda;

--
-- Name: loaders_id_seq; Type: SEQUENCE; Schema: public; Owner: geronda
--

CREATE SEQUENCE public.loaders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.loaders_id_seq OWNER TO geronda;

--
-- Name: loaders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: geronda
--

ALTER SEQUENCE public.loaders_id_seq OWNED BY public.loaders.id;


--
-- Name: order_delivery; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.order_delivery (
    order_id integer,
    delivery_id integer,
    delivery_name text,
    products_weight numeric,
    max_weight numeric,
    delivery_address character varying(100),
    need_ride integer,
    delivery_price numeric,
    delivery_time timestamp without time zone,
    total_price numeric
);


ALTER TABLE public.order_delivery OWNER TO geronda;

--
-- Name: order_info; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.order_info (
    id integer NOT NULL,
    session_id text,
    ip_addres inet,
    location text,
    address text,
    phone character varying(15),
    full_price numeric,
    product_price numeric,
    delivery_price numeric,
    load_price numeric,
    driver_id integer,
    loader_id integer,
    date_time timestamp without time zone,
    order_status text
);


ALTER TABLE public.order_info OWNER TO geronda;

--
-- Name: order_info_id_seq; Type: SEQUENCE; Schema: public; Owner: geronda
--

CREATE SEQUENCE public.order_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.order_info_id_seq OWNER TO geronda;

--
-- Name: order_info_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: geronda
--

ALTER SEQUENCE public.order_info_id_seq OWNED BY public.order_info.id;


--
-- Name: order_loaders; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.order_loaders (
    order_id integer,
    load_id integer,
    load_name text,
    load_weight numeric,
    coll integer,
    price numeric,
    total_price numeric
);


ALTER TABLE public.order_loaders OWNER TO geronda;

--
-- Name: order_products; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.order_products (
    order_id integer,
    product_id integer,
    product_name character varying(50),
    coll integer,
    price numeric,
    total_price numeric,
    seller_id integer
);


ALTER TABLE public.order_products OWNER TO geronda;

--
-- Name: product; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.product (
    id integer NOT NULL,
    name character varying(50),
    description text,
    ava_link text,
    link text,
    seller_id integer,
    price numeric(5,2),
    price2 numeric(5,2),
    price3 numeric(5,2),
    sale_for1 integer,
    sale_for2 integer,
    weight numeric,
    comission numeric(5,2),
    order_num integer,
    sold integer
);


ALTER TABLE public.product OWNER TO geronda;

--
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: geronda
--

CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_id_seq OWNER TO geronda;

--
-- Name: product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: geronda
--

ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;


--
-- Name: product_img; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.product_img (
    id integer NOT NULL,
    product_id integer,
    link text,
    order_num integer
);


ALTER TABLE public.product_img OWNER TO geronda;

--
-- Name: product_img_id_seq; Type: SEQUENCE; Schema: public; Owner: geronda
--

CREATE SEQUENCE public.product_img_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_img_id_seq OWNER TO geronda;

--
-- Name: product_img_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: geronda
--

ALTER SEQUENCE public.product_img_id_seq OWNED BY public.product_img.id;


--
-- Name: seller; Type: TABLE; Schema: public; Owner: geronda
--

CREATE TABLE public.seller (
    id integer NOT NULL,
    name character varying(50),
    description text,
    address character varying(50),
    phone character varying(10),
    telegram character varying(40),
    email character varying(40),
    logo text,
    avatar text
);


ALTER TABLE public.seller OWNER TO geronda;

--
-- Name: seller_id_seq; Type: SEQUENCE; Schema: public; Owner: geronda
--

CREATE SEQUENCE public.seller_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seller_id_seq OWNER TO geronda;

--
-- Name: seller_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: geronda
--

ALTER SEQUENCE public.seller_id_seq OWNED BY public.seller.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: delivery_price id; Type: DEFAULT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.delivery_price ALTER COLUMN id SET DEFAULT nextval('public.delivery_price_id_seq'::regclass);


--
-- Name: drivers id; Type: DEFAULT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.drivers ALTER COLUMN id SET DEFAULT nextval('public.drivers_id_seq'::regclass);


--
-- Name: load_price id; Type: DEFAULT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.load_price ALTER COLUMN id SET DEFAULT nextval('public.load_price_id_seq'::regclass);


--
-- Name: loaders id; Type: DEFAULT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.loaders ALTER COLUMN id SET DEFAULT nextval('public.loaders_id_seq'::regclass);


--
-- Name: order_info id; Type: DEFAULT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.order_info ALTER COLUMN id SET DEFAULT nextval('public.order_info_id_seq'::regclass);


--
-- Name: product id; Type: DEFAULT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);


--
-- Name: product_img id; Type: DEFAULT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.product_img ALTER COLUMN id SET DEFAULT nextval('public.product_img_id_seq'::regclass);


--
-- Name: seller id; Type: DEFAULT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.seller ALTER COLUMN id SET DEFAULT nextval('public.seller_id_seq'::regclass);


--
-- Data for Name: cat_prod; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.cat_prod (category_id, product_id) FROM stdin;
1	1
1	2
1	3
1	4
1	5
1	6
1	7
5	12
5	14
5	15
5	16
3	17
3	18
3	19
3	20
3	21
3	22
3	23
3	24
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.categories (id, name, link, description, order_num) FROM stdin;
1	Цемент и наполнители	cement	Цемент М400, М500, М550, Белый цемент, Песок мытый, Песок сеянный, Гравий, Мелуза молотая(отсев).	1
3	Плитка, бордюры и прочие изделия	plitka	Тротуарная плитка, Коньки и крышки для заборов, Бордюры, Водостоки	\N
5	Клей, шпатлевка и сетка	klei	Клей 333, Шпатлевка первичная и вторичная. Армирующая сетка 1*2м с ячейкой: 100*100мм, 150*150мм.	\N
\.


--
-- Data for Name: delivery_price; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.delivery_price (id, name, price, max_weight, location, comission, order_num) FROM stdin;
1	Самовывоз	0	9999999		0	1
2	Тирасполь до 3х тон	150	3000	Тирасполь	20	2
3	Суклея  до 3х тон	180	3000	Суклея	20	3
4	Кицканы до 3х тон	300	3000	Кицканы	20	4
5	Манипулятор по Тирасполю до 5 тон	500	5000	Тирасполь	20	5
6	ЗИЛ по Тирасполю до 6 тон	300	6000	Тирасполь	20	6
\.


--
-- Data for Name: drivers; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.drivers (id, name, phone, email, telegram) FROM stdin;
\.


--
-- Data for Name: load_price; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.load_price (id, name, descriprion, price, weight, comission, order_num) FROM stdin;
1	Мешок 40 кг.	Мешки по 40 кг. по 5 рублей за этаж или каждые 15 метров	5	40	0.7	1
2	Мешок 25 кг.	Мешки по 25 кг. по 3.5 рубля за этаж или каждые 15 метров	3.5	25	0.4	2
3	Кирпичи.	Кирпичи по 3.5 рубля за 5 кирпичей этаж или каждые 15 метров	0.75	3.5	0.6	3
4	Фортан и Пеноблоки маленькие(до 10 кг).	Блоки по 1 рублю до 10кг за этаж или каждые 15 метров	1	10	0.11	4
5	Фортан и Пеноблоки крупные(от 10 кг).	Блоки по 1.5 рублей от 10кг за этаж или каждые 15 метров	1.5	10	0.16	5
\.


--
-- Data for Name: loaders; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.loaders (id, name, phone, email, telegram) FROM stdin;
\.


--
-- Data for Name: order_delivery; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.order_delivery (order_id, delivery_id, delivery_name, products_weight, max_weight, delivery_address, need_ride, delivery_price, delivery_time, total_price) FROM stdin;
1	2	Тирасполь до 3х тон	2000.0	3000.0	Ул федько дом 19 квартира 19	1	150.0	\N	150.0
2	2	Тирасполь до 3х тон	1200.0	3000.0	Ул федько дом 19 квартира 19	1	150.0	\N	150.0
3	2	Тирасполь до 3х тон	1200.0	3000.0	Гоголя 11	1	150.0	\N	150.0
4	2	Тирасполь до 3х тон	1400.0	3000.0	sdfd df fdsa fdf	1	150.0	\N	150.0
5	2	Тирасполь до 3х тон	40.0	3000.0	гоголя 11	1	150.0	\N	150.0
6	2	Тирасполь до 3х тон	40.0	3000.0	Гоголя 11	1	150.0	\N	150.0
9	2	Тирасполь до 3х тон	156.0	3000.0	Достоевского 13	1	150.0	\N	150.0
\.


--
-- Data for Name: order_info; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.order_info (id, session_id, ip_addres, location, address, phone, full_price, product_price, delivery_price, load_price, driver_id, loader_id, date_time, order_status) FROM stdin;
1	9c31785c-0007-49a6-8d6b-aca152c6776d	217.19.208.99	Тирасполь	Ул федько дом 19 квартира 19	77553291	5050.0	4400	150.0	500.0	\N	\N	2023-07-06 10:51:33	in process
2	2571e7b4-9f51-4f3e-b08f-cb37efd57c50	217.19.208.99	Тирасполь	Ул федько дом 19 квартира 19	77553291	3240.0	2490	150.0	600.0	\N	\N	2023-07-06 11:51:43	in process
3	68308891-1648-4a84-8abf-cfdc682d15fe	217.19.208.99	Тирасполь	Гоголя 11	77777777	2790.0	2490	150.0	150.0	\N	\N	2023-07-06 14:21:34	in process
4	0ed93247-4fbe-44b3-b21e-64f3532aa950	217.19.208.99	Тирасполь	sdfd df fdsa fdf	12345678	3930.0	2905	150.0	875.0	\N	\N	2023-07-06 16:04:08	in process
5	e54492fe-7a85-44f0-bc36-44e9e350c21b	217.19.208.99	Тирасполь	гоголя 11	77553288	235.0	85	150.0	0	\N	\N	2023-07-07 11:17:38	in process
6	40b2d0b7-1f7b-4266-bf92-068f68401c5d	217.19.208.99	Тирасполь	Гоголя 11	77553288	174.0	14	150.0	10.0	\N	\N	2023-07-07 13:36:25	in process
7	40b2d0b7-1f7b-4266-bf92-068f68401c5d	217.19.208.99	\N	\N	77777777	784	784	0	0	\N	\N	2023-07-07 13:37:50	in process
8	3d77cd4f-4f8d-41c4-9323-5db3164ea590	80.94.250.169	\N	\N	77777777	75	75	0	0	\N	\N	2023-07-08 23:57:35	in process
9	d0096b73-bfef-4f0b-b9f9-e597aa7bf0ac	80.94.250.169	Тирасполь	Достоевского 13	055982043	1410.0	1260	150.0	0	\N	\N	2023-07-09 08:53:52	in process
\.


--
-- Data for Name: order_loaders; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.order_loaders (order_id, load_id, load_name, load_weight, coll, price, total_price) FROM stdin;
1	1	Подъем на  2 Этаж	40.0	50	10.0	500.0
2	1	Подъем на  4 Этаж	40.0	30	20.0	600.0
3	1	Выгрузка на  1 Этаж	40.0	30	5.0	150.0
4	1	Подъем на  5 Этаж	40.0	35	25.0	875.0
6	1	Подъем лифтом	40.0	1	10.0	10.0
\.


--
-- Data for Name: order_products; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.order_products (order_id, product_id, product_name, coll, price, total_price, seller_id) FROM stdin;
1	2	Цемент М 500	50	88	4400	2
2	1	Цемент М 400	30	83	2490	2
3	1	Цемент М 400	30	83	2490	2
4	1	Цемент М 400	35	83	2905	2
5	1	Цемент М 400	1	85	85	2
6	5	Песок Мытый	1	14	14	2
7	5	Песок Мытый	56	14	784	2
8	16	Клей 333	1	75	75	2
9	17	Бордюры / Поребрики 4см.\n	30	22	660	2
9	15	Сетка  / ячейка 200*200 мм.	20	30	600	2
\.


--
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.product (id, name, description, ava_link, link, seller_id, price, price2, price3, sale_for1, sale_for2, weight, comission, order_num, sold) FROM stdin;
8	Кирпич полнотелый	Полнотелый кирпич	poln_kirpich.jpg	kirpich_poln	3	4.00	0.00	0.00	\N	\N	3.5	0.00	1	0
9	Кирпич полый	Полый кирпич	polii_kirpich.jpeg	kirpich_polii	3	3.80	0.00	0.00	\N	\N	3.5	0.00	2	0
10	Кирпич полуторный	Полый кирпич	polutor_kirpich.jpg	kirpich_polutor	3	4.50	0.00	0.00	\N	\N	3.5	0.00	\N	0
11	Кирпич Огнеупорный	Огнеупорный кирпич	ogneupor_kirpich.jpeg	kirpich_ogneupor	3	45.00	0.00	0.00	\N	\N	3.5	0.00	3	0
6	Гравий	<div class="product__description">\n    <b>Вес: 40 кг.</b> Гравий, мытый, среднего размера. Идеально подходит в качестве наполнителя для бетонных смесей. Также он используется в качестве декоративной подсыпки для ландшафта.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Гравий добывается и промывается в карьерах Приднестровья. Мы осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	gravii.jpg	gravii	2	17.00	0.00	0.00	\N	\N	40	0.00	4	0
5	Песок Мытый	<div class="product__description">\n    <b>Вес: 40 кг.</b> Песок, не содержащий глины и других примесей, позволяет формировать стабильный бетон, который в последствии не вызовет трещин. Он идеально подходит для заливки фундаментов, полов, опалубки и других строительных работ, кроме штукатурки. Не рекомендуется использовать этот песок для штукатурки из-за отсутствия глины и пластифицирующих примесей, так как штукатурная смесь с наполннением этого песка плохо моделируется.\n</div>\n<div class="clear__both"></div>\n<p class="made_in">Песок добыт в карьерах в окрестносятх Тирасполя. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	pesok.jpg	pesok-2	2	14.00	0.00	0.00	\N	\N	40	0.00	3	0
18	Коньки для заборов	<div class="product__description">\n    <b>Размер: 50*18 см.</b> Бетонное изделие изготовлено из цемента марки 550, что обеспечивает его долговечность и надежность.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Изделие произведено в Тирасполе на предприятии АВАЛЬ. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	konki.jpg	konki_zabornie	2	22.00	\N	\N	\N	\N	5	\N	2	\N
2	Цемент М 500	<div class="product__description">\n    <b>Вес: 40 кг.</b> Универсальное решение для различных строительных работ. Цемент М 500 обладает высокой прочностью и устойчивостью, что позволяет использовать его при создании надежных и долговечных бетонных конструкций. Он хорошо справляется с воздействием агрессивной среды, такой как влага и мороз. За свою универсальность и надежность этот цемент высоко ценится профессиональными строителями.\n</div>\n<div class="clear__both"></div>\n<div class="char__prod">\n    <p class="char_item">\n        <b>Гарантированное качество:</b><br>\n        Цемент М 500 прошел строгие испытания и соответствует высочайшим стандартам качества. Вы можете быть уверены в его надежности и долговечности.\n    </p>\n    <p class="char_item">\n        <b>Удобство использования:</b><br>\n        Благодаря своим характеристикам, наш цемент облегчает выполнение строительных работ. Вы сможете легко наносить и моделировать его, достигая идеальных результатов.\n    </p>\n        <p class="char_item">\n        <b>Универсальность:</b><br>\n        Подходит для различных видов строительных работ, включая кладку, штукатурку, бетонирование и заливку полов. Он является надежным и универсальным решением для вашего проекта.\n    </p>\n        <p class="char_item">\n        <b>Долговечность:</b><br>\n        М 500 обеспечивает прочность и стабильность вашей конструкции на протяжении многих лет. Вы можете быть уверены, что ваше строение будет стойким и надежным.\n    </p>\n</div>\n\n<p class="made_in">Цемент произведен в Приднестровье г. Рыбница. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	cement_m500.png	cement-m500	2	88.00	0.00	0.00	\N	\N	40	0.00	2	0
7	Мелуза	<div class="product__description">\n    <b>Вес: 40 кг.</b> Мелуза или известковый отсев, молотая и сеянная. Она подходит для фасадной декоративной штукатурки и используется в качестве пластификатора для штукатурных смесей. Также он может использоваться в качестве кормовой добавки для домашних птиц (куры, утки).\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Мелуза добывается в г.Григориополь в Приднестровье. Мы осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	meluza.jpg	meluza	2	25.00	0.00	0.00	\N	\N	40	0.00	5	0
4	Песок сеянный	<div class="product__description">\n    <b>Вес: 40 кг.</b> Песок с примесями глины позволяет сформировать пластичный раствор, который применяется для кладки и штукатурки. Не рекомендуется использовать его для бетонирования и заливки полов, так как при схватывании и застывании могут возникнуть трещины.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Песок добывается в карьерах Приднестровья. Мы осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	pesok_s.jpg	pesok-1	2	13.00	0.00	0.00	\N	\N	40	0.00	\N	0
20	Плитка паутинка  2,5см. 1м²	<div class="product__description">\n    <b>Размер: 50*16*2,5 см.</b> Бетонное изделие изготовлено из цемента марки 550, что обеспечивает его долговечность и надежность.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Изделие произведено в Тирасполе на предприятии АВАЛЬ. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	plitka.jpg\n	trotuarnaia_plitka_pautinka_25mm	2	85.00	\N	\N	\N	\N	60	\N	4	\N
23	Бордюры / Поребрики 7см.\n	<div class="product__description">\n    <b>Размер: 50*20*7 см.</b> Бетонное изделие изготовлено из цемента марки 550, что обеспечивает его долговечность и надежность.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Изделие произведено в Тирасполе на предприятии АВАЛЬ. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	bordur_sh.jpg	bordur_shirokii	2	35.00	\N	\N	\N	\N	5	\N	\N	\N
3	Цемент М 550	<div class="product__description">\n    <b>Вес: 40 кг.</b> Подходит для строительства фундаментов, армопоясов и других ответственных конструкций. Выдерживает воздействие любой агрессивной среды. Благодаря тому, что цемент марки 550 быстро застывает, идеально подходит для работы в сырую и холодную погоду.\n</div>\n<div class="clear__both"></div>\n<div class="char__prod">\n    <p class="char_item">\n        <b>Гарантированное качество:</b><br>\nЦемент М 550 прошел строгие испытания и соответствует высочайшим стандартам качества. Вы можете быть уверены в его надежности и долговечности.\n</p>\n    <p class="char_item">\n        <b>Быстрое застывание:</b><br>\n\tБлагодаря отсутствию извести в составе, цемент М 550 начинает схватываться менее чем за полчаса.\n\t</p>\n        <p class="char_item">\n        <b>Универсальность:</b><br>\n        Подходит для различных видов строительных работ, включая высоконагруженные конструкции.\n    </p>\n        <p class="char_item">\n        <b>Долговечность и экономичность</b><br>\n        М 550 обеспечивает высокую прочность. Если не требуется такая высокая прочность, можно добавить больше наполнителя, что позволит достичь марки прочности, аналогичной цементу М 500, с меньшими затратами.\n\t</p>\n</div>\n\n<p class="made_in">Цемент произведен в Приднестровье г. Рыбница. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	cement_m550.png	cement-m550	2	91.00	0.00	0.00	\N	\N	40	0.00	\N	0
1	Цемент М 400	<div class="product__description">\n    <b>Вес: 40 кг.</b> Идеальное решение для кладки и штукатурки. Благодаря высокому содержанию извести, цемент М 400 обладает пластичностью, что значительно упрощает его использование при штукатурке и кладке. Он также идеально подходит для бетонирования и заливки полов внутри помещений. Важно помнить, что не рекомендуется использовать его для бетонирования в областях, подверженных постоянному воздействию влаги. К сожалению, известь, которая делает эту марку цемента пластичной, также вымывается при контакте с водой, что уменьшает срок эксплуатации бетонного изделия.\n</div>\n<div class="clear__both"></div>\n<div class="char__prod">\n    <p class="char_item">\n        <b>Гарантированное качество:</b><br>\nНаш цемент М 400 прошел строгие испытания и соответствует высочайшим стандартам качества. Вы можете быть уверены в его надежности и долговечности\n</p>\n    <p class="char_item">\n        <b>Удобство использования:</b><br>\nБлагодаря высокой пластичности, наш цемент М 400 облегчает ваши строительные работы. Вы сможете легко наносить и моделировать его, достигая идеальных результатов.\n   </p>\n        <p class="char_item">\n        <b>Универсальность:</b><br>\n        Подходит для различных видов строительных работ, включая кладку, штукатурку, бетонирование и заливку полов(только в помещении). Он является надежным и универсальным решением для вашего проекта.\n    </p>\n        <p class="char_item">\n        <b>Долговечность:</b><br>\n        Цемент М 400 обеспечивает прочность и стабильность вашей конструкции на долгие годы. Вы можете быть уверены, что ваше строение будет стойким и надежным.\n/p>\n</div>\n\n<p class="made_in">Цемент произведен в Приднестровье г. Рыбница. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	cement_m400.png	cement-m400	2	83.00	0.00	0.00	\N	\N	40	0.00	1	0
16	Клей 333	<div class="product__description">\n    <b>Вес: 25 кг.</b> Клей плиточный усиленный, с микрофиброй. Подходит для отделки в любой агресинвной среде. Клей на основе цемента М 550, что делает его особенно прочным.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Клей произведен в Тирасполе. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	klei333.jpg	klei_333	2	75.00	\N	\N	\N	\N	25	\N	2	\N
19	Ливневки / Водостоки	<div class="product__description">\n    <b>Размер: 50*16 см.</b> Бетонное изделие изготовлено из цемента марки 550, что обеспечивает его долговечность и надежность.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Изделие произведено в Тирасполе на предприятии АВАЛЬ. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	vodostoki.jpg	vodostoki	2	28.00	\N	\N	\N	\N	5	\N	3	\N
24	Коньки красные	<div class="product__description">\n    <b>Размер: 50*18 см.</b> Бетонное изделие изготовлено из цемента марки 550, что обеспечивает его долговечность и надежность.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Изделие произведено в Тирасполе на предприятии АВАЛЬ. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	konki_k.jpg	konki_zabornie_krasnie	2	30.00	\N	\N	\N	\N	5	\N	\N	\N
21	Плитка паутинка  3см. 1м²	<div class="product__description">\n    <b>Размер: 50*16*3 см.</b> Бетонное изделие изготовлено из цемента марки 550, что обеспечивает его долговечность и надежность.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Изделие произведено в Тирасполе на предприятии АВАЛЬ. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	plitka.jpg	trotuarnaia_plitka_pautinka_30mm	2	90.00	\N	\N	\N	\N	65	\N	\N	\N
22	Плитка паутинка  4см. 1м²	<div class="product__description">\n    <b>Размер: 50*16*4 см.</b> Бетонное изделие изготовлено из цемента марки 550, что обеспечивает его долговечность и надежность.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Изделие произведено в Тирасполе на предприятии АВАЛЬ. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	plitka.jpg	trotuarnaia_plitka_pautinka_40mm	2	105.00	\N	\N	\N	\N	70	\N	\N	\N
12	Сетка  / ячейка 150*150 мм.	<div class="product__description">\n    <b>Площадь: 1*2 м. Сечение прутьев 2,5 мм</b> Армирующая  сетка  с размером ячеек 150*150мм. используется для придания большей прочности бетонным конструкциям таким как: отмостка, наливные полы, бетонные площадки и т.д.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Сетка произведена в Тирасполе. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	setka1.jpg	setka_150X150	2	32.00	\N	\N	\N	\N	0.3	\N	1	\N
17	Бордюры / Поребрики 4см.\n	<div class="product__description">\n    <b>Размер: 50*20*4 см.</b> Бетонное изделие изготовлено из цемента марки 550, что обеспечивает его долговечность и надежность.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Изделие произведено в Тирасполе на предприятии АВАЛЬ. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	bordur.jpg	bordur	2	22.00	\N	\N	\N	\N	5	\N	1	\N
15	Сетка  / ячейка 200*200 мм.	<div class="product__description">\n    <b>Площадь: 1*2 м. Сечение прутьев 2,5 мм</b> Армирующая сетка с размером ячеек 200*200мм. используется для придания большей прочности бетонным конструкциям таким как: отмостка, наливные полы, бетонные площадки и т.д. \n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Сетка произведена в Тирасполе. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	setka3.jpg	setka_200X200	2	30.00	\N	\N	\N	\N	0.3	\N	\N	\N
14	Сетка  / ячейка 100*100 мм.	<div class="product__description">\n    <b>Площадь: 1*2 м. Сечение прутьев 2,5 мм</b> Армирующая сетка с размером ячеек 100*100мм. используется для придания большей прочности бетонным конструкциям таким как: отмостка, наливные полы, бетонные площадки и т.д.\n</div>\n<div class="clear__both"></div>\n\n<p class="made_in">Сетка произведена в Тирасполе. Осуществляем доставку в Тирасполь, Бендеры, Парканы, Малаешты, Слободзею и другие направления. </p>\n	setka2.jpg	setka_100X100	2	42.00	\N	\N	\N	\N	0.3	\N	\N	\N
\.


--
-- Data for Name: product_img; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.product_img (id, product_id, link, order_num) FROM stdin;
\.


--
-- Data for Name: seller; Type: TABLE DATA; Schema: public; Owner: geronda
--

COPY public.seller (id, name, description, address, phone, telegram, email, logo, avatar) FROM stdin;
1	self	self	aval	77553291	15444654565	iiiliev.igor@gmail.com	\N	\N
2	Аваль	Цемент Песок Гравий	Мегатранс	77782349	15444654565	iiiliev.igor@gmail.com	\N	\N
3	Кирпичок	Кирпичи, бетонные изделия, печное оборудование	Мегатранс	77782349	15444654565	nikolay@gmail.com	\N	\N
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: geronda
--

SELECT pg_catalog.setval('public.categories_id_seq', 5, true);


--
-- Name: delivery_price_id_seq; Type: SEQUENCE SET; Schema: public; Owner: geronda
--

SELECT pg_catalog.setval('public.delivery_price_id_seq', 6, true);


--
-- Name: drivers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: geronda
--

SELECT pg_catalog.setval('public.drivers_id_seq', 1, false);


--
-- Name: load_price_id_seq; Type: SEQUENCE SET; Schema: public; Owner: geronda
--

SELECT pg_catalog.setval('public.load_price_id_seq', 5, true);


--
-- Name: loaders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: geronda
--

SELECT pg_catalog.setval('public.loaders_id_seq', 1, false);


--
-- Name: order_info_id_seq; Type: SEQUENCE SET; Schema: public; Owner: geronda
--

SELECT pg_catalog.setval('public.order_info_id_seq', 9, true);


--
-- Name: product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: geronda
--

SELECT pg_catalog.setval('public.product_id_seq', 24, true);


--
-- Name: product_img_id_seq; Type: SEQUENCE SET; Schema: public; Owner: geronda
--

SELECT pg_catalog.setval('public.product_img_id_seq', 1, false);


--
-- Name: seller_id_seq; Type: SEQUENCE SET; Schema: public; Owner: geronda
--

SELECT pg_catalog.setval('public.seller_id_seq', 3, true);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: delivery_price delivery_price_pkey; Type: CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.delivery_price
    ADD CONSTRAINT delivery_price_pkey PRIMARY KEY (id);


--
-- Name: drivers drivers_pkey; Type: CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT drivers_pkey PRIMARY KEY (id);


--
-- Name: load_price load_price_pkey; Type: CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.load_price
    ADD CONSTRAINT load_price_pkey PRIMARY KEY (id);


--
-- Name: loaders loaders_pkey; Type: CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.loaders
    ADD CONSTRAINT loaders_pkey PRIMARY KEY (id);


--
-- Name: order_info order_info_pkey; Type: CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.order_info
    ADD CONSTRAINT order_info_pkey PRIMARY KEY (id);


--
-- Name: product_img product_img_pkey; Type: CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.product_img
    ADD CONSTRAINT product_img_pkey PRIMARY KEY (id);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- Name: seller seller_pkey; Type: CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.seller
    ADD CONSTRAINT seller_pkey PRIMARY KEY (id);


--
-- Name: cat_prod cat_prod_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.cat_prod
    ADD CONSTRAINT cat_prod_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: cat_prod cat_prod_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.cat_prod
    ADD CONSTRAINT cat_prod_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id);


--
-- Name: order_delivery order_delivery_delivery_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.order_delivery
    ADD CONSTRAINT order_delivery_delivery_id_fkey FOREIGN KEY (delivery_id) REFERENCES public.delivery_price(id);


--
-- Name: order_delivery order_delivery_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.order_delivery
    ADD CONSTRAINT order_delivery_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.order_info(id);


--
-- Name: order_info order_info_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.order_info
    ADD CONSTRAINT order_info_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(id);


--
-- Name: order_info order_info_loader_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.order_info
    ADD CONSTRAINT order_info_loader_id_fkey FOREIGN KEY (loader_id) REFERENCES public.loaders(id);


--
-- Name: order_loaders order_loaders_load_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.order_loaders
    ADD CONSTRAINT order_loaders_load_id_fkey FOREIGN KEY (load_id) REFERENCES public.load_price(id);


--
-- Name: order_loaders order_loaders_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.order_loaders
    ADD CONSTRAINT order_loaders_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.order_info(id);


--
-- Name: order_products order_products_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.order_products
    ADD CONSTRAINT order_products_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.order_info(id);


--
-- Name: order_products order_products_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.order_products
    ADD CONSTRAINT order_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id);


--
-- Name: order_products order_products_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.order_products
    ADD CONSTRAINT order_products_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.seller(id);


--
-- Name: product_img product_img_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.product_img
    ADD CONSTRAINT product_img_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id);


--
-- Name: product product_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: geronda
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.seller(id);


--
-- PostgreSQL database dump complete
--

