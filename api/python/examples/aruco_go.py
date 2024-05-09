import cv2 as cv

from rosa import Rosa

import cv2.aruco as aruco


def look_around(rosa, speed=0.2):
    rosa.left_wheel.speed = speed
    rosa.right_wheel.speed = 0

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
                target = calculate_target_aruco(center, (320, 256))  # Assurez-vous que les dimensions de l'image sont correctes
                follow_marker(rosa, target, ratio = 2)

        cv.imshow('rosa', frame_with_markers)
        cv.waitKey(20)
