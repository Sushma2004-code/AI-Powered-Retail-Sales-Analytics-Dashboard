import streamlit as st
from database import add_user, login_user, update_password

# ----------------------------
# LOGIN PAGE
# ----------------------------
def login_page():
    st.title("🔐 Login System")

    menu = ["Login", "Register", "Forgot Password"]
    choice = st.selectbox("Select Option", menu)

    # ---------------- LOGIN ----------------
    if choice == "Login":
        with st.form("login_form"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")

            submit = st.form_submit_button("Login")

            if submit:
                if not user or not pwd:
                    st.warning("⚠️ Enter username & password")
                    return

                if login_user(user, pwd):
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success(f"✅ Welcome {user}")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

    # ---------------- REGISTER ----------------
    elif choice == "Register":
        with st.form("register_form"):
            user = st.text_input("New Username")
            pwd = st.text_input("New Password", type="password")

            submit = st.form_submit_button("Register")

            if submit:
                if not user or not pwd:
                    st.warning("⚠️ Fill all fields")
                    return

                success = add_user(user, pwd)

                if success:
                    st.success("✅ Account created! Please login.")
                else:
                    st.error("❌ Username already exists")

    # ---------------- FORGOT PASSWORD ----------------
    elif choice == "Forgot Password":
        with st.form("forgot_form"):
            user = st.text_input("Username")
            new_pwd = st.text_input("New Password", type="password")

            submit = st.form_submit_button("Reset Password")

            if submit:
                if not user or not new_pwd:
                    st.warning("⚠️ Fill all fields")
                    return

                try:
                    update_password(user, new_pwd)
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