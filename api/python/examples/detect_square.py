import cv2
import numpy as np
from rosa import Rosa

def detect_white_square(image):
    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray", gray)

    # Appliquer un seuil pour obtenir une image binaire
    #_, threshold = cv2.threshold(gray, 65, 255, cv2.THRESH_BINARY)
    threshold = 100
    canny_output = cv2.Canny(gray, threshold, threshold * 2)

    #ret, thresh= cv2.threshold(canny_output,200,255,cv2.THRESH_BINARY_INV)
    cv2.imshow("Thresold", canny_output)
    # Trouver les contours
    contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image_height = image.shape[0]  # Hauteur de l'image
    lower_third_height = 2 * image_height / 3  # Position de début des deux tiers inférieurs

    # Dessiner les contours et chercher des carrés
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        area = cv2.contourArea(cnt)
        if area > 100:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if y + h > lower_third_height: 
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
        rosa.right_wheel.speed = 0.0

        cv2.imshow('rosa', image_with_square)
        cv2.waitKey(1)
    