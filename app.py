import pandas as pd
import streamlit as st

from main import (
    geocode_location,
    download_station_data,
    find_nearby_stations,
    get_fuel_price
)

# Page settings
st.set_page_config(
    page_title="UK Petrol Price Finder",
    layout="wide"
)

# Page heading
st.title("Fuel Price Finder")

st.write(
    "Find current fuel prices"
)

# Search controls
location = st.text_input(
    "Enter postcode or town"
)

radius = st.slider(
    "Search radius in miles",
    min_value=1,
    max_value=100,
    value=10
)

fuel_type = st.selectbox(
    "Fuel type",
    [
        "Unleaded",
        "Super Unleaded",
        "Diesel",
        "Premium Diesel"
    ]
)

# Match fuel type names
fuel_codes = {

    "Unleaded":
        "E10",

    "Super Unleaded":
        "E5",

    "Diesel":
        "B7S",

    "Premium Diesel":
        "B7P"
}

# Get code for selected fuel
selected_fuel_code = fuel_codes[
    fuel_type
]

# Search button
if st.button(
    "Find Fuel Prices",
    type="primary"
):

    # Check location was entered
    if not location:

        st.error(
            "Please enter a postcode or town"
        )

    else:

        # Show loading message
        with st.spinner(
            "Finding petrol stations..."
        ):

           # Convert location coords
            coordinates = geocode_location(
                location
            )

            if coordinates is None:

                st.error(
                    "Location could not be found."
                )

                st.stop()

            latitude, longitude = (
                coordinates
            )

            # Download fuel data
            data = download_station_data()

            if data is None:

                st.error(
                    "Could not download prices "
                )

                st.stop()

            stations = data.get(
                "stations",
                []
            )

            # Check station data exists
            if not stations:

                st.error(
                    "No petrol station data downloaded"
                )

                st.stop()

            # Find near fuel stations
            nearby_stations = (
                find_nearby_stations(
                    stations,
                    latitude,
                    longitude,
                    radius
                )
            )

        # Check results
        if not nearby_stations:

            st.warning(
                "No petrol stations were found "
                f"within {radius} miles of "
                f"{location}."
            )

            st.stop()

        # Build thr results
        results = []

        for station in nearby_stations:

            price = get_fuel_price(
                station,
                selected_fuel_code
            )

            # Skip stations without a price
            if price is None:
                continue

            results.append(
                {
                    "Station":
                        station.get(
                            "name",
                            "Unknown"
                        ),

                    "Brand":
                        station.get(
                            "brand",
                            ""
                        ),

                    "Town":
                        station.get(
                            "town",
                            ""
                        ),

                    "Postcode":
                        station.get(
                            "postcode",
                            ""
                        ),

                    "Distance (miles)":
                        station.get(
                            "distance_miles"
                        ),

                    "Price (p/l)":
                        price
                }
            )

        # Check results
        if not results:

            st.warning(
                f"{len(nearby_stations)} petrol "
                "stations were found, but none "
                f"currently has a {fuel_type} "
                "price available."
            )

            st.stop()

        # Sort results
        results.sort(
            key=lambda station:
                station["Price (p/l)"]
        )

        # Create a dataframe for results
        df = pd.DataFrame(
            results
        )


        # Search summery
        st.success(
            f"Found {len(results)} stations "
            f"with {fuel_type} prices."
        )


        cheapest = results[0]


        # Summery boxes
        column1, column2, column3 = (
            st.columns(3)
        )

        with column1:

            st.metric(
                "Stations found",
                len(results)
            )

        with column2:

            st.metric(
                "Cheapest price",
                f"{cheapest['Price (p/l)']}p"
            )

        with column3:

            st.metric(
                "Cheapest station",
                cheapest["Station"]
            )

        #Show cheapest fuel
        st.subheader(
            "The Cheapest Station is:"
        )

        st.write(
            f"**{cheapest['Station']}**"
        )

        st.write(
            f"{cheapest['Brand']} "
            f"— {cheapest['Town']} "
            f"{cheapest['Postcode']}"
        )

        st.write(
            f"Distance: "
            f"{cheapest['Distance (miles)']} miles"
        )

        st.write(
            f"{fuel_type}: "
            f"**{cheapest['Price (p/l)']}p/litre**"
        )

        # Create results table
        st.subheader(
            "Fuel Prices"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


        # Option to download CSV
        csv_data = df.to_csv(
            index=False
        ).encode(
            "utf-8"
        )


        st.download_button(
            label="Download Results as CSV",
            data=csv_data,
            file_name="petrol_prices.csv",
            mime="text/csv"
        )