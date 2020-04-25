import time

import keyboard
import numpy as np
import pyautogui
import pyscreenshot as ImageGrab
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import pyttsx3
import random


class AutoJumper():
    def __init__(self, dest_colors, start_timeout):
        time.sleep(start_timeout)
        self.dest_colors = dest_colors
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.say('AutoJumper has started')
        self.engine.runAndWait()

    def find_color(self, arr, elem):
        for x in range(arr.shape[1]):
            for y in range(arr.shape[0]):
                if list(arr[y, x, :]) == elem:
                    return True, x, y
        return False, 0, 0

    def jump_to(self, x, y):
        pyautogui.keyDown('d')
        time.sleep(random.uniform(0.2, 0.3))
        pyautogui.click(x=x, y=y, clicks=2, interval=random.uniform(0.08, 0.12))
        pyautogui.keyUp('d')

    def choose_area(self):
        self.engine.say('Put mouse on the upper left point and press J')
        self.engine.runAndWait()
        flag = True
        while flag:
            if keyboard.is_pressed('m'):
                flag = False
            if keyboard.is_pressed('j'):
                self.upper_left_x, self.upper_left_y = pyautogui.position()
                self.engine.say('Upper left point saved')
                self.engine.say('Put mouse on the bottom right point and press K')
                self.engine.runAndWait()
                print(f'Upper left point coordinates: X {self.upper_left_x}, Y {self.upper_left_y}')
            if keyboard.is_pressed('k'):
                self.bottom_right_x, self.bottom_right_y = pyautogui.position()
                self.engine.say('Bottom right point saved')
                self.engine.runAndWait()
                print(f'Bottom right point coordinates: X {self.bottom_right_x}, Y {self.bottom_right_y}')
                flag = False
        self.engine.say(f'All coordinates saved')
        self.engine.runAndWait()

    def find_dest_gate(self):
        flag = True
        while flag:
            time.sleep(random.uniform(0.15, 0.25))
            im = ImageGrab.grab()
            # im.save('screen.bmp')
            orig_width, orig_height = im.size
            center_x = orig_width // 2
            center_y = orig_height // 2

            im_cropped = im.crop((self.upper_left_x, self.upper_left_y, self.bottom_right_x, self.bottom_right_y))
            im_arr = np.array(im_cropped)
            # im.save('cropped.bmp')

            for dest_color in self.dest_colors:
                result, x, y = self.find_color(im_arr, dest_color)
                x += self.upper_left_x
                y += self.upper_left_y
                if result:
                    print(f'Dest gate found at {x}, {y}')
                    self.jump_to(x, y)
                    pyautogui.moveTo(center_x, center_y, duration=random.uniform(0.4, 0.6),
                                     tween=pyautogui.easeInOutQuad)
                    time.sleep(4)
                    break
            print('No gate found')

            if keyboard.is_pressed('m'):
                print('AutoJumper shutting down')
                flag = False
