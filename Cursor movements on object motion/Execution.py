import base64
import time#
import keyboard#
import Hand_Detector#
import Mouse_Movement#
import os#
import Tkinter_object as tp#
import cv2 as cv#
from tkinter import *#
from tkinter import messagebox as mb#
import pyautogui as pg#
from os.path import exists#
import pickle#
from help_description import help_1#
from help_shortcut import help_2#
from io import BytesIO
import win32api#
import PIL.Image as pi#
import PIL.ImageTk as pk#
import sys#
import ctypes#



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)
win32api.SetConsoleTitle("AirTouch")

screen_width = pg.size()[0]
screen_height = pg.size()[1]
webcam_id = None


class ReferencePoints:
    def __init__(self):
        self.rptr1 = None
        self.rptr2 = None

    def update(self, ptr1=None, ptr2=None):
        self.rptr1 = ptr1
        self.rptr2 = ptr2


class Gesture:
    def __init__(self):
        self.ges_list = ["Default"]
        self.gestures = [[100001, 100011, 101001, 100111, 101000, 101100, "Default", 13, 5, [None, None], "Top",
                          False]]
        self.possible_gestures = [100001, 100011, 100111, 101000, 101100, 101110]

    def add_new_gesture(self, new_ges):
        self.gestures.append(new_ges)

    def update_gestures(self, name_index, gesture_index, value):
        self.gestures[name_index][gesture_index] = value

    def gestures_list_updater(self):
        for i in self.gestures:
            if i[6] not in self.ges_list:
                self.ges_list.append(i[6])

    def get_gesture(self, gesture_name):
        for i in self.gestures:
            for j in i:
                if j == gesture_name:
                    return self.gestures.index(i)
        return 0

    def isGesturePresent(self, gesture_name):
        for i in self.gestures:
            if gesture_name in i:
                return True
        return False

    def gestureColliderChecker(self, gesture_value, its_index, gesture_position):
        for i in self.gestures[gesture_position]:
            if self.gestures[gesture_position].index(i) != its_index:
                if i == gesture_value:
                    return self.gestures[gesture_position].index(i)
        return -1

    def is_new_gesture_possible(self, gesture_val):
        if gesture_val in self.possible_gestures:
            return True
        else:
            return False


class Gesture_prev:
    name = "Default"


ges_Prev = Gesture_prev()
all_gestures = Gesture()
rptr = ReferencePoints()


def end_program():
    exit(0)


