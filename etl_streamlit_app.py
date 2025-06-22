# etl_streamlit_app.py

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import os

st.set_page_config(layout="wide", page_title="E-Commerce ETL + Dashboard")

st.title("🛍️ E-Commerce ETL Pipeline and Streamlit Dashboard")

# -----------------------
# Step 1: Upload Raw Files
# -----------------------

st.sidebar.header("📤 Upload Raw Files")
customer_file = st.sidebar.file_uploader("Upload customers_messy_data.json", type=["json"])
product_file = st.sidebar.file_uploader("Upload products_inconsistent_data.json", type=["json"])
order_file = st.sidebar.file_uploader("Upload orders_unstructured_data.csv", type=["csv"])

if customer_file and product_file and order_file:
    st.success("All files uploaded. Starting ETL process...")

    # -----------------------
    # Step 2: Load Raw Data
    # -----------------------

    customers = pd.read_json(customer_file)
    products = pd.read_json(product_file)
    orders = pd.read_csv(order_file)

    # -----------------------
    # Step 3: Define Cleaning Functions
    # -----------------------

    def clean_nulls(df):
        return df.replace(['', 'null', 'NULL', 'N/A', 'n/a', None], np.nan)

    def normalize_case(df, columns):
        for col in columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.lower()
        return df

    def convert_numeric(df, columns):
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def convert_dates(df, columns):
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df

    # -----------------------
    # Step 4: Clean Customers
    # -----------------------

    customers['name'] = customers['customer_name'].combine_first(customers['full_name'])
    customers['email_clean'] = customers['email'].combine_first(customers['email_address'])
    customers['phone_clean'] = customers['phone'].combine_first(customers['phone_number'])
    customers['registration_date'] = customers['registration_date'].combine_first(customers['reg_date'])

    customers = clean_nulls(customers)
    customers = normalize_case(customers, ['status', 'customer_status', 'gender', 'segment'])
    customers = convert_numeric(customers, ['total_orders', 'total_spent', 'loyalty_points', 'age'])
    customers = convert_dates(customers, ['registration_date', 'birth_date'])

    # -----------------------
    # Step 5: Clean Products
    # -----------------------

    products['product_name_clean'] = products['product_name'].combine_first(products['item_name'])
    products['category_clean'] = products['category'].combine_first(products['product_category'])

    products = clean_nulls(products)
    products = normalize_case(products, ['brand', 'manufacturer', 'category', 'product_category'])
    products = convert_numeric(products, ['price', 'list_price', 'cost', 'weight', 'rating'])
    products = convert_dates(products, ['created_date', 'last_updated'])

    # -----------------------
    # Step 6: Clean Orders
    # -----------------------

    orders = clean_nulls(orders)
    orders = convert_dates(orders, ['order_date'])
    orders = convert_numeric(orders, ['quantity', 'order_total'])

    # -----------------------
    # Step 7: Save Cleaned CSVs
    # -----------------------

    customers.to_csv("cleaned_customers.csv", index=False)
    products.to_csv("cleaned_products.csv", index=False)
    orders.to_csv("cleaned_orders.csv", index=False)

    st.success("✅ ETL Completed. Cleaned data saved as CSV.")

    # -----------------------
    # Step 8: Streamlit Dashboard
    # -----------------------

    st.header("📊 Interactive Dashboard")

    tab1, tab2, tab3 = st.tabs(["👥 Customers", "📦 Products", "🧾 Orders"])

    with tab1:
        st.subheader("Cleaned Customers")
        st.dataframe(customers)
        st.metric("Total Customers", customers['cust_id'].nunique())
        st.metric("Avg Spend", round(customers['total_spent'].mean(), 2))

    with tab2:
        st.subheader("Cleaned Products")
        st.dataframe(products)
        st.metric("Total Products", products['product_id'].nunique())
        st.metric("Avg Price", round(products['price'].mean(), 2))

    with tab3:
        st.subheader("Cleaned Orders")
        st.dataframe(orders)
        st.metric("Total Orders", len(orders))
        st.metric("Total Revenue", round(orders['order_total'].sum(), 2))

else:
    st.warning("Please upload all three files to begin.")
