import streamlit as st
import pickle
import numpy as  np
import sqlite3 

pickle_in = open("classifier.pkl", "rb")
classifier = pickle.load(pickle_in)

connection = sqlite3.connect("Users.db",check_same_thread=False)
c = connection.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Users(username TEXT,password TEXT)")
connection.commit()

def add_user(username, password):
    c.execute("INSERT INTO Users VALUES (?,?)",(username,password))
    connection.commit()

def Authenticate_user(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username, password))
    return c.fetchone()

st.title("Lassa Fever Prediction Model")
if "page" not in st.session_state:
    st.session_state.page = "signup"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.saved_username = ""

st.markdown(
        """
        <style>
        div.stButton > button {
                background-color: blue;
                color: white;
                font-weight: bold;
                }
        </style>
    """, unsafe_allow_html= True)


def signup_page():
    st.header("Sign Up")
    username = st.text_input("username")
    password = st.text_input("password", type="password")

    if st.button("Create Account"):
        if username and password:
            add_user(username, password)
            st.session_state.page = "login"
            st.success("Account created! Now log in.")
        else:
            st.warning("Please fill in both fields.")

def login_page():
    st.header("Login")
    username = st.text_input("username")
    password = st.text_input("password", type="password")

    if st.button("Login"):
        user = Authenticate_user(username, password)
        if user:
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.current_user  = username
            st.session_state.page = "prediction"
        else:
            st.error("Incorrect username or password")

def prediction_page():
    st.write("Enter symptoms to get a prediction")
    col1,col2,col3,col4= st.columns(4)
    with col1:
        a1 = st.text_input("Temperature (°C)")
        a2 = st.text_input("BP Level (mmHg)")
        a3 = st.text_input("Radial Pulse (bpm)")
        a4 = st.text_input("Vomiting")
    with col2:
        a5 = st.text_input("Packed Cell Volume (%)")
        a6 = st.text_input("Respiratory Rate (c/m)")
        a7 = st.text_input("Sore Throat")
        a8 = st.text_input("ERS (mm/hr)")
    with col3:
        b1 = st.text_input("Kidney Function (eGFR)")
        b2 = st.text_input("SNHL (dB)")
        b3 = st.text_input("WBC Count (/ml")
        b4 = st.text_input("Neutrophil Count (/ml)")
    with col4:
        b5 = st.text_input("Lymphocyte Count (/ml)")
    if st.button("Diagnose"):
        features = np.array([[a1,a2,a3,a4,a5,a6,a7,a8,b1,b2,b3,b4,b5]])
        Outcome = classifier.predict(features)
        if Outcome[0] == 1:
            st.success("you have Lassa Fever")
        else:
            st.success("you do not have Lassa Fever")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.session_state.current_user = ""

if st.session_state.logged_in:
    prediction_page()
else:
    if st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "login":
        login_page()