def webcam_config():
    global webcam_id

    def get_input(event=None):
        global webcam_id
        global recurrence
        webcam_id = None
        try:
            value = input_id.get(1.0, "end-1c")
            if value == "":
                raise
            temp_webcam_id = int(value)
            temp_vid = cv.VideoCapture(temp_webcam_id)
            if temp_vid.isOpened():
                webcam_id = temp_webcam_id
                webcam_data = open("Webcam Config.pickle", "wb")
                pickle.dump(webcam_id, webcam_data)
                del temp_vid
                window_2.quit()
                window_2.destroy()
                window_1.deiconify()
                window_1.quit()
                window_1.destroy()
                recurrence = False
            else:
                mb.showerror("Webcam Configuration", "The Webcam ID, you specified is not available. Please try again")
                window_2.quit()
                window_2.destroy()
                window_1.deiconify()
                window_1.quit()
                window_1.destroy()

        except:
            mb.showerror("Invalid Input", "Please Enter the Valid Input.")
            window_2.quit()
            window_2.destroy()
            window_1.deiconify()
            window_1.quit()
            window_1.destroy()

    global screen_width
    global screen_height
    recurrence = True
    while recurrence:
        window_1 = Tk()
        window_1.withdraw()
        window_1.geometry("500x500")
        result = mb.askyesnocancel("Webcam Configuration", "Do you know the ID of your Webcam?")
        if result:
            window_2 = Tk()
            window_2.title("Webcam Configuration")
            relative_width = 384
            relative_height = 216
            relative_size = str(relative_width) + "x" + str(relative_height)
            relative_x = 768
            relative_y = 432
            relative_coordinates = '+' + str(relative_x) + '+' + str(relative_y)
            window_2.geometry(relative_size)
            window_2.geometry(relative_coordinates)
            window_2.protocol("WM_DELETE_WINDOW", end_program)
            information_label1 = Label(window_2, text="Specify the Webcam ID:")
            information_label1.config(font=('Helvetica bold', 11))
            information_label1.place(relx=0.5, rely=0.1, anchor=CENTER)
            input_id = Text(window_2, height=1, width=18)
            input_id.place(relx=0.5, rely=0.3, anchor=CENTER)
            enter_button = Button(window_2, text="Enter", command=get_input)
            enter_button.config(font=('Helvetica bold', 15))
            enter_button.place(relx=0.5, rely=0.6, anchor=CENTER)
            input_id.config(font=('Helvetica bold',17))
            information_label2 = Label(window_2, text="If you have only one webcam, \nthen type 0 and click on Enter.")
            information_label2.config(font=('Helvetica bold', 11))
            information_label2.place(relx=0.5, rely=0.85, anchor=CENTER)
            window_2.bind("<Return>", get_input)
            window_2.mainloop()
            if webcam_id is not None:
                recurrence = False

        elif result == False:
            temp_res = mb.askokcancel("Webcam Configuration", "We will show each webcam one by one and if the required "
                                                              "webcam is displayed then select Yes else No")
            if temp_res:
                webcam_id_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                webcam_id = None
                for i in webcam_id_list:
                    obj = tp.WebCamConfiguration(i)
                    if obj.stat2:
                        result = mb.askyesnocancel("Webcam Configuration", "Do you want to select this camera?")
                    if result:
                        webcam_id = i
                        webcam_data = open("Webcam Config.pickle", "wb")
                        pickle.dump(webcam_id, webcam_data)
                        window_1.deiconify()
                        window_1.quit()
                        window_1.destroy()
                        recurrence = False
                        break
                    elif result == False:
                        del obj
                        continue
                    else:
                        end_program()
                if webcam_id is None:
                    mb.showerror("Webcam Configuration", "All available Webcam are displayed. Please select a Webcam")
                    window_1.deiconify()
                    window_1.quit()
                    window_1.destroy()
            else:
                end_program()
        else:
            end_program()

flag_check = 0


def reference_frame_config():
    global rptr
    global flag_check
    while all_gestures.gestures[ges_idx][9][0] is None and all_gestures.gestures[ges_idx][9][1] is None:
        flag_check = 1
        webcam_obj = tp.WebCamDisplay(webcam_id, all_gestures.gestures[ges_idx][9][0], all_gestures.gestures[ges_idx][9][1], 0)
        all_gestures.gestures[ges_idx][9][0] = webcam_obj.point1
        if webcam_obj.stat1:
            all_gestures.gestures[ges_idx][9][0] = None
            webcam_config()
            continue
        webcam_obj = tp.WebCamDisplay(webcam_id, all_gestures.gestures[ges_idx][9][0], all_gestures.gestures[ges_idx][9][1], 1)
        if webcam_obj.stat2:
            all_gestures.gestures[ges_idx][9][0] = None
            continue
        all_gestures.gestures[ges_idx][9][1] = webcam_obj.point2

    if flag_check == 1:
        all_gestures.gestures[ges_idx][9][0] = list(all_gestures.gestures[ges_idx][9][0])
        all_gestures.gestures[ges_idx][9][1] = list(all_gestures.gestures[ges_idx][9][1])
        all_gestures.gestures[ges_idx][9][0].remove(8)
        all_gestures.gestures[ges_idx][9][1].remove(8)

    if all_gestures.gestures[ges_idx][9][0][0] > all_gestures.gestures[ges_idx][9][1][0]:
        temp = all_gestures.gestures[ges_idx][9][0][0]
        all_gestures.gestures[ges_idx][9][0][0] = all_gestures.gestures[ges_idx][9][1][0]
        all_gestures.gestures[ges_idx][9][1][0] = temp

    if all_gestures.gestures[ges_idx][9][0][1] > all_gestures.gestures[ges_idx][9][1][1]:
        temp = all_gestures.gestures[ges_idx][9][0][1]
        all_gestures.gestures[ges_idx][9][0][1] = all_gestures.gestures[ges_idx][9][1][1]
        all_gestures.gestures[ges_idx][9][1][1] = temp


