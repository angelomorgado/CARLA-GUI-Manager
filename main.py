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
from carla_functions import change_map_action

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5 import uic
import sys

# Load UI from "manager.ui"
uifile = 'manager.ui'

weather_dict = {
    "ClearNoon": carla.WeatherParameters.ClearNoon,
    "CloudyNoon": carla.WeatherParameters.CloudyNoon,
    "WetNoon": carla.WeatherParameters.WetNoon,
    "WetCloudyNoon": carla.WeatherParameters.WetCloudyNoon,
    "SoftRainNoon": carla.WeatherParameters.SoftRainNoon,
    "MidRainyNoon": carla.WeatherParameters.MidRainyNoon,
    "HardRainNoon": carla.WeatherParameters.HardRainNoon,
    "ClearSunset": carla.WeatherParameters.ClearSunset,
    "CloudySunset": carla.WeatherParameters.CloudySunset,
    "WetSunset": carla.WeatherParameters.WetSunset,
    "WetCloudySunset": carla.WeatherParameters.WetCloudySunset,
    "SoftRainSunset": carla.WeatherParameters.SoftRainSunset,
    "MidRainSunset": carla.WeatherParameters.MidRainSunset,
    "HardRainSunset": carla.WeatherParameters.HardRainSunset,
}

class Ui(QtWidgets.QMainWindow):
    def __init__(self, carla_client):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(uifile, self) # Load the .ui file
        self.carla_client = carla_client

        # Set combo boxes
        self.available_maps = self.carla_client.get_available_maps()
        self.map_list.addItems(self.available_maps)
        self.weather_list.addItems(list(weather_dict.keys()))

        # Set buttons
        self.change_map.clicked.connect(self.change_map_action)

        self.show() # Show the GUI

    def change_map_action(self):
        map_index = self.map_list.currentIndex()
        world = self.carla_client.get_world()
        current_map = world.get_map()

        if map_index == current_map:
            self.carla_client.reload_world()
        else:
            self.carla_client.load_world(self.available_maps[map_index])

def connect_to_carla_server():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
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