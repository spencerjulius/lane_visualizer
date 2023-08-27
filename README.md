# Lane Visualizer

The LaneMap Visualizer is a Python script that reads data from an Excel file containing information about loaded lanes, geolocates the cities involved, and creates an interactive map visualizing the lanes and their traffic.

## Features

- Reads data from an Excel file to extract information about loaded lanes.
- Uses geolocation services to determine the latitude and longitude of cities.
- Generates an interactive map using Folium, displaying lanes as heatmaps and cities as markers.

## Requirements

- Python 3.x
- Required Python packages: openpyxl, folium, haversine, geopy

## Usage

1. Install the required packages:

```bash
pip install openpyxl folium haversine geopy
