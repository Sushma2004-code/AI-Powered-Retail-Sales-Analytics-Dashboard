import streamlit as st
from database import create_table
from auth import login_page, logout

# ----------------------------
# IMPORT PAGES (IMPORTANT)
# ----------------------------
import Dashboard
import Insights
import Forecast
import AI_Assisstant
import Profile

# ----------------------------
# PAGE CONFIG (FIRST)
# ----------------------------
st.set_page_config(page_title="Retail AI Platform", layout="wide")

# ----------------------------
# INIT DATABASE
# ----------------------------
create_table()

# ----------------------------
# SESSION INIT
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ----------------------------
# LOGIN GATE
# ----------------------------
if not st.session_state.logged_in:
    login_page()
    st.stop()

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Insights", "Forecast", "AI Assistant", "Profile"]
)

# Logout button
logout()

# ----------------------------
# HEADER
# ----------------------------
st.title("🛒 Retail AI Platform")
st.success(f"Welcome {st.session_state.user} 👋")

# ----------------------------
# PAGE ROUTING (🔥 MOST IMPORTANT)
# ----------------------------
if page == "Dashboard":
    Dashboard.show()

elif page == "Insights":
    Insights.show()

elif page == "Forecast":
    Forecast.show()

elif page == "AI Assistant":
    AI_Assisstant.show()

elif page == "Profile":
    Profile.show()