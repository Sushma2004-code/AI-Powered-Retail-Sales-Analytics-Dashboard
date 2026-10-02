import streamlit as st
import pandas as pd

def show():

    st.title("📌 Business Insights Dashboard")

    # ----------------------------
    # LOAD DATA
    # ----------------------------
    @st.cache_data
    def load_data():
        df = pd.read_csv("retail_sales_dataset.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        df['Revenue'] = df['Quantity'] * df['Price']
        return df

    df = load_data()

    if df.empty:
        st.warning("⚠️ No data available")
        return

    # ----------------------------
    # CALCULATIONS
    # ----------------------------
    category_sales = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
    product_sales = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False)

    top_category = category_sales.idxmax()
    low_category = category_sales.idxmin()
    top_product = product_sales.idxmax()

    # ----------------------------
    # KPI SECTION
    # ----------------------------
    st.markdown("## 📊 Key Highlights")

    c1, c2, c3 = st.columns(3)
    c1.success(f"🏆 Top Category\n\n{top_category}")
    c2.info(f"🔥 Top Product\n\n{top_product}")
    c3.warning(f"📉 Low Category\n\n{low_category}")

    # ----------------------------
    # VISUAL ANALYSIS
    # ----------------------------
    st.markdown("## 📈 Revenue Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Category Performance")
        st.bar_chart(category_sales)

    with col2:
        st.subheader("Top Products")
        st.bar_chart(product_sales.head(10))

    # ----------------------------
    # SMART INSIGHTS
    # ----------------------------
    st.markdown("## 🧠 Smart Insights")

    insights = []

    if category_sales.iloc[0] > category_sales.mean():
        insights.append("Top category is significantly outperforming others.")

    if category_sales.iloc[-1] < category_sales.mean():
        insights.append("Lowest category is underperforming and needs attention.")

    if product_sales.iloc[0] > product_sales.mean():
        insights.append("Top product drives major revenue contribution.")

    if len(product_sales) > 5:
        insights.append("Revenue is concentrated in top few products.")

    for insight in insights:
        st.write(f"✔️ {insight}")

    # ----------------------------
    # RECOMMENDATIONS
    # ----------------------------
    st.markdown("## 🚀 Business Recommendations")

    recommendations = [
        "Increase inventory for top-performing products",
        "Launch offers on low-performing categories",
        "Focus marketing on high-revenue segments",
        "Use seasonal analysis for demand forecasting",
    ]

    for rec in recommendations:
        st.write(f"👉 {rec}")

    # ----------------------------
    # EXPORT REPORT
    # ----------------------------
    st.markdown("## 📥 Export Insights")

    report = f"""
BUSINESS INSIGHTS REPORT

Top Category: {top_category}
Top Product: {top_product}
Low Category: {low_category}

Insights:
- {'; '.join(insights)}

Recommendations:
- {'; '.join(recommendations)}
"""

    st.download_button(
        "📥 Download Full Report",
        report,
        "business_insights.txt"
    )