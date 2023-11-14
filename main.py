'''
GUI Manager:

Using PyQT5, it creates a GUI for the user to easily interact with the simulation.
It can:
 - Change the weather
 - Change the map
 - Spawn vehicles
'''

# Imports
import typing
import carla
from carla_aux import weather_dict, weather_list, connect_to_carla_server, is_valid_ip

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5 import uic
import qdarktheme

import sys
import random
import time

# UI filename and IP of the carla server
uifile = 'manager.ui'
loginfile = 'login.ui'
ip = 'localhost'

class Login_Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Login_Ui, self).__init__()
        uic.loadUi(loginfile, self) # Load the .ui file
        qdarktheme.setup_theme('light')
        # center status bar message

        self.statusBar.showMessage('Please enter the IP and port of the Carla Server.')

        # Set buttons
        self.confirm_button.clicked.connect(self.login_action)
    
    def login_action(self):
        self.ip = self.ip_set.text().strip()
        self.port = self.port_set.text().strip()

        # Verify the ip and port
        # If the port is empty, set it to 2000
        if self.port == '':
            self.port = '2000'

        # If the ip is empty, set it to localhost
        if self.ip == '':
            self.ip = 'localhost'

        # If the ip is not empty, check if it is a valid ip address
        if self.ip != 'localhost' and not is_valid_ip(self.ip):
            self.statusBar.showMessage('Invalid IP address.')
            return
        
        # If the port is not empty, check if it is a valid port number
        if not self.port.isdigit():
            self.statusBar.showMessage('Invalid port number.')
            return
        else:
            self.port = int(self.port)

        # Connect if valid
        self.statusBar.showMessage('Connecting to Carla server, it may take 15 seconds...')
        self.carla_client = connect_to_carla_server(self.ip, self.port)
        if self.carla_client is None:
            self.statusBar.showMessage('Failed to connect to Carla Server!')
        else:
            self.statusBar.showMessage('Connected to Carla Server! -- IP: ' + self.ip + ' Port: ' + str(self.port))
            self.main_window = Main_Ui(self.carla_client)
            self.main_window.setFixedSize(self.main_window.size())

            # Close the login window
            self.close()
            self.main_window.show()
        
class Main_Ui(QtWidgets.QMainWindow):
    def __init__(self, carla_client):
        super(Main_Ui, self).__init__()
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
        self.update_terminal(f'Spawning {self.num_vehicles} vehicles...')

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
    app = QtWidgets.QApplication(sys.argv)
    window = Login_Ui()
    window.setFixedSize(window.size()) # Make window non-resizable
    window.show()
    app.exec_() # Start the application

if __name__ == '__main__':
    main()