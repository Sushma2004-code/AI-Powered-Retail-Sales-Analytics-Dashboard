import streamlit as st
import os
import time
from openai import OpenAI

def show():

    st.title("🤖 AI Assistant")

    # ----------------------------
    # API SETUP
    # ----------------------------
    api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else None

    if not client:
        st.warning("⚠️ AI not available (No API key / credits)")

    # ----------------------------
    # CHAT MEMORY
    # ----------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ----------------------------
    # CLEAR CHAT
    # ----------------------------
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

    # ----------------------------
    # TYPEWRITER EFFECT
    # ----------------------------
    def typewriter(text, speed=0.01):
        placeholder = st.empty()
        output = ""
        for char in text:
            output += char
            placeholder.markdown(output)
            time.sleep(speed)

    # ----------------------------
    # SHOW CHAT HISTORY
    # ----------------------------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ----------------------------
    # USER INPUT
    # ----------------------------
    user_input = st.chat_input("Ask about sales, revenue, products...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        # ----------------------------
        # CONTEXT
        # ----------------------------
        context = """
        You are a professional retail data analyst.
        Give short, clear, business-friendly insights.
        """

        messages = [{"role": "system", "content": context}] + st.session_state.messages

        # ----------------------------
        # AI RESPONSE
        # ----------------------------
        try:
            if client:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                reply = response.choices[0].message.content
            else:
                raise Exception("No API")

        except Exception:
            # Fallback (IMPORTANT)
            if "revenue" in user_input.lower():
                reply = "📈 Revenue is increasing steadily. Focus on high-performing categories."
            elif "product" in user_input.lower():
                reply = "🛍️ Top products are driving most sales. Consider boosting inventory."
            elif "sales" in user_input.lower():
                reply = "📊 Sales show seasonal trends. Plan marketing accordingly."
            else:
                reply = "⚠️ AI unavailable. Try asking about revenue, products, or sales."

        # ----------------------------
        # SAVE RESPONSE
        # ----------------------------
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # ----------------------------
        # DISPLAY RESPONSE
        # ----------------------------
        with st.chat_message("assistant"):
            typewriter(reply)