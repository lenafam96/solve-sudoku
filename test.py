import pyautogui as pya
from PIL import Image
import numpy as np
import cv2

# Switch to the window on macOS
pya.keyDown('command')
pya.press('tab')
pya.keyUp('command')
