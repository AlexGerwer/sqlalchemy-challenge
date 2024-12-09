# Climate Analysis and Exploration with Flask API

## Overview

This project performs climate analysis and data exploration of a weather dataset for Hawaii using Python, SQLAlchemy, Pandas, and Matplotlib. It then creates a Flask API to serve the analyzed data and visualizations.  This project performs climate analysis and data exploration of weather data for Honolulu, Hawaii. It leverages Python, SQLAlchemy, Pandas, Matplotlib, and Flask to:

1. Analyze precipitation trends over the last 12 months.
2. Conduct station analysis to identify the most active stations and their temperature data.
3. Create a Flask API to provide easy access to the analyzed data.

The project consists of two main parts:

1. **Data Analysis:** Jupyter Notebook (`climate_starter.ipynb`) performs climate data analysis, including:
    *   Precipitation analysis for the last 12 months.
    *   Station analysis to identify the most active station.
    *   Temperature observation analysis for the most active station.

2. **Flask API:** A Flask application (`app_flask.py`) is designed to provide an API for accessing the analyzed climate data. It also generates and displays two important visualizations:
    *   Precipitation analysis histogram
    *   Temperature observation histogram

## Repository Structure
SurfsUp/
├── .gitignore
├── README.md
├── app_flask.py
├── climate_starter.ipynb
├── requirements.txt
└── Resources/
    ├── hawaii.sqlite
    ├── hawaii_measurement.xlsx
    ├── hawaii_stations.xlsx
    ├── precipitation_graph.html
    ├── precipitation_histogram.png
    ├── temp_graph.html
    └── temp_histogram.png

## Data Source

The project utilizes a SQLite database (`hawaii.sqlite`) containing weather data for Hawaii. The database includes two tables:

*   **measurement:** Contains precipitation and temperature observation data.
*   **station:** Contains information about the weather stations.

Excel files (`hawaii_measurement.xlsx` and `hawaii_stations.xlsx`) provide a tabular view of the data, these files are not essential for running the application but are useful for understanding the data structure.

## Project Structure

The project is structured as follows:

* **climate_analysis.ipynb:** Jupyter Notebook containing the core analysis logic using SQLAlchemy, Pandas, and Matplotlib.
* **app.py:** Flask application that provides API endpoints to access the analyzed data.
* **Resources:** Folder containing the SQLite database (`hawaii.sqlite`).

## Getting Started

### Prerequisites

*   Python 3.7+
*   Required Python packages (specified in `requirements.txt`)

### Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd climate-analysis-api
    ```

2. Create a virtual environment (recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Flask Application

1. Run the `app_flask.py` script:

    ```bash
    python app_flask.py
    ```

2. The Flask development server will start, and you can access the API endpoints in your browser or using an API client.

## Analysis Summary

### Precipitation Analysis

The precipitation analysis focuses on the last 12 months of available data. It calculates and visualizes precipitation trends using a bar chart and provides summary statistics (mean, standard deviation, quartiles, etc.) for the precipitation data.   The API endpoint `/api/v1.0/precipitation` returns this data as JSON.

### Station Analysis

The station analysis identifies the most active station (station with the most observations) and calculates the lowest, highest, and average temperatures recorded by that station. A histogram visualizing the temperature observations for the most active station over the last 12 months is also generated. The API endpoints `/api/v1.0/stations` and `/api/v1.0/tobs` returns this data as JSON.

## API Endpoints

The following API endpoints are available:

*   `/`: Home page, listing all available routes.
*   `/api/v1.0/precipitation`: Returns a JSON representation of precipitation data for the last 12 months.
*   `/api/v1.0/stations`: Returns a JSON list of weather stations.
*   `/api/v1.0/tobs`: Returns a JSON list of temperature observations for the most active station for the last 12 months.
*   `/api/v1.0/temp/`: Returns temperature statistics (min, avg, max) for the last year (relative to the most recent date in the dataset).
*   `/api/v1.0/temp/<end>`: Returns temperature statistics for one year up to the specified end date (format: YYYY-MM-DD).
*   `/api/v1.0/temp/<start>/<end>`: Returns temperature statistics for a specific date range (format: YYYY-MM-DD).
*   `/api/v1.0/temp/graph`: Generates and displays a histogram of temperature observations for the most active station. The plot will be saved as `temp_histogram.png` and the route will render an HTML page `temp_graph.html` that displays the image.
*   `/api/v1.0/precipitation/graph`: Generates and displays a histogram of the precipitation analysis. The plot will be saved as `precipitation_histogram.png` and the route will render an HTML page `precipitation_graph.html` that displays the image.
*   `/images/<filename>`: Serves the generated images (`temp_histogram.png`, `precipitation_histogram.png`).

## Running the Application

1.  Clone this repository: `git clone <repository_url>`
2.  Install the required libraries: `pip install -r requirements.txt`
3.  Run the Flask application: `python app.py`

The API will then be available at `http://127.0.0.1:5000/`.

## Requirements

Flask==2.2.2

Jinja2==3.1.2

MarkupSafe==2.1.1

numpy==1.23.5

pandas==1.5.2

python-dateutil==2.8.2

six==1.16.0

SQLAlchemy==1.4.46

Werkzeug==2.2.2

**Example Usage of the /api/v1.0/temp/ routes:**

*   Get stats for the last year: `http://127.0.0.1:5000/api/v1.0/temp/`
*   Get stats for one year up to a specific end date (e.g., June 30, 2017): `http://127.0.0.1:5000/api/v1.0/temp/2017-06-30`
*   Get stats for a specific date range: `http://127.0.0.1:5000/api/v1.0/temp/2016-06-30/2017-06-30`

## Notes
* The `app_flask.py` code dynamically calculates the "last 12 months" based on the most recent date found in the dataset.
* The date range validation in the `stats()` function ensures that provided start and end dates are within the valid range of dates in the dataset.
* The application includes error handling for out-of-range dates and returns appropriate error messages.

## Contributing

Contributions to this project are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (You might want to add a LICENSE file if you intend to share this publicly on GitHub).
