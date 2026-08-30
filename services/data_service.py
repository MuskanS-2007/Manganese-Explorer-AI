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


# ==========================================
# SATELLITE NDVI
# ==========================================

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

        # PRIMARY: SENTINEL-2
        sentinel = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(region)
            .filterDate(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 50))
        )

        if sentinel.size().getInfo() > 0:

            image = sentinel.median()

            ndvi = image.normalizedDifference(
                ["B8", "B4"]
            ).rename("NDVI")

            value = ndvi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=region,
                scale=30,
                maxPixels=100000000,
                bestEffort=True
            ).get("NDVI").getInfo()

            if value is not None:
                return round(float(value), 3)

        # FALLBACK: MODIS
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
                maxPixels=100000000,
                bestEffort=True
            ).get("NDVI").getInfo()

            if value is not None:
                return round(float(value) * 0.0001, 3)

        return None

    except Exception as error:
        print(f"NDVI retrieval error: {error}")
        return None


# ==========================================
# LAND SURFACE TEMPERATURE
# ==========================================

def get_satellite_temperature(latitude, longitude):
    """
    Get recent average Land Surface Temperature from MODIS.
    Returns temperature in degrees Celsius.
    """

    try:
        point = ee.Geometry.Point([longitude, latitude])
        region = point.buffer(5000)

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

        if collection.size().getInfo() == 0:
            return None

        image = collection.mean()

        value = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=1000,
            maxPixels=100000000,
            bestEffort=True
        ).get("LST_Day_1km").getInfo()

        if value is not None:
            temperature_celsius = float(value) * 0.02 - 273.15
            return round(temperature_celsius, 2)

        return None

    except Exception as error:
        print(f"Temperature retrieval error: {error}")
        return None


# ==========================================
# SOIL MOISTURE
# ==========================================

def get_satellite_soil_moisture(latitude, longitude):
    """
    Get recent soil moisture from SMAP satellite data.
    """

    try:
        point = ee.Geometry.Point([longitude, latitude])
        region = point.buffer(10000)

        collection = (
            ee.ImageCollection("NASA/SMAP/SPL4SMGP/007")
            .filterBounds(region)
            .select("sm_surface")
        )

        if collection.size().getInfo() == 0:
            return None

        latest_image = ee.Image(
            collection.sort("system:time_start", False).first()
        )

        latest_date = ee.Date(
            latest_image.get("system:time_start")
        )

        start_date = latest_date.advance(-90, "day")

        recent_collection = collection.filterDate(
            start_date,
            latest_date.advance(1, "day")
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
        print(f"Soil moisture retrieval error: {error}")
        return None


# ==========================================
# TERRAIN DATA
# ==========================================

def get_terrain_data(latitude, longitude):
    """
    Get elevation and terrain slope from SRTM data.
    """

    try:
        point = ee.Geometry.Point([longitude, latitude])
        region = point.buffer(1000)

        elevation_image = ee.Image("USGS/SRTMGL1_003")
        terrain = ee.Terrain.products(elevation_image)

        elevation = elevation_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=30,
            maxPixels=100000000,
            bestEffort=True
        ).get("elevation").getInfo()

        slope = terrain.select("slope").reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=30,
            maxPixels=100000000,
            bestEffort=True
        ).get("slope").getInfo()

        elevation_value = (
            round(float(elevation), 2)
            if elevation is not None else None
        )

        slope_value = (
            round(float(slope), 2)
            if slope is not None else None
        )

        return elevation_value, slope_value

    except Exception as error:
        print(f"Terrain data retrieval error: {error}")
        return None, None


# ==========================================
# NASA POWER RAINFALL DATA
# ==========================================

