import streamlit as st
import pickle
import numpy as np
from db import insert_data
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# DB connection
def get_data():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    df = pd.read_sql("SELECT * FROM predictions", conn)
    return df


# Session state (login control)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    st.title("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Credentials ❌")


# ---------------- MAIN APP (AFTER LOGIN) ----------------
else:

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Load model
    model = pickle.load(open("model.pkl", "rb"))

    st.title("📈 YouTube Video View Prediction")

    # Inputs
    
    like_count = st.number_input("Like Count", min_value=0)
    comment_count = st.number_input("Comment Count", min_value=0)
    duration = st.number_input("Duration (seconds)", min_value=1)

    # Prediction
    if st.button("Predict"):

        features = np.array([[like_count, comment_count, duration]])
        prediction = model.predict(features)[0]

        st.success(f"Predicted Views: {int(prediction)}")

        # Save to DB
        insert_data(like_count, comment_count, duration, int(prediction))

        # Viral check
        if prediction > 100000:
            st.success("🔥 This video can go VIRAL!")
        else:
            st.warning("📉 Low chances of going viral")

        # Graph
        st.subheader("📊 Comparison")

        labels = ["Likes", "Comments", "Views"]
        values = [like_count, comment_count, prediction]

        plt.figure()
        plt.bar(labels, values)
        plt.yscale('log')
        st.pyplot(plt)

    