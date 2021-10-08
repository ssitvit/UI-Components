import cv2
import mediapipe as mp
import time
import serial 

class GestureRecognizer:
    finger_pts = [4, 8, 12, 16, 20]
    fingers = ["Thumb", "Index", "Middle", "Ring", "Little"]
    # to change the gesture we have to edit this switcher key values.
    switcher = {
        "[1, 0, 0, 0, 0]": "7",
        "[0, 0, 0, 0, 0]": "0",
        "[0, 1, 0, 0, 0]": "1",
        "[0, 1, 1, 0, 0]": "2",
        "[0, 1, 1, 1, 0]": "3",
        "[0, 1, 1, 1, 1]": "4",
        "[1, 1, 1, 1, 1]": "5",
    }

    def __init__(self, mode=False, hands_max=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode = mode
        self.hands_max = hands_max
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.mpHands = mp.solutions.hands  # Object
        self.mpDraw = mp.solutions.drawing_utils  # for drawing from the 21 points
        self.hands = self.mpHands.Hands()

    def start_tracking(self):
        cap = cv2.VideoCapture(0)
        w, h = 640,480
        cap.set(3, 640)
        cap.set(4, 480)
        # tracker = GestureRecognizer()

        arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
        time.sleep(2)
            
        while 1:
            suc, img = cap.read()
            img = self.find_hands(img)
            pts = self.find_posi(img)  # points of the hand
            fan_input = self.count_open(pts)
            # prev_fan_input = fan_input
            time.sleep(1)
            print("fi- {}".format(fan_input))
            
            
            if fan_input == '1':
                arduino.write(b'1')

            elif fan_input == '2':
                arduino.write(b'2')

            elif fan_input == '3':
                arduino.write(b'3')

            elif fan_input == '4':
                arduino.write(b'4')

            cv2.imshow("image", img)
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            
    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_posi(self, img, hand_number=0, draw=False):
        lm_list = []
        if self.result.multi_hand_landmarks:
            my_hand = self.result.multi_hand_landmarks[hand_number]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (0, 177, 225), cv2.FILLED)
        return lm_list

    # def hand_signs(self,f_out):
    #     # if f_out == [0,0,0,0,0]:
    #     #     fan_input=0;
    #     switcher = {
    #         [0, 0, 0, 0, 0]: 0,
    #         [1, 0, 0, 0, 0]: 1,
    #         [1, 1, 0, 0, 0]: 2,
    #         [1, 1, 1, 0, 0]: 3,
    #         [1, 1, 1, 1, 0]: 4,
    #         [1, 1, 1, 1, 1]: 5,
    #     }
    #     return switcher.get(f_out)

    def count_open(self, pts):
        f_open = []  # open fingers
        if len(pts) != 0:
            if pts[4][1] > pts[3][1]:  # thumb
                f_open.append(1)
            else:
                f_open.append(0)
            for pt in self.finger_pts[1:]:
                if pts[pt][2] < pts[pt - 2][2]:
                    f_open.append(1)
                else:
                    f_open.append(0)
        fan_input = self.switcher.get(str(f_open))
        return fan_input
    # def set_sign(self,img):


def main():
    gr = GestureRecognizer()
    gr.start_tracking()

if __name__ == "__main__":
    main()
