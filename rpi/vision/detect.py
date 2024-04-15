import cv2
import numpy as np

def detect_object(frame):
    # Hauteur et largeur de l'image
    height, width = frame.shape[:2]

    # Couper l'image pour ne garder que la moitié inférieure
    #cropped_frame = frame[height//2:height, 0:width]
    cropped_frame = frame[height//2:height, 0:width]
    # Convertir l'image en nuances de gris
    gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
    # Appliquer un flou pour réduire le bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Détecter les contours avec Canny
    edged = cv2.Canny(blurred, 30, 150)
    # Trouver les contours dans l'image binarisée
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objects_detected = []
    output_frame = frame.copy()

    for contour in contours:
        
        area = cv2.contourArea(contour)
        if area > 1500 or area < 150:  # Seuil de taille à ajuster
            continue

        # Approximer les contours pour simplifier les formes
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        
        # Déterminer la forme en fonction du nombre de points dans l'approximation
        if len(approx) > 4 or len(approx) < 5:  # Supposons que le cube ait une forme quadrilatérale
            object_type = 'cube'
            x, y, w, h = cv2.boundingRect(contour)
            y += height // 2
            
            if w - h > 20:
                continue
            center = (int(x), int(y))
            objects_detected.append({
                        'label': object_type,
                        'center': center,
                        'confidence': 1
            })            
            cv2.rectangle(output_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(output_frame, object_type, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        elif len(approx) > 5 or len(approx) < 8:  # Supposons que le cube ait une forme quadrilatérale
            object_type = 'star'
        
            x, y, w, h = cv2.boundingRect(contour)
            y += height // 2
                
            #objects_detected.append((object_type, x, y, w, h))
            cv2.rectangle(output_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(output_frame, object_type, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        elif len(approx) > 10:  # Une forme ronde pour la balle
            object_type = 'ball'
            (x, y), radius = cv2.minEnclosingCircle(contour)
            y += height // 2
            center = (int(x), int(y))
            radius = int(radius)
            if radius > 10:
                #objects_detected.append((object_type, center[0], center[1], radius))
                cv2.circle(output_frame, center, radius, (255, 0, 0), 2)
                cv2.putText(output_frame, object_type, (center[0] - radius, center[1] - radius - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        # Vous pouvez ajouter d'autres formes ici selon le besoin

    return objects_detected, output_frame

# Utilisation:
# input_frame = cv2.imread('chemin_vers_votre_image.jpg')
# detected_objects, modified_frame = detect_object(input_frame)
