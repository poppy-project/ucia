import unittest

import requests
import cv2 as cv
import numpy as np

from io import BytesIO

from rosa.vision import detect_objects, get_line_center


class VisionTestCase(unittest.TestCase):
    RES = 640, 480, 3
    line_url = 'https://github.com/pollen-robotics/rosa/raw/master/api/python/tests/line.jpg'
    obj_url = 'https://github.com/pollen-robotics/rosa/raw/master/api/python/tests/obj.jpg'
    no_obj_url = 'https://github.com/pollen-robotics/rosa/raw/master/api/python/tests/no-obj.jpg'

    def setUp(self):
        self.random_img = self.generate_random_image()

        self.line_img = self.load_img(VisionTestCase.line_url)
        self.obj_img = self.load_img(VisionTestCase.obj_url)
        self.no_obj_img = self.load_img(VisionTestCase.no_obj_url)

    def load_img(self, url):
        resp = requests.get(url)

        with BytesIO(resp.content) as io:
            img = np.asarray(bytearray(io.read()), dtype=np.uint8)
            img = cv.imdecode(img, cv.IMREAD_COLOR)
            return cv.resize(img, (VisionTestCase.RES[1], VisionTestCase.RES[0]))

    def test_line_detector(self):
        center = get_line_center(self.random_img)
        self.assertTrue(center is None or len(center) == 2)

        center = get_line_center(self.line_img)
        self.assertEqual(center, (250, 325))
        center = get_line_center(self.obj_img)
        self.assertIsNone(center)
        center = get_line_center(self.no_obj_img)
        self.assertEqual(center, (401, 312))

    def test_obj_detector(self):
        obj = detect_objects(self.random_img)
        self.assertEqual(len(obj), 0)

        obj = detect_objects(self.line_img)
        self.assertEqual(obj, [])
        obj = detect_objects(self.no_obj_img)
        self.assertEqual(obj, [])

        obj = detect_objects(self.obj_img)
        self.assertEqual(len(obj), 2)

        cube, star = obj
        self.assertEqual(cube.label, 'cube')
        self.assertTrue(
            np.linalg.norm(np.array(cube.center) - np.array((97, 109))) < 5.0
        )
        self.assertEqual(star.label, 'star')
        self.assertTrue(
            np.linalg.norm(np.array(star.center) - np.array((194, 95))) < 5.0
        )

    def generate_random_image(self):
        return np.uint8(np.random.rand(*VisionTestCase.RES) * 255)
