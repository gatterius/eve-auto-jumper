import time

import keyboard
import numpy as np
import pyautogui
import pyscreenshot as ImageGrab
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import pyttsx3
import random


class AutoJumper:
    """
    This is a class for constant jumping through the next destination object (stargate/ansiblex gate/citadel) while any
    is present in overview. It works by selecting a detection area, finding a part with given color in it and pressing
    jump on this part.
    Attributes:
        dest_colors: list of colors which belong to destination objects in overview
        engine: text-to-speech engine
        upper_left_x, upper_left_y: upper left corner of destination object detection area of screen
        bottom_right_x, bottom_right_y: bottom right corner of destination object detection area of screen
    """

    def __init__(self, dest_colors, start_timeout):
        time.sleep(start_timeout)
        self.dest_colors = dest_colors
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.say('AutoJumper has started')
        self.engine.runAndWait()
        self.engine.say('Setting overview window coordinates')
        self.engine.runAndWait()
        self.over_upper_left_x, self.over_upper_left_y, \
        self.over_bottom_right_x, self.over_bottom_right_y = self.choose_screen_area()

    def find_color(self, arr, color):
        """
        Finds pixel of given color on image (in np.array form) by simply scanning through the whole array. Returns the
        coordinates of first found pixel (zeros if color was not found).

        Parameters:
            -arr: image in np.array form
            -color: color to be found

        Returns:
            -result: True or False depending on whether the color was found
            -x: x coordinate of found pixel (0 if none found)
            -y: y coordinate of found pixel (0 if none found)
        """
        for x in range(arr.shape[1]):
            for y in range(arr.shape[0]):
                if list(arr[y, x, :]) == color:
                    return True, x, y
        return False, 0, 0

    def jump_to(self, x, y):
        """
        Jumps through the gate by pressing D key on given screen coordinates.

        Parameters:
            -x: x coordinate of gate in overview window
            -y: y coordinate of gate in overview window
        Returns:
            None
        """
        pyautogui.keyDown('d')
        time.sleep(random.uniform(0.2, 0.3))
        pyautogui.click(x=x, y=y, clicks=2, interval=random.uniform(0.08, 0.12))
        pyautogui.keyUp('d')

    def choose_screen_area(self):
        """
        Saves screen coordinates by choosing bbox corners using mouse pointer.

        Parameters:
            None
        Returns:
            upper_left_x: x coordinate of upper left corner of bbox
            upper_left_y: y coordinate of upper left corner of bbox
            bottom_right_x: x coordinate of bottom right corner of bbox
            bottom_right_y: y coordinate of bottom right corner of bbox
        """
        upper_left_x, upper_left_y, bottom_right_x, bottom_right_y = 0, 0, 0, 0
        self.engine.say('Put mouse on the upper left point and press J')
        self.engine.runAndWait()
        flag = True
        while flag:
            if keyboard.is_pressed('m'):
                flag = False
            if keyboard.is_pressed('j'):
                upper_left_x, upper_left_y = pyautogui.position()
                self.engine.say('Upper left point saved')
                self.engine.say('Put mouse on the bottom right point and press K')
                self.engine.runAndWait()
                print(f'Upper left point coordinates: X {upper_left_x}, Y {upper_left_y}')
            if keyboard.is_pressed('k'):
                bottom_right_x, bottom_right_y = pyautogui.position()
                self.engine.say('Bottom right point saved')
                self.engine.runAndWait()
                print(f'Bottom right point coordinates: X {bottom_right_x}, Y {bottom_right_y}')
                flag = False
        self.engine.say(f'All coordinates saved')
        self.engine.runAndWait()
        return upper_left_x, upper_left_y, bottom_right_x, bottom_right_y

    def find_dest_gate(self, mode):
        """
        Finds destination object icon in the detection area of screen by looking for pixels of designated color and
        jumps through it. The search is conducted continuously, no limit to the number of jumps is given. The cycle can
        be stopped my pressing 'M' key.

        Parameters:
            mode: mode of next gate detection
        Returns:
            None
        """
        if mode == 'color':
            flag = True
            while flag:
                time.sleep(random.uniform(0.15, 0.25))
                im = ImageGrab.grab()
                # im.save('screen.bmp')
                orig_width, orig_height = im.size
                center_x = orig_width // 2
                center_y = orig_height // 2

                im_cropped = im.crop((self.over_upper_left_x, self.over_upper_left_y,
                                      self.over_bottom_right_x, self.over_bottom_right_y))
                im_arr = np.array(im_cropped)
                # im.save('cropped.bmp')

                for dest_color in self.dest_colors:
                    result, x, y = self.find_color(im_arr, dest_color)
                    x += self.over_upper_left_x
                    y += self.over_upper_left_y
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
        # elif mode == 'ocr':

