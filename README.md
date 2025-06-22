
#  E-Commerce ETL & Streamlit Dashboard

###  Overview

This project performs a complete ETL pipeline and provides an interactive Streamlit dashboard using raw e-commerce data from JSON and CSV formats.

###  Features

-  Upload raw customer, product, and order files
-  ETL: Cleans messy data (nulls, date formats, casing, types)
-  Visualizes cleaned data in a Streamlit UI
- Exports cleaned CSVs for downstream use

###  Project Structure

```
techcorp_etl_streamlit/
├── etl_streamlit_app.py      # All-in-one ETL + Streamlit dashboard
├── README.md
```

###  How to Run

1. Install Streamlit:
```bash
pip install streamlit pandas numpy
```

2. Run the app:
```bash
streamlit run etl_streamlit_app.py
```

3. Upload the following when prompted:
- `customers_messy_data.json`
- `products_inconsistent_data.json`
- `orders_unstructured_data.csv`

### Output

- `cleaned_customers.csv`
- `cleaned_products.csv`
- `cleaned_orders.csv`

These files are saved locally after the ETL process and displayed in the dashboard.

---

Made for TechCorp Internship Assignment by vaishnavi gaikwad
