import streamlit as st
from flight_search import search_flights
import pandas as pd
import plotly.express as px

#----PAGE SETUP----#
st.set_page_config(
    page_title="Flight Price Tracker",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded"
)

#----APP TITLE----#
st.title("Flight Price Tracker ✈️")

#----USER INPUTS----#
origin = st.text_input("Origin Airport Code (e.g., YYZ for Toronto Pearson): ")
destination = st.text_input("Destination Airport Code (e.g., LAX for Los Angeles): ")
departure_date = st.date_input("Departure Date (YYYY-MM-DD): ")
adults = st.number_input("Number of Adults:", min_value=1, max_value=10, value=1)

flights = []

#----SEARCH BUTTON----#
if st.button("Search Flights"):
    if origin and destination:
        flights = search_flights(origin, destination, departure_date, adults)
        if flights:
            st.success(f"Found {len(flights)} flights!")
        else:
            st.warning("No flights found. Please try different parameters.")
    else:
        st.error("Please enter both origin and destination airport codes.")

#----DISPLAY RESULTS----#
if flights:
    df_flights = pd.DataFrame(flights)

    df_flights["price"] = df_flights["price"].astype(float)
    df_flights["Departure Time"] = pd.to_datetime(df_flights["departure"])
    df_flights["Arrival Time"] = pd.to_datetime(df_flights["arrival"])
    df_flights["Price (USD)"] = df_flights["price"].apply(lambda x: f"${x:.2f}")

    df_flights["Booking Link"] = df_flights.apply(
        lambda row: f"https://www.google.com/flights?hl=en#flt={origin}.{destination}.{departure_date};c:USD;e:1;sd:1;t:f",
        axis=1
    )


    #----PRICE SCATTER PLOT----#
    fig = px.scatter(
        df_flights,
        x="Departure Time",
        y="price",
        hover_data={
            "airline": True,
            "Departure Time": True,
            "Arrival Time": True,
            "price": ':.2f',
            "Booking Link": False
        },
        labels={"price": "Price (USD)"},
        title=f"Flight Prices from {origin} to {destination}",
    )

    fig.update_traces(marker=dict(size=10, color="skyblue"))
    fig.update_layout(hovermode="closest")

    st.plotly_chart(fig, use_container_width=True)

    #----FLIGHT OPTIONS TABLE----#
    st.subheader("Flight Details Table")

    table_html = """
    <table style="width:100%; border-collapse: collapse;">
            <tr style="background-color: #262730; color: white;">
                <th style="padding: 8px; border: 1px solid #444;">Airline</th>
                <th style="padding: 8px; border: 1px solid #444;">Departure Time</th>
                <th style="padding: 8px; border: 1px solid #444;">Arrival Time</th>
                <th style="padding: 8px; border: 1px solid #444;">Price (USD)</th>
                <th style="padding: 8px; border: 1px solid #444;">Booking Link</th>
            </tr>
    """

    for _, row in df_flights.iterrows():
        table_html += f"""
            <tr style="background-color: #0E1117; color: white; text-align: center;">
                <td style="padding: 8px; border: 1px solid #444; text-align: center;">{row['airline']}</td>
                <td style="padding: 8px; border: 1px solid #444; text-align: center;">{row['Departure Time']}</td>
                <td style="padding: 8px; border: 1px solid #444; text-align: center;">{row['Arrival Time']}</td>
                <td style="padding: 8px; border: 1px solid #444; text-align: center;">{row['Price (USD)']}</td>
                <td style="padding: 8px; border: 1px solid #444;">
                    <a href="{row["Booking Link"]}" target="_blank" style="color: #1E90FF; text-decoration: none;">
                        Book Flight
                    </a>
                </td>
            </tr>
                
        """
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)
