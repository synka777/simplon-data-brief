-- schema.sql

-- Enable foreign keys (important for SQLite)
PRAGMA foreign_keys = ON;

-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    name TEXT NOT NULL,
    id VARCHAR PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    qty INTEGER NOT NULL
);

-- Create the shops table
CREATE TABLE IF NOT EXISTS shops (
    id INTEGER PRIMARY KEY,
    city VARCHAR(255) NOT NULL,
    employees INTEGER NOT NULL
);

-- Create the orders table
CREATE TABLE IF NOT EXISTS orders (
    order_date DATE NOT NULL,
    product_id VARCHAR NOT NULL,
    qty INTEGER NOT NULL,
    shop_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);
