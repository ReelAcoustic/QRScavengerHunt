import os
import sys
import psutil
import playsound
import time

sound = os.path.join(os.path.dirname(__file__), 'sound.mp3')
battery = psutil.sensors_battery()

