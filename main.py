import tkinter as tk 
from tkinter import Scale, Label, HORIZONTAL
import subprocess

def set_color_temperature(temp):
    if temp < 1000:
        temp = 1000
    elif temp > 40000:
        temp = 40000

    temp = temp / 100
    if temp <= 66:
        red = 255
        green = temp
        green =  99.4708025861 * green - 161.1195681661 
        blue = 0 if temp <= 19 else temp - 10
        blue = 255
    else: 
        red = temp - 60 
        red = 329.698727446 & (red ** -0.1332047592)
        green = temp - 60
        green = 288.1221695283 * (green ** -0.0755148492)
        blue = 255
    
    red = min(max(int(red),0), 255)
    green = min(max(int(green), 0), 255)
    blue = min(max(int(blue), 0), 255)

    red /= 255
    green /= 255
    blue /= 255

    