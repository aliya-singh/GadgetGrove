import sqlite3
import pandas as pd

def setup_sql_database(db_name="gadgetgrove.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create Tables
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT,
            registration_date DATE
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            price REAL
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            order_date DATE,
            quantity INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        );
    ''')
    
    # Insert Initial Synthetic Data
    customers = [
        (1, 'Alice Wang', '2023-01-15'), (2, 'Bob Smith', '2023-02-20'),
        (3, 'Charlie Brown', '2023-03-10'), (4, 'David Miller', '2023-04-05'),
        (5, 'Eve Torres', '2023-05-12'), (6, 'Frank Wright', '2023-06-01'),
        (7, 'Grace Lee', '2023-07-22'), (8, 'Hank Hill', '2023-08-30'),
        (9, 'Ivy Chen', '2023-09-14'), (10, 'Jack Ross', '2023-10-05')
    ]
    
    products = [
        (101, 'Quantum Watch', 'Wearables', 199.99),
        (102, 'Sonic Headphones', 'Audio', 149.50),
        (103, 'Pixel Tablet', 'Computing', 499.00),
        (104, 'Glow Keyboard', 'Accessories', 89.99),
        (105, 'Nova Phone', 'Mobile', 799.00)
    ]

    cursor.executemany("INSERT OR IGNORE INTO customers VALUES (?,?,?)", customers)
    cursor.executemany("INSERT OR IGNORE INTO products VALUES (?,?,?,?)", products)
    
    # 20 Synthetic Orders
    orders = [
        (501, 1, 101, '2024-01-01', 1), (502, 2, 102, '2024-01-02', 1),
        (503, 1, 103, '2024-01-05', 1), (504, 3, 101, '2024-01-06', 2),
        (505, 4, 105, '2024-01-10', 1), (506, 5, 104, '2024-01-12', 1),
        (507, 2, 101, '2024-01-15', 1), (508, 6, 102, '2024-01-16', 3),
        (509, 7, 103, '2024-01-20', 1), (510, 8, 105, '2024-01-21', 1),
        (511, 9, 101, '2024-01-25', 1), (512, 10, 102, '2024-01-26', 1),
        (513, 1, 105, '2024-02-01', 1), (514, 3, 102, '2024-02-03', 1),
        (515, 4, 104, '2024-02-05', 2), (516, 5, 101, '2024-02-07', 1),
        (517, 2, 103, '2024-02-10', 1), (518, 6, 105, '2024-02-12', 1),
        (519, 7, 104, '2024-02-15', 1), (520, 8, 102, '2024-02-18', 1)
    ]
    cursor.executemany("INSERT OR IGNORE INTO orders VALUES (?,?,?,?,?)", orders)

    conn.commit()
    conn.close()
    return "SQL Database initialized with 10 customers, 5 products, and 20 orders."