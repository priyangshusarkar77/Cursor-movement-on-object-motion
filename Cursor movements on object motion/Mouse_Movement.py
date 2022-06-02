import numpy as np
import cv2 as cv
import time
import mouse as m
import pyautogui as py
import screen_brightness_control as bright



class AirTouch:
    def __init__(self):
        self.screen = py.size()
        self.prev_x = 0
        self.prev_y = 0
        self.mute_operations = 0

    def track(self, ptr, draw=False, ptr1=None, ptr2=None, img=None, smooth_factor=8, stealth=False):
        if ptr is not None:
            ptr = list(ptr)
            if ptr[0] > ptr2[0]:
                ptr[0] = ptr2[0]
            elif ptr[0] < ptr1[0]:
                ptr[0] = ptr1[0]

            if ptr[1] < ptr1[1]:
                ptr[1] = ptr1[1]
            elif ptr[1] > ptr2[1]:
                ptr[1] = ptr2[1]

            if not stealth:
                smooth_factor = 25 - smooth_factor

            relative_coord_x = np.interp(ptr[0], (ptr1[0], ptr2[0]), (0, self.screen[0]))
            relative_coord_y = np.interp(ptr[1], (ptr1[1], ptr2[1]), (0, self.screen[1]))
            newx = self.prev_x + (relative_coord_x - self.prev_x)/smooth_factor
            newy = self.prev_y + (relative_coord_y - self.prev_y) / smooth_factor
            self.prev_x = newx
            self.prev_y = newy
            m.move(newx, newy)
            if draw:
                cv.rectangle(img, ptr1, ptr2, (0, 255, 0), 2)

    def left_click(self):
        py.click()
        time.sleep(0.2)

    def right_click(self):
        py.click(button="right")
        time.sleep(0.6)

    def volume_ctrl(self, y_coordinate, range):

        mid = int((range[1] - range[0]) / 2)
        mid = mid + range[0]
        if y_coordinate > range[1]:
            self.mute_operations = self.mute_operations + 1
            if self.mute_operations > 18:
                py.press("volumemute")
                self.mute_operations = 0
        elif y_coordinate < mid:
            cur_op = 1
            py.press("volumeup")
        elif y_coordinate > mid:
            cur_op = 0
            py.press("volumedown")

    def mouse_scroll(self, scroll_point, ptr1, ptr2):
        referece_range = int((ptr2[1] - ptr1[1]))
        if scroll_point[1] > int(referece_range * 0.75) + ptr1[1]:
            py.scroll(-1 * int(scroll_point[1] - (referece_range * 0.75 + ptr1[1])))
        elif scroll_point[1] < int(referece_range * 0.25) + ptr1[1]:
            py.scroll(int(referece_range * 0.25) + ptr1[1] - scroll_point[1])

    def mouse_bright(self, val, range):
        if val > range[1]:
            val = range[1]
        elif val < range[0]:
            val = range[0]
        bright.set_brightness(int(((range[1] - val)/(range[1] - range[0]))*100))


