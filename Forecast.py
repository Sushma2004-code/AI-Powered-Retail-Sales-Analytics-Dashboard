import streamlit as st
import pandas as pd
from prophet import Prophet

def show():

    st.title("🔮 Sales Forecast Dashboard")

    # ----------------------------
    # LOAD DATA
    # ----------------------------
    @st.cache_data
    def load_data():
        df = pd.read_csv("retail_sales_dataset.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        df['Revenue'] = df['Quantity'] * df['Price']
        df = df[['Date', 'Revenue']].dropna().sort_values('Date')
        return df

    df = load_data()

    if df.empty:
        st.warning("⚠️ No data available")
        return

    # ----------------------------
    # SIDEBAR SETTINGS
    # ----------------------------
    st.sidebar.header("⚙️ Forecast Settings")

    periods = st.sidebar.slider(
        "Forecast Days",
        min_value=30,
        max_value=180,
        value=90
    )

    # ----------------------------
    # PREPARE DATA
    # ----------------------------
    df_prophet = df.rename(columns={'Date': 'ds', 'Revenue': 'y'})

    # ----------------------------
    # MODEL TRAINING
    # ----------------------------
    @st.cache_resource
    def train_model(data):
        model = Prophet()
        model.fit(data)
        return model

    if len(df_prophet) > 15:

        with st.spinner("📊 Training forecasting model..."):
            model = train_model(df_prophet)

            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)

        # ----------------------------
        # FORECAST CHART
        # ----------------------------
        st.subheader("📈 Forecast Trend")
        st.line_chart(forecast.set_index('ds')['yhat'])

        # ----------------------------
        # METRICS
        # ----------------------------
        latest = forecast.iloc[-1]['yhat']
        current = df_prophet['y'].iloc[-1]

        st.markdown("### 📊 Forecast Insights")

        col1, col2 = st.columns(2)
        col1.metric("Current Revenue", f"₹{current:,.0f}")
        col2.metric(f"Predicted Revenue ({periods} days)", f"₹{latest:,.0f}")

        # ----------------------------
        # INTERPRETATION
        # ----------------------------
        if latest > current:
            st.success("📈 Sales are expected to grow.")
        else:
            st.warning("📉 Sales may decline.")

        # ----------------------------
        # COMPONENTS (ADVANCED)
        # ----------------------------
        st.subheader("📊 Forecast Components")
        fig = model.plot_components(forecast)
        st.pyplot(fig)

    else:
        st.warning("⚠️ Not enough data (minimum 15 records required)")