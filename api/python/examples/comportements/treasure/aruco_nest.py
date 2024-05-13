import cv2 as cv
import cv2.aruco as aruco
import numpy as np

def stop_robot(rosa):
    rosa.left_wheel.speed = 0.0
    rosa.right_wheel.speed = 0.0

def turn_behind(rosa):
    rosa.left_wheel.speed = -0.25
    rosa.right_wheel.speed = -0.25

def set_speed_aruco(rosa,turn, speed):
    base_speed = speed
    turn_adjustment = -turn * 2.0
    
    left_speed = base_speed - turn_adjustment
    right_speed = base_speed + turn_adjustment
    
    max_motor_speed = 0.15
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
    target_x = ((center[0] / width) * 2) - 1
    target_y = -((center[1] / height) * 2 - 1)
    return (target_x, target_y)

def follow_marker(rosa, target, marker_size, max_speed=0.3, stop_size=700):
    target_x, target_y = target
    print(target_x)

    speed = max_speed * (1 - abs(target_x))  # Reduce speed if we approach center
    turn = target_x

    if marker_size < stop_size:
        if abs(target_x) > 0.4:  # Seulement si le marqueur n'est pas assez centré
            print("Non centré")
            set_speed_aruco(rosa, turn, speed)
        else:  # Si le marqueur est centré, ajuster seulement l'avancée
            print("Centré")
            set_speed_aruco(rosa, 0, min(speed, 0.25))  # Réduire la vitesse d'avancée près du marqueur
        return False
    else:
        stop_robot(rosa)
        print("Marqueur atteint, actions à définir")
        return True

def detect_aruco(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
    parameters = aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(dictionary, parameters)

    markerCorners, markerIds, _ = detector.detectMarkers(gray)

    if markerIds is not None:
        aruco.drawDetectedMarkers(image, markerCorners, markerIds)
    
    return image, markerCorners, markerIds

def calculate_marker_size(corners):
    width = np.linalg.norm(corners[0] - corners[3])
    height = np.linalg.norm(corners[0] - corners[1])
    return max(width, height)

def go_to_aruco(rosa, img):
    frame_with_markers, corners, ids = detect_aruco(img)
    
    cv.imshow('Frame markers', frame_with_markers)

    change_state = False    
    if ids is None:
        look_around(rosa)
    else:
        center = corners[0][0].mean(axis=0)
        marker_size = calculate_marker_size(corners[0][0])  
        target = calculate_target_aruco(center, (1280, 960))
        print(target)
        change_state = follow_marker(rosa, target, marker_size, stop_size=350)
    
    return change_state
