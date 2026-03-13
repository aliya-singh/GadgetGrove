import sqlite3
import pandas as pd
import json

def run_etl_pipeline(db_name="gadgetgrove.db", nosql_file="mongo_reviews.json"):
    # --- 1. EXTRACT ---
    conn = sqlite3.connect(db_name)
    
    # Extract SQL data using a Join for a unified transaction view
    query = """
    SELECT 
        o.order_id, o.order_date, o.quantity,
        c.customer_id, c.customer_name,
        p.product_id, p.product_name, p.category, p.price
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products p ON o.product_id = p.product_id
    """
    df_orders = pd.read_sql_query(query, conn)
    
    # Extract NoSQL data (Reviews)
    with open(nosql_file, 'r') as f:
        reviews_data = json.load(f)
    df_reviews = pd.DataFrame(reviews_data)

    # --- 2. TRANSFORM ---
    # Merge SQL (Orders) with NoSQL (Reviews)
    # Left join because not every order has a review
    df_merged = pd.merge(
        df_orders, 
        df_reviews[['product_id', 'customer_id', 'rating']], 
        on=['product_id', 'customer_id'], 
        how='left'
    )

    # Handle missing data: Fill NaN ratings with 0 (neutral/none)
    df_merged['rating'] = df_merged['rating'].fillna(0).astype(int)

    # Calculate Total Price (Quantity * Price)
    df_merged['total_price'] = df_merged['quantity'] * df_merged['price']

    # Logic for is_satisfied: True if rating is 4 or 5
    df_merged['is_satisfied'] = df_merged['rating'].apply(lambda x: 1 if x >= 4 else 0)

    # --- 3. LOAD (Star Schema) ---
    cursor = conn.cursor()

    # A. Create Dimension Table: dim_product_report
    cursor.execute("DROP TABLE IF EXISTS dim_product_report")
    cursor.execute("""
        CREATE TABLE dim_product_report (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT
        )
    """)
    
    dim_products = df_merged[['product_id', 'product_name', 'category']].drop_duplicates()
    dim_products.to_sql('dim_product_report', conn, if_exists='append', index=False)

    # B. Create Fact Table: fact_sales_reviews
    cursor.execute("DROP TABLE IF EXISTS fact_sales_reviews")
    cursor.execute("""
        CREATE TABLE fact_sales_reviews (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            customer_id INTEGER,
            order_date DATE,
            quantity INTEGER,
            total_price REAL,
            rating INTEGER,
            is_satisfied INTEGER,
            FOREIGN KEY (product_id) REFERENCES dim_product_report (product_id)
        )
    """)

    fact_data = df_merged[[
        'order_id', 'product_id', 'customer_id', 'order_date', 
        'quantity', 'total_price', 'rating', 'is_satisfied'
    ]]
    fact_data.to_sql('fact_sales_reviews', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()
    
    return f"ETL successful! {len(df_merged)} records processed into Star Schema."