import streamlit as st

st.set_page_config(
    page_title="Flight Price Tracker",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Flight Price Tracker ✈️")

origin = st.text_input("Origin Airport Code (e.g., YYZ for Toronto Pearson): ")
destination = st.text_input("Destination Airport Code (e.g., LAX for Los Angeles): ")
departure_date = st.date_input("Departure Date (YYYY-MM-DD): ")
adults = st.number_input("Number of Adults:", min_value=1, max_value=10, value=1)

if st.button("Search Flights"):
    st.write("Searching for flights...")