import cv2
import json
import os
import threading
import time
import numpy as np
import logging
from settings import Config
import shutil
import tempfile

def write_image_safely(frame, target_dir, filename='camera.jpg'):
    os.makedirs(target_dir, exist_ok=True)

    temp_fd, temp_path = tempfile.mkstemp(suffix='.jpg', dir=target_dir)
    try:
        cv2.imwrite(temp_path, frame)
        os.close(temp_fd)
        temp_fd = None
    finally:
        if temp_fd is not None:
            os.close(temp_fd)
            os.remove(temp_path)
            raise

    final_path = os.path.join(target_dir, filename)

    # Remove the existing file if it exists
    if os.path.exists(final_path):
        os.remove(final_path)

    shutil.move(temp_path, final_path)
    return final_path

class Camera:
    _instance = None
    logger = logging.getLogger(__name__)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_camera()
        return cls._instance

    def _init_camera(self):
        self.cap = cv2.VideoCapture(0)

        self.update_camera_settings()

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
                #write_image_safely(frame, self.image_dir)
                cv2.imwrite(original_img_path, frame)
                self.last_frame = frame
            
            time.sleep(0.1)

    def _detect_objects_continuously(self):
        self.last_detected_frame = self.last_frame
        pass
        # from .object_detector import detect_objects
        # last_detection_time = time.time()

        # while True:
        #     frame = self.last_frame 
        #     if frame is not None:
        #         self.last_detected_frame = frame
        #         try:
        #             self.last_found_obj = detect_objects(frame, render=True)
        #             settings.loading_model = False
        #         except:
        #             self.logger.error("Error when you call detect_object")
        #             continue
        #         # Save the detected image and data
        #         detected_img_path = os.path.join(self.image_dir, 'detected_img.jpg')
        #         detected_data_path = os.path.join(self.image_dir, 'detected_data.json')
                
        #         if self.last_found_obj or time.time() - last_detection_time >= 3:
        #             last_detection_time = time.time()
                                        
        #             cv.imwrite(detected_img_path, frame)
        #             with open(detected_data_path, 'w') as f:
        #                 json_data = [visual_object_to_dict(vo) for vo in self.last_found_obj]
        #                 json.dump(json_data, f)
        #     time.sleep(0.010) 

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
    
    def update_camera_settings(self):
        config = Config()
        camera_config = config.get_config("camera")

        if camera_config is None:
            return

        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, camera_config["brightness"])
        self.cap.set(cv2.CAP_PROP_EXPOSURE, camera_config["exposure"])
        self.cap.set(cv2.CAP_PROP_CONTRAST, camera_config["contrast"])
        self.cap.set(cv2.CAP_PROP_SATURATION, camera_config["saturation"])

    def __del__(self):
        self.cap.release()