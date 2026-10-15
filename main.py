import requests
from math import radians, sin, cos, atan2, sqrt
import csv
from pathlib import Path

# Define a function to collect the location and search radius from the user
def get_search_details():

    # Print the program heading
    print("=" * 22)
    print("UK PETROL PRICE FINDER")
    print("=" * 22)

    # Ask for a postcode, town or city and remove surrounding spaces
    location = input(
        "Enter postcode, town or city: "
    ).strip()

    # Keep asking until the user enters a non-empty location
    while not location:

        # Explain why the location must be entered again
        print("Please enter a location.")

        location = input(
            "Enter postcode, town or city: "
        ).strip()

    # Repeat until the user enters a valid radius
    while True:

        # Try converting the radius into a decimal number
        try:

            # Allow whole numbers or decimals such as 5 or 2.5
            radius = float(
                input(
                    "Enter search radius in miles: "
                )
            )

            # Reject a zero or negative search radius
            if radius <= 0:
                # Trigger the error handler for an invalid radius
                raise ValueError

            # Exit the loop after a valid radius has been entered
            break

        # Handle non-numeric, zero or negative inputs
        except ValueError:

            print(
                "Please enter a valid radius."
            )

    # Send both search values back to the main program
    return location, radius

# Define a function to convert a UK place name or postcode into GPS coordinates
def geocode_location(location):

    # Show the location being looked up
    print(
        f"\nFinding location: {location}"
    )

    # Set the OpenStreetMap Nominatim geocoding API address
    url = (
        "https://nominatim.openstreetmap.org/search"
    )

    # Set the search text, response format, result limit and UK country filter
    params = {
        # Add the entered location and UK to the search query
        "q": f"{location}, UK",
        # Request a JSON response
        "format": "json",
        # Ask for only one matching place
        "limit": 1,
        # Restrict matching places to the United Kingdom
        "countrycodes": "gb"
    }

    # Identify this application to the API using a User-Agent header
    headers = {
        "User-Agent":
            "PetrolPriceFinder/1.0"
    }

    # Try contacting the geocoding API
    try:

        # Send the search request with parameters, headers and a 15-second timeout
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        # Raise an error for unsuccessful HTTP responses
        response.raise_for_status()

    # Catch connection, timeout and HTTP errors
    except requests.RequestException as error:

        print(
            f"Location request failed: {error}"
        )

        # Stop if the request fails or no location is found
        return None

    # Convert the API JSON response into Python data
    results = response.json()

    # Check whether any matching location was returned
    if not results:

        print(
            "Location could not be found."
        )

        return None

    # Read the first result’s latitude and convert it to a decimal number
    latitude = float(
        results[0]["lat"]
    )
    # Read the first result’s longitude and convert it to a decimal number
    longitude = float(
        results[0]["lon"]
    )

    # Read the full description of the matched location
    display_name = (
        results[0]["display_name"]
    )

    print(
        f"Found: {display_name}"
    )

    print(
        f"Latitude: {latitude}"
    )
    print(
        f"Longitude: {longitude}"
    )

    # Return the latitude and longitude as a pair
    return latitude, longitude

# Store the URL for the UK petrol station data API
# Python automatically joins the two strings inside the parentheses
FUEL_DATA_URL = (
    "https://cheapfuelnearme.uk/"
    "api/v1/stations.json"
)

# Define a function to download fuel station data
def download_station_data():

    # Tell the user that the download is starting
    print(
        "\nDownloading UK fuel prices..."
    )

    # Try to retrieve data from the fuel station API
    try:

        # Send a GET request with a 30-second timeout
        response = requests.get(
            FUEL_DATA_URL,
            timeout=30
        )

        # Check for an unsuccessful HTTP response
        response.raise_for_status()

    # Catch network, timeout and HTTP errors
    except requests.RequestException as error:

        print(
            f"Download failed: {error}"
        )

        # Return None so the main program knows the download failed
        return None

    # Convert the JSON response into a Python dictionary
    data = response.json()

    # Read the station list or use an empty list if it is missing
    stations = data.get(
        "stations",
        []
    )

    print(
        f"Downloaded "
        f"{len(stations)} stations."
    )

    print(
        f"Data generated: "
        f"{data.get('source_generated_at')}"
    )

    # Return the complete response dictionary
    return data


