import ee
import pandas as pd
import requests
from datetime import datetime, timedelta


# ==========================================
# GOOGLE EARTH ENGINE CONNECTION
# ==========================================

try:
    ee.Initialize(project="manganese-explorer-ai")
    print("Google Earth Engine connected successfully!")
except Exception as error:
    print(f"Earth Engine connection error: {error}")

def get_satellite_ndvi(latitude, longitude):
    """
    Get recent NDVI from Google Earth Engine.

    Primary source: Sentinel-2
    Fallback source: MODIS
    """

    try:
        point = ee.Geometry.Point([longitude, latitude])
        region = point.buffer(1000)

        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=90)

        # ==========================================
        # PRIMARY: SENTINEL-2 NDVI
        # ==========================================

        sentinel = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(region)
            .filterDate(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 50))
        )

        # Check whether images are available
        if sentinel.size().getInfo() > 0:

            image = sentinel.median()

            ndvi = image.normalizedDifference(
                ["B8", "B4"]
            ).rename("NDVI")

            value = ndvi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=region,
                scale=30,
                maxPixels=100000000
            ).get("NDVI").getInfo()

            if value is not None:
                return round(float(value), 3)

        # ==========================================
        # FALLBACK: MODIS NDVI
        # ==========================================

        modis = (
            ee.ImageCollection("MODIS/061/MOD13Q1")
            .filterBounds(region)
            .filterDate(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            .select("NDVI")
        )

        if modis.size().getInfo() > 0:

            image = modis.mean()

            value = image.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=region,
                scale=250,
                maxPixels=100000000
            ).get("NDVI").getInfo()

            if value is not None:
                # MODIS NDVI has a scale factor of 0.0001
                return round(float(value) * 0.0001, 3)

        return None

    except Exception as error:
        print(f"NDVI retrieval error: {error}")
        return None
def get_satellite_temperature(latitude, longitude):
    """
    Get recent average Land Surface Temperature from MODIS
    using Google Earth Engine.

    Returns temperature in degrees Celsius.
    """

    try:
        point = ee.Geometry.Point([longitude, latitude])
        region = point.buffer(5000)

        # Use a wider period for better satellite coverage
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=90)

        collection = (
            ee.ImageCollection("MODIS/061/MOD11A2")
            .filterBounds(region)
            .filterDate(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            .select("LST_Day_1km")
        )

        image_count = collection.size().getInfo()

        if image_count == 0:
            print(
                f"No MODIS temperature data available for "
                f"{latitude}, {longitude}"
            )
            return None

        # Calculate average temperature from available images
        image = collection.mean()

        value = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=1000,
            maxPixels=100000000,
            bestEffort=True
        ).get("LST_Day_1km").getInfo()

        if value is not None:
            # MODIS LST scale factor = 0.02 Kelvin
            temperature_celsius = float(value) * 0.02 - 273.15

            return round(temperature_celsius, 2)

        return None

    except Exception as error:
        print(
            f"Temperature retrieval error for "
            f"{latitude}, {longitude}: {error}"
        )
        return None    
def get_satellite_soil_moisture(latitude, longitude):
    """
    Get soil moisture from the latest available SMAP satellite data
    using Google Earth Engine.

    Returns surface soil moisture in volumetric units.
    """

    try:
        point = ee.Geometry.Point([longitude, latitude])
        region = point.buffer(10000)

        # Get the SMAP collection and use the latest available data
        collection = (
            ee.ImageCollection("NASA/SMAP/SPL4SMGP/007")
            .filterBounds(region)
            .select("sm_surface")
        )

        image_count = collection.size().getInfo()

        if image_count == 0:
            print("No SMAP soil moisture data available.")
            return None

        # Find the latest available image date
        latest_image = ee.Image(
            collection.sort("system:time_start", False).first()
        )

        latest_date = ee.Date(
            latest_image.get("system:time_start")
        )

        # Use the previous 90 days from the latest available date
        start_date = latest_date.advance(-90, "day")

        recent_collection = (
            collection
            .filterDate(start_date, latest_date.advance(1, "day"))
        )

        image = recent_collection.mean()

        value = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=9000,
            maxPixels=100000000,
            bestEffort=True
        ).get("sm_surface").getInfo()

        if value is not None:
            return round(float(value), 3)

        return None

    except Exception as error:
        print(
            f"Soil moisture retrieval error for "
            f"{latitude}, {longitude}: {error}"
        )
        return None
# ==========================================
# DATA SOURCE INFORMATION
# ==========================================

SOURCES = {
    "nasa_gpm": {
        "name": "NASA GPM IMERG Early",
        "purpose": "NASA satellite-derived precipitation data",
        "url": "https://cmr.earthdata.nasa.gov/search/granules.json",
        "short_name": "GPM_3IMERGDE",
        "version": "07",
    },
}


# ==========================================
# PROTOTYPE BASE DATA
# ==========================================

def get_prototype_data():
    """
    Structured baseline data for prototype demonstration.
    NASA satellite data enriches this dataset when available.
    """

    data = {
        "Location": [
            "Keonjhar, Odisha",
            "Vizianagaram, Andhra Pradesh",
            "Balaghat, Madhya Pradesh",
            "Chirala, Andhra Pradesh",
            "Chitradurga, Karnataka",
            "Visakhapatnam, Andhra Pradesh",
        ],
        "Geological_Score": [88, 82, 91, 76, 79, 72],
        "Soil_Anomaly_Index": [8.7, 7.9, 9.1, 7.2, 7.8, 6.9],
        "Target_Production": [100, 95, 110, 85, 80, 75],
        "Actual_Production": [92, 81, 105, 68, 76, 60],
        "Latitude": [21.63, 18.12, 21.81, 15.82, 14.23, 17.69],
        "Longitude": [85.58, 83.42, 80.60, 80.35, 76.40, 83.22],
    }

    return pd.DataFrame(data)


