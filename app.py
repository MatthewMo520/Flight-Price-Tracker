import streamlit as st
from flight_search import search_flights
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
#----PAGE SETUP----#
st.set_page_config(
    page_title="Flight Price Tracker",
    layout="centered",
    initial_sidebar_state="expanded"
)

#----APP TITLE----#
st.title("Flight Price Tracker")

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
            "link": False
        },
        labels={"price": "Price (USD)"},
        title=f"Flight Prices from {origin} to {destination}",
    )

    fig.update_traces(marker=dict(size=10, color="skyblue"))
    fig.update_layout(hovermode="closest")

    st.plotly_chart(fig, use_container_width=True)

    #----FLIGHT OPTIONS TABLE----#
    st.subheader("Flight Details Table")

    # ensure strings for safe HTML rendering
    df_flights["Departure Time"] = df_flights["Departure Time"].dt.strftime("%Y-%m-%d %H:%M")
    df_flights["Arrival Time"] = df_flights["Arrival Time"].dt.strftime("%Y-%m-%d %H:%M")

    # Build HTML table (no leading indentation before the first <table>)
    table_html = (
        '<table style="width:100%; border-collapse: collapse;">'
        '<tr style="background-color:#262730; color:white;">'
        '<th style="padding:8px; border:1px solid #444;">Airline</th>'
        '<th style="padding:8px; border:1px solid #444;">Departure Time</th>'
        '<th style="padding:8px; border:1px solid #444;">Arrival Time</th>'
        '<th style="padding:8px; border:1px solid #444;">Price (USD)</th>'
        '<th style="padding:8px; border:1px solid #444;">Booking Link</th>'
        '</tr>'
    )

    for _, row in df_flights.iterrows():
        # make sure link is a plain URL string
        link_url = row.get("link", "")
        # sanitize missing link
        if not link_url or str(link_url).strip() in ("#", "N/A"):
            link_html = "N/A"
        else:
            link_html = f'<a href="{link_url}" target="_blank" style="color:#1E90FF; text-decoration:none;">Book Flight</a>'

        table_html += (
            '<tr style="background-color:#0E1117; color:white; text-align:center;">'
            f'<td style="padding:8px; border:1px solid #444;">{row["airline"]}</td>'
            f'<td style="padding:8px; border:1px solid #444;">{row["Departure Time"]}</td>'
            f'<td style="padding:8px; border:1px solid #444;">{row["Arrival Time"]}</td>'
            f'<td style="padding:8px; border:1px solid #444;">{row["Price (USD)"]}</td>'
            f'<td style="padding:8px; border:1px solid #444;">{link_html}</td>'
            '</tr>'
        )

    table_html += '</table>'

    # Render the HTML via components (reliable)
    components.html(table_html, height=360, scrolling=True)
