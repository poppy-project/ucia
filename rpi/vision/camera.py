import cv2 as cv

class Camera:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_camera()
        return cls._instance

    def init_camera(self):
        self.cap = cv.VideoCapture(0)

    def grab_frame_loop(self):
        return self.cap.read()
        
    def __del__(self):
        self.cap.release()