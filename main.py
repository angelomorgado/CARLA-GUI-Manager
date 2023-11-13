'''
GUI Manager:

Using PyQT5, it creates a GUI for the user to easily interact with the simulation.
It can:
 - Change the weather
 - Change the map
 - Spawn vehicles
'''

# Imports
import carla

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5 import uic
import sys

# Load UI from "manager.ui"
uifile = 'manager.ui'

# List of weather presets
weather_dict = {
    0 : carla.WeatherParameters.ClearNoon,
    1 : carla.WeatherParameters.CloudyNoon,
    2 : carla.WeatherParameters.WetNoon,
    3 : carla.WeatherParameters.WetCloudyNoon,
    4 : carla.WeatherParameters.SoftRainNoon,
    5 : carla.WeatherParameters.MidRainyNoon,
    6 : carla.WeatherParameters.HardRainNoon,
    7 : carla.WeatherParameters.ClearSunset,
    8 : carla.WeatherParameters.CloudySunset,
    9 : carla.WeatherParameters.WetSunset,
    10 : carla.WeatherParameters.WetCloudySunset,
    11 : carla.WeatherParameters.SoftRainSunset,
    12 : carla.WeatherParameters.MidRainSunset,
    13 : carla.WeatherParameters.HardRainSunset,
}

weather_list = [
    "ClearNoon",
    "CloudyNoon",
    "WetNoon",
    "WetCloudyNoon",
    "SoftRainNoon",
    "MidRainyNoon",
    "HardRainNoon",
    "ClearSunset",
    "CloudySunset",
    "WetSunset",
    "WetCloudySunset",
    "SoftRainSunset",
    "MidRainSunset",
    "HardRainSunset",
]
class Ui(QtWidgets.QMainWindow):
    def __init__(self, carla_client):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(uifile, self) # Load the .ui file
        self.carla_client = carla_client

        # Set combo boxes
        self.available_maps = self.carla_client.get_available_maps()
        self.map_list.addItems(self.available_maps)
        self.weather_list.addItems(weather_list)

        # Set buttons
        self.change_map.clicked.connect(self.change_map_action)
        self.change_weather.clicked.connect(self.change_weather_action)

        self.show() # Show the GUI

    def change_map_action(self):
        map_index = self.map_list.currentIndex()
        world = self.carla_client.get_world()
        current_map = world.get_map()

        if map_index == current_map:
            self.carla_client.reload_world()
        else:
            self.carla_client.load_world(self.available_maps[map_index])
    
    # TODO: Change the physics manually to the appropriate weather
    def change_weather_action(self):
        weather_index = self.weather_list.currentIndex()
        world = self.carla_client.get_world()
        world.set_weather(weather_dict[weather_index])

def connect_to_carla_server():
    client = carla.Client('localhost', 2000)
    client.set_timeout(100.0)
    return client

def main():
    # Connect to carla server
    client = connect_to_carla_server()

    # Initialize gui application
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui(client) # Create an instance of our class
    window.setFixedSize(window.size()) # Make window non-resizable
    app.exec_() # Start the application

if __name__ == '__main__':
    main()