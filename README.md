# UK Fuel Price Finder

A Python application for finding and comparing fuel prices at petrol stations across the UK.

Enter a **postcode, town or city**, choose a **search radius** and select a **fuel type**. The application finds nearby stations, calculates their distance from the search location, compares available prices and displays the cheapest options first.

The project began as a command-line Python application and was later developed into a **Streamlit web app** with an interactive interface and CSV export.

---

## Screenshots

### Search interface



Enter a UK postcode or town, select the search radius and choose the fuel type.

![Fuel Price Finder search interface](screenshots/fuel-price-finder-home.png)

### Search results

The application displays the number of matching stations, the cheapest price and the cheapest station.

![Fuel Price Finder search results](screenshots/fuel-price-finder-results.png)

### Fuel price table

Results are displayed in a sortable table and can be downloaded as a CSV file.

![Fuel Price Finder results table](screenshots/fuel-price-finder-table.png)

> **Note:** Prices shown in the screenshots are examples captured when the application was tested. 



##  Features

- Search by UK postcode, town or city
- Adjustable search radius
- Choose between multiple fuel types
- Finds petrol stations within the selected radius
- Calculates distance to each station
- Sorts results by cheapest fuel price
- Highlights the cheapest station
- Displays station name, brand, town and postcode
- Shows distance in miles
- Displays price in pence per litre
- Interactive Streamlit web interface
- Download search results as a CSV file
- Handles missing fuel-price information

---

##  Technologies Used

- **Python**
- **Streamlit** — web application interface
- **Requests** — downloading web/API data
- **Pandas** — displaying and exporting results
- **OpenStreetMap Nominatim** — converting locations into latitude and longitude
- **JSON** — processing fuel station data
- **CSV** — exporting search results
- **Haversine formula** — calculating geographical distance between locations

---

##  How It Works

The application follows this process:

```text
User enters postcode, town or city
            │
            ▼
Location is converted to coordinates
            │
            ▼
UK fuel station data is downloaded
            │
            ▼
Distance to each station is calculated
            │
            ▼
Stations outside the selected radius are removed
            │
            ▼
Selected fuel prices are extracted
            │
            ▼
Results are sorted by price
            │
            ▼
Results are displayed in Streamlit
            │
            ▼
User can download results as CSV
```

---

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/Paul-Col/uk-petrol-price-finder/tree/main
```

Move into the project directory:

```bash
cd uk-petrol-price-finder
```

### 2. Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

A typical `requirements.txt` for the project contains:

```text
requests
streamlit
pandas
```

---

##  Running the Web App

Start the Streamlit application with:

```bash
python3 -m streamlit run app.py
```

On Windows you can use:

```bash
python -m streamlit run app.py
```

Streamlit will normally open the application automatically in your browser.

If it does not, open:

```text
http://localhost:8501
```

---

##  Using the Application

1. Enter a UK postcode, town or city.
2. Choose the required search radius.
3. Select a fuel type.
4. Click **Find Fuel Prices**.
5. Review the cheapest station and price.
6. Browse the full results table.
7. Click **Download Results as CSV** if you want to save the results.

---

## CSV Output

Downloaded results contain fields such as:

| Field | Description |
|---|---|
| Station | Petrol station name |
| Brand | Fuel retailer or brand |
| Town | Town or locality |
| Postcode | Station postcode |
| Distance (miles) | Distance from the searched location |
| Price (p/l) | Fuel price in pence per litre |

Example:

```csv
Station,Brand,Town,Postcode,Distance (miles),Price (p/l)
Example Station,TESCO,Example Town,AB1 2CD,1.25,167.9
```

---

##  Project Structure

```text
uk-petrol-price-finder/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── screenshots/
│   ├── fuel-price-finder-home.png
│   ├── fuel-price-finder-results.png
│   └── fuel-price-finder-table.png
│
└── data/
    └── petrol_prices.csv
```

### `main.py`

Contains the core application logic, including:

- location geocoding
- downloading station data
- distance calculations
- radius filtering
- fuel-price extraction

### `app.py`

Contains the Streamlit user interface, including:

- search controls
- fuel selection
- results summary
- cheapest-station display
- results table
- CSV download button

---

##  Data Sources

The project uses publicly available UK fuel-price information and OpenStreetMap geocoding data.

Fuel-price availability and update times depend on the underlying data source. Prices can change frequently, so users should confirm the current pump price before travelling specifically to purchase fuel.

---

## Project Goals

This project was created to practise and demonstrate:

- consuming web/API data with Python
- processing JSON data
- validating user input
- working with geographical coordinates
- implementing the Haversine distance formula
- filtering and sorting datasets
- exporting structured data to CSV
- building an interactive Python web application
- using Git and GitHub for version control and project documentation

---

##  Possible Future Improvements

- Add an interactive map showing station locations
- Allow sorting by distance as well as price
- Add estimated cost for a full tank
- Calculate potential savings between stations
- Add petrol-station brand filters
- Cache downloaded data to improve performance
- Add fuel-price update timestamps
- Improve mobile layout
- Deploy the application publicly using Streamlit Community Cloud

---


