import streamlit as st
from database import update_password, login_user

def show():

    st.title("👤 User Profile")

    # ----------------------------
    # CHECK LOGIN
    # ----------------------------
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("🔒 Please login first")
        return

    username = st.session_state.user

    st.success(f"Welcome, {username} 👋")

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
    # CHANGE PASSWORD
    # ----------------------------
    st.markdown("### 🔑 Change Password")

    with st.form("password_form"):
        old_pass = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")

        submit = st.form_submit_button("Update Password")

        if submit:
            if not old_pass or not new_pass or not confirm_pass:
                st.warning("⚠️ Fill all fields")

            elif not login_user(username, old_pass):
                st.error("❌ Current password is incorrect")

            elif new_pass != confirm_pass:
                st.error("❌ New passwords do not match")

            elif not is_strong_password(new_pass):
                st.error("❌ Password must be 6+ chars with letters & numbers")

            else:
                update_password(username, new_pass)
                st.success("✅ Password updated successfully")