import cv2 as cv

from rosa import Rosa

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

    return image

if __name__ == '__main__':
    rosa = Rosa('rosa.local', local_robot=False)

    while True:
        # We can access the last frame from the robot camera using:
        # It will automatically updated with the most up-to-date image
        img = rosa.camera.last_frame

        if img is None:
            continue

        frame_with_markers = detect_aruco(img)

        cv.imshow('rosa', frame_with_markers)
        cv.waitKey(20)
