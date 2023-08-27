# Lane Visualizer

The Lane Visualizer is a Python script that reads data from an Excel file containing information about loaded lanes, 
geolocates the cities involved, and creates an interactive map visualizing the lanes and their traffic.

<iframe src="https://drive.google.com/file/d/19ukbAPzOAJZ3y8zYredZZKnSd4Gr6X23/preview" width="640" height="480" allow="autoplay"></iframe>

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
```

2. Replace the test_data4.xlsx file with your own Excel file containing the lane data.

3. Run the script:

```bash
python lane_map.py
```
4. After the script completes, open the generated map.html file in your web browser to view the interactive heatmap.

## Customizing Excel Parameters

The LaneMap Visualizer script is designed to work with Excel files containing lane data. 
To customize the script for your specific use case, follow these steps:

1. Open the `lane_map.py` file in a text editor.

2. Locate the `LaneMap` class's constructor (`__init__` method).
In this method, you'll find code that loads data from the Excel file:

```python
self.wb = openpyxl.load_workbook(filename='test_data4.xlsx')
self.sheet = self.wb.active

# Extract relevant columns from the sheet
self.loaded_col = self.sheet['D'][1:]
self.origin_city_col = self.sheet['E'][1:]
self.origin_state_col = self.sheet['F'][1:]
self.dest_city_col = self.sheet['G'][1:]
self.dest_state_col = self.sheet['H'][1:]
```

3. Replace 'test_data4.xlsx' with the path to your Excel file.
Make sure your Excel file follows a similar structure with columns for loaded status, origin city, origin state, destination city, and destination state.

4. Adjust the column indices in the above code if your Excel file has a different structure. For example, if your "Loaded" status is in column C, update 'D' to 'C'.

5. Save the lane_map.py file after making these changes.

6. Run the script again to generate the map based on your customized Excel data:

```bash
python lane_map.py
```

This will ensure that the script correctly reads and processes your Excel data to create the interactive map.

## Additional Configuration

1. Adjust the radius, blur, and min_opacity values in the folium.plugins.HeatMap function call to control the appearance of the heatmap.

```python
# Add HeatMap layer
folium.plugins.HeatMap(heat_data, radius=35, blur=35, min_opacity=0.3).add_to(lanemap)
```

2. Modify the num_segments calculation to change the level of detail in the lane segments on the map.
Since a normal heat map uses points to visualize data, this code creates segments of data between the
origin and destination to visualize the frequency of the lane. Adjust as needed.

```python
    def plot_map(self):
        first_origin = list(self.lanes.values())[0]["origin"]
        lanemap = folium.Map(location=first_origin, zoom_start=9)
        heat_data = []

        for key, values in self.lanes.items():
            origin = values["origin"]
            destination = values["destination"]
            count = values["count"]
            distance = haversine(origin, destination)
            num_segments = int(distance * 100)  # <-- Adjust this factor as needed --
```
## Contributing

If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. We welcome contributions to make this tool more versatile and useful.

Note: This project is for educational purposes and may require additional enhancements for production use.
