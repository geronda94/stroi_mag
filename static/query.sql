SELECT
    p.name AS product_name,
    p.description AS product_description,
    p.link AS product_link,
    c.name AS category_name,
    c.description AS category_description,
    s.name AS seller_name,
    s.description AS seller_description,
    s.address AS seller_address,
    s.phone AS seller_phone,
    s.telegram AS seller_telegram,
    s.email AS seller_email
FROM
    product p
    JOIN cat_prod cp ON p.id = cp.product_id
    JOIN categories c ON cp.category_id = c.id
    JOIN seller s ON p.seller_id = s.id
WHERE
    cp.category_id = 1
ORDER BY
    p.order_num;
