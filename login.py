import streamlit as st
import time
from database import add_user, login_user, create_table, update_password

create_table()

# ----------------------------
# CONFIG
# ----------------------------
MAX_ATTEMPTS = 3
LOCK_TIME = 60  # seconds

# ----------------------------
# PASSWORD VALIDATION
# ----------------------------
def is_strong_password(password):
    return (
        len(password) >= 6 and
        any(c.isdigit() for c in password) and
        any(c.isalpha() for c in password)
    )

# ----------------------------
# SESSION INIT
# ----------------------------
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

if "lock_time" not in st.session_state:
    st.session_state.lock_time = 0

# ----------------------------
# LOGIN PAGE
# ----------------------------
def login():
    st.title("🔐 Retail AI Login System")

    menu = ["Login", "Register", "Forgot Password"]
    choice = st.selectbox("Select Option", menu)

    # ---------------- LOGIN ----------------
    if choice == "Login":
        with st.form("login_form"):
            username = st.text_input("Username").strip()
            password = st.text_input("Password", type="password")

            submit = st.form_submit_button("Login")

            # LOCK CHECK
            if time.time() < st.session_state.lock_time:
                st.error("🔒 Too many attempts. Try again later.")
                return

            if submit:
                if not username or not password:
                    st.warning("⚠️ Enter username & password")
                    return

                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.session_state.login_attempts = 0
                    st.success(f"✅ Welcome {username}!")
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    st.error("❌ Invalid credentials")

                    # LOCK AFTER MAX ATTEMPTS
                    if st.session_state.login_attempts >= MAX_ATTEMPTS:
                        st.session_state.lock_time = time.time() + LOCK_TIME
                        st.session_state.login_attempts = 0
                        st.warning("🔒 Too many failed attempts. Locked for 60 sec.")

    # ---------------- REGISTER ----------------
    elif choice == "Register":
        with st.form("register_form"):
            username = st.text_input("Create Username").strip()
            password = st.text_input("Create Password", type="password")

            submit = st.form_submit_button("Register")

            if submit:
                if not username or not password:
                    st.warning("⚠️ Fill all fields")
                    return

                if not is_strong_password(password):
                    st.error("❌ Password must be 6+ chars with letters & numbers")
                    st.info("Example: pass123")
                    return

                if add_user(username, password):
                    st.success("✅ Account created! Please login.")
                else:
                    st.error("❌ Username already exists")

    # ---------------- FORGOT PASSWORD ----------------
    elif choice == "Forgot Password":
        with st.form("forgot_form"):
            username = st.text_input("Username").strip()
            new_password = st.text_input("New Password", type="password")

            submit = st.form_submit_button("Reset Password")

            if submit:
                if not username or not new_password:
                    st.warning("⚠️ Fill all fields")
                    return

                if not is_strong_password(new_password):
                    st.error("❌ Weak password")
                    return

                try:
                    update_password(username, new_password)
                    st.success("✅ Password updated successfully")
                except:
                    st.error("❌ User not found")

# ----------------------------
# LOGOUT
# ----------------------------
def logout():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()