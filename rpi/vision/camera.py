import cv2 as cv
import json
import os
import threading
import time
import numpy as np

def visual_object_to_dict(vo):
    return {
        'label': vo.label,
        'center': tuple(float(c) for c in vo.center),
        'box': [float(b) for b in vo.box.tolist()],
        'confidence': float(vo.confidence)
    }

class Camera:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_camera()
        return cls._instance

    def _init_camera(self):
        self.cap = cv.VideoCapture(0)
        self.last_frame = None
        self.last_detected_frame = None
        self.last_found_obj = np.empty((0, 0))

        self.image_dir = "/tmp/rosa/images"
        os.makedirs(self.image_dir, exist_ok=True)

        self.capture_thread = threading.Thread(target=self._capture_frames)
        self.capture_thread.daemon = True  # Set the thread as a daemon to exit when the main program exits
        self.capture_thread.start()

        self.detect_thread = threading.Thread(target=self._detect_objects_continuously)
        self.detect_thread.daemon = True
        self.detect_thread.start()

    def _capture_frames(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                original_img_path = os.path.join(self.image_dir, 'camera.jpg')
                cv.imwrite(original_img_path, frame)
                self.last_frame = frame
            
            time.sleep(0.010)

    def _detect_objects_continuously(self):
        from .object_detector import detect_objects

        while True:
            frame = self.last_frame  # Capture the last available frame
            if frame is not None:
                self.last_detected_frame = frame  # Assuming detect_objects does not modify the frame
                try:
                    self.last_found_obj = detect_objects(frame, render=True)
                except:
                    self.logger.error("Error when you call detect_object")
                    continue
                # Save the detected image and data
                detected_img_path = os.path.join(self.image_dir, 'detected_img.jpg')
                detected_data_path = os.path.join(self.image_dir, 'detected_data.json')

                if self.last_found_obj:
                    cv.imwrite(detected_img_path, frame)
                    with open(detected_data_path, 'w') as f:
                        json_data = [visual_object_to_dict(vo) for vo in self.last_found_obj]
                        json.dump(json_data, f)
            time.sleep(0.010) 

    def grab_frame(self):
        """
        Returns the last frame captured.
        :return: frame: ndarray
        """
        return self.last_frame

    def grab_detected_data_and_frame(self):
        """
        Returns the last detected data and processed frame.
        :return: last_found_obj: dict, detected_frame: ndarray
        """
        return self.last_found_obj, self.last_detected_frame

    def grab_detected_data(self):
        """
        Returns the last detected data.
        :return: last_found_obj: dict
        """
        return self.last_found_obj

    def grab_detected_frame(self):
        """
        Returns the last detected frame.
        :return: detected_frame: ndarray
        """
        return self.last_detected_frame

    def __del__(self):
        self.cap.release()