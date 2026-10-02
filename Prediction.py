import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Sales Prediction", layout="wide")

st.title("🔮 Sales Prediction Dashboard")

# ----------------------------
# LOAD DATA (CACHED)
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("retail_sales_dataset.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Revenue'] = df['Quantity'] * df['Price']
    df = df.sort_values('Date')
    return df

df = load_data()

if df.empty:
    st.warning("⚠️ No data available")
    st.stop()

# ----------------------------
# FEATURE ENGINEERING
# ----------------------------
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

monthly = df.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()

# Create time index (VERY IMPORTANT)
monthly['TimeIndex'] = range(len(monthly))

# ----------------------------
# MODEL (BETTER)
# ----------------------------
X = monthly[['TimeIndex']]
y = monthly['Revenue']

model = LinearRegression()
model.fit(X, y)

# ----------------------------
# FUTURE PREDICTION
# ----------------------------
future_periods = st.sidebar.slider("Months to Predict", 3, 24, 12)

future_index = list(range(len(monthly), len(monthly) + future_periods))
future_df = pd.DataFrame({'TimeIndex': future_index})

pred = model.predict(future_df)

# ----------------------------
# VISUALIZATION
# ----------------------------
st.subheader("📊 Actual vs Predicted")

fig, ax = plt.subplots()

# Actual
ax.plot(monthly['TimeIndex'], y, label="Actual", marker='o')

# Predicted
ax.plot(future_df['TimeIndex'], pred, linestyle='--', label="Predicted")

ax.set_xlabel("Time")
ax.set_ylabel("Revenue")
ax.legend()

st.pyplot(fig)

# ----------------------------
# METRICS
# ----------------------------
st.markdown("### 📈 Prediction Insights")

current = y.iloc[-1]
predicted = pred[-1]

col1, col2 = st.columns(2)

col1.metric("Latest Revenue", f"₹{current:,.0f}")
col2.metric("Future Prediction", f"₹{predicted:,.0f}")

# Interpretation
if predicted > current:
    st.success("📈 Business is expected to grow")
else:
    st.warning("📉 Growth slowdown expected")

# ----------------------------
# DOWNLOAD
# ----------------------------
future_output = pd.DataFrame({
    "TimeIndex": future_index,
    "Predicted Revenue": pred
})

st.download_button(
    "📥 Download Forecast",
    future_output.to_csv(index=False),
    "prediction.csv"
)