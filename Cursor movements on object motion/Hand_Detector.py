import cv2 as cv
import mediapipe as mp
import math


class HandDetector:
    def __init__(self, static_image_mode=False, max_num_hands=1, model_complexity=1,min_detection_confidence=0.4,
                 min_tracking_confidence=0.5):
        self.hand_obj = mp.solutions.hands.Hands(static_image_mode, max_num_hands, model_complexity, min_detection_confidence,
                                            min_tracking_confidence)
        self.draw_hand = mp.solutions.drawing_utils
        self.scale_factor = 0
        self.all_points_raw = 0

    def scale_factor_cal(self):
        point1 = list(self.all_points_raw[1])
        point2 = [self.all_points_raw[17][0], point1[1]]
        min = 10000
        for i in self.all_points_raw:
            if i[1] < min:
                min = i[1]
        point3 = [point1[0], min]
        point4 = [point2[0], min]

        area = self.dist(point1, point4) * self.dist(point2, point4)



    def position(self, img, draw=False):
        rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        output = self.hand_obj.process(rgb_img)
        all_points = []
        self.all_points_raw = []
        if output.multi_hand_landmarks:
            for each_hand in output.multi_hand_landmarks:
                x, y, c = img.shape
                req = [7, 8, 11, 12, 15, 16, 19, 20]
                for idx,point in enumerate(each_hand.landmark):
                    if idx in req:
                        tempx = int(y * point.x)
                        tempy = int(x * point.y)
                        t = (idx, tempx, tempy)
                        all_points.append(t)
                scale_ptr1_x = all_points[1][1]
                scale_ptr1_y = 0
                scale_ptr2_x = all_points[7][1]
                scale_ptr2_y = 0
                scale_ptr1 = (0, scale_ptr1_x, scale_ptr1_y)
                scale_ptr2 = (0, scale_ptr2_x, scale_ptr2_y)

                if draw:
                    color = self.color_decider(all_points[1], (img.shape[0], img.shape[1]), img)
                    for each_point in all_points: #int(self.scale_factor * 0.09)
                        cv.circle(img, (each_point[1], each_point[2]),6 , color, cv.FILLED)
                hand_stat = self.mouse_fingers(all_points)
                img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
                return hand_stat, all_points
        else:
            return None, None

    def mouse_fingers(self, hand_points):
        sum = 100000
        if hand_points is not None: # 0.0375, 0.0887, 0.1663, 0.163
            if hand_points[1][2] < hand_points[0][2]:#and (hand_points[0][2] - hand_points[1][2]) >= 0.0375*scale_factor:
                sum = sum + 1
            if hand_points[3][2] < hand_points[2][2]:
                sum = sum + 10
            if hand_points[5][2] < hand_points[4][2]:
                sum = sum + 100
            if hand_points[7][2] < hand_points[6][2]:
                sum = sum + 1000
            return sum
        else:
            return 0
    def dist(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        distance = math.sqrt((p2[0] - p1[0]) **2 + (p2[1] - p1[1])**2)
        return distance

    def color_decider(self, point, camera, img):
        range_main = int(camera[1]*0.0115)
        point = list(point)
        if point[1] < 0:
            point[1] = 0
        elif point[1] > camera[1]:
            point[1] = camera[1]

        if point[2] < 0:
            point[2] = 0
        elif point[2] > camera[0]:
            point[2] = camera[0]

        if point[1] - range_main >= 0:
            if point[2] - range_main >= 0:
                point_1 = [point[1] - range_main, point[2] - range_main]
            else:
                point_1 = [point[1] - range_main, 0]
        else:
            if point[2] - range_main >= 0:
                point_1 = [0, point[2] - range_main]
            else:
                point_1 = [0, 0]

        if point[1] + range_main < camera[1]:
            if point[2] + range_main < camera[0]:
                point_2 = [point[1] + range_main, point[2] + range_main]
            else:
                point_2 = [point[1] + range_main, camera[0]]
        else:
            if point[2] + range_main < camera[0]:
                point_2 = [camera[1], point[2] + range_main]
            else:
                point_2 = [camera[1], camera[0]]

        r = 0
        g = 0
        b = 0
        no_of_samples = 0
        for i in range(point_1[0], point_2[0]):
            for j in range(point_1[1], point_2[1]):
                no_of_samples = no_of_samples + 1
                for k in range(3):
                    if k == 0:
                        b = b + img[j, i, k]
                    elif k == 1:
                        g = g + img[j, i , k]
                    else:
                        r = r + img[j, i, k]
        r = int(r/no_of_samples)
        b = int(b/no_of_samples)
        g = int(g/no_of_samples)

        r_ = 255 - r
        g_ = 255 - g
        b_ = 255 - b
        return (b_, g_, r_)






