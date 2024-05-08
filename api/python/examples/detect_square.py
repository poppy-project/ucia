import cv2
import numpy as np
from rosa import Rosa

def detect_white_square(image):
    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un seuil pour obtenir une image binaire
    _, threshold = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Trouver les contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dessiner les contours et chercher des carrés
    for cnt in contours:
        # Approximer les contours pour réduire le nombre de points
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        # Conditions pour être un carré: 4 côtés et à peu près des angles droits
        if len(approx) == 4:
            area = cv2.contourArea(approx)
            if area > 1000:  # Assurez-vous que la zone est assez grande pour être notre carré
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h
                if 0.95 < aspect_ratio < 1.05:  # Aspect ratio proche de 1 (carré)
                    cv2.drawContours(image, [approx], 0, (0, 255, 0), 5)
                    return image, (x, y, w, h)

    return image, None

if __name__ == '__main__':
    rosa = Rosa('rosa.local', local_robot=False)

    while True:
        # We can access the last frame from the robot camera using:
        # It will automatically updated with the most up-to-date image
        img = rosa.camera.last_frame

        if img is None:
            continue
        image_with_square, square_details = detect_white_square(img)

        if square_details:
            print("Carré détecté à la position:", square_details)
        else:
            print("Aucun carré détecté.")

        cv2.imshow('rosa', image_with_square)
        cv2.waitKey(0)
    