if exists("Webcam Config.pickle"):
    prev_webcam_config = open("Webcam Config.pickle", "rb")
    if os.stat("Webcam Config.pickle").st_size != 0:
        try:
            webcam_id = pickle.load(prev_webcam_config)
            temp_vid = cv.VideoCapture(webcam_id)
            if not temp_vid.isOpened():
                webcam_config()
        except:
            webcam_config()
    else:
        webcam_config()
    prev_webcam_config.close()
else:
    webcam_config()





if exists("Gesture Config__prev.pickle"):
    prev_gesture_config = open("Gesture Config__prev.pickle", "rb")
    if os.stat("Gesture Config__prev.pickle").st_size != 0:
        try:
            ges_Prev = pickle.load(prev_gesture_config)
        except:
            ges_Prev = Gesture_prev()
    prev_gesture_config.close()



if exists("Gesture Config__memory.pickle"):
    gesture_memory = open("Gesture Config__memory.pickle", "rb")
    if os.stat("Gesture Config__memory.pickle").st_size != 0:
        try:
            all_gestures = pickle.load(gesture_memory)
        except:
            all_gestures = Gesture()
    gesture_memory.close()

if not all_gestures.isGesturePresent(ges_Prev.name):
    ges_Prev.name = "Default"
    ges_idx = 0
else:
    ges_idx = all_gestures.get_gesture(ges_Prev.name)

mode = all_gestures.gestures[all_gestures.get_gesture(ges_Prev.name)][11]

def pm():
    global mode
    mode = True
    temp_wind.destroy()

def gui():
    global mode
    mode = False
    temp_wind.destroy()


if mode is None:
    temp_wind = Tk()
    temp_wind.geometry("750x200")
    temp_wind.title("Mode Selection")
    information_about_mode = Label(master=temp_wind, text="Select \"Performance Mode\" for less latency or Select \"GUI"
                                                          " Mode\" to\nAdjust the settings using a Graphical User Interface")
    information_about_mode.config(font=("Arial", 13))
    information_about_mode.place(relx=0.067, rely=0.1)
    b1 = Button(master=temp_wind, text="Performance Mode", command=pm)
    b1.config(font=("Arial", 12))
    b1.place(relx=0.067, rely=0.65)
    b2 = Button(master=temp_wind, text="GUI Mode", command=gui)
    b2.config(font=("Arial", 12), width=16)
    b2.place(relx= 0.38, rely=0.65)
    b3 = Button(master=temp_wind, text="Cancel", command=end_program)
    b3.config(font=("Arial", 12), width=16)
    b3.place(relx= 0.7, rely=0.65)
    temp_wind.protocol("WM_DELETE_WINDOW", end_program)
    temp_wind.mainloop()


def stealth_checker(current_coordinates):
    global stealth_check
    if hand.dist((stealth_check[0], stealth_check[1]), (current_coordinates[0], current_coordinates[1])) \
            < 1.5:
        return True
    else:
        return False

ptime = 0

execution = True


def onsky():
    os.startfile(r"C:\WINDOWS\system32\osk.exe")

def pause_destroy():
    temp_wind.quit()
    temp_wind.destroy()