# Define a function to calculate straight-line distance between two GPS points
def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):

    # Use the approximate radius of Earth in miles
    earth_radius_miles = 3958.8

    # Convert the first latitude from degrees to radians
    lat1 = radians(lat1)
    # Convert the first longitude from degrees to radians
    lon1 = radians(lon1)

    # Convert the second latitude from degrees to radians
    lat2 = radians(lat2)
    # Convert the second longitude from degrees to radians
    lon2 = radians(lon2)

    # Calculate the difference between the two latitudes
    difference_lat = (
        lat2 - lat1
    )

    # Calculate the difference between the two longitudes
    difference_lon = (
        lon2 - lon1
    )

    # Calculate the first part of the Haversine formula
    a = (
        sin(
            difference_lat / 2
        ) ** 2
        +
        cos(lat1)
        * cos(lat2)
        * sin(
            difference_lon / 2
        ) ** 2
    )

    # Calculate the angular distance between the two locations
    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    # Convert the angular distance into miles
    distance = (
        earth_radius_miles
        * c
    )

    # Return the straight-line distance in miles
    return distance

# Define a function to find stations inside the requested radius
def find_nearby_stations(
    stations,
    user_lat,
    user_lon,
    radius
):

    # Create an empty list for stations inside the radius
    nearby_stations = []

    # Tell the user which distance is being searched
    print(
        f"\nFinding stations within "
        f"{radius} miles..."
    )

    # Check each station in the downloaded data
    for station in stations:

        # Read this station’s latitude, if available
        station_lat = station.get(
            "lat"
        )

        # Read this station’s longitude, if available
        station_lon = station.get(
            "lon"
        )

        # Skip stations without both coordinates
        if (
            station_lat is None
            or station_lon is None
        ):
            # Move on to the next station
            continue

        # Calculate the distance from the user to this station
        distance = calculate_distance(
            user_lat,
            user_lon,
            station_lat,
            station_lon
        )

        # Keep stations at or inside the requested radius
        if distance <= radius:

            # Store the distance rounded to two decimal places
            station[
                "distance_miles"
            ] = round(
                distance,
                2
            )

            # Add this station to the results list
            nearby_stations.append(
                station
            )

    # Sort matching stations from nearest to furthest
    nearby_stations.sort(
        key=lambda station:
            station[
                "distance_miles"
            ]
    )

    print(
        f"Found "
        f"{len(nearby_stations)} "
        f"stations."
    )

    # Return the sorted list of nearby petrol stations
    return nearby_stations
# Define a helper function to look up the price of one fuel type
def get_fuel_price(
    station,
    fuel_code
):

    # Read the station’s fuel price dictionary, defaulting to empty
    prices = station.get(
        "prices",
        {}
    )

    # Look up the requested fuel code, such as E10 or B7S
    fuel = prices.get(
        fuel_code
    )

    # Check whether the station has data for that fuel
    if not fuel:
        # Return None when the requested fuel is unavailable
        return None

    # Return the price in pence per litre, if provided
    return fuel.get(
        "pence_per_litre"
    )

# Define a helper function to look up when a fuel price was submitted
def get_price_date(
    station,
    fuel_code
):

    # Read the station’s fuel price dictionary
    prices = station.get(
        "prices",
        {}
    )

    # Find the details for the requested fuel type
    fuel = prices.get(
        fuel_code
    )

    # Check whether fuel data is present
    if not fuel:
        # Return None if no matching fuel data was found
        return None

    # Return the date or timestamp of the price submission
    return fuel.get(
        "submitted_at"
    )

# Define a function to show the nearby stations in the terminal
def display_stations(
    stations
):

    # Add a blank line and print the results heading
    print()
    print("=" * 70)
    print("PETROL STATIONS FOUND")
    print("=" * 70)

    # Display the details for each nearby station
    for station in stations:

        print()

        print(
            # Get station data safely, using a default for missing values
            station.get(
                "name",
                "Unknown"
            )
        )

        print(
            f"Brand: "
            f"{station.get('brand', '')}"
        )

        print(
            f"Town: "
            f"{station.get('town', '')}"
        )

        print(
            f"Postcode: "
            f"{station.get('postcode', '')}"
        )

        print(
            f"Distance: "
            f"{station['distance_miles']} "
            f"miles"
        )

        # Look up standard unleaded petrol using fuel code E10
        unleaded = get_fuel_price(
            station,
            "E10"
        )

        # Look up standard diesel using fuel code B7S
        diesel = get_fuel_price(
            station,
            "B7S"
        )

        print(
            # Display the unleaded price in pence per litre
            f"Unleaded: "
            f"{unleaded}p"
        )

        print(
            # Display the diesel price in pence per litre
            f"Diesel: "
            f"{diesel}p"
        )

