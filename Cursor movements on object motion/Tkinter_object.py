from tkinter import *#
import cv2 as cv#
import PIL.Image as pi#
import PIL.ImageTk as pk#
import Hand_Detector as hd#
import Mouse_Movement as mv#
import time#
import tkinter.messagebox as mb#
import keyboard#
import base64
from io import BytesIO
from Hand_Coloured_Byte import explode#
from First_Reference_Point import first_ref#
from Second_Reference_Point import second_ref#
from help_description import help_1#
from help_shortcut import help_2#
import os#
import sys#


class WebCamConfiguration:
    def __init__(self, web_id):
        self.img = None
        self.con = None
        self.new_img = None
        self.stat2 = False
        self.iterations = 0
        self.vid = cv.VideoCapture(web_id)
        self.stat = self.vid.isOpened()
        if self.stat:
            self.stat2 = True
            self.wid = Tk()
            self.wid.title("Webcam Configuration")
            self.can = Canvas(self.wid, width=self.vid.get(cv.CAP_PROP_FRAME_WIDTH),
                              height=self.vid.get(cv.CAP_PROP_FRAME_HEIGHT))
            self.can.pack()
            self.wid.protocol("WM_DELETE_WINDOW", self.end_program)
            self.l = Label(self.wid, text="00:00 sec")
            self.l.config(font=('Arial', 12))
            self.temp_prev = 0
            self.l.pack()
            self.start_time = time.time()
            self.web_id_display = Label(self.wid, text=f"Webcam ID: {web_id}")
            self.web_id_display.config(font=('Arial', 12))
            self.web_id_display.pack()
            self.update()
            self.wid.mainloop()

    def update(self):
        t_end = time.time()
        time_dif = int(t_end - self.start_time)
        if time_dif <= 5:
            if time_dif != self.temp_prev:
                if time_dif > 3:
                    self.l.config(fg="red")
                self.l.config(text=str(f"0:0{time_dif} sec"))
                self.temp_prev = time_dif
        else:
            self.stat = False
        if self.stat:
            self.con, self.img = self.vid.read()
            if self.con:
                self.new_img = pk.PhotoImage(master=self.can, image=pi.fromarray(cv.cvtColor(self.img, cv.COLOR_RGB2BGR)
                                                                                 ))
                self.can.create_image(0, 0, image=self.new_img, anchor=NW)
            self.wid.after(1, self.update)
        else:
            self.wid.quit()
            self.wid.destroy()

    def end_program(self):
        self.stat = False


def end_program():
    sys.exit(0)


class WebCamDisplay:
    def __init__(self, web_id, rptr1=0, rptr2=0, mode=0):
        self.mod = mode
        self.vid_obj = cv.VideoCapture(web_id)
        self.point1 = rptr1
        self.point2 = rptr2
        self.stat1 = True
        self.stat2 = True
        if mode == 0:
            if self.vid_obj.isOpened():
                self.stat = True
                self.window = Tk()
                self.window.title("Reference Frame Configuration")
                self.can = Canvas(self.window, width=self.vid_obj.get(cv.CAP_PROP_FRAME_WIDTH),
                                  height=self.vid_obj.get(cv.CAP_PROP_FRAME_HEIGHT))
                self.can.pack()
                self.button1 = Button(self.window, text="Change Webcam", command=self.changewebcam)
                self.button1.config(font=('Arial', 12))
                self.button1.pack()
                self.window.protocol("WM_DELETE_WINDOW", end_program)
                self.hand = hd.HandDetector()
                self.tstart = time.time()
                self.temp_prev = 0
                self.timer = Label(self.window, text="0:00 sec")
                self.timer.config(font=("Arial", 12))
                self.timer.pack()
                self.inform1 = Label(self.window, text="Please specify the first reference point using index/point finger "
                                                      "only.\nClick on Help, if there is any problem.")
                self.inform1.config(font=("Arial", 12))
                self.inform1.pack()
        elif mode == 1:
            self.stat = True
            self.window = Tk()
            self.can = Canvas(self.window, width=self.vid_obj.get(cv.CAP_PROP_FRAME_WIDTH),  height=self.vid_obj.get
            (cv.CAP_PROP_FRAME_HEIGHT))
            self.can.pack()
            self.button1 = Button(self.window, text="Reset First Reference Point", command=self.reset_first_point)
            self.button1.config(font=('Arial', 12))
            self.button1.pack()
            self.window.protocol("WM_DELETE_WINDOW", end_program)
            self.hand = hd.HandDetector()
            self.tstart = time.time()
            self.temp_prev = 0
            self.timer = Label(self.window, text="0:00 sec")
            self.timer.config(font=("Arial", 12))
            self.timer.pack()
            self.inform2 = Label(self.window, text="Please Specify the second reference point using index/point finger only."
                                                   "\nFor Good Operation, try to maximize the size of the Frame (Rectangle).")
            self.inform2.config(font=("Arial", 12))
            self.inform2.pack()
        self.help = Button(self.window, text="Help", command=self.helping)
        self.help.config(font=("Arial", 12))
        self.help.pack()
        self.bound_out = 0
        self.timer_cancel = False
        self.is_help_open = False
        self.update()
        self.window.mainloop()

    def helping(self):
        if not self.is_help_open:
            self.is_help_open = True
            self.timer_cancel = True
            if self.mod == 0:
                self.new_window = Toplevel()
                self.new_window.title("Help")
                byte_data = base64.b64decode(first_ref)
                image_data = BytesIO(byte_data)
                image = pi.open(image_data)
                self.new_window.geometry("+0+0")
                self.temp_img = pk.PhotoImage(image.resize((1168, 735), pi.ANTIALIAS))
                self.temp_can = Canvas(self.new_window, width=self.temp_img.width(), height=self.temp_img.height())
                self.temp_can.create_image(0, 0, image=self.temp_img, anchor=NW)
                self.temp_can.grid(row=0, column=0)
                self.information = Label(self.new_window, text="Please, specify the first reference point using the index finger only\n"
                                                               "as shown in the above picture. Note: Your complete palm should be placed\n"
                                                               "within the borders of the camera display. If not, an error will prompt.\n"
                                                               "The goal here is to draw a reference frame (A Rectangle). So, to draw it,\n"
                                                               "we need two points. And right now you need to specify the first point.")
                self.information.config(font=("Arial", 15))
                self.new_window.protocol("WM_DELETE_WINDOW", self.start_timer)
                self.information.grid(row=1, column=0)
                self.tstart = time.time()
                self.temp_can.grid(row=0, column=0)
            else:
                self.new_window = Toplevel()
                self.new_window.title("Help")
                byte_data = base64.b64decode(second_ref)
                image_data = BytesIO(byte_data)
                image = pi.open(image_data)
                self.new_window.geometry("+0+0")
                self.temp_img = pk.PhotoImage(image.resize((1168, 748), pi.ANTIALIAS))
                self.temp_can = Canvas(self.new_window, width=self.temp_img.width(), height=self.temp_img.height())
                self.temp_can.create_image(0, 0, image=self.temp_img, anchor=NW)
                self.temp_can.grid(row=0, column=0)
                self.information = Label(self.new_window,
                                         text="Please, specify the second reference point using the index finger only as shown\n"
                                              "in the above picture. Note: Your complete palm should be placed within the borders\n"
                                              "of the camera display. If not, an error will prompt. Using a second reference point \n"
                                              "draw a rectangle like shown in the picture. This rectangle frame acts like the whole\n"
                                              "screen during execution. You can draw the rectangle according to your comfort.")
                self.information.config(font=("Arial", 15))
                self.new_window.protocol("WM_DELETE_WINDOW", self.start_timer)
                self.information.grid(row=1, column=0)
                self.tstart = time.time()
                self.temp_can.grid(row=0, column=0)

    def start_timer(self):
        self.is_help_open = False
        self.new_window.destroy()
        self.timer_cancel = False
        self.tstart = time.time()


    def update(self):
        if self.stat:
            self.con, self.img = self.vid_obj.read()
            if self.con:
                self.img = cv.flip(self.img, 1)
                if self.timer_cancel:
                    time_dif = 0
                else:
                    self.t_end = time.time()
                    time_dif = int(self.t_end - self.tstart)
                if time_dif <= 5:
                    if not self.timer_cancel:
                        if time_dif != self.temp_prev:
                            if time_dif > 3:
                                self.timer.config(fg="red")
                            else:
                                self.timer.config(fg="black")
                            self.timer.config(text=str(f"0:0{time_dif} sec"))
                            self.temp_prev = time_dif
                    else:
                        self.timer.config(text=str(f"0:00 sec"))
                        self.temp_prev = time_dif
                else:
                    if self.mod == 0:
                        if self.point1 is None:
                            mb.showerror("Reference Frame Configuration", "Please specify the first reference point "
                                                                          "using the index/pointing finger only.")
                            self.tstart = time.time()
                            self.timer.config(fg="black")
                        else:
                            self.stat = False
                            self.stat1 = False
                    elif self.mod == 1:
                        if self.point2 is None:
                            mb.showerror("Reference Frame Configuration",
                                         "Please specify the second reference point using"
                                         " the index/pointing finger only.")
                            self.tstart = time.time()
                            self.timer.config(fg="black")
                        else:
                            self.stat = False
                            self.stat2 = False
                if not self.timer_cancel:
                    fingers, coordinates = self.hand.position(self.img, draw=True)
                    if self.mod == 1:
                        cv.circle(self.img, (self.point1[1], self.point1[2]), (int(self.vid_obj.get(cv.CAP_PROP_FRAME_WIDTH) * 0.01)),
                                  (0, 0, 0), cv.FILLED)
                    if coordinates is not None:
                        for each in coordinates:
                            if each[1] < 0:
                                self.bound_out = self.bound_out + 1
                                if self.bound_out > 2:
                                    mb.showerror("Reference Frame Configuration", "Please make sure the all displayed "
                                                                                  "coordinates are with camera frame")
                                    self.tstart = time.time()
                                    self.timer.config(fg="black")
                                    self.bound_out = 0
                            elif each[1] > self.vid_obj.get(cv.CAP_PROP_FRAME_WIDTH):
                                self.bound_out = self.bound_out + 1
                                if self.bound_out > 2:
                                    mb.showerror("Reference Frame Configuration", "Please make sure the all displayed "
                                                                                  "coordinates are with camera frame")
                                    self.tstart = time.time()
                                    self.timer.config(fg="black")
                                    self.bound_out = 0
                            elif each[2] < 0:
                                self.bound_out = self.bound_out + 1
                                if self.bound_out > 2:
                                    mb.showerror("Reference Frame Configuration", "Please make sure the all displayed "
                                                                                  "coordinates are with camera frame")
                                    self.tstart = time.time()
                                    self.timer.config(fg="black")
                                    self.bound_out = 0
                            elif each[2] > self.vid_obj.get(cv.CAP_PROP_FRAME_HEIGHT):
                                self.bound_out = self.bound_out + 1
                                if self.bound_out > 2:
                                    mb.showerror("Reference Frame Configuration", "Please make sure the all displayed "
                                                                                  "coordinates are with camera frame")
                                    self.tstart = time.time()
                                    self.timer.config(fg="black")
                                    self.bound_out = 0

                        if self.mod == 1 and fingers == 100001:
                            cv.rectangle(self.img, (self.point1[1], self.point1[2]), (coordinates[1][1], coordinates[1][2]),
                            (0, 255, 0), 2)
                        if self.mod == 0:
                            if fingers == 100001:
                                self.point1 = coordinates[1]
                            else:
                                self.point1 = None
                        elif self.mod == 1:
                            if fingers == 100001:
                                self.point2 = coordinates[1]
                            else:
                                self.point2 = None
                    else:
                        if self.mod == 0:
                            self.point1 = None
                        elif self.mod == 1:
                            self.point2 = None
            self.new_img = pk.PhotoImage(master=self.can, image=pi.fromarray(cv.cvtColor(self.img,
                                                                                         cv.COLOR_RGB2BGR)))
            self.can.create_image(0, 0, image=self.new_img, anchor=NW)
            self.window.after(1, self.update)
        else:
            self.window.quit()
            self.window.destroy()

    def changewebcam(self):
        self.stat1 = True
        self.stat = False

    def reset_first_point(self):
        self.stat2 = True
        self.stat = False


