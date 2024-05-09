from __future__ import division

import cv2 as cv
import cv2
import time
from enum import Enum

from rosa import Rosa
from rosa.vision import detect_objects
import cv2.aruco as aruco

def detect_aruco(image):
    # Convertir l'image en niveaux de gris
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # Charger le dictionnaire ArUco préféré
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
    parameters = aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(dictionary, parameters)
    # Détecter les marqueurs
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(gray)

    # Si des marqueurs sont détectés, les afficher
    if markerIds is not None:
        aruco.drawDetectedMarkers(image, markerCorners, markerIds)
        for corner, id in zip(markerCorners, markerIds):
            print(f"Marqueur ID: {id[0]} aux coins: {corner[0]}")
    else:
        print("Aucun marqueur détecté.")

    return image, markerCorners, markerIds

class StateTreasure(Enum):
    SEARCH_CUBE = 1
    GRAB_CUBE = 2
    PUT_CUBE_LINE = 3


def look_around(rosa, speed=0.2):
    rosa.left_wheel.speed = speed
    rosa.right_wheel.speed = 0


def follow_cube(rosa, center, gain=0.4):
    dx, _ = center
    ls = gain * (0.5 * dx + 0.5)
    rs = gain * (0.5 * -dx + 0.5)

    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def calculate_target_aruco(center, image_dimensions):
    width, height = image_dimensions
    # Normaliser les coordonnées x, y pour qu'elles soient comprises entre -1 et 1
    target_x = (center[0] / width - 0.5) * 2
    target_y = -(center[1] / height - 0.5) * 2  # Inverser l'axe y si nécessaire
    return (target_x, target_y)

def follow_marker(robot, target, width=320, max_speed=0.5):
    target_x, target_y = target
    # Calculer les commandes de direction et de vitesse
    speed = max_speed * (1 - abs(target_x))  # Réduire la vitesse en s'approchant du centre
    turn = target_x  # Proportionnellement à la distance du centre

    # Envoyer les commandes au robot
    if abs(target_x) > 0.1:  # Seulement si le marqueur n'est pas assez centré
        robot.left_wheel.speed = turn
        robot.right_wheel.speed = speed
        print("Marqueur non centré")
    else:  # Si le marqueur est centré, ajuster seulement l'avancée
        robot.left_wheel.speed = 0.0
        robot.right_wheel.speed = min(speed, 0.2)
        print("Marqueur centré")

    # Condition d'arrêt à proximité du marqueur
    if abs(target_x) < 0.05 and abs(target_y) < 0.05:
        robot.left_wheel.speed = 0.0
        robot.right_wheel.speed = 0.0
        print("Marqueur atteint, actions à définir")


if __name__ == '__main__':
    rosa = Rosa('rosa.local', local_robot=False)
    state = StateTreasure.SEARCH_CUBE
    timer = time.time()

    while True:
        img = rosa.camera.last_frame

        if img is None:
            continue

        

        if state == StateTreasure.SEARCH_CUBE:
            try:
                found_obj = detect_objects(img, render=True)
            except:
                continue
            cubes = [obj for obj in found_obj if obj.label == 'cube']

            if not cubes:  # We can't find a cube so we have to look around
                look_around(rosa)
            else:
                has_gathered_cube = any([c for c in cubes if c.center[1] > 220 and 150 < c.center[0] < 200])
                if has_gathered_cube:
                    state = StateTreasure.GRAB_CUBE
                    rosa.left_wheel.speed = 0
                    rosa.right_wheel.speed = 0
                    timer = time.time()
                else:
                    (x, y) = cubes[0].center
                    height, width = 256, 320
                    # height, width = 480, 640
                    target = (((x / width) * 2 - 1), -((y / height) * 2 - 1))
    
                    follow_cube(rosa, target)
                
        elif state == StateTreasure.GRAB_CUBE:
            if time.time() - timer > 3.0:
                rosa.left_wheel.speed = 0
                rosa.right_wheel.speed = 0
                state = StateTreasure.PUT_CUBE_LINE
            else:
                rosa.left_wheel.speed = 0.25
                rosa.right_wheel.speed = 0.25
        elif state == StateTreasure.PUT_CUBE_LINE:
            frame_with_markers, corners, ids = detect_aruco(img)
            if ids is None:
                look_around(rosa)
            else:
                # We have something
                center = corners[0][0].mean(axis=0)
                target = calculate_target_aruco(center, (320, 256))  # Assurez-vous que les dimensions de l'image sont correctes
                follow_marker(rosa, target, ratio = 2)
            pass
        else:
            pass

        try:
            cv.imshow('get cube', img)
            cv.waitKey(1)
        except:
            pass