# Define a function to export the results into a CSV file
def save_to_csv(
    stations,
    search_location,
    radius
):

    # Choose the data folder for the saved file
    output_directory = Path(
        "data"
    )

    # Create the folder if it does not already exist
    output_directory.mkdir(
        exist_ok=True
    )

    # Set the full output path to data/petrol_prices.csv
    output_file = (
        output_directory
        / "petrol_prices.csv"
    )

    # Define the CSV column names and their order
    fieldnames = [
        "search_location",
        "radius_miles",
        "station_id",
        "station",
        "brand",
        "town",
        "postcode",
        "distance_miles",

        "unleaded_e10",
        "unleaded_updated",

        "super_unleaded_e5",
        "super_unleaded_updated",

        "diesel_b7",
        "diesel_updated",

        "premium_diesel_b7",
        "premium_diesel_updated"
    ]

    # Open the CSV for writing using UTF-8; close it automatically afterwards
    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        # Create a CSV writer that maps dictionary keys to the column names
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        # Write the column headings into the first CSV row
        writer.writeheader()

        # Build and save one CSV row for each matching station
        for station in stations:

            # Collect search details, station details and fuel prices for this row
            row = {

                # Record the place originally entered by the user
                "search_location":
                    search_location,

                # Record the requested search radius
                "radius_miles":
                    radius,

                # Record the station’s unique identifier
                "station_id":
                    station.get("id"),

                # Record the station name
                "station":
                    station.get("name"),

                # Record the fuel retailer or brand
                "brand":
                    station.get("brand"),

                # Record the station’s town
                "town":
                    station.get("town"),

                # Record the station’s postcode
                "postcode":
                    station.get("postcode"),

                # Record the calculated distance from the search location
                "distance_miles":
                    station.get(
                        "distance_miles"
                    ),

                # Get the standard unleaded petrol price
                "unleaded_e10":
                    get_fuel_price(
                        station,
                        "E10"
                    ),

                # Get the date of the unleaded petrol price
                "unleaded_updated":
                    get_price_date(
                        station,
                        "E10"
                    ),

                # Get the super unleaded petrol price
                "super_unleaded_e5":
                    get_fuel_price(
                        station,
                        "E5"
                    ),

                # Get the date of the super unleaded price
                "super_unleaded_updated":
                    get_price_date(
                        station,
                        "E5"
                    ),

                # Get the standard diesel price
                "diesel_b7":
                    get_fuel_price(
                        station,
                        "B7S"
                    ),

                # Get the date of the standard diesel price
                "diesel_updated":
                    get_price_date(
                        station,
                        "B7S"
                    ),

                # Get the premium diesel price
                "premium_diesel_b7":
                    get_fuel_price(
                        station,
                        "B7P"
                    ),

                # Get the date of the premium diesel price
                "premium_diesel_updated":
                    get_price_date(
                        station,
                        "B7P"
                    )
            }

            # Write the completed station row into the CSV file
            writer.writerow(
                row
            )

    print()
    print(
        f"Saved {len(stations)} "
        f"stations to:"
    )

    print(
        # Show the full path of the saved CSV file
        output_file.resolve()
    )

# Define the main function that controls the program
def main():

    # Ask the user for their search location and radius
    location, radius = (
        get_search_details()
    )

    # Find the GPS coordinates of the entered location
    coordinates = geocode_location(
        location
    )

    # Stop the program if the location could not be found
    if coordinates is None:
        return

    # Unpack the returned latitude and longitude
    latitude, longitude = coordinates

    # Download the fuel station data
    data = download_station_data()

    # Stop if the data download failed
    if data is None:
        return

    # Read the list of stations from the downloaded data
    stations = data.get(
        "stations",
        []
    )

    # Find stations within the requested radius
    nearby_stations = (
        find_nearby_stations(
            stations,
            latitude,
            longitude,
            radius
        )
    )

    # Check whether any stations were found
    if not nearby_stations:

        print(
            "\nNo petrol stations found "
            "within that radius."
        )

        return

    # Print the matching stations and their fuel prices
    display_stations(
        nearby_stations
    )

    # Save the matching stations to a CSV file
    save_to_csv(
        nearby_stations,
        location,
        radius
    )


# Only start the program when this Python file is run directly
if __name__ == "__main__":
    main()