while execution:
    if mode == True:
        def information_window_close():
            information_window.quit()
            information_window.destroy()

        information_window = Tk()
        information_window.geometry("600x115")
        information_window.title("Performance Mode")
        information_window.protocol("WM_DELETE_WINDOW", information_window_close)
        message = Label(master=information_window,
                                       text="Starting in Performance Mode. \nTo open help window press alt + h."
                                            "\nTo terminate properly, always use alt + v shortcut only."
                                            "\nPlease don't close the console window by yourself.")
        message.config(font=("Arial", 13))
        message.place(relx=0.067, rely=0.05)
        information_window.attributes('-topmost', True)
        information_window.after(2500, information_window_close)
        information_window.mainloop()

        video_obj = cv.VideoCapture(webcam_id)
        termination1 = False
        hand = Hand_Detector.HandDetector()
        gesture_index = all_gestures.get_gesture(ges_Prev.name)
        mouse = Mouse_Movement.AirTouch()
        prev_count = 0
        total = 0
        c = 0
        prev_fing = all_gestures.gestures[gesture_index][0]
        pause = False
        proof_stealth = 0
        stealth_confirm = 0
        stealth_check = [0, 0]
        prev_time = 0
        on_screen_proof = 0
        pause_proof = 0
        is_help_open = False
        while not termination1:
            if True:
                con, img = video_obj.read()
                img = cv.flip(img, 1)
                fingers, coordinates = hand.position(img, -1)
                if coordinates is not None:
                    if fingers == prev_fing:
                        if fingers == 101111:
                            on_screen_proof = on_screen_proof + 1
                            if on_screen_proof > 68 and not pause:
                                onsky()
                                on_screen_proof = 0
                        elif fingers == 100000:
                            if not pause:
                                pause_proof = pause_proof + 1
                                if pause_proof > 80:
                                    pause_proof = 0
                                    pause = True
                                    temp_wind = Tk()
                                    temp_wind.geometry("500x100")
                                    temp_wind.title("Pause Mode")
                                    temp_wind.protocol("WM_DELETE_WINDOW", pause_destroy)
                                    information_about_mode = Label(master=temp_wind,
                                                                            text="Pause mode is activated successfully")
                                    information_about_mode.config(font=("Arial", 13))
                                    information_about_mode.place(relx=0.067, rely=0.25)
                                    temp_wind.attributes('-topmost', True)
                                    temp_wind.after(3500, pause_destroy)
                                    temp_wind.mainloop()
                        elif fingers == 101011:
                            if pause:
                                pause_proof = pause_proof + 1
                                if pause_proof > 80:
                                    pause = False
                                    pause_proof = 0
                                    temp_wind = Tk()
                                    temp_wind.geometry("500x100")
                                    temp_wind.title("Pause Mode")
                                    information_about_mode = Label(master=temp_wind,
                                                                   text="Pause mode is deactivated successfully.")
                                    information_about_mode.config(font=("Arial", 13))
                                    information_about_mode.place(relx=0.067, rely=0.3)
                                    temp_wind.protocol("WM_DELETE_WINDOW", pause_destroy)
                                    temp_wind.attributes('-topmost', True)
                                    temp_wind.after(3500, pause_destroy)
                                    temp_wind.mainloop()
                        else:
                            pause_proof = 0
                            on_screen_proof = 0
                        if not pause:
                            if fingers == all_gestures.gestures[gesture_index][0]:
                                if fingers % 10 == 1:
                                    temp_cood = (coordinates[1][1], coordinates[1][2])
                                    if stealth_checker(temp_cood):
                                        proof_stealth = proof_stealth + 1
                                        if proof_stealth > 2:
                                            stealth_confirm = 0
                                            mouse.track([temp_cood[0], temp_cood[1]],
                                                        ptr1=all_gestures.gestures[gesture_index][9][0],
                                                        ptr2=all_gestures.gestures[gesture_index][9][1], stealth=True)
                                            one_point = temp_cood
                                        else:
                                            mouse.track([temp_cood[0], temp_cood[1]],
                                                        ptr1=all_gestures.gestures[gesture_index][9][0],
                                                        ptr2=all_gestures.gestures[gesture_index][9][1],
                                                        smooth_factor=all_gestures.gestures[gesture_index][7])
                                    else:
                                        stealth_confirm = stealth_confirm + 1
                                        if stealth_confirm > 2:
                                            mouse.track([temp_cood[0], temp_cood[1]],
                                                        ptr1=all_gestures.gestures[gesture_index][9][0],
                                                        ptr2=all_gestures.gestures[gesture_index][9][1],
                                                        smooth_factor=all_gestures.gestures[gesture_index][7])
                                            proof_stealth = 0

                                    stealth_check = [temp_cood[0], temp_cood[1]]
                                else:
                                    if (fingers % 100) / 10 == 1:
                                        temp_cood = (coordinates[3][1], coordinates[3][2])
                                        if stealth_checker(temp_cood):
                                            proof_stealth = proof_stealth + 1
                                            if proof_stealth > 2:
                                                stealth_confirm = 0
                                                mouse.track([temp_cood[0], temp_cood[1]],
                                                            ptr1=all_gestures.gestures[gesture_index][9][0],
                                                            ptr2=all_gestures.gestures[gesture_index][9][1], stealth=True)
                                                one_point = temp_cood
                                            else:
                                                mouse.track([temp_cood[0], temp_cood[1]],
                                                            ptr1=all_gestures.gestures[gesture_index][9][0],
                                                            ptr2=all_gestures.gestures[gesture_index][9][1],
                                                            smooth_factor=all_gestures.gestures[gesture_index][7])
                                        else:
                                            stealth_confirm = stealth_confirm + 1
                                            if stealth_confirm > 2:
                                                mouse.track([temp_cood[0], temp_cood[1]],
                                                            ptr1=all_gestures.gestures[gesture_index][9][0],
                                                            ptr2=all_gestures.gestures[gesture_index][9][1],
                                                            smooth_factor=all_gestures.gestures[gesture_index][7])
                                                proof_stealth = 0

                                        stealth_check = [temp_cood[0], temp_cood[1]]
                                    elif (fingers % 1000) / 100 == 1:
                                        temp_cood = (coordinates[5][1], coordinates[5][2])
                                        if stealth_checker(temp_cood):
                                            proof_stealth = proof_stealth + 1
                                            if proof_stealth > 2:
                                                stealth_confirm = 0
                                                mouse.track([temp_cood[0], temp_cood[1]],
                                                            ptr1=all_gestures.gestures[gesture_index][9][0],
                                                            ptr2=all_gestures.gestures[gesture_index][9][1], stealth=True)
                                                one_point = temp_cood
                                            else:
                                                mouse.track([temp_cood[0], temp_cood[1]],
                                                            ptr1=all_gestures.gestures[gesture_index][9][0],
                                                            ptr2=all_gestures.gestures[gesture_index][9][1],
                                                            smooth_factor=all_gestures.gestures[gesture_index][7])
                                        else:
                                            stealth_confirm = stealth_confirm + 1
                                            if stealth_confirm > 2:
                                                mouse.track([temp_cood[0], temp_cood[1]],
                                                            ptr1=all_gestures.gestures[gesture_index][9][0],
                                                            ptr2=all_gestures.gestures[gesture_index][9][1],
                                                            smooth_factor=all_gestures.gestures[gesture_index][7])
                                                proof_stealth = 0

                                        stealth_check = [temp_cood[0], temp_cood[1]]
                                    elif (fingers % 10000) / 1000 == 1:
                                        temp_cood = (coordinates[7][1], coordinates[7][2])
                                        if stealth_checker(temp_cood):
                                            proof_stealth = proof_stealth + 1
                                            if proof_stealth > 2:
                                                stealth_confirm = 0
                                                mouse.track([temp_cood[0], temp_cood[1]],
                                                            ptr1=all_gestures.gestures[gesture_index][9][0],
                                                            ptr2=all_gestures.gestures[gesture_index][9][1], stealth=True)
                                                one_point = temp_cood
                                            else:
                                                mouse.track([temp_cood[0], temp_cood[1]],
                                                            ptr1=all_gestures.gestures[gesture_index][9][0],
                                                            ptr2=all_gestures.gestures[gesture_index][9][1],
                                                            smooth_factor=all_gestures.gestures[gesture_index][7])
                                        else:
                                            stealth_confirm = stealth_confirm + 1
                                            if stealth_confirm > 2:
                                                mouse.track([temp_cood[0], temp_cood[1]],
                                                            ptr1=all_gestures.gestures[gesture_index][9][0],
                                                            ptr2=all_gestures.gestures[gesture_index][9][1],
                                                            smooth_factor=all_gestures.gestures[gesture_index][7])
                                                proof_stealth = 0

                                        stealth_check = [temp_cood[0], temp_cood[1]]
                                    else:
                                        mouse.track([coordinates[1][1], coordinates[1][2]])
                            elif fingers == all_gestures.gestures[gesture_index][1]:
                                mouse.left_click()
                                prev_fing = None
                            elif fingers == all_gestures.gestures[gesture_index][2]:
                                mouse.right_click()
                            elif fingers == all_gestures.gestures[gesture_index][3]:
                                if fingers % 10 == 1:
                                    mouse.mouse_scroll([coordinates[1][1], coordinates[1][2]],
                                                       ptr1=all_gestures.gestures[gesture_index][9][0],
                                                       ptr2=all_gestures.gestures[gesture_index][9][1])
                                else:
                                    if (fingers % 100) / 10 == 1:
                                        mouse.mouse_scroll([coordinates[3][1], coordinates[3][2]],
                                                           ptr1=all_gestures.gestures[gesture_index][9][0],
                                                           ptr2=all_gestures.gestures[gesture_index][9][1])
                                    elif (fingers % 1000) / 100 == 1:
                                        mouse.mouse_scroll([coordinates[5][1], coordinates[5][2]],
                                                           ptr1=all_gestures.gestures[gesture_index][9][0],
                                                           ptr2=all_gestures.gestures[gesture_index][9][1])
                                    elif (fingers % 10000) / 1000 == 1:
                                        mouse.mouse_scroll([coordinates[7][1], coordinates[7][2]],
                                                           ptr1=all_gestures.gestures[gesture_index][9][0],
                                                           ptr2=all_gestures.gestures[gesture_index][9][1])
                                    else:
                                        mouse.mouse_scroll([coordinates[1][1], coordinates[1][2]],
                                                           ptr1=all_gestures.gestures[gesture_index][9][0],
                                                           ptr2=all_gestures.gestures[gesture_index][9][1])
                            elif fingers == all_gestures.gestures[gesture_index][4]:
                                if fingers % 10 == 1:
                                    mouse.volume_ctrl(coordinates[1][2], (all_gestures.gestures[gesture_index][9][0][1],
                                                                            all_gestures.gestures[gesture_index][9][1][1]))
                                else:
                                    if (fingers % 100) / 10 == 1:
                                        mouse.volume_ctrl(coordinates[3][2], (all_gestures.gestures[gesture_index][9][0][1],
                                                                            all_gestures.gestures[gesture_index][9][1][1]))
                                    elif (fingers % 1000) / 100 == 1:
                                        mouse.volume_ctrl(coordinates[5][2], (all_gestures.gestures[gesture_index][9][0][1],
                                                                            all_gestures.gestures[gesture_index][9][1][1]))
                                    elif (fingers % 10000) / 1000 == 1:
                                        mouse.volume_ctrl(coordinates[7][2], (all_gestures.gestures[gesture_index][9][0][1],
                                                                            all_gestures.gestures[gesture_index][9][1][1]))
                                    else:
                                        mouse.volume_ctrl(coordinates[1][2], (all_gestures.gestures[gesture_index][9][0][1],
                                                                            all_gestures.gestures[gesture_index][9][1][1]))

                            elif fingers == all_gestures.gestures[gesture_index][5]:
                                if fingers % 10 == 1:
                                    mouse.mouse_bright(coordinates[1][2], (all_gestures.gestures[gesture_index][9][0][1],
                                                                            all_gestures.gestures[gesture_index][9][1][1]))
                                else:
                                    if (fingers % 100) / 10 == 1:
                                        mouse.mouse_bright(coordinates[3][2], (all_gestures.gestures[gesture_index][9][0][1],
                                                                            all_gestures.gestures[gesture_index][9][1][1]))
                                    elif (fingers % 1000) / 100 == 1:
                                        mouse.mouse_bright(coordinates[5][2], (all_gestures.gestures[gesture_index][9][0][1],
                                                                            all_gestures.gestures[gesture_index][9][1][1]))
                                    elif (fingers % 10000) / 1000 == 1:
                                        mouse.mouse_bright(coordinates[7][2], (all_gestures.gestures[gesture_index][9][0][1],
                                                                            all_gestures.gestures[gesture_index][9][1][1]))
                                    else:
                                        mouse.mouse_bright(coordinates[1][2], (all_gestures.gestures[gesture_index][9][0][1],
                                                                            all_gestures.gestures[gesture_index][9][1][1]))
                    else:
                        prev_count = prev_count + 1
                        if prev_count == all_gestures.gestures[gesture_index][8]:
                            prev_count = 0
                            prev_fing = fingers
            if keyboard.is_pressed("Alt"):
                if keyboard.is_pressed("c"):
                    termination1 = True
                    all_gestures.gestures[gesture_index][11] = False
                    mode = False
                elif keyboard.is_pressed("v"):
                    def termination_display():
                        temp_wind.quit()
                        temp_wind.destroy()
                    temp_wind = Tk()
                    temp_wind.geometry("450x100")
                    temp_wind.title("Termination")
                    information_about_mode = Label(master=temp_wind,
                                                   text="Termination process initiated. \nPlease wait till the "
                                                        "application close itself.")
                    information_about_mode.config(font=("Arial", 13))
                    information_about_mode.place(relx=0.067, rely=0.1)
                    temp_wind.protocol("WM_DELETE_WINDOW", termination_display)
                    temp_wind.attributes('-topmost', True)
                    temp_wind.after(2500, termination_display)
                    temp_wind.mainloop()


                    gesture_file = open("Gesture Config__memory.pickle", "wb")
                    pickle.dump(all_gestures, gesture_file)
                    prev_ges = Gesture_prev()
                    prev_ges.name = ges_Prev.name
                    prev_gesture_config = open("Gesture Config__prev.pickle", "wb")
                    pickle.dump(prev_ges, prev_gesture_config)
                    sys.exit(0)
                elif keyboard.is_pressed("b"):
                    time.sleep(0.5)
                    if pause == True:
                        pause = False
                        pause_proof = 0
                        temp_wind = Tk()
                        temp_wind.geometry("500x100")
                        temp_wind.title("Pause Mode")
                        information_about_mode = Label(master=temp_wind,
                                                       text="Pause mode is deactivated successfully.")
                        information_about_mode.config(font=("Arial", 13))
                        information_about_mode.place(relx=0.067, rely=0.3)
                        temp_wind.protocol("WM_DELETE_WINDOW", pause_destroy)
                        temp_wind.attributes('-topmost', True)
                        temp_wind.after(3500, pause_destroy)
                        temp_wind.mainloop()
                    else:
                        pause_proof = 0
                        pause = True
                        temp_wind = Tk()
                        temp_wind.geometry("500x100")
                        temp_wind.title("Pause Mode")
                        temp_wind.protocol("WM_DELETE_WINDOW", pause_destroy)
                        information_about_mode = Label(master=temp_wind,
                                                       text="Pause mode is activated successfully.")
                        information_about_mode.config(font=("Arial", 13))
                        information_about_mode.place(relx=0.067, rely=0.25)
                        temp_wind.attributes('-topmost', True)
                        temp_wind.after(3500, pause_destroy)
                        temp_wind.mainloop()
                elif keyboard.is_pressed("h"):
                    def help_function():
                        global is_help_open
                        if not is_help_open:
                            help_window = Tk()
                            def help_function_1():
                                help_window.quit()
                                help_window.destroy()
                                help_window_1 = Tk()
                                def help_end():
                                    global is_help_open
                                    is_help_open = False
                                    help_window_1.quit()
                                    help_window_1.destroy()

                                help_window_1.protocol("WM_DELETE_WINDOW", help_end)
                                help_window_1.title("Help[Buttons]")
                                help_window_1.geometry(f"1673x919")
                                byte_data = base64.b64decode(help_1)
                                image_data = BytesIO(byte_data)
                                image = pi.open(image_data)
                                temp_img = pk.PhotoImage(
                                    image.resize((1673, 864), pi.ANTIALIAS))
                                temp_can = Canvas(master=help_window_1, width=temp_img.width(),
                                                  height=temp_img.height())
                                temp_can.create_image(0, 0, image=temp_img, anchor=NW)
                                help_window_1.geometry("+0+0")
                                temp_can.pack()
                                ok_button_1 = Button(help_window_1, text="Ok", command=help_end)
                                ok_button_1.config(font=("Arial", 15, "bold"), width=17)
                                ok_button_1.pack()
                                help_window_1.mainloop()

                            def help_function_2():
                                help_window.quit()
                                help_window.destroy()
                                help_window_1 = Tk()
                                def help_end():
                                    global is_help_open
                                    is_help_open = False
                                    help_window_1.quit()
                                    help_window_1.destroy()
                                help_window_1.protocol("WM_DELETE_WINDOW", help_end)
                                help_window_1.title("Help[Shortcut]")
                                help_window_1.geometry("1519x898")
                                byte_data = base64.b64decode(help_2)
                                image_data = BytesIO(byte_data)
                                image = pi.open(image_data)
                                temp_img = pk.PhotoImage( image.resize((1519, 842), pi.ANTIALIAS))
                                temp_can = Canvas(master=help_window_1, width=temp_img.width(), height=temp_img.height())
                                temp_can.create_image(0, 0, image=temp_img, anchor=NW)
                                help_window_1.geometry("+0+0")
                                temp_can.pack()
                                ok_button_1 = Button(help_window_1, text="Ok", command=help_end)
                                ok_button_1.config(
                                    font=("Arial", 15, "bold"), width=17)
                                ok_button_1.pack()
                                help_window_1.mainloop()

                            def help_end_2():
                                global is_help_open
                                is_help_open = False
                                help_window.quit()
                                help_window.destroy()

                            is_help_open = True
                            help_window.title("Help")
                            help_window.geometry("400x200")
                            b1 = Button(help_window, text="Help[Buttons]", command=help_function_1)
                            b1.config(font=("Arial", 15))
                            b1.place(relx=0.027, rely=0.25)
                            b2 = Button(help_window, text="Help[Shortcuts]", command=help_function_2)
                            b2.config(font=("Arial", 15))
                            help_window.protocol("WM_DELETE_WINDOW", help_end_2)
                            b2.place(relx=0.4799, rely=0.25)
                            help_window.mainloop()
                    help_function()
    elif mode == False:
        termination2 = False
        while not termination2:
            if all_gestures.gestures[ges_idx][9][0] is not None and all_gestures.gestures[ges_idx][9][1] is \
                    not None:
                obj = tp.TheControl(web_id=webcam_id, gestures=all_gestures, gesture_name=ges_Prev)
                ges_idx = obj.all_gestures_position
                ges_Prev.name = obj.ges_name
                all_gestures = obj.all_gestures
                if obj.chgWebCamstat:
                    webcam_id = None
                    webcam_config()
                elif obj.chgRefstat:
                    all_gestures.gestures[ges_idx][9][0] = None
                    all_gestures.gestures[ges_idx][9][1] = None
                    reference_frame_config()
                elif obj.mode_transfer_stat:
                    mode = True
                    termination2 = True
                    all_gestures = obj.all_gestures
                    ges_Prev.name = obj.ges_name
                    gesture_obj = obj.all_gestures
                    for i in gesture_obj.ges_list:
                        if i == "Add User":
                            gesture_obj.ges_list.remove(i)
                    for i in gesture_obj.ges_list:
                        if i == "Delete User":
                            gesture_obj.ges_list.remove(i)
                    gesture_file = open("Gesture Config__memory.pickle", "wb")
                    pickle.dump(gesture_obj, gesture_file)
                    prev_ges = Gesture_prev()
                    prev_ges.name = obj.ges_name
                    prev_gesture_config = open("Gesture Config__prev.pickle", "wb")
                    pickle.dump(prev_ges, prev_gesture_config)
                else:
                    if obj.prop_exit:
                        gesture_obj = obj.all_gestures
                        for i in gesture_obj.ges_list:
                            if i == "Add User":
                                gesture_obj.ges_list.remove(i)
                        for i in gesture_obj.ges_list:
                            if i == "Delete User":
                                gesture_obj.ges_list.remove(i)
                        gesture_file = open("Gesture Config__memory.pickle", "wb")
                        pickle.dump(gesture_obj, gesture_file)
                        prev_ges = Gesture_prev()
                        prev_ges.name = obj.ges_name
                        prev_gesture_config = open("Gesture Config__prev.pickle", "wb")
                        pickle.dump(prev_ges, prev_gesture_config)
                        sys.exit(0)
                    else:
                        gesture_obj = obj.all_gestures
                        for i in gesture_obj.ges_list:
                            if i == "Add User":
                                gesture_obj.ges_list.remove(i)
                        for i in gesture_obj.ges_list:
                            if i == "Delete User":
                                gesture_obj.ges_list.remove(i)
                        sys.exit(0)
            else:
                reference_frame_config()

    else:
        end_program()


















