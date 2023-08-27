import openpyxl
import folium
from haversine import haversine
from folium import plugins
from collections import defaultdict
from geopy.geocoders import Nominatim

# Define a class for LaneMap
class LaneMap:
    def __init__(self):
        # Load the Excel workbook and set up the active sheet
        self.wb = openpyxl.load_workbook(filename='test_data1.xlsx')
        self.sheet = self.wb.active

        # Extract relevant columns from the sheet
        self.loaded_col = self.sheet['D'][1:]
        self.origin_city_col = self.sheet['E'][1:]
        self.origin_state_col = self.sheet['F'][1:]
        self.dest_city_col = self.sheet['G'][1:]
        self.dest_state_col = self.sheet['H'][1:]

        # Initialize data storage
        self.lane_counts = defaultdict(int)  # To store counts of lanes
        self.unique_cities = {}  # To store unique city locations
        self.lanes = {}  # To store lane data

    # Method to extract data from Excel
    def get_excel_data(self):
        for index, cell in enumerate(self.loaded_col, start=1):
            if cell.value == 'Loaded':
                origin_city = self.origin_city_col[index - 1].value
                origin_state = self.origin_state_col[index - 1].value
                dest_city = self.dest_city_col[index - 1].value
                dest_state = self.dest_state_col[index - 1].value

                lane = f'{origin_city}, {origin_state} - {dest_city}, {dest_state}'
                self.lane_counts[lane] += 1

    # Method to geolocate cities and gather lane data
    def get_lane_data(self):
        geolocate = Nominatim(user_agent="MyApp")
        sorted_lane_counts = sorted(self.lane_counts.items(), key=lambda x: x[1], reverse=True)

        for lane, count in sorted_lane_counts:
            origin_name, dest_name = lane.split(" - ")

            origin = geolocate.geocode(origin_name)
            destination = geolocate.geocode(dest_name)

            if origin_name not in self.unique_cities:
                self.unique_cities[origin_name] = {'location': (origin.latitude, origin.longitude)}

            if dest_name not in self.unique_cities:
                self.unique_cities[dest_name] = {'location': (destination.latitude, destination.longitude)}

            if origin and destination:
                self.lanes[lane] = {
                    "origin": (origin.latitude, origin.longitude),
                    "destination": (destination.latitude, destination.longitude),
                    "count": count
                }
            else:
                print(f"Coordinates not found for {origin_name} or {dest_name}")

    # Method to plot the map
    def plot_map(self):
        first_origin = list(self.lanes.values())[0]["origin"]
        lanemap = folium.Map(location=first_origin, zoom_start=9)
        heat_data = []

        for key, values in self.lanes.items():
            origin = values["origin"]
            destination = values["destination"]
            count = values["count"]
            distance = haversine(origin, destination)  # Calculate distance in kilometers
            num_segments = int(distance * 100)  # Adjust this factor as needed
            lat_diff = (destination[0] - origin[0]) / num_segments
            lon_diff = (destination[1] - origin[1]) / num_segments
            segments = [(origin[0] + i * lat_diff, origin[1] + i * lon_diff) for i in range(num_segments + 1)]
            heat_data.extend([(lat, lon, count) for lat, lon in segments])

        # Add HeatMap layer
        folium.plugins.HeatMap(heat_data, radius=35, blur=35, min_opacity=0.3).add_to(lanemap)

        # Add markers for unique cities
        for key, values in self.unique_cities.items():
            location = values["location"]
            folium.Marker(location=location, popup=key).add_to(lanemap)

        # Save the map to an HTML file
        lanemap.save('map.html')


if __name__ == "__main__":
    lanemap = LaneMap()
    lanemap.get_excel_data()
    lanemap.get_lane_data()
    lanemap.plot_map()
