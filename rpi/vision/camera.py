import cv2 as cv
import json
import os
import threading
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

        self.thread = threading.Thread(target=self._save_images)
        self.thread.start()

    def _save_images(self):
        """
        Saves the original and detected images in a loop.
        """
        from .object_detector import detect_objects

        while True:
            ret, frame = self.cap.read()
            if ret:
                self.last_frame = frame
                # Define the paths to save the images
                original_img_path = os.path.join(self.image_dir, 'original_img.jpg')
                detected_img_path = os.path.join(self.image_dir, 'detected_img.jpg')
                detected_data_path = os.path.join(self.image_dir, 'detected_data.json')

                # Save the original image
                cv.imwrite(original_img_path, frame)

                # Process and save the detected image
                self.last_found_obj = detect_objects(frame)
                self.last_detected_frame = frame  # Assuming detect_objects does not modify the frame

                cv.imwrite(detected_img_path, frame)
                with open(detected_data_path, 'w') as f:
                    json_data = [visual_object_to_dict(vo) for vo in self.last_found_obj]
                    json.dump(json_data, f)

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
        self.thread.join()

