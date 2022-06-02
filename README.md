This project is about controlling the cursor movement using the hand gestures and motion. The hand is tracked using a webcam and by using libraries like 
Mediapipe and OpenCV. By this project we can replace the traditional mouse and keyboard system. This project proposes a novel vision-based cursor control system, using hand gestures captured from a webcam. Like in sci-fi movies we saw how hologram technology can be used to make information touch free, but in reality, we are 
not close to this technology. Our project acts as a bridge between the hologram 3-d technology and the traditional mouse system. In this project the system will 
allow the user to navigate the computer cursor using their hand and cursor functions, such as right and left clicks, will be performed using different hand 
gestures. 

METHODOLOGY 
Back End: 
1. The libraries used in this project are open CV, mediapipe, autopy, numpy, time, pyautogui, ctypes, comtypes, pycaw, screen_brightness_control. 

2. Open CV: It is an open source library which is used for real time image processing. It helps us in computer vision tasks. By using OpenCV, we can 
manipulate 2d array of image. 

3. Mediapipe: It is a cross-platform developed by Google for Advanced Tracking. By using Mediapipe, we can track hands, posture, facial 
expression, etc. very easily. The Mediapipe uses only CPU for Image processing. Due to this advantage, the mediapipe can be used in old system 
or systems with less specifications effectively. 

4. Autopy: It is a cross-platform, GUI automation library which is used to control the mouse of the computer in Python. By using this library, we will 
have coordinates for where the mouse needs to be present and this library executes it. 

5. Numpy: This library is one of the mostly used library in Python. My using Numpy, we will generate relative coordinates as the solution of our camera 
is different from our screen resolution, we need to generate relative coordinates. 

6. Time: We used time library to calculate the FPS of our program. The main analyzing parameter for our project is the FPS. Based on FPS only we can 
determine the performance of our program. If the FPS is low then the program is lagging and vise versa. So, to get FPS we need time library. 
 
7. Pyautogui: The library also works same as Autopy, but in comparison for operations like left click and right click, the Pyautogui is working better 
than Autopy. So, we used Pyautogui. 

8. ctypes, comtypes, pycaw: There are the libraries which we used to control audio in windows using Python. In our project we can control the volume 
based on our finger gestures. So, to implement that we used the above libraries. 

9. screen_brightness_control: As the name suggests, we used this library to control the brightness of windows using Python. In our program, we included separate gesture to control the Screen Brightness.  Till now, we discussed about the libraries used. Now, we will explain the program execution.
