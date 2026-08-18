import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="E-Commerce Sales Dashboard", layout="wide")

st.title("📊 E-Commerce Sales Dashboard")
st.caption("Upload your raw sales CSV to clean it and explore revenue, category, and product trends.")

# ------------------------------------------------------------------
# FILE UPLOAD
# ------------------------------------------------------------------
uploaded_file = st.file_uploader("Upload your sales CSV file", type=["csv"])

if uploaded_file is None:
    st.info("👆 Upload a CSV file to get started. Expected columns include things like "
            "Order_Date, Quantity, Price, Category, Total, Payment_Method, Status, Product.")
    st.stop()

df = pd.read_csv(uploaded_file)

# ------------------------------------------------------------------
# CLEANING (mirrors the notebook logic)
# ------------------------------------------------------------------
clean_df = df.copy()
clean_df.columns = clean_df.columns.str.strip()

if "Order_Date" in clean_df.columns:
    clean_df["Order_Date"] = pd.to_datetime(clean_df["Order_Date"], errors="coerce")
    clean_df = clean_df.dropna(subset=["Order_Date"])

if "Quantity" in clean_df.columns:
    clean_df["Quantity"] = pd.to_numeric(clean_df["Quantity"], errors="coerce")

if "Price" in clean_df.columns:
    clean_df["Price"] = (
        clean_df["Price"].astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    clean_df["Price"] = pd.to_numeric(clean_df["Price"], errors="coerce")

clean_df = clean_df.drop_duplicates()

if "Category" in clean_df.columns:
    clean_df["Category"] = clean_df["Category"].fillna("Unknown")

if "Quantity" in clean_df.columns:
    clean_df["Quantity"] = clean_df["Quantity"].fillna(clean_df["Quantity"].median())

if "Price" in clean_df.columns:
    clean_df["Price"] = clean_df["Price"].fillna(clean_df["Price"].median())

if "Total" not in clean_df.columns and {"Quantity", "Price"}.issubset(clean_df.columns):
    clean_df["Total"] = clean_df["Quantity"] * clean_df["Price"]
elif "Total" in clean_df.columns and {"Quantity", "Price"}.issubset(clean_df.columns):
    calculated_total = clean_df["Quantity"] * clean_df["Price"]
    clean_df["Total"] = clean_df["Total"].fillna(calculated_total)

# ------------------------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------------------------
st.sidebar.header("Filters")

if "Order_Date" in clean_df.columns and not clean_df["Order_Date"].isna().all():
    min_date = clean_df["Order_Date"].min().date()
    max_date = clean_df["Order_Date"].max().date()
    date_range = st.sidebar.date_input("Date range", value=(min_date, max_date),
                                        min_value=min_date, max_value=max_date)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        clean_df = clean_df[
            (clean_df["Order_Date"].dt.date >= start) & (clean_df["Order_Date"].dt.date <= end)
        ]

if "Category" in clean_df.columns:
    categories = sorted(clean_df["Category"].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
    clean_df = clean_df[clean_df["Category"].isin(selected_categories)]

# ------------------------------------------------------------------
# KPI METRICS
# ------------------------------------------------------------------
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_revenue = clean_df["Total"].sum() if "Total" in clean_df.columns else np.nan
total_quantity = clean_df["Quantity"].sum() if "Quantity" in clean_df.columns else np.nan
avg_order_value = clean_df["Total"].mean() if "Total" in clean_df.columns else np.nan
num_orders = len(clean_df)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}" if pd.notna(total_revenue) else "N/A")
col2.metric("Total Quantity Sold", f"{total_quantity:,.0f}" if pd.notna(total_quantity) else "N/A")
col3.metric("Average Order Value", f"₹{avg_order_value:,.2f}" if pd.notna(avg_order_value) else "N/A")
col4.metric("Number of Orders", f"{num_orders:,}")

st.divider()

# ------------------------------------------------------------------
# CHARTS
# ------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Revenue by Category", "Quantity by Category", "Payment Method",
     "Order Status", "Top Products"]
)

with tab1:
    if {"Category", "Total"}.issubset(clean_df.columns):
        category_sales = clean_df.groupby("Category")["Total"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(category_sales, x="Category", y="Total", title="Revenue by Category")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Missing Category or Total column.")

with tab2:
    if {"Category", "Quantity"}.issubset(clean_df.columns):
        category_qty = clean_df.groupby("Category")["Quantity"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(category_qty, x="Category", y="Quantity", title="Quantity Sold by Category")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Missing Category or Quantity column.")

with tab3:
    if {"Payment_Method", "Total"}.issubset(clean_df.columns):
        payment_sales = clean_df.groupby("Payment_Method")["Total"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(payment_sales, x="Payment_Method", y="Total", title="Revenue by Payment Method")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Missing Payment_Method or Total column.")

with tab4:
    if "Status" in clean_df.columns:
        status_counts = clean_df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig = px.bar(status_counts, x="Status", y="Count", title="Order Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Missing Status column.")

with tab5:
    if {"Product", "Total"}.issubset(clean_df.columns):
        product_sales = clean_df.groupby("Product")["Total"].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(product_sales, x="Product", y="Total", title="Top 10 Products by Revenue")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Missing Product or Total column.")

st.divider()

# ------------------------------------------------------------------
# DAILY SALES TREND
# ------------------------------------------------------------------
st.subheader("Daily Sales Trend")

if {"Order_Date", "Total"}.issubset(clean_df.columns):
    daily_sales = clean_df.groupby("Order_Date")["Total"].sum().reset_index().sort_values("Order_Date")
    fig = px.line(daily_sales, x="Order_Date", y="Total", title="Daily Sales Trend")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Missing Order_Date or Total column.")

st.divider()

# ------------------------------------------------------------------
# CLEANED DATA + DOWNLOAD
# ------------------------------------------------------------------
st.subheader("Cleaned Data Preview")
st.dataframe(clean_df.head(50), use_container_width=True)

csv_bytes = clean_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Cleaned Data as CSV",
    data=csv_bytes,
    file_name="cleaned_ecommerce_sales.csv",
    mime="text/csv"
)
