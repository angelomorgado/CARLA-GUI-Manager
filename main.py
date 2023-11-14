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
from carla_aux import weather_dict, weather_list, connect_to_carla_server

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5 import uic
import qdarktheme

import sys
import random
import time

# UI filename and IP of the carla server
uifile = 'manager.ui'
ip = 'localhost'

class Ui(QtWidgets.QMainWindow):
    def __init__(self, carla_client):
        super(Ui, self).__init__()
        uic.loadUi(uifile, self) # Load the .ui file
        self.carla_client = carla_client

        self.update_terminal('Connected to Carla Server! -- IP: ' + ip)
        qdarktheme.setup_theme('auto')

        # Set combo boxes
        self.available_maps = self.carla_client.get_available_maps()
        self.map_list.addItems(self.available_maps)
        self.weather_list.addItems(weather_list)

        # Set buttons
        self.change_map.clicked.connect(self.change_map_action)
        self.change_weather.clicked.connect(self.change_weather_action)
        self.spawn_vehicles.clicked.connect(self.spawn_vehicles_action)
        self.delete_vehicles.clicked.connect(self.delete_vehicles_action)
        self.activate_autopilot.clicked.connect(self.start_autopilot_action)

        # Set actions
        self.set_theme1.triggered.connect(lambda: qdarktheme.setup_theme())
        self.set_theme2.triggered.connect(lambda: qdarktheme.setup_theme('light'))

        # Get number of cars to spawn from the spinbox
        self.num_vehicles = self.number_of_cars.value()

        self.show()
    
    def update_terminal(self, message):
        self.terminal.clear()
        self.terminal.setText(message)

    def change_map_action(self):
        self.update_terminal('Changing map...')
        map_index = self.map_list.currentIndex()
        world = self.carla_client.get_world()
        current_map = world.get_map()

        if map_index == current_map:
            self.carla_client.reload_world()
            self.update_terminal('Reloaded the current map.')
        else:
            self.carla_client.load_world(self.available_maps[map_index])
            self.update_terminal('Changed map to ' + self.available_maps[map_index])
    
    # TODO: Change the physics manually to the appropriate weather
    def change_weather_action(self):
        weather_index = self.weather_list.currentIndex()
        world = self.carla_client.get_world()
        world.set_weather(weather_dict[weather_index])
        self.update_terminal('Changed weather to ' + weather_list[weather_index])

    def spawn_vehicles_action(self):
        world = self.carla_client.get_world()
        self.num_vehicles = self.number_of_cars.value()

        if world.get_actors().filter('vehicle.*'):
            print('There are vehicles already in the simulation')
            self.update_terminal('There are vehicles already in the simulation.')
            return

        if self.num_vehicles == 0:
            print('No vehicles to spawn')
            self.update_terminal('No vehicles to spawn.')
            return

        vehicle_bp = world.get_blueprint_library().filter('vehicle.*')
        spawn_points = world.get_map().get_spawn_points()
        for i in range(self.num_vehicles):
            vehicle = None
            while vehicle is None:
                spawn_point = random.choice(spawn_points)
                transform = carla.Transform(
                    spawn_point.location,
                    spawn_point.rotation
                )
                try:
                    vehicle = world.try_spawn_actor(random.choice(vehicle_bp), transform)
                except:
                    # try again if failed to spawn vehicle
                    continue
            time.sleep(0.1)
        print('Successfully spawned {} vehicles!'.format(self.num_vehicles))
        self.update_terminal('Successfully spawned {} vehicles.'.format(self.num_vehicles))
    
    def delete_vehicles_action(self):
        world = self.carla_client.get_world()
        for actor in world.get_actors().filter('vehicle.*'):
            actor.destroy()
        print('Successfully deleted all vehicles!')
        self.update_terminal('Successfully deleted all vehicles.')
    
    def start_autopilot_action(self):
        world = self.carla_client.get_world()
        for actor in world.get_actors().filter('vehicle.*'):
            actor.set_autopilot(True)
        print('Successfully started autopilot for all vehicles!')
        self.update_terminal('Successfully started autopilot for all vehicles.')

def main():
    # Connect to carla server
    client = connect_to_carla_server(ip)

    # Initialize gui application
    app = QtWidgets.QApplication(sys.argv)
    window = Ui(client)
    window.setWindowTitle('Carla GUI Manager')
    window.setFixedSize(window.size()) # Make window non-resizable
    app.exec_() # Start the application

if __name__ == '__main__':
    main()