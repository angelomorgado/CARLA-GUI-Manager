# CARLA GUI Manager

This application focused on the Carla client can manage:
- Map selection
- Weather and time of day
- NPC vehicles

---

## TODO

- Change car physics to adapt to different weather

## Known Issues
- When connecting to the CARLA server if the connection time expires, it's impossible to catch the error with a try except, i don't know why, tried everything, so the program crashes, if that happens, simply boot it again.

---

## How to run

1. `pip3 install -r requirements.txt`
2. Run Carla server
3. `python3 main.py`

---

## My Next project

I'm going to build an ego vehicle and then display the sensors' information in one or multiple windows, possible with pygame or another framework.

---

Feel free to leave suggestions or complaints. Always receptive of criticism.