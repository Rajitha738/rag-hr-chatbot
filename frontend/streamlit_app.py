import streamlit as st
import requests

st.set_page_config(page_title="RAG HR Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 HR Policy Chatbot")
st.write("Ask me anything about HR policies!")

# Input box
user_query = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_query.strip() == "":
        st.warning("Please enter a question.")
    else:
        try:
            # Send request to FastAPI backend
            response = requests.post(
                "http://127.0.0.1:8000/query",
                json={"query": user_query}
            )

            if response.status_code == 200:
                answer = response.json().get("answer", "No answer found.")
                st.success(answer)
            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend. Is FastAPI running?")
