'''
This file contains functions that are used to interact with the CARLA environment.
'''
import carla
import re

def is_valid_ip(ip):
    ip_pattern = re.compile(
        r'^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'
    )
    return bool(ip_pattern.match(ip))

def connect_to_carla_server(ip = 'localhost', port=2000):
    # If ran in wsl put the ip of the host machine, not just localhost (e.g., 192.168. ...)
    try:
        client = carla.Client(ip, port)
        client.set_timeout(5.0)
    except Exception as e:
        print('Error connecting to the server: %s' % e)
        return None
    return client

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
