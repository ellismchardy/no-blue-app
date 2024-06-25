import tkinter as tk 
from tkinter import Scale, Label, HORIZONTAL
import subprocess

def set_color_temperature(temp):
    if temp < 1000:
        temp = 1000
    elif temp > 40000:
        temp = 40000