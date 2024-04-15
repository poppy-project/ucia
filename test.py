import cv2
import numpy as np

def detect_star(image):
    # Charger l'image
    # image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Seuil pour convertir l'image en noir et blanc
    _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

    # Trouver les contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # Approximation du contour pour réduire le nombre de sommets
        epsilon = 0.1 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Condition basique pour une étoile: ayant un nombre spécifique de sommets
        if len(approx) == 10:  # Ce nombre peut varier selon la forme de l'étoile
            cv2.drawContours(image, [cnt], 0, (0, 255, 0), 5)

    #cv2.imshow("Star Detected", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return image

# Remplacez 'path_to_your_image' par le chemin vers votre image contenant une étoile
# detect_star('path_to_your_image')


def detect_color(image):
    # Convertir l'image de BGR à HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Plages HSV pour le rose
    rose_bas = np.array([140, 100, 100], dtype=np.uint8)
    rose_haut = np.array([170, 255, 255], dtype=np.uint8)

    # Plages HSV pour le vert foncé
    vert_fonce_bas = np.array([45, 100, 50], dtype=np.uint8)
    vert_fonce_haut = np.array([80, 255, 150], dtype=np.uint8)

    # Plages HSV pour le jaune
    jaune_bas = np.array([20, 100, 100], dtype=np.uint8)
    jaune_haut = np.array([35, 255, 255], dtype=np.uint8)

    # Rouge foncé (vous pourriez devoir ajuster ces plages)
    rouge_fonce_bas1 = np.array([0, 50, 50], dtype=np.uint8)
    rouge_fonce_haut1 = np.array([10, 255, 120], dtype=np.uint8)
    rouge_fonce_bas2 = np.array([170, 50, 50], dtype=np.uint8)
    rouge_fonce_haut2 = np.array([180, 255, 120], dtype=np.uint8)

    # Bleu
    bleu_bas = np.array([100, 50, 50], dtype=np.uint8)
    bleu_haut = np.array([140, 255, 255], dtype=np.uint8)
    
    # Créer des masques pour chaque couleur
    masque_rouge_fonce1 = cv2.inRange(hsv, rouge_fonce_bas1, rouge_fonce_haut1)
    masque_rouge_fonce2 = cv2.inRange(hsv, rouge_fonce_bas2, rouge_fonce_haut2)
    masque_bleu = cv2.inRange(hsv, bleu_bas, bleu_haut)


    masque_rose = cv2.inRange(hsv, rose_bas, rose_haut)
    masque_vert_fonce = cv2.inRange(hsv, vert_fonce_bas, vert_fonce_haut)
    masque_jaune = cv2.inRange(hsv, jaune_bas, jaune_haut)

    # Combiner les masques du rouge foncé
    masque_rouge_fonce = cv2.bitwise_or(masque_rouge_fonce1, masque_rouge_fonce2)

    masque_combiné = cv2.bitwise_or(masque_rose, masque_vert_fonce)
    masque_combiné = cv2.bitwise_or(masque_combiné, masque_jaune)
    masque_combiné = cv2.bitwise_or(masque_combiné, masque_rouge_fonce)
    masque_combiné = cv2.bitwise_or(masque_combiné, masque_bleu)

    # resultat_rose = cv2.bitwise_and(image, image, mask=masque_rose)
    # resultat_vert_fonce = cv2.bitwise_and(image, image, mask=masque_vert_fonce)
    # resultat_jaune = cv2.bitwise_and(image, image, mask=masque_jaune)
 
    resultat_final = cv2.bitwise_and(image, image, mask=masque_combiné)
    # cv2.imshow('Rose', resultat_rose)
    # cv2.imshow('Vert Foncé', resultat_vert_fonce)
    # cv2.imshow('Jaune', resultat_jaune)
    cv2.imshow('Resultat des Couleurs Détectées', resultat_final)

    return image

def detect_shape(image):
    # Charger l'image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Seuil pour convertir l'image en noir et blanc
    # _, thresh = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY) 
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    #                           cv2.THRESH_BINARY, 11, 2)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_inv = cv2.bitwise_not(gray)  # Inverser les couleurs
    # _, thresh = cv2.threshold(gray_inv, 140, 255, cv2.THRESH_BINARY)
    
    # Trouver les contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(image, contours, 0, (0, 255, 0), 5)
    cv2.imshow('Flux video gris', thresh)
    
    i = 0

    for cnt in contours:
        if i == 0:
            i = 1
            continue
        
        # Approximation du contour
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        area = cv2.contourArea(cnt)

        #print(area)

        if area > 2000 or area < 100:  # Ajustez cette valeur en fonction de la taille des objets que vous souhaitez détecter
            continue  # Ignorer les contours trop petits

        # Chercher des formes avec 6 sommets, pouvant représenter un cube en perspective
        if len(approx) >= 4:
            cv2.drawContours(image, [cnt], -1, (0, 255, 0), 5)

    return image


def capture_video():
    # Initialiser la capture vidéo
    cap = cv2.VideoCapture(0)  # 0 est généralement l'ID de la première caméra
    
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 60)

    cap.set(cv2.CAP_PROP_EXPOSURE, 0)
    cap.set(cv2.CAP_PROP_CONTRAST, 20)
    cap.set(cv2.CAP_PROP_SATURATION, 10)
    # Vérifier si la caméra a été correctement initialisée
    if not cap.isOpened():
        print("Erreur : La caméra n'a pas pu être ouverte.")
        return

    while True:
        # Capturer frame par frame
        ret, frame = cap.read()

        # Si la frame est lue correctement ret est True
        if not ret:
            print("Erreur : Impossible de lire le flux vidéo.")
            break
        frame_with_cube = detect_color(frame.copy())

        #frame_with_stars = detect_star(frame.copy())

        # Afficher le frame capturé
        #cv2.imshow('Flux video', frame_with_stars)
        
        cv2.imshow('Flux video 2', frame_with_cube)

        # Arrêter la boucle si 'q' est pressé
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libérer la capture et fermer toutes les fenêtres ouvertes
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_video()