class TheControl:
    def __init__(self, web_id, gestures, gesture_name):
        self.temp_label = None
        self.temp_window = None
        self.chgWebCamstat = False
        self.chgRefstat = False
        self.prop_exit = False
        self.vid_obj = cv.VideoCapture(web_id)
        if self.vid_obj.isOpened():
            self.all_gestures = gestures
            self.ges_name = gesture_name.name
            self.all_gestures_position = self.all_gestures.get_gesture(self.ges_name)
            self.rpoint1 = self.all_gestures.gestures[self.all_gestures_position][9][0]
            self.rpoint2 = self.all_gestures.gestures[self.all_gestures_position][9][1]
            self.window = Tk()
            self.window.title("AirTouch")
            self.can = Canvas(self.window, width=self.vid_obj.get(cv.CAP_PROP_FRAME_WIDTH),
                              height=self.vid_obj.get(cv.CAP_PROP_FRAME_HEIGHT))
            self.window.protocol("WM_DELETE_WINDOW", self.proper_exit)
            self.can.pack()
            self.chgWebCam = Button(self.window, text="Change Webcam", command=self.chgWebcm)
            self.chgWebCam.config(font=("Arial", 11))
            self.chgWebCam.pack(side=LEFT)
            self.resetReference = Button(self.window, text="Reset Reference Frame", command=self.resetReference)
            self.resetReference.config(font=("Arial", 11))
            self.resetReference.pack(side=LEFT)
            self.mouse_sen = Button(self.window, text="Mouse Speed", command=self.mouse_sen)
            self.mouse_sen.config(font=("Arial", 11))
            self.mouse_sen.pack(side=LEFT)
            self.reaction_time = Button(self.window, text="Reaction Time", command=self.reaction_time_setter)
            self.reaction_time.config(font=("Arial", 11))
            self.reaction_time.pack(side=LEFT)
            self.reaction_time_value = self.all_gestures.gestures[self.all_gestures_position][8]
            self.gesture_menu = StringVar()
            self.gesture_menu.set("Controls")
            self.menu2 = OptionMenu(self.window, self.gesture_menu, "For Movement", "For Left-Click", "For Right-Click",
                                    "For Scrolling", "Volume Control", "Brightness Control", "Current Controls",
                                    "Allowed Controls List", command=self.gesture_options)
            self.menu2.config(font=("Arial", 11))
            self.size_menu2 = self.window.nametowidget(self.menu2.menuname)
            self.size_menu2.config(font=("Arial", 11))
            self.menu2.pack(side=LEFT)
            self.gesture_list = self.all_gestures.ges_list
            while "Delete User" in self.gesture_list:
                self.gesture_list.remove("Delete User")
            while "Add User" in self.gesture_list:
                self.gesture_list.remove("Add User")
            self.gesture_list.append("Add User")
            self.gesture_list.append("Delete User")
            self.gesture = StringVar()
            self.gesture.set(self.ges_name)
            self.menu3 = OptionMenu(self.window, self.gesture, *self.gesture_list,
                                    command=self.gesture_select)
            self.menu3.config(font=("Arial", 11))
            self.size_menu3 = self.window.nametowidget(self.menu3.menuname)
            self.size_menu3.config(font=("Arial", 11))
            self.menu3.pack(side=LEFT)
            self.win_positions = ["Top", "Left", "Right", "Center", "Minimize"]
            self.window_pos = StringVar()
            self.wind_pos = self.all_gestures.gestures[self.all_gestures_position][10]
            if  self.wind_pos is not None:
                self.run = 0
                self.window_pos.set(self.wind_pos)
            else:
                self.run = 2
                self.window_pos.set("Window Position")
            self.window_position = OptionMenu(self.window, self.window_pos, *self.win_positions, command=self.window_position_change)
            self.window_position.config(font=("Arial", 11))
            self.size_menu_window_position = self.window.nametowidget(self.window_position.menuname)
            self.size_menu_window_position.config(font=("Arial", 11))
            self.window_position.pack(side=LEFT)

            self.on_screen_keyboard = Button(self.window, text="On-Screen Keyboard", command=self.onsky)
            self.on_screen_keyboard.config(font=("Arial", 11))
            self.on_screen_keyboard.pack(side=LEFT)
            self.mode_chg = Button(self.window, text="Change Mode", command=self.chg_mode)
            self.mode_chg.config(font=("Arial", 11))
            self.mode_chg.pack(side=LEFT)

            self.reset_config = Button(self.window, text="Reset Previous Settings", command=self.reset_config_files)
            self.reset_config.config(font=("Arial", 11))
            self.reset_config.pack(side=LEFT)

            self.help = Button(self.window, text="Help", command=self.help_function)
            self.help.config(font=("Arial", 11),
                             width=11)
            self.help.pack(side=LEFT)

            self.quitbutton = Button(self.window, text="Quit", command=self.proper_exit)
            self.quitbutton.config(font=("Arial", 11))
            self.quitbutton.config(width=11)
            self.quitbutton.pack(side=LEFT)
            self.stat = True
            self.hand = hd.HandDetector()
            self.mouse = mv.AirTouch()
            self.all_gestures_position = self.all_gestures.get_gesture(self.ges_name)
            self.move = self.all_gestures.gestures[self.all_gestures_position][0]
            self.left_click = self.all_gestures.gestures[self.all_gestures_position][1]
            self.right_click = self.all_gestures.gestures[self.all_gestures_position][2]
            self.scroll = self.all_gestures.gestures[self.all_gestures_position][3]
            self.volume_control = self.all_gestures.gestures[self.all_gestures_position][4]
            self.brightness_control = self.all_gestures.gestures[self.all_gestures_position][5]
            self.temp_img = 0
            self.temp_fing1 = None
            self.temp_fing2 = None
            self.temp_fing3 = None
            self.temp_fing4 = None
            self.menu_cancel_stat = True
            self.mode_transfer_stat = False

            self.gesture_names = {0: "For Movement", 1: "For Left-Click", 2: "For Right-Click", 3: "For Scrolling",
                             4: "Volume Control", 5: "Brightness Control"}
            self.m_speed = self.all_gestures.gestures[self.all_gestures_position][7]
            self.prev_count = 0
            self.prev_fing = self.all_gestures.gestures[self.all_gestures_position][0]
            self.isGesture_option_open = False
            self.prev_Gesture_select = None
            self.isMouse_speed_selected = False
            self.isReaction_Time_selected = False
            self.pause = False
            self.stealth_check = [0, 0]
            self.stealth_confirm = 0
            self.proof_stealth = 0
            self.one_point = None
            self.on_screen_keyboard_proof = 0
            self.is_help_open = False
            self.pause_proof = 0
            self.reset_config_lock = False
            self.update()
            self.window.mainloop()

    def reset_config_window(self):
        self.temp_wind.quit()
        self.temp_wind.destroy()

    def reset_config_files(self):
        if not self.reset_config_lock:
            self.reset_config_lock = True
            if os.path.exists("Webcam Config.pickle"):
                os.remove("Webcam Config.pickle")
            if os.path.exists("Gesture Config__prev.pickle"):
                os.remove("Gesture Config__prev.pickle")
            if os.path.exists("Gesture Config__memory.pickle"):
                os.remove("Gesture Config__memory.pickle")
            self.temp_wind = Tk()
            self.temp_wind.geometry("630x100")
            self.temp_wind.title("Reset Previous Settings")
            self.temp_wind.protocol("WM_DELETE_WINDOW", self.reset_config_window)
            self.information_about_mode = Label(master=self.temp_wind,
                                                text="Previous Settings are deleted successfully. \nPlease, re-run the"
                                                     " program for the changes to take place.")
            self.information_about_mode.config(font=("Arial", 13))
            self.information_about_mode.place(relx=0.067, rely=0.25)
            self.temp_wind.attributes('-topmost', True)
            self.temp_wind.after(3500, self.reset_config_window)
            self.temp_wind.mainloop()
            sys.exit(0)



    def help_function(self):
        if not self.is_help_open:
            self.is_help_open = True
            self.help_window = Toplevel()
            self.help_window.title("Help")
            self.help_window.geometry("400x200")
            self.b1 = Button(self.help_window, text="Help[Buttons]", command=self.help_function_1)
            self.b1.config(font=("Arial", 15))
            self.b1.place(relx=0.027, rely=0.25)
            self.b2 = Button(self.help_window, text="Help[Shortcuts]", command=self.help_function_2)
            self.b2.config(font=("Arial", 15))
            self.help_window.protocol("WM_DELETE_WINDOW", self.help_end_2)
            self.b2.place(relx=0.4799, rely=0.25)
            self.help_window.mainloop()

    def help_function_1(self):
        self.help_window.quit()
        self.help_window.destroy()
        self.help_window_1 = Toplevel()
        self.help_window_1.protocol("WM_DELETE_WINDOW", self.help_end)
        self.help_window_1.title("Help[Buttons]")
        self.help_window_1.geometry("1673x919")
        byte_data = base64.b64decode(help_1)
        image_data = BytesIO(byte_data)
        image = pi.open(image_data)
        self.temp_img = pk.PhotoImage(image.resize((1673, 864), pi.ANTIALIAS))
        self.temp_can = Canvas(master=self.help_window_1, width=self.temp_img.width(), height=self.temp_img.height())
        self.temp_can.create_image(0, 0, image=self.temp_img, anchor=NW)
        self.help_window_1.geometry("+0+0")
        self.temp_can.pack()
        self.ok_button_1 = Button(self.help_window_1, text="Ok", command=self.help_end)
        self.ok_button_1.config(font=("Arial", 15, "bold"), width=17)
        self.ok_button_1.pack()
        self.help_window_1.mainloop()

    def help_function_2(self):
        self.help_window.quit()
        self.help_window.destroy()
        self.help_window_1 = Toplevel()
        self.help_window_1.protocol("WM_DELETE_WINDOW", self.help_end)
        self.help_window_1.title("Help[Shortcut]")
        self.help_window_1.geometry("1519x898")
        byte_data = base64.b64decode(help_2)
        image_data = BytesIO(byte_data)
        image = pi.open(image_data)
        self.temp_img = pk.PhotoImage(image.resize((1519, 842), pi.ANTIALIAS))
        self.temp_can = Canvas(master=self.help_window_1, width=self.temp_img.width(), height=self.temp_img.height())
        self.temp_can.create_image(0, 0, image=self.temp_img, anchor=NW)
        self.help_window_1.geometry("+0+0")
        self.temp_can.pack()
        self.ok_button_1 = Button(self.help_window_1, text="Ok", command=self.help_end)
        self.ok_button_1.config(font=("Arial", 15, "bold"),
                                width=17)
        self.ok_button_1.pack()
        self.help_window_1.mainloop()

    def help_end(self):
        self.is_help_open = False
        self.help_window_1.quit()
        self.help_window_1.destroy()

    def help_end_2(self):
        self.is_help_open = False
        self.help_window.quit()
        self.help_window.destroy()


    def onsky(self):
        os.startfile(r"C:\WINDOWS\system32\osk.exe")

    def chg_mode(self):
        self.all_gestures.gestures[self.all_gestures_position][11] = True
        self.mode_transfer_stat = True
        self.stat = False

    def reaction_time_setter(self):
        if not self.isReaction_Time_selected:
            self.isReaction_Time_selected = True
            self.temp_new_window1 = Tk()
            self.temp_new_window1.title("Reaction Time")
            self.react_time= Scale(self.temp_new_window1, width=70, length=442, from_=3, to=20, orient=HORIZONTAL)
            self.react_time.config(font=('Helvetica bold', 25))
            self.react_time.set(self.reaction_time_value)
            self.react_time.pack()
            self.temp_new_window1.protocol("WM_DELETE_WINDOW", self.react_time_close)
            self.temp_new_button1 = Button(self.temp_new_window1, text="Set", command=self.set_react_time)
            self.temp_new_button1.config(font=('Helvetica bold', 25))
            self.temp_new_button1.pack()



    def set_react_time(self):
        self.reaction_time_value = self.react_time.get()
        self.all_gestures.gestures[self.all_gestures_position][8] = self.reaction_time_value
        self.isReaction_Time_selected = False
        self.temp_new_window1.destroy()
    def react_time_close(self):
        self.isReaction_Time_selected = False
        self.temp_new_window1.destroy()

    def gesture_index_updater(self):
        self.all_gestures_position = self.all_gestures.get_gesture(self.ges_name)

    def window_position_change(self, event):
        inp = self.window_pos.get()
        self.all_gestures.gestures[self.all_gestures_position][10] = inp
        if inp == "Top":
            window_size_x = self.window.winfo_width()
            window_size_x = int(window_size_x/2)
            relative_top_x = int(self.window.winfo_screenwidth()*0.5 - window_size_x)
            self.window.geometry("+0+0")
            self.window.geometry(f"+{relative_top_x}+0")
        elif inp == "Left":
            relative_left_y = int(self.window.winfo_screenheight()*0.13)
            self.window.geometry("+0+0")
            self.window.geometry(f"+0+{relative_left_y}")
        elif inp == "Right":
            relative_right_y = int(self.window.winfo_screenheight()*0.13)
            relative_right_x = int(self.window.winfo_screenwidth() - self.window.winfo_width() -
                                   int(0.013*self.window.winfo_screenwidth()))
            self.window.geometry("+0+0")
            self.window.geometry(f"+{relative_right_x}+{relative_right_y}")
        elif inp == "Center":
            relative_center_x = int(self.window.winfo_screenwidth()*0.5) - int(self.window.winfo_width()/2)
            relative_center_y = int(self.window.winfo_screenheight() * 0.5) - int(self.window.winfo_height() / 2)
            self.window.geometry("+0+0")
            self.window.geometry(f"+{relative_center_x}+{relative_center_y}")
        elif inp == "Minimize":
            self.window.iconify()

    def stealth_checker(self, current_coordinates):
        if self.hand.dist((self.stealth_check[0], self.stealth_check[1]),
                          (current_coordinates[0], current_coordinates[1])) < 1.5:
            return True
        else:
            return False

    def pause_destroy(self):
        self.temp_wind.quit()
        self.temp_wind.destroy()

    def update(self):
        if self.run < 2:
            self.window_position_change(0)
            self.run = self.run+1

        if self.rpoint1 is None or self.rpoint2 is None:
            self.chgRefstat = True
            self.stat = False
        if self.stat:
            self.con, self.img = self.vid_obj.read()
            if self.con:
                self.img = cv.flip(self.img, 1)
                fingers, coordinates = self.hand.position(self.img, draw=True)
                cv.rectangle(self.img, (self.rpoint1[0], self.rpoint1[1]), (self.rpoint2[0], self.rpoint2[1]), (255, 255, 255), 2)
                if coordinates is not None:
                    if fingers == self.prev_fing:
                        if fingers == 100000:
                            if not self.pause:
                                self.pause_proof = self.pause_proof + 1
                                if self.pause_proof > 80:
                                    self.pause_proof = 0
                                    self.pause = True
                                    self.temp_wind = Tk()
                                    self.temp_wind.geometry("500x100")
                                    self.temp_wind.title("Pause Mode")
                                    self.temp_wind.protocol("WM_DELETE_WINDOW", self.pause_destroy)
                                    self.information_about_mode = Label(master=self.temp_wind,
                                                                       text="Pause mode is activated successfully")
                                    self.information_about_mode.config(font=("Arial", 13))
                                    self.information_about_mode.place(relx=0.067, rely=0.25)
                                    self.temp_wind.attributes('-topmost', True)
                                    self.temp_wind.after(3500, self.pause_destroy)
                                    self.temp_wind.mainloop()
                        elif fingers == 101011:
                            if self.pause:
                                self.pause_proof = self.pause_proof + 1
                                if self.pause_proof > 80:
                                    self.pause_proof = 0
                                    self.pause = False
                                    self.temp_wind = Tk()
                                    self.temp_wind.geometry("500x100")
                                    self.temp_wind.title("Pause Mode")
                                    self.information_about_mode = Label(master=self.temp_wind,
                                                                            text="Pause mode is deactivated successfully.")
                                    self.information_about_mode.config(font=("Arial", 13))
                                    self.information_about_mode.place(relx=0.067, rely=0.3)
                                    self.temp_wind.protocol("WM_DELETE_WINDOW", self.pause_destroy)
                                    self.temp_wind.attributes('-topmost', True)
                                    self.temp_wind.after(3500, self.pause_destroy)
                                    self.temp_wind.mainloop()
                        else:
                            self.pause_proof = 0
                        if not self.pause:
                            if fingers == 101111:
                                self.on_screen_keyboard_proof = self.on_screen_keyboard_proof + 1
                                if self.on_screen_keyboard_proof > 80:
                                    self.onsky()
                                    self.on_screen_keyboard_proof = 0
                            else:
                                self.on_screen_keyboard_proof = 0
                                if fingers == self.all_gestures.gestures[self.all_gestures_position][0]:
                                    if fingers % 10 == 1:
                                        temp_cood = (coordinates[1][1], coordinates[1][2])
                                        if self.stealth_checker(temp_cood):
                                            self.proof_stealth = self.proof_stealth + 1
                                            if self.proof_stealth > 2:
                                                self.stealth_confirm = 0
                                                self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                 ptr2=self.rpoint2,smooth_factor=50, stealth=True)
                                                self.one_point = temp_cood
                                            else:
                                                self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                 ptr2=self.rpoint2,
                                                                 smooth_factor=self.m_speed)
                                        else:
                                            self.stealth_confirm = self.stealth_confirm + 1
                                            if self.stealth_confirm > 2:
                                                self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                 ptr2=self.rpoint2, smooth_factor=self.m_speed)
                                                self.proof_stealth = 0

                                        self.stealth_check = [temp_cood[0], temp_cood[1]]
                                    else:
                                        if (fingers % 100) / 10 == 1:
                                            temp_cood = (coordinates[3][1], coordinates[3][2])
                                            if self.stealth_checker(temp_cood):
                                                self.proof_stealth = self.proof_stealth + 1
                                                if self.proof_stealth > 2:
                                                    self.stealth_confirm = 0
                                                    self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                     ptr2=self.rpoint2, smooth_factor=50, stealth=True)
                                                    self.one_point = temp_cood
                                                else:
                                                    self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                     ptr2=self.rpoint2,
                                                                     smooth_factor=self.m_speed)
                                            else:
                                                self.stealth_confirm = self.stealth_confirm + 1
                                                if self.stealth_confirm > 2:
                                                    self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                     ptr2=self.rpoint2, smooth_factor=self.m_speed)
                                                    self.proof_stealth = 0

                                            self.stealth_check = [temp_cood[0], temp_cood[1]]
                                        elif (fingers % 1000) / 100 == 1:
                                            temp_cood = (coordinates[5][1], coordinates[5][2])
                                            if self.stealth_checker(temp_cood):
                                                self.proof_stealth = self.proof_stealth + 1
                                                if self.proof_stealth > 2:
                                                    self.stealth_confirm = 0
                                                    self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                     ptr2=self.rpoint2, smooth_factor=50, stealth=True)
                                                    self.one_point = temp_cood
                                                else:
                                                    self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                     ptr2=self.rpoint2,
                                                                     smooth_factor=self.m_speed)
                                            else:
                                                self.stealth_confirm = self.stealth_confirm + 1
                                                if self.stealth_confirm > 2:
                                                    self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                     ptr2=self.rpoint2, smooth_factor=self.m_speed)
                                                    self.proof_stealth = 0

                                            self.stealth_check = [temp_cood[0], temp_cood[1]]
                                        elif (fingers % 10000) / 1000 == 1:
                                            temp_cood = (coordinates[7][1], coordinates[7][2])
                                            if self.stealth_checker(temp_cood):
                                                self.proof_stealth = self.proof_stealth + 1
                                                if self.proof_stealth > 2:
                                                    self.stealth_confirm = 0
                                                    self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                     ptr2=self.rpoint2, smooth_factor=50,  stealth=True)
                                                    self.one_point = temp_cood
                                                else:
                                                    self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                     ptr2=self.rpoint2,
                                                                     smooth_factor=self.m_speed)
                                            else:
                                                self.stealth_confirm = self.stealth_confirm + 1
                                                if self.stealth_confirm > 2:
                                                    self.mouse.track([temp_cood[0], temp_cood[1]], ptr1=self.rpoint1,
                                                                     ptr2=self.rpoint2, smooth_factor=self.m_speed)
                                                    self.proof_stealth = 0

                                            self.stealth_check = [temp_cood[0], temp_cood[1]]
                                        else:
                                            self.mouse.track([coordinates[1][1], coordinates[1][2]], ptr1=self.rpoint1,
                                                                 ptr2=self.rpoint2, smooth_factor=self.m_speed)
                                elif fingers == self.all_gestures.gestures[self.all_gestures_position][1]:
                                    self.mouse.left_click()
                                elif fingers == self.all_gestures.gestures[self.all_gestures_position][2]:
                                    self.mouse.right_click()
                                elif fingers == self.all_gestures.gestures[self.all_gestures_position][3]:
                                    if fingers % 10 == 1:
                                        self.mouse.mouse_scroll((coordinates[1][1], coordinates[1][2]), ptr1=self.rpoint1,
                                                                 ptr2=self.rpoint2,)
                                    else:
                                        if (fingers % 100) / 10 == 1:
                                            self.mouse.mouse_scroll((coordinates[3][1], coordinates[3][2]), ptr1=self.rpoint1,
                                                                 ptr2=self.rpoint2,)
                                        elif (fingers % 1000) / 100 == 1:
                                            self.mouse.mouse_scroll((coordinates[4][1], coordinates[4][2]), ptr1=self.rpoint1,
                                                                 ptr2=self.rpoint2,)
                                        elif (fingers % 10000) / 1000 == 1:
                                            self.mouse.mouse_scroll((coordinates[7][1], coordinates[7][2]), ptr1=self.rpoint1,
                                                                 ptr2=self.rpoint2,)
                                        else:
                                            self.mouse.mouse_scroll((coordinates[1][1], coordinates[1][2]), ptr1=self.rpoint1,
                                                                 ptr2=self.rpoint2,)

                                elif fingers == self.all_gestures.gestures[self.all_gestures_position][4]:
                                    if fingers % 10 == 1:
                                        self.mouse.volume_ctrl(coordinates[1][2], [self.rpoint1[1], self.rpoint2[1]])
                                    else:
                                        if (fingers % 100) / 10 == 1:
                                            self.mouse.volume_ctrl(coordinates[3][2], [self.rpoint1[1], self.rpoint2[1]])
                                        elif (fingers % 1000) / 100 == 1:
                                            self.mouse.volume_ctrl(coordinates[5][2], [self.rpoint1[1], self.rpoint2[1]])
                                        elif (fingers % 10000) / 1000 == 1:
                                            self.mouse.volume_ctrl(coordinates[7][2], [self.rpoint1[1], self.rpoint2[1]])
                                        else:
                                            self.mouse.volume_ctrl(coordinates[1][2], [self.rpoint1[1], self.rpoint2[1]])
                                elif fingers == self.all_gestures.gestures[self.all_gestures_position][5]:
                                    if fingers % 10 == 1:
                                        self.mouse.mouse_bright(coordinates[1][2], (self.rpoint1[1], self.rpoint2[1]))
                                    else:
                                        if (fingers % 100) / 10 == 1:
                                            self.mouse.mouse_bright(coordinates[3][2], (self.rpoint1[1], self.rpoint2[1]))
                                        elif (fingers % 1000) / 100 == 1:
                                            self.mouse.mouse_bright(coordinates[5][2], (self.rpoint1[1], self.rpoint2[1]))
                                        elif (fingers % 10000) / 1000 == 1:
                                            self.mouse.mouse_bright(coordinates[7][2], (self.rpoint1[1], self.rpoint2[1]))
                                        else:
                                            self.mouse.mouse_bright(coordinates[1][2], (self.rpoint1[1], self.rpoint2[1]))
                    else:
                        self.prev_count = self.prev_count + 1
                        if self.prev_count == self.reaction_time_value:
                            self.prev_count = 0
                            self.prev_fing = fingers
                self.new_img = pk.PhotoImage(master=self.can, image=pi.fromarray(cv.cvtColor(self.img, cv.COLOR_RGB2BGR)
                                                                                 ))
                self.can.create_image(0, 0, image=self.new_img, anchor=NW)
            if keyboard.is_pressed("Alt"):
                if keyboard.is_pressed("c"):
                    self.chg_mode()
                elif keyboard.is_pressed("v"):
                    self.proper_exit()
                elif keyboard.is_pressed("b"):
                    time.sleep(0.5)
                    if self.pause == True:
                        self.pause_proof = 0
                        self.pause = False
                        self.temp_wind = Tk()
                        self.temp_wind.geometry("500x100")
                        self.temp_wind.title("Pause Mode")
                        self.information_about_mode = Label(master=self.temp_wind,
                                                            text="Pause mode is deactivated successfully.")
                        self.information_about_mode.config(font=("Arial", 13))
                        self.information_about_mode.place(relx=0.067, rely=0.3)
                        self.temp_wind.protocol("WM_DELETE_WINDOW", self.pause_destroy)
                        self.temp_wind.attributes('-topmost', True)
                        self.temp_wind.after(3500, self.pause_destroy)
                        self.temp_wind.mainloop()
                    else:
                        self.pause_proof = 0
                        self.pause = True
                        self.temp_wind = Tk()
                        self.temp_wind.geometry("500x100")
                        self.temp_wind.title("Pause Mode")
                        self.temp_wind.protocol("WM_DELETE_WINDOW", self.pause_destroy)
                        self.information_about_mode = Label(master=self.temp_wind,
                                                            text="Pause mode is activated successfully")
                        self.information_about_mode.config(font=("Arial", 13))
                        self.information_about_mode.place(relx=0.067, rely=0.25)
                        self.temp_wind.attributes('-topmost', True)
                        self.temp_wind.after(3500, self.pause_destroy)
                        self.temp_wind.mainloop()
            self.window.after(1, self.update)
        else:
            self.window.quit()
            self.window.destroy()

    def chgWebcm(self):
        del self.vid_obj
        self.chgWebCamstat = True
        self.stat = False

    def resetReference(self):
        self.chgRefstat = True
        self.stat = False

    def mouse_sen(self):
        if not self.isMouse_speed_selected:
            self.isMouse_speed_selected = True
            self.temp_new_window = Tk()
            self.temp_new_window.title("Mouse Speed")
            self.speed = Scale(self.temp_new_window, width=70, length=442, from_=2, to=23, orient=HORIZONTAL)
            self.speed.config(font=('Helvetica bold', 25))
            self.speed.set(self.m_speed)
            self.speed.pack()
            self.temp_new_window.protocol("WM_DELETE_WINDOW", self.mspeed_close)
            self.temp_new_button = Button(self.temp_new_window, text="Set", command=self.set_mspeed)
            self.temp_new_button.config(font=('Helvetica bold', 25))
            self.temp_new_button.pack()

    def set_mspeed(self):
        self.isMouse_speed_selected = False
        temp = self.speed.get()
        self.m_speed = temp
        self.all_gestures.gestures[self.all_gestures_position][7] = self.m_speed
        self.temp_new_window.destroy()
    def mspeed_close(self):
        self.isMouse_speed_selected = False
        self.temp_new_window.destroy()

    def gesture_options(self, event):
        if not self.isGesture_option_open:
            inp = self.gesture_menu.get()
            self.prev_Gesture_select = inp
            self.gesture_menu.set(inp)
            self.controlSettings(inp)
        else:
            self.gesture_menu.set(self.prev_Gesture_select)

    def gesture_select(self, event):
        inp = self.gesture.get()
        if inp != "Add User" and inp != "Delete User":
            self.ges_name = inp
            self.all_gestures_position = self.all_gestures.get_gesture(self.ges_name)
            self.move = self.all_gestures.gestures[self.all_gestures_position][0]
            self.left_click = self.all_gestures.gestures[self.all_gestures_position][1]
            self.right_click = self.all_gestures.gestures[self.all_gestures_position][2]
            self.scroll = self.all_gestures.gestures[self.all_gestures_position][3]
            self.volume_control = self.all_gestures.gestures[self.all_gestures_position][4]
            self.brightness_control = self.all_gestures.gestures[self.all_gestures_position][5]
            self.m_speed = self.all_gestures.gestures[self.all_gestures_position][7]
            self.rpoint1 = self.all_gestures.gestures[self.all_gestures_position][9][0]
            self.rpoint2 = self.all_gestures.gestures[self.all_gestures_position][9][1]
            self.react_time = self.all_gestures.gestures[self.all_gestures_position][8]
            self.window_pos.set(self.all_gestures.gestures[self.all_gestures_position][10])
            self.gesture_menu.set("Controls")
            self.window_position_change(0)
        else:
            self.temp_window1 = Toplevel()
            self.temp_window1.geometry(f"400x170")
            if inp == "Add User":
                self.temp_window1.title("Add User")
            else:
                self.temp_window1.title("Delete User")
            self.temp_label1 = Label(self.temp_window1, text="Enter the Name of the User: ")
            self.temp_label1.config(font=('Helvetica bold', 15))
            self.temp_label1.pack()
            self.temp_text1 = Text(self.temp_window1, height=1, width=25)
            self.temp_text1.config(font=('Helvetica bold', 15))
            self.temp_text1.pack()
            self.temp_button1 = Button(self.temp_window1, text="Enter", command=self.gesture_name)
            self.temp_button1.config(width=12, font=("Arial", 15))
            self.temp_button1.place(relx=0.25, rely=0.52)
            self.temp_text1.bind("<Return>", self.gesture_name)

    def gesture_name(self, event=None):
        gesture_input_name = self.temp_text1.get(1.0, "end-1c")
        if gesture_input_name.lower() != "add user" and gesture_input_name != "delete user":
            if gesture_input_name == "":
                mb.showerror(title="User Name", message="Invalid name. Try Again!!")
            elif self.gesture.get() == "Add User":
                self.all_gestures.add_new_gesture([100001, 100011, 101001, 100111, 101000, 101100, str(gesture_input_name)
                                                   , 13, 5, [None, None], "Top", False])
                for i in self.all_gestures.ges_list:
                    if i == "Add User":
                        self.all_gestures.ges_list.remove(i)
                for i in self.all_gestures.ges_list:
                    if i == "Delete User":
                        self.all_gestures.ges_list.remove(i)
                self.all_gestures.gestures_list_updater()
                self.gesture_list = self.all_gestures.ges_list
                self.gesture_list.append("Add User")
                self.gesture_list.append("Delete User")
                self.ges_name = str(gesture_input_name)
                temp_idx = self.all_gestures.get_gesture(gesture_input_name)
                self.all_gestures_position = temp_idx
                self.move = self.all_gestures.gestures[temp_idx][0]
                self.left_click = self.all_gestures.gestures[temp_idx][1]
                self.right_click = self.all_gestures.gestures[temp_idx][2]
                self.scroll = self.all_gestures.gestures[temp_idx][3]
                self.volume_control = self.all_gestures.gestures[temp_idx][4]
                self.brightness_control = self.all_gestures.gestures[temp_idx][5]
                self.all_gestures_position = temp_idx
                self.menu3.destroy()
                self.window_position.destroy()
                self.on_screen_keyboard.destroy()
                self.mode_chg.destroy()
                self.reset_config.destroy()
                self.help.destroy()
                self.quitbutton.destroy()


                self.gesture.set(gesture_input_name)
                self.menu3 = OptionMenu(self.window, self.gesture, *self.gesture_list,
                                        command=self.gesture_select)
                self.menu3.config(font=("Arial", 11))
                self.size_menu3 = self.window.nametowidget(self.menu3.menuname)
                self.size_menu3.config(font=("Arial", 11))
                self.menu3.pack(side=LEFT)

                self.window_position = OptionMenu(self.window, self.window_pos, *self.win_positions,
                                                  command=self.window_position_change)
                self.window_position.config(font=("Arial", 11))
                self.size_menu_window_position = self.window.nametowidget(self.window_position.menuname)
                self.size_menu_window_position.config(
                    font=("Arial", 11))
                self.window_position.pack(side=LEFT)

                self.on_screen_keyboard = Button(self.window, text="On-Screen Keyboard", command=self.onsky)
                self.on_screen_keyboard.config(font=("Arial", 11))
                self.on_screen_keyboard.pack(side=LEFT)

                self.mode_chg = Button(self.window, text="Change Mode", command=self.chg_mode)
                self.mode_chg.config(font=("Arial", 11))
                self.mode_chg.pack(side=LEFT)

                self.reset_config = Button(self.window, text="Reset Previous Settings", command=self.reset_config_files)
                self.reset_config.config(font=("Arial", 11))
                self.reset_config.pack(side=LEFT)

                self.help = Button(self.window, text="Help", command=self.help_function)
                self.help.config(font=("Arial", 11),
                                 width=11)
                self.help.pack(side=LEFT)

                self.quitbutton = Button(self.window, text="Quit", command=self.proper_exit)
                self.quitbutton.config(font=("Arial", 11))
                self.quitbutton.config(width=11)
                self.quitbutton.pack(side=LEFT)

                self.chgRefstat = True
                self.stat = False
            else:
                if gesture_input_name in self.gesture_list:
                    self.gesture_list.remove(gesture_input_name)
                    idx = self.all_gestures.get_gesture(gesture_input_name)
                    self.all_gestures.gestures.remove(self.all_gestures.gestures[idx])
                    self.menu3.destroy()
                    self.window_position.destroy()
                    self.on_screen_keyboard.destroy()
                    self.mode_chg.destroy()
                    self.reset_config.destroy()
                    self.help.destroy()
                    self.quitbutton.destroy()
                    self.gesture.set("Default")
                    self.menu3 = OptionMenu(self.window, self.gesture, *self.gesture_list,
                                            command=self.gesture_select)
                    self.menu3.config(font=("Arial", 11))
                    self.size_menu3 = self.window.nametowidget(self.menu3.menuname)
                    self.size_menu3.config(font=("Arial", 11))
                    self.menu3.pack(side=LEFT)

                    self.window_position = OptionMenu(self.window, self.window_pos, *self.win_positions,
                                                      command=self.window_position_change)
                    self.window_position.config(
                        font=("Arial", 11))
                    self.size_menu_window_position = self.window.nametowidget(self.window_position.menuname)
                    self.size_menu_window_position.config(
                        font=("Arial", 11))
                    self.window_position.pack(side=LEFT)

                    self.on_screen_keyboard = Button(self.window, text="On-Screen Keyboard", command=self.onsky)
                    self.on_screen_keyboard.config(
                        font=("Arial", 11))
                    self.on_screen_keyboard.pack(side=LEFT)

                    self.mode_chg = Button(self.window, text="Change Mode", command=self.chg_mode)
                    self.mode_chg.config(font=("Arial", 11))
                    self.mode_chg.pack(side=LEFT)

                    self.reset_config = Button(self.window, text="Reset Previous Settings",
                                               command=self.reset_config_files)
                    self.reset_config.config(font=("Arial", 11))
                    self.reset_config.pack(side=LEFT)

                    self.help = Button(self.window, text="Help", command=self.help_function)
                    self.help.config(font=("Arial", 11),
                                     width=11)
                    self.help.pack(side=LEFT)

                    self.quitbutton = Button(self.window, text="Quit", command=self.proper_exit)
                    self.quitbutton.config(font=("Arial", 11))
                    self.quitbutton.config(width=11)
                    self.quitbutton.pack(side=LEFT)
                else:
                    mb.showerror(title="Delete User", message="Invalid name. Try Again!!")
                    self.gesture.set("Default")
        else:
            mb.showerror(title="User Name", message="Invalid name. Try Again!!")
            self.gesture.set("Default")

        self.temp_window1.destroy()

    def gesture_string_generator(self, ges_val):
        result_string = ""
        for i in (10, 100, 1000, 10000):
            if int((ges_val % i) / (i / 10)) == 1:
                result_string = result_string + "UP "
            else:
                result_string = result_string + "DOWN "
        return result_string

    def controlSettings(self, which_option):
        self.isGesture_option_open = True
        if which_option != "Current Controls" and which_option != "Allowed Controls List":
            self.temp_window = Toplevel()
            self.temp_window.title(which_option)

            byte_data = base64.b64decode(explode)
            image_data = BytesIO(byte_data)
            image = pi.open(image_data)

            self.temp_img = pk.PhotoImage(image.resize((400, 500), pi.ANTIALIAS))
            self.temp_can = Canvas(self.temp_window, width=self.temp_img.width(), height=self.temp_img.height())
            self.temp_can.create_image(0, 0, image=self.temp_img, anchor=NW)
            self.temp_can.grid()
            for_movement = self.all_gestures.gestures[self.all_gestures_position][0]
            left_click = self.all_gestures.gestures[self.all_gestures_position][1]
            right_click = self.all_gestures.gestures[self.all_gestures_position][2]
            scrolling = self.all_gestures.gestures[self.all_gestures_position][3]
            vol = self.all_gestures.gestures[self.all_gestures_position][4]
            brigh = self.all_gestures.gestures[self.all_gestures_position][5]
            controls = [[], ["For Movement"], ["Left Click"], ["Right Click"], ["Scrolling"], ["Volume Control"],
                        ["Brightness Control"]]
            controls[1] = controls[1] + self.gesture_string_generator(for_movement).split(" ")
            controls[2] = controls[2] + self.gesture_string_generator(left_click).split(" ")
            controls[3] = controls[3] + self.gesture_string_generator(right_click).split(" ")
            controls[4] = controls[4] + self.gesture_string_generator(scrolling).split(" ")
            controls[5] = controls[5] + self.gesture_string_generator(vol).split(" ")
            controls[6] = controls[6] + self.gesture_string_generator(brigh).split(" ")
            colour_comb = ["", "red", "#7F38EC", "green", "#F433FF"]
            colour_row = ["", "#B6B6B4", "#C9C0BB", "#B6B6B4", "#C9C0BB", "#B6B6B4", "#C9C0BB", "#B6B6B4", "#C9C0BB"
                , "#B6B6B4", "#C9C0BB"]
            self.e = Entry(self.temp_window, width=27, fg='white', bg="black", font=('Arial', 16, 'bold'))
            self.e.grid(row=1, column=0)
            self.e.insert(END, "CONTROLS")
            self.e.config(state=DISABLED, disabledbackground="black", disabledforeground="white")

            temp_list = ["", "Finger A", "Finger B", "Finger C", "Finger D"]
            for i in range(1, 5):
                self.e = Entry(self.temp_window, width=9, fg=colour_comb[i], font=('Arial', 16, 'bold'), bg="black")
                self.e.grid(row=1, column=i)
                self.e.insert(END, temp_list[i])
                self.e.config(state=DISABLED, disabledforeground=colour_comb[i], disabledbackground="black")

            for i in range(2, 8):
                for j in range(5):
                    if j == 0:
                        self.e = Entry(self.temp_window, width=27, fg='black', bg=colour_row[i],
                                       font=('Arial', 16))
                        self.e.grid(row=i, column=j)
                        self.e.insert(END, controls[i - 1][j])
                        self.e.config(state=DISABLED, disabledforeground="black", disabledbackground=colour_row[i])
                    else:
                        self.e = Entry(self.temp_window, width=9, fg=colour_comb[j], bg=colour_row[i],
                                       font=('Arial', 16))
                        self.e.grid(row=i, column=j)
                        self.e.insert(END, controls[i - 1][j])
                        self.e.config(state=DISABLED, disabledforeground=colour_comb[j], disabledbackground=colour_row[i])
            self.description = Label(self.temp_window, text=f"Please specify the gesture '{which_option}' using  the \n"
                                                            "below options. If you want to use finger A, then select \n"
                                                            "UP in finger A else DOWN. Same procedure is followed \nby"
                                                            " others. The table below displays the current controls\n"
                                                            "settings. Change Accordingly.")
            self.description.config(font=("Arial", 13))
            self.description.grid(row=0, column=1, columnspan=4)
            self.menu_b1 = StringVar()
            self.menu_b1.set("Finger A")
            self.options_b1 = OptionMenu(self.temp_window, self.menu_b1, "UP", "DOWN", command=self.fing_1)
            self.options_b1.config(bg="red", width=7,  font=("Arial", 13))
            self.options_b1.grid(row=9, column=1)

            self.menu_b2 = StringVar()
            self.menu_b2.set("Finger B")
            self.options_b2 = OptionMenu(self.temp_window, self.menu_b2, "UP", "DOWN", command=self.fing_2)
            self.options_b2.config(bg="#7F38EC", width=7,  font=("Arial", 13))
            self.options_b2.grid(row=9, column=2)

            self.menu_b3 = StringVar()
            self.menu_b3.set("Finger C")
            self.options_b3 = OptionMenu(self.temp_window, self.menu_b3, "UP", "DOWN", command=self.fing_3)
            self.options_b3.config(bg="green",  width=7,  font=("Arial", 13))
            self.options_b3.grid(row=9, column=3)

            self.menu_b4 = StringVar()
            self.menu_b4.set("Finger D")
            self.options_b4 = OptionMenu(self.temp_window, self.menu_b4, "UP", "DOWN", command=self.fing_4)
            self.options_b4.config(bg="#F433FF",  width=7,  font=("Arial", 13))
            self.options_b4.grid(row=9, column=4)


            self.temp_ll = Label(master=self.temp_window ,text=" ")
            self.temp_ll.grid(row=10, column=0)
            self.temp_ll1 = Label(master=self.temp_window, text=" ")
            self.temp_ll.grid(row=11, column=0)
            self.temp_button = Button(self.temp_window, text="Enter", command=self.get_fingers)
            self.temp_button.config(width=20, bg="#B6B6B4",  font=("Arial", 13))
            self.temp_button.grid(row=12, column=1, columnspan=2)

            self.temp_button2 = Button(self.temp_window, text="Cancel", command=self.can_cancel)
            self.temp_button2.config(width=20, bg="#B6B6B4", font=("Arial", 13))
            self.temp_button2.grid(row=12, column=3, columnspan=4)
            self.temp_window.protocol("WM_DELETE_WINDOW", self.can_cancel)
            self.temp_window.mainloop()
        else:
            self.temp_window = Toplevel()
            self.temp_window.title(which_option)
            byte_data = base64.b64decode(explode)
            image_data = BytesIO(byte_data)
            image = pi.open(image_data)
            self.temp_img = pk.PhotoImage(image.resize((400, 500),
                                                      pi.ANTIALIAS))
            self.temp_can = Canvas(self.temp_window, width=self.temp_img.width(), height=self.temp_img.height())
            self.temp_can.create_image(0, 0, image=self.temp_img, anchor=NW)
            self.temp_window.protocol("WM_DELETE_WINDOW", self.can_cancel)
            self.temp_can.grid(row=0, column=0)
            if which_option == "Current Controls":
                self.information_label = Label(master=self.temp_window,
                                               text="Here, each control is a combination of these \n"
                                                    "four fingers. If in the table, for certain control\n"
                                                    "finger A is UP that means that we should lift\n"
                                                    "the finger A and also other required fingers to\n "
                                                    "activate that control and in the same way if \n"
                                                    "a finger is DOWN that means that we should \n"
                                                    "put down that finger.")
                self.information_label.config(font=('Arial', 14, 'bold'))
                self.information_label.grid(row=0, column=1, columnspan=4)
                for_movement = self.all_gestures.gestures[self.all_gestures_position][0]
                left_click = self.all_gestures.gestures[self.all_gestures_position][1]
                right_click = self.all_gestures.gestures[self.all_gestures_position][2]
                scrolling = self.all_gestures.gestures[self.all_gestures_position][3]
                vol = self.all_gestures.gestures[self.all_gestures_position][4]
                brigh = self.all_gestures.gestures[self.all_gestures_position][5]
                controls = [[], ["For Movement"], ["Left Click"], ["Right Click"], ["Scrolling"], ["Volume Control"],
                            ["Brightness Control"]]
                controls[1] = controls[1] + self.gesture_string_generator(for_movement).split(" ")
                controls[2] = controls[2] + self.gesture_string_generator(left_click).split(" ")
                controls[3] = controls[3] + self.gesture_string_generator(right_click).split(" ")
                controls[4] = controls[4] + self.gesture_string_generator(scrolling).split(" ")
                controls[5] = controls[5] + self.gesture_string_generator(vol).split(" ")
                controls[6] = controls[6] + self.gesture_string_generator(brigh).split(" ")
                colour_comb = ["", "red", "#7F38EC", "green", "#F433FF"]
                colour_row = ["", "#B6B6B4", "#C9C0BB", "#B6B6B4", "#C9C0BB", "#B6B6B4", "#C9C0BB",  "#B6B6B4", "#C9C0BB"
                    ,  "#B6B6B4", "#C9C0BB"]
                self.e = Entry(self.temp_window, width=27, fg='white', bg="black", font=('Arial', 16, 'bold'))
                self.e.grid(row=1, column=0)
                self.e.insert(END, "CONTROLS")
                self.e.config(state=DISABLED, disabledbackground="black", disabledforeground="white")
                temp_list = ["", "Finger A", "Finger B", "Finger C", "Finger D"]
                for i in range(1, 5):
                    self.e = Entry(self.temp_window, width=9, fg=colour_comb[i], font=('Arial', 16, 'bold'), bg="black")
                    self.e.grid(row=1, column=i)
                    self.e.insert(END, temp_list[i])
                    self.e.config(state=DISABLED, disabledbackground="black", disabledforeground=colour_comb[i])

                for i in range(2, 8):
                    for j in range(5):
                        if j == 0:
                            self.e = Entry(self.temp_window, width=27, fg='black', bg=colour_row[i], font=('Arial', 16))
                            self.e.grid(row=i, column=j)
                            self.e.insert(END, controls[i-1][j])
                            self.e.config(state=DISABLED, disabledforeground="black", disabledbackground=colour_row[i])
                        else:
                            self.e = Entry(self.temp_window, width=9, fg=colour_comb[j], bg=colour_row[i], font=('Arial', 16))
                            self.e.grid(row=i, column=j)
                            self.e.insert(END, controls[i-1][j])
                            self.e.config(state=DISABLED, disabledbackground=colour_row[i], disabledforeground=colour_comb[j])
            elif which_option == "Allowed Controls List":
                self.information_label = Label(master=self.temp_window,
                                               text="Here, are the list of combinations of fingers \n"
                                                    "which are allowed to use in this application.\n"
                                                    "If in the table finger A is UP signifies that \n"
                                                    "in order to activate that gesture, we need to lift\n"
                                                    "the the finger A and also with other fingers\n"
                                                    "according to the gesture combination.")
                self.information_label.config(font=('Arial', 14, 'bold'))
                self.information_label.grid(row=0, column=1, columnspan=4)
                colour_comb = ["", "red", "#7F38EC", "green", "#F433FF"]
                colour_row = ["", "#B6B6B4", "#C9C0BB", "#B6B6B4", "#C9C0BB", "#B6B6B4", "#C9C0BB", "#B6B6B4", "#C9C0BB",
                              "#B6B6B4", "#C9C0BB","#B6B6B4", "#C9C0BB"]
                self.e = Entry(self.temp_window, width=27, fg='white', bg="black", font=('Arial', 16, 'bold'))
                self.e.grid(row=1, column=0)
                self.e.insert(END, "Gestures")
                self.e.config(state=DISABLED, disabledforeground="white", disabledbackground="black")
                temp_list = ["", "Finger A", "Finger B", "Finger C", "Finger D"]
                for i in range(1, 5):
                    self.e = Entry(self.temp_window, width=9, fg=colour_comb[i], font=('Arial', 16, 'bold'), bg="black")
                    self.e.grid(row=1, column=i)
                    self.e.insert(END, temp_list[i])
                    self.e.config(state=DISABLED, disabledforeground=colour_comb[i], disabledbackground="black")
                req_list = ["", ["Gesture 1"], ["Gesture 2"], ["Gesture 3"], ["Gesture 4"], ["Gesture 5"], ["Gesture 6"]]

                for i in range(1, len(self.all_gestures.possible_gestures)+1):
                    req_list[i] = req_list[i] + self.gesture_string_generator(self.all_gestures.possible_gestures[i-1]).split(" ")
                for i in range(1, 5):
                    self.e = Entry(self.temp_window, width=9, fg=colour_comb[i], font=('Arial', 16, 'bold'), bg="black")
                    self.e.grid(row=1, column=i)
                    self.e.insert(END, temp_list[i])
                    self.e.config(state=DISABLED, disabledbackground="black", disabledforeground=colour_comb[i])

                for i in range(1, 7):
                    for j in range(5):
                        if j == 0:
                            self.e = Entry(self.temp_window, width=27, fg='black', bg=colour_row[i], font=('Arial', 16))
                            self.e.grid(row=i+1, column=j)
                            self.e.insert(END, req_list[i][j])
                            self.e.config(state=DISABLED, disabledforeground="black", disabledbackground=colour_row[i])
                        else:
                            self.e = Entry(self.temp_window, width=9, fg=colour_comb[j], bg=colour_row[i], font=('Arial', 16))
                            self.e.grid(row=i+1, column=j)
                            self.e.insert(END, req_list[i][j])
                            self.e.config(state=DISABLED, disabledbackground=colour_row[i], disabledforeground=colour_comb[j])

    def can_cancel(self):
        if self.menu_cancel_stat:
            self.isGesture_option_open = False
            self.temp_window.destroy()
        else:
            mb.showerror(title="Control Settings", message="You cannot close this without updating the gesture")


    def fing_1(self, event):
        inp = self.menu_b1.get()
        if inp == "UP":
            self.temp_fing1 = 1
        else:
            self.temp_fing1 = 0

    def fing_2(self, event):
        inp = self.menu_b2.get()
        if inp == "UP":
            self.temp_fing2 = 1
        else:
            self.temp_fing2 = 0

    def fing_3(self, event):
        inp = self.menu_b3.get()
        if inp == "UP":
            self.temp_fing3 = 1
        else:
            self.temp_fing3 = 0

    def fing_4(self, event):
        inp = self.menu_b4.get()
        if inp == "UP":
            self.temp_fing4 = 1
        else:
            self.temp_fing4 = 0

    def get_fingers(self):
        self.isGesture_option_open = False
        self.menu_cancel_stat = True
        if self.menu_b1.get() == "Finger A" or self.menu_b2.get() == "Finger B" or self.menu_b3.get() == "Finger C" or self.menu_b4.get() == "Finger D":
            mb.showerror("Control Settings", "Please, specify the gesture properly")
        else:
            total_gesture = 100000
            total_gesture = total_gesture + self.temp_fing1 + 10*self.temp_fing2 + 100*self.temp_fing3 + 1000*self.temp_fing4
            if self.all_gestures.is_new_gesture_possible(total_gesture):
                if self.gesture_menu.get() == "For Movement":
                    update_stat = self.all_gestures.gestureColliderChecker(total_gesture, 0, self.all_gestures_position)
                    if update_stat == -1:
                        self.all_gestures.update_gestures(self.all_gestures_position, 0, total_gesture)
                        self.gesture_menu.set("Controls")
                        self.temp_window.destroy()
                    else:
                        self.all_gestures.update_gestures(self.all_gestures_position, 0, total_gesture)
                        mb.showerror("For Movement Control Settings", message="The new gesture inputted is colliding with "
                                                                              "another gesture. It will be opened. Please "
                                                                              "update that setting also")
                        self.menu_cancel_stat = False
                        self.gesture_menu.set(self.gesture_names[update_stat])
                        self.temp_window.destroy()
                        self.controlSettings(self.gesture_names[update_stat])


                elif self.gesture_menu.get() == "For Left-Click":
                    update_stat = self.all_gestures.gestureColliderChecker(total_gesture, 1, self.all_gestures_position)
                    if update_stat == -1:
                        self.all_gestures.update_gestures(self.all_gestures_position, 1, total_gesture)
                        self.temp_window.destroy()
                        self.gesture_menu.set("Controls")
                    else:
                        self.all_gestures.update_gestures(self.all_gestures_position, 1, total_gesture)
                        mb.showerror("For Left-Click Control Settings", message="The new gesture inputted is colliding with "
                                                                              "another gesture. It will be opened. Please "
                                                                              "update that setting also")
                        self.menu_cancel_stat = False
                        self.gesture_menu.set(self.gesture_names[update_stat])
                        self.temp_window.destroy()
                        self.controlSettings(self.gesture_names[update_stat])

                elif self.gesture_menu.get() == "For Right-Click":
                    update_stat = self.all_gestures.gestureColliderChecker(total_gesture, 2, self.all_gestures_position)
                    if update_stat == -1:
                        self.all_gestures.update_gestures(self.all_gestures_position, 2, total_gesture)
                        self.temp_window.destroy()
                        self.gesture_menu.set("Controls")
                    else:
                        self.all_gestures.update_gestures(self.all_gestures_position, 2, total_gesture)
                        mb.showerror("For Right-Click Control Settings", message="The new gesture inputted is colliding with "
                                                                          "another gesture. It will be opened. Please "
                                                                          "update that setting also")
                        self.menu_cancel_stat = False
                        self.gesture_menu.set(self.gesture_names[update_stat])
                        self.temp_window.destroy()
                        self.controlSettings(self.gesture_names[update_stat])

                elif self.gesture_menu.get() == "For Scrolling":
                    update_stat = self.all_gestures.gestureColliderChecker(total_gesture, 3, self.all_gestures_position)
                    if update_stat == -1:
                        self.all_gestures.update_gestures(self.all_gestures_position, 3, total_gesture)
                        self.temp_window.destroy()
                        self.gesture_menu.set("Controls")
                    else:
                        self.all_gestures.update_gestures(self.all_gestures_position, 3, total_gesture)
                        mb.showerror("For Scrolling Control Settings", message="The new gesture inputted is colliding with "
                                                                          "another gesture. It will be opened. Please "
                                                                          "update that setting also")
                        self.menu_cancel_stat = False
                        self.gesture_menu.set(self.gesture_names[update_stat])
                        self.temp_window.destroy()
                        self.controlSettings(self.gesture_names[update_stat])

                elif self.gesture_menu.get() == "Volume Control":
                    update_stat = self.all_gestures.gestureColliderChecker(total_gesture, 4, self.all_gestures_position)
                    if update_stat == -1:
                        self.all_gestures.update_gestures(self.all_gestures_position, 4, total_gesture)
                        self.temp_window.destroy()
                        self.gesture_menu.set("Controls")
                    else:
                        self.all_gestures.update_gestures(self.all_gestures_position, 4, total_gesture)
                        mb.showerror("For Volume Control Settings", message="The new gesture inputted is colliding with "
                                                                          "another gesture. It will be opened. Please "
                                                                          "update that setting also")
                        self.menu_cancel_stat = False
                        self.gesture_menu.set(self.gesture_names[update_stat])
                        self.temp_window.destroy()
                        self.controlSettings(self.gesture_names[update_stat])
                elif self.gesture_menu.get() == "Brightness Control":
                    update_stat = self.all_gestures.gestureColliderChecker(total_gesture, 5, self.all_gestures_position)
                    if update_stat == -1:
                        self.all_gestures.update_gestures(self.all_gestures_position, 5, total_gesture)
                        self.temp_window.destroy()
                        self.gesture_menu.set("Controls")
                    else:
                        update_stat = self.all_gestures.gestureColliderChecker(total_gesture, 5, self.all_gestures_position)
                        mb.showerror("For Brightness Control Settings", message="The new gesture inputted is colliding with "
                                                                          "another gesture. It will be opened. Please "
                                                                          "update that setting also")
                        self.menu_cancel_stat = False
                        self.gesture_menu.set(self.gesture_names[update_stat])
                        self.temp_window.destroy()
                        self.controlSettings(self.gesture_names[update_stat])
            else:
                mb.showerror("Invalid Gesture", message="The Gesture you selected creates ambiguity to the Application."
                                                        " Please Select Another Gesture. You can check the allowed "
                                                        "gestures in Controls tab.")

    def proper_exit(self):
        if self.menu_cancel_stat:
            self.stat = False
            self.chgRefstat = False
            self.chgWebCamstat = False
            self.prop_exit = True
        else:
            self.stat = False
            self.chgRefstat = False
            self.chgWebCamstat = False
            self.prop_exit = False

    def end_program(self):
        sys.exit(0)
