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
        self.map_list = self.carla_client.get_available_maps()
        self.weather_list = list(weather_dict.keys())

        # Set buttons

        self.show() # Show the GUI


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