import cv2 as cv

from rosa import Rosa

import cv2.aruco as aruco
import numpy as np
import time

def stop_robot(rosa):
    rosa.left_wheel.speed = 0.0
    rosa.right_wheel.speed = 0.0

def turn_behind(rosa):
    rosa.left_wheel.speed = -0.25
    rosa.right_wheel.speed = -0.25

def set_speed(rosa,turn, speed):
    base_speed = speed
    turn_adjustment = -turn * 2.0
    
    left_speed = base_speed - turn_adjustment
    right_speed = base_speed + turn_adjustment
    
    max_motor_speed = 0.25
    left_speed = max(min(left_speed, max_motor_speed), -max_motor_speed)
    right_speed = max(min(right_speed, max_motor_speed), -max_motor_speed)

    rosa.left_wheel.speed = left_speed
    rosa.right_wheel.speed = right_speed


def look_around(rosa, speed=0.2):
    rosa.left_wheel.speed = speed
    rosa.right_wheel.speed = 0

def calculate_target_aruco(center, image_dimensions):
    width, height = image_dimensions
    # Normalise x,y between [-1,1] 
    target_x = (center[0] / width) - 1
    target_y = -(center[1] / height) + 1
    return (target_x, target_y)

def follow_marker(rosa, target, marker_size, width=320, max_speed=0.2, stop_size=300):
    target_x, target_y = target

    speed = max_speed * (1 - abs(target_x))  # Reduce speed if we approach center
    turn = target_x

    if marker_size < stop_size:
        if abs(target_x) > 0.2:  # Seulement si le marqueur n'est pas assez centré
            #print("Non centré")
            set_speed(rosa, turn, speed)
        else:  # Si le marqueur est centré, ajuster seulement l'avancée
            #print("Centré")
            set_speed(rosa, 0, min(speed, 0.2))  # Réduire la vitesse d'avancée près du marqueur
        return False
    else:
        stop_robot(rosa)
        print("Marqueur atteint, actions à définir")
        return True

    # # Envoyer les commandes au robot
    # if abs(target_x) > 0.1:  # Seulement si le marqueur n'est pas assez centré
    #     robot.left_wheel.speed = turn
    #     robot.right_wheel.speed = speed
    #     print("Marqueur non centré")
    # else:  # 
    #     robot.left_wheel.speed = -min(speed, 0.2)
    #     robot.right_wheel.speed = min(speed, 0.2)
    #     print("Marqueur centré")
    
    # # Condition d'arrêt à proximité du marqueur
    # if abs(target_x) < 0.05 and abs(target_y) < 0.05:
    #     robot.left_wheel.speed = 0.0
    #     robot.right_wheel.speed = 0.0
    #     print("Marqueur atteint, actions à définir")


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
    else:
        look_around(rosa)
        #print("Aucun marqueur détecté.")

    return image, markerCorners, markerIds

def calculate_marker_size(corners):
    # corners est un array de points x,y pour chaque coin du marqueur
    width = np.linalg.norm(corners[0] - corners[3])
    height = np.linalg.norm(corners[0] - corners[1])
    return max(width, height)

if __name__ == '__main__':
    rosa = Rosa('rosa.local', local_robot=False)

    while True:
        # We can access the last frame from the robot camera using:
        # It will automatically updated with the most up-to-date image
        img = rosa.camera.last_frame

        if img is None:
            continue
        
        frame_with_markers, corners, ids = detect_aruco(img)
        
        if ids is None:
            look_around(rosa)
        else:
            # We have something
            center = corners[0][0].mean(axis=0)
            marker_size = calculate_marker_size(corners[0][0])  
            target = calculate_target_aruco(center, (320, 256)) 
            print(marker_size)
            follow_marker(rosa, target, marker_size, stop_size=220)
        time.sleep(0.016)
        cv.imshow('rosa', frame_with_markers)
        cv.waitKey(20)
        continue
        if ids is None:
            stop_robot(rosa)
        else:
            stop_robot(rosa)
            center = corners[0][0].mean(axis=0)
            marker_size = calculate_marker_size(corners[0][0])  
            target = calculate_target_aruco(center, (320, 256)) 
            print(target)
        cv.imshow('rosa', frame_with_markers)
        cv.waitKey(20)