# ==========================================
# NASA GPM DATA AVAILABILITY CHECK
# ==========================================

def check_nasa_connection(latitude, longitude):
    """
    Check whether NASA GPM IMERG satellite data is available
    near the specified geographic location.
    """

    end_date = datetime.utcnow().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=7)

    buffer = 0.2

    bounding_box = (
        f"{longitude - buffer},{latitude - buffer},"
        f"{longitude + buffer},{latitude + buffer}"
    )

    params = {
        "short_name": SOURCES["nasa_gpm"]["short_name"],
        "version": SOURCES["nasa_gpm"]["version"],
        "bounding_box": bounding_box,
        "temporal": (
            f"{start_date.strftime('%Y-%m-%d')}T00:00:00Z,"
            f"{end_date.strftime('%Y-%m-%d')}T23:59:59Z"
        ),
        "page_size": 1,
    }

    try:
        response = requests.get(
            SOURCES["nasa_gpm"]["url"],
            params=params,
            timeout=20,
            headers={"User-Agent": "ManganeseExplorerAI/1.0"},
        )

        response.raise_for_status()

        result = response.json()
        entries = result.get("feed", {}).get("entry", [])

        return len(entries) > 0

    except Exception as error:
        print(f"NASA connection error: {error}")
        return False


# ==========================================
# NASA POWER RAINFALL DATA
# ==========================================

def get_nasa_rainfall(latitude, longitude):
    """
    Get recent precipitation data from NASA POWER API.
    Returns average daily precipitation in mm.
    """

    end_date = datetime.utcnow().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=6)

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    params = {
        "parameters": "PRECTOTCORR",
        "community": "RE",
        "longitude": longitude,
        "latitude": latitude,
        "start": start_date.strftime("%Y%m%d"),
        "end": end_date.strftime("%Y%m%d"),
        "format": "JSON",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20,
        )

        response.raise_for_status()

        result = response.json()

        rainfall_data = (
            result["properties"]["parameter"]["PRECTOTCORR"]
        )

        values = [
            value for value in rainfall_data.values()
            if value is not None and value >= 0
        ]

        if values:
            return round(sum(values) / len(values), 2)

        return None

    except Exception as error:
        print(f"NASA rainfall retrieval error: {error}")
        return None


# ==========================================
# NASA SATELLITE DATA STATUS
# ==========================================

def add_nasa_satellite_status(df):
    """
    Check NASA GPM satellite data availability
    for each project location.
    """

    results = df.copy()
    status_list = []

    for _, row in results.iterrows():
        available = check_nasa_connection(
            row["Latitude"],
            row["Longitude"],
        )

        status_list.append(
            "Available" if available else "Unavailable"
        )

    results["NASA_Satellite_Data"] = status_list

    return results


# ==========================================
# DATA STANDARDIZATION
# ==========================================

def standardize_data(df):
    """
    Ensure the final dataset contains the required
    location, geological, production, and real environmental data.
    """

    required_columns = [
        "Location",
        "Geological_Score",
        "Soil_Anomaly_Index",
        "Target_Production",
        "Actual_Production",
        "Latitude",
        "Longitude",
        "GEE_NDVI",
        "GEE_Temperature_C",
        "GEE_Soil_Moisture",
        "NASA_Rainfall_mm",
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = None

    return df

# ==========================================
# MAIN DATA PIPELINE
# ==========================================

# ==========================================
# MAIN DATA PIPELINE
# ==========================================

def fetch_online_data():
    """
    Build the manganese intelligence dataset and enrich it
    with real satellite and environmental data.
    """

    data = get_prototype_data()

    # ==========================================
    # FETCH REAL NDVI FROM GOOGLE EARTH ENGINE
    # ==========================================

    satellite_ndvi = []

    for _, row in data.iterrows():
        ndvi = get_satellite_ndvi(
            row["Latitude"],
            row["Longitude"]
        )
        satellite_ndvi.append(ndvi)

    data["GEE_NDVI"] = satellite_ndvi

    # ==========================================
    # FETCH REAL TEMPERATURE FROM GEE
    # ==========================================

    satellite_temperature = []

    for _, row in data.iterrows():
        temperature = get_satellite_temperature(
            row["Latitude"],
            row["Longitude"]
        )
        satellite_temperature.append(temperature)

    data["GEE_Temperature_C"] = satellite_temperature

    # ==========================================
    # FETCH REAL SOIL MOISTURE FROM GEE
    # ==========================================

    satellite_soil_moisture = []

    for _, row in data.iterrows():
        soil_moisture = get_satellite_soil_moisture(
            row["Latitude"],
            row["Longitude"]
        )
        satellite_soil_moisture.append(soil_moisture)

    data["GEE_Soil_Moisture"] = satellite_soil_moisture

    # ==========================================
    # FETCH REAL NASA RAINFALL
    # ==========================================

    nasa_rainfall = []

    for _, row in data.iterrows():
        rainfall = get_nasa_rainfall(
            row["Latitude"],
            row["Longitude"]
        )
        nasa_rainfall.append(rainfall)

    data["NASA_Rainfall_mm"] = nasa_rainfall

    return standardize_data(data)       