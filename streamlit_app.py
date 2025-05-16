import streamlit as st
import pandas as pd

st.set_page_config(page_title="Shopify Returns Dashboard", layout="wide")
st.title("📦 Shopify Clean Returns Dashboard")
st.markdown("Shows only **non-cancelled refunded orders** (clean returns).")

# Load the CSV file
try:
    df = pd.read_csv("dazzle_returns_clean.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # KPIs
    total_refunds = df["Total Refunded"].sum()
    total_orders = df["Order ID"].nunique()

    col1, col2 = st.columns(2)
    col1.metric("💰 Total Refund Amount", f"${total_refunds:,.2f}")
    col2.metric("🔁 Number of Returned Orders", total_orders)

    # Returns over time
    df_by_date = df.groupby(df["Order Date"].dt.date)["Total Refunded"].sum().reset_index()
    st.subheader("📈 Returns Over Time")
    st.line_chart(df_by_date.set_index("Order Date"))

    # Table
    st.subheader("🧾 Return Order Details")
    st.dataframe(df.sort_values("Order Date", ascending=False))

except FileNotFoundError:
    st.error("❌ File not found. Make sure 'dazzle_returns_clean.csv' is in the same folder.")
