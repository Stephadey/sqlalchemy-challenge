# Climate Analysis and Exploration

## Overview

This challenge performs a climate analysis and data exploration of the Honolulu, Hawaii area. It uses Python, SQLAlchemy, Pandas, and Matplotlib to analyse climate data stored in a SQLite database. Additionally, a Flask API is created to provide easy access to the data through various endpoints.

## Files

- `climate_analysis.ipynb`: Jupyter notebook for climate analysis and data exploration.
- `app.py`: Flask application to create API endpoints for climate data.

## Requirements

- Python 3.7+
- Packages: `numpy`, `pandas`, `matplotlib`, `sqlalchemy`, `flask`

## Installation

1. **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install numpy pandas matplotlib sqlalchemy flask
    ```

## Running the Jupyter Notebook

1. **Launch Jupyter Notebook:**
    ```bash
    jupyter notebook
    ```

2. **Open and run `climate_analysis.ipynb`**:
    - This notebook performs the following tasks:
        - Connects to the SQLite database using SQLAlchemy.
        - Performs precipitation and station analysis.
        - Plots the results using Matplotlib.

## Running the Flask Application

1. **Ensure your virtual environment is activated:**
    ```bash
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Run the Flask application:**
    ```bash
    python app.py
    ```

3. **Access the application:**
    - Open your web browser and navigate to `http://127.0.0.1:5000/`.
    - Available routes:
        - `/api/v1.0/precipitation`
        - `/api/v1.0/stations`
        - `/api/v1.0/tobs`
        - `/api/v1.0/<start>`
        - `/api/v1.0/<start>/<end>`

## API Endpoints

- **`/api/v1.0/precipitation`**
    - Returns JSON with date as the key and precipitation as the value for the last year of data.

- **`/api/v1.0/stations`**
    - Returns a JSON list of stations from the dataset.

- **`/api/v1.0/tobs`**
    - Returns a JSON list of temperature observations (TOBS) for the most active station for the previous year.

- **`/api/v1.0/<start>`**
    - Returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date.

- **`/api/v1.0/<start>/<end>`**
    - Returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end date range.

## Notes

- Ensure the SQLite database file `hawaii.sqlite` is located in the `Resources` directory.
- Adjust the file paths in the scripts if your directory structure is different.

## References

- Tutor Session with Christopher, personal communication (Zoom), Monday, March 11th, 2024
- Flask Documentation: Flask is the micro web framework used to create the API endpoints in this project. The official Flask documentation provides comprehensive guides and tutorials on how to use Flask effectively. [Flask Documentation](https://flask.palletsprojects.com/) 
- SQLAlchemy Documentation: SQLAlchemy is the SQL toolkit and Object Relational Mapper (ORM) used in this project for database operations. The official SQLAlchemy documentation provides detailed information on how to use the library for database manipulation and querying. [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, [https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml.](https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml), measurements converted to metric in Pandas.