def get_nasa_rainfall(latitude, longitude):
    """
    Get recent average daily precipitation from NASA POWER.
    Returns rainfall in mm.
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
            timeout=20
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
# PROTOTYPE BASE DATA
# ==========================================

def get_prototype_data():
    """
    Representative pilot locations selected to demonstrate
    different exploration and production scenarios in the
    SIH prototype.
    """

    data = {
        "Location": [
            "Keonjhar, Odisha",
            "Balaghat, Madhya Pradesh",
            "Chitradurga, Karnataka",
            "Nagpur, Maharashtra",
            "Visakhapatnam, Andhra Pradesh",
            "Chirala, Andhra Pradesh",
        ],

        # Prototype geochemical indicator values
        # Different values help demonstrate varied conditions
        "Soil_Anomaly_Index": [
            9.2, 8.8, 7.5, 6.5, 5.8, 4.5
        ],

        # Production scenarios:
        # stable, moderate shortfall, severe shortfall, etc.
        "Target_Production": [
            100, 110, 90, 95, 80, 75
        ],

        "Actual_Production": [
            98, 82, 72, 88, 50, 73
        ],

        "Latitude": [
            21.63, 21.81, 14.23,
           21.15, 17.69, 15.82
        ],

        "Longitude": [
            85.58, 80.60, 76.40,
            79.09, 83.22, 80.35
        ],
    }

    return pd.DataFrame(data)

# ==========================================
# DATA STANDARDIZATION
# ==========================================

def standardize_data(df):
    """
    Ensure all required columns exist in the final dataset.
    """

    required_columns = [
        "Location",
        "Soil_Anomaly_Index",
        "Target_Production",
        "Actual_Production",
        "Latitude",
        "Longitude",
        "GEE_NDVI",
        "GEE_Temperature_C",
        "GEE_Soil_Moisture",
        "NASA_Rainfall_mm",
        "GEE_Elevation_m",
        "GEE_Slope_Degrees",
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = None

    return df


# ==========================================
# MAIN DATA PIPELINE
# ==========================================

def fetch_online_data():
    """
    Build the manganese intelligence dataset and enrich it
    with real satellite and environmental data.
    """

    data = get_prototype_data()

    # --------------------------------------
    # FETCH NDVI
    # --------------------------------------

    satellite_ndvi = []

    for _, row in data.iterrows():
        ndvi = get_satellite_ndvi(
            row["Latitude"],
            row["Longitude"]
        )
        satellite_ndvi.append(ndvi)

    data["GEE_NDVI"] = satellite_ndvi

    # --------------------------------------
    # FETCH TEMPERATURE
    # --------------------------------------

    satellite_temperature = []

    for _, row in data.iterrows():
        temperature = get_satellite_temperature(
            row["Latitude"],
            row["Longitude"]
        )
        satellite_temperature.append(temperature)

    data["GEE_Temperature_C"] = satellite_temperature

    # --------------------------------------
    # FETCH SOIL MOISTURE
    # --------------------------------------

    satellite_soil_moisture = []

    for _, row in data.iterrows():
        soil_moisture = get_satellite_soil_moisture(
            row["Latitude"],
            row["Longitude"]
        )
        satellite_soil_moisture.append(soil_moisture)

    data["GEE_Soil_Moisture"] = satellite_soil_moisture

    # --------------------------------------
    # FETCH TERRAIN DATA
    # --------------------------------------

    satellite_elevation = []
    satellite_slope = []

    for _, row in data.iterrows():

        elevation, slope = get_terrain_data(
            row["Latitude"],
            row["Longitude"]
        )

        satellite_elevation.append(elevation)
        satellite_slope.append(slope)

    data["GEE_Elevation_m"] = satellite_elevation
    data["GEE_Slope_Degrees"] = satellite_slope

    # --------------------------------------
    # FETCH NASA RAINFALL
    # --------------------------------------

    nasa_rainfall = []

    for _, row in data.iterrows():

        rainfall = get_nasa_rainfall(
            row["Latitude"],
            row["Longitude"]
        )

        nasa_rainfall.append(rainfall)

    data["NASA_Rainfall_mm"] = nasa_rainfall

    return standardize_data(data)