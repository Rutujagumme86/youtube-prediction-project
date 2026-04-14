import streamlit as st
import pickle
import numpy as np
from db import insert_data
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
import os


# ---------------- DB CONNECTION ----------------
def get_data():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    df = pd.read_sql("SELECT * FROM predictions", conn)
    return df


# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))


# ---------------- UI ----------------
st.title("📈 YouTube Video View Prediction")

st.markdown("Enter video details to predict views and performance 🚀")


# ---------------- INPUTS ----------------
like_count = st.number_input("👍 Like Count", min_value=0)
comment_count = st.number_input("💬 Comment Count", min_value=0)
duration = st.number_input("⏱ Duration (seconds)", min_value=1)


# ---------------- PREDICTION ----------------
if st.button("Predict"):

    features = np.array([[like_count, comment_count, duration]])
   prediction = np.expm1(model.predict(features)[0])

    st.success(f"📊 Predicted Views: {int(prediction)}")

    # Save to DB
    insert_data(like_count, comment_count, duration, int(prediction))

    # ---------------- LEVEL LOGIC ----------------
    st.subheader("📊 Performance Level")

    if prediction > 5000000:
        st.success("🔥 High Viral Potential")
        st.markdown("🚀 This video has a strong chance of going viral!")

    elif prediction > 1000000:
        st.info("⚡ Medium Performance")
        st.markdown("👍 This video can perform well with good engagement.")

    else:
        st.warning("📉 Low Performance")
        st.markdown("❌ This video may not reach a wide audience.")


    # ---------------- GRAPH ----------------
    st.subheader("📊 Comparison Chart")

    labels = ["Likes", "Comments", "Views"]
    values = [like_count, comment_count, prediction]

    plt.figure()
    plt.bar(labels, values)
    plt.yscale('log')
    st.pyplot(plt)


