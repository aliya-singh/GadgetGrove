import streamlit as st
import pandas as pd
import sqlite3
import os
from database_manager import setup_sql_database
from nosql_manager import setup_nosql_data
from etl_pipeline import run_etl_pipeline
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# --- Page Configuration ---
st.set_page_config(page_title="GadgetGrove Analytics", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stMetric { background-color: #000; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("🛠 Pipeline Control")
app_mode = st.sidebar.selectbox("Choose the Stage", ["1. Data Setup", "2. Run ETL", "3. Analytics Dashboard"])

st.title("🚀 GadgetGrove: Miniature Customer Analytics Pipeline")

# --- DB Helper Function ---
def get_db_connection():
    return sqlite3.connect("gadgetgrove.db")

# --- Mode 1: Data Setup ---
if app_mode == "1. Data Setup":
    st.header("Step 1: Raw Data Generation")
    st.info("This stage simulates our operational SQL and NoSQL environments.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Initialize SQL DB (SQLite)"):
            msg = setup_sql_database()
            st.success(msg)
            
    with col2:
        if st.button("Initialize NoSQL Store (JSON/Mongo)"):
            msg = setup_nosql_data()
            st.success(msg)

    if os.path.exists("gadgetgrove.db"):
        st.subheader("Preview: Raw Orders (SQL)")
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM orders LIMIT 5", conn)
        st.dataframe(df, use_container_width=True)
        conn.close()

# --- Mode 2: Run ETL ---
elif app_mode == "2. Run ETL":
    st.header("Step 2: Transform & Load")
    st.write("Merging relational order data with flexible review documents into a Star Schema.")
    
    if st.button("Execute ETL Pipeline"):
        with st.spinner("Processing data..."):
            result = run_etl_pipeline()
            st.success(result)
            
            # Show the newly created Star Schema tables
            conn = get_db_connection()
            st.subheader("Fact Table: fact_sales_reviews")
            df_fact = pd.read_sql_query("SELECT * FROM fact_sales_reviews LIMIT 5", conn)
            st.dataframe(df_fact, use_container_width=True)
            conn.close()

# --- Mode 3: Analytics Dashboard (ENHANCED) ---
elif app_mode == "3. Analytics Dashboard":
    st.header("Step 3: Marketing Insights Dashboard")
    
    try:
        conn = get_db_connection()
        df_final = pd.read_sql_query("""
            SELECT f.*, p.product_name, p.category 
            FROM fact_sales_reviews f
            JOIN dim_product_report p ON f.product_id = p.product_id
        """, conn)
        conn.close()

        # --- Top Metrics (as before) ---
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Revenue", f"${df_final['total_price'].sum():,.2f}")
        m2.metric("Avg Rating (Excl. Unrated)", round(df_final[df_final['rating'] > 0]['rating'].mean(), 2))
        m3.metric("Satisfied Orders (Rating 4+)", df_final['is_satisfied'].sum())
        m4.metric("Unrated Orders", len(df_final[df_final['rating'] == 0]))
        st.divider()

        # --- CREATIVE EXTENSION 1: Interactive Plotly Viz ---
        st.subheader("💡 Revenue & Satisfaction by Category")
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.write("**Product Category Revenue (Click to explore)**")
            fig_rev = px.sunburst(df_final, path=['category', 'product_name'], values='total_price', color='total_price', color_continuous_scale='RdBu')
            st.plotly_chart(fig_rev, use_container_width=True)

        with col_chart2:
            st.write("**Is_Satisfied Distribution by Category**")
            fig_sat = px.histogram(df_final, x="category", color="is_satisfied", barmode="group", labels={'is_satisfied': 'Satisfied (1=Yes, 0=No)'}, color_discrete_map={1: '#198754', 0: '#dc3545'})
            st.plotly_chart(fig_sat, use_container_width=True)


        # --- CREATIVE EXTENSION 2: Advanced Seaborn Heatmap ---
        st.subheader("🔥 Satisfaction Heatmap: Product vs. Month")
        
        # Transform data for heatmap
        df_heatmap = df_final.copy()
        df_heatmap['order_month'] = pd.to_datetime(df_heatmap['order_date']).dt.strftime('%B')
        heatmap_data = df_heatmap.pivot_table(index='product_name', columns='order_month', values='is_satisfied', aggfunc=np.mean).fillna(0)

        # Plot Seaborn Heatmap in Streamlit
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(heatmap_data, cmap="Greens", annot=True, fmt=".1f", linewidths=.5, ax=ax)
        plt.title("Average Satisfaction (1=100% Satisfied)")
        plt.xlabel("Month")
        plt.ylabel("Product")
        st.pyplot(fig)


        # --- SCENARIO ANSWER: Top Products Among Satisfied Customers ---
        st.divider()
        st.subheader("🏆 Marketing Gold: Top Products Among Satisfied Customers")
        
        # Filter for satisfied customers, group, count, and sort
        df_satisfied = df_final[df_final['is_satisfied'] == 1]
        top_products = df_satisfied.groupby('product_name')['quantity'].sum().reset_index().sort_values(by='quantity', ascending=False)
        
        # Rename column for clarity
        top_products = top_products.rename(columns={'quantity': 'Total Units Sold to Satisfied Customers'})
        
        st.markdown("This list identifies **high-performing products** that are driving customer satisfaction, indicating good **product-market fit**. Focus marketing efforts here!")
        st.dataframe(top_products, use_container_width=True)


    except Exception as e:
        st.error(f"Error: Please run the ETL pipeline first to generate the analytics data! (Details: {e})")