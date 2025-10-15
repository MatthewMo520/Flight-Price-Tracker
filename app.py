import streamlit as st
from flight_search import search_flights
import pandas as pd
import plotly.express as px
from datetime import timedelta

#----PAGE SETUP----#
st.set_page_config(
    page_title="Flight Price Tracker",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "flights" not in st.session_state:
    st.session_state.flights = []
if "search_params" not in st.session_state:
    st.session_state.search_params = {}

#----APP TITLE----#
st.title("Flight Price Tracker ✈️")

#----USER INPUTS----#
origin = st.text_input("Origin Airport Code (e.g., YYZ for Toronto Pearson): ")
destination = st.text_input("Destination Airport Code (e.g., LAX for Los Angeles): ")
departure_date = st.date_input("Departure Date (YYYY-MM-DD): ")
adults = st.number_input("Number of Adults:", min_value=1, max_value=10, value=1)

#----SEARCH BUTTON----#
if st.button("Search Flights"):
    if origin and destination:
        with st.spinner("Searching for flights..."):
            try:
                # Convert date to string format for API
                date_str = departure_date.strftime("%Y-%m-%d")
                flights = search_flights(origin, destination, date_str, adults)

                if flights:
                    st.session_state.flights = flights
                    st.session_state.search_params = {
                        "origin": origin,
                        "destination": destination,
                        "date": date_str,
                        "adults": adults
                    }
                    st.success(f"Found {len(flights)} flights!")
                else:
                    st.warning("No flights found. Please try different parameters.")
                    st.session_state.flights = []
            except Exception as e:
                st.error(f"Error searching for flights: {str(e)}")
                st.session_state.flights = []
    else:
        st.error("Please enter both origin and destination airport codes.")

#----DISPLAY RESULTS----#
if st.session_state.flights:
    df_flights = pd.DataFrame(st.session_state.flights)

    # Data processing
    df_flights["price"] = df_flights["price"].astype(float)

    # Try to parse times, use NaT if fails
    df_flights["Departure Time"] = pd.to_datetime(df_flights["departure"], errors='coerce')
    df_flights["Arrival Time"] = pd.to_datetime(df_flights["arrival"], errors='coerce')

    # Calculate flight duration (handle NaT values)
    df_flights["Duration (hrs)"] = (df_flights["Arrival Time"] - df_flights["Departure Time"]).dt.total_seconds() / 3600
    # Fill NaN durations with 0
    df_flights["Duration (hrs)"] = df_flights["Duration (hrs)"].fillna(0)

    # Sort by price (cheapest first)
    df_flights = df_flights.sort_values("price")

    # Display cheapest flight highlight
    cheapest = df_flights.iloc[0]
    source = cheapest.get('source', 'Unknown')
    st.info(f"💰 Cheapest Flight: {cheapest['airline']} - ${cheapest['price']:.2f} (found on {source})")

    #----FLIGHT OPTIONS TABLE----#
    st.subheader("Flight Details")

    # Prepare display dataframe
    display_df = df_flights.copy()
    display_df["Departure"] = display_df["Departure Time"].dt.strftime("%Y-%m-%d %H:%M")
    display_df["Arrival"] = display_df["Arrival Time"].dt.strftime("%Y-%m-%d %H:%M")
    display_df["Price"] = display_df["price"].apply(lambda x: f"${x:.2f}")
    display_df["Duration"] = display_df["Duration (hrs)"].apply(lambda x: f"{x:.1f}h")
    display_df["Booking Link"] = display_df["link"]

    # Add source column if available
    if 'source' in display_df.columns:
        display_df["Source"] = display_df["source"]
        table_df = display_df[["airline", "Departure", "Arrival", "Duration", "Price", "Source", "Booking Link"]]
        table_df.columns = ["Airline", "Departure", "Arrival", "Duration", "Price (USD)", "Source", "Book"]
    else:
        table_df = display_df[["airline", "Departure", "Arrival", "Duration", "Price", "Booking Link"]]
        table_df.columns = ["Airline", "Departure", "Arrival", "Duration", "Price (USD)", "Book"]

    # Display with Streamlit dataframe (supports clickable links)
    st.dataframe(
        table_df,
        column_config={
            "Book": st.column_config.LinkColumn("Book", display_text="Book Flight")
        },
        hide_index=True,
        use_container_width=True
    )
