import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show():

    st.title("📊 Dashboard")

    # ----------------------------
    # LOAD DATA
    # ----------------------------
    @st.cache_data
    def load_data():
        df = pd.read_csv("retail_sales_dataset.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        df['Revenue'] = df['Quantity'] * df['Price']
        return df

    df = load_data()

    # ----------------------------
    # FILTERS
    # ----------------------------
    st.sidebar.title("📊 Filters")

    store_filter = st.sidebar.multiselect(
        "Store", df['Store'].unique(), default=df['Store'].unique()
    )

    category_filter = st.sidebar.multiselect(
        "Category", df['Category'].unique(), default=df['Category'].unique()
    )

    start_date = st.sidebar.date_input("Start Date", df['Date'].min())
    end_date = st.sidebar.date_input("End Date", df['Date'].max())

    # ----------------------------
    # FILTER DATA
    # ----------------------------
    df_filtered = df[
        (df['Store'].isin(store_filter)) &
        (df['Category'].isin(category_filter)) &
        (df['Date'] >= pd.to_datetime(start_date)) &
        (df['Date'] <= pd.to_datetime(end_date))
    ]

    if df_filtered.empty:
        st.warning("⚠️ No data available")
        return

    # ----------------------------
    # CALCULATIONS
    # ----------------------------
    total_revenue = df_filtered['Revenue'].sum()
    total_orders = len(df_filtered)
    total_quantity = df_filtered['Quantity'].sum()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    category_sales = df_filtered.groupby('Category')['Revenue'].sum()
    product_sales = df_filtered.groupby('Product')['Revenue'].sum()

    # ----------------------------
    # KPIs
    # ----------------------------
    st.markdown("## 📊 Key Metrics")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Revenue", f"₹{total_revenue:,.0f}")
    c2.metric("📦 Orders", total_orders)
    c3.metric("🛍️ Quantity", total_quantity)
    c4.metric("💸 Avg Order", f"₹{avg_order_value:.2f}")

    # ----------------------------
    # CHARTS
    # ----------------------------
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Monthly Trend")
        monthly = df_filtered.groupby('Month')['Revenue'].sum().reset_index()
        fig, ax = plt.subplots()
        sns.lineplot(data=monthly, x='Month', y='Revenue', ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("📅 Yearly Trend")
        yearly = df_filtered.groupby('Year')['Revenue'].sum()
        st.line_chart(yearly)

    # ----------------------------
    # DOWNLOAD REPORT
    # ----------------------------
    report = f"""
    Retail Sales Report

    Revenue: ₹{total_revenue:,.0f}
    Orders: {total_orders}
    Quantity: {total_quantity}
    Avg Order Value: ₹{avg_order_value:.2f}

    Top Category: {category_sales.idxmax()}
    Top Product: {product_sales.idxmax()}
    """

    st.download_button("📥 Download Report", report, "report.txt")