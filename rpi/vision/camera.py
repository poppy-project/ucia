import cv2 as cv

class Camera:
    def __init__(self):
        self.cap = cv.VideoCapture(0)

    def grab_frame_loop(self):
        _, img = self.cap.read()

        return img
