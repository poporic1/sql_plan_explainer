DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    status TEXT NOT NULL,
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_name TEXT NOT NULL,
    qty INT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    CONSTRAINT fk_items_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

INSERT INTO customers
SELECT
    i,
    'customer_' || i,
    CASE
        WHEN i % 3 = 0 THEN 'Moscow'
        WHEN i % 3 = 1 THEN 'Kazan'
        ELSE 'SPB'
    END
FROM generate_series(1, 1000) AS s(i);

INSERT INTO orders
SELECT
    i,
    ((i - 1) % 1000) + 1,
    DATE '2026-01-01' + ((i - 1) % 30),
    (100 + (i % 500))::numeric,
    CASE
        WHEN i % 5 = 0 THEN 'cancelled'
        ELSE 'paid'
    END
FROM generate_series(1, 100000) AS s(i);

INSERT INTO order_items
SELECT
    i,
    ((i - 1) % 100000) + 1,
    'product_' || ((i - 1) % 100),
    ((i - 1) % 5) + 1,
    (50 + ((i - 1) % 50))::numeric
FROM generate_series(1, 200000) AS s(i);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_items_order_id ON order_items(order_id);