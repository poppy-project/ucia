import cv2 as cv
from rosa import Rosa
import time

base_speed = 0.1
turn_ratio = 0.9
THRESHOLD_DIFFERENCE = 250
following_left_edge = False
timer = time.time()

def get_line_centers(img, near_band_center_y, band_height, band_width_ratio, vmax, render=True):
    height, width, _ = img.shape
    band_width = int(width * band_width_ratio)
    x1 = (width - band_width) // 2
    x2 = x1 + band_width

    near_y1, near_y2 = (near_band_center_y - band_height // 2, near_band_center_y + band_height // 2)
    near_band = img[near_y1:near_y2, x1:x2]


    if render:
        cv.rectangle(img, (x1, near_y1), (x2, near_y2), (255, 0, 0), 2)  # Near band (blue rectangle)

    def process_band(band, offset_y):
        _, _, v = cv.split(cv.cvtColor(band, cv.COLOR_BGR2HSV))
        v[v > vmax] = 0
        contours, _ = cv.findContours(v, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return None
        contours = sorted(contours, key=cv.contourArea, reverse=True)
        cnt = contours[0]
        m = cv.moments(cnt)
        if m['m00'] > 0:
            cx, cy = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            cx, cy = cx + x1, cy + offset_y
            if render:
                cv.circle(img, (cx, cy), 10, (0, 0, 255), -1)
            return (cx, cy)
        return None

    near_center = process_band(near_band, near_y1)

    return near_center

def follow_line(rosa, near_center, base_speed=0.1, gain=0.2, img_width=1280):
    # Calculate the deviation from the center
    near_dx = (((near_center[0] / img_width)) * 2) - 1

    print(f"near_dx: {near_dx}")  # Debug


    ls = base_speed + gain * near_dx
    rs = base_speed - gain * near_dx

    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def set_speed(rosa, ls, rs):
    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def set_straight(rosa):
    set_speed(rosa, base_speed, base_speed)

def set_right(rosa):
    left_wheel_speed = base_speed * (1 - turn_ratio)
    right_wheel_speed = base_speed * (1 + turn_ratio)

    set_speed(rosa,left_wheel_speed, right_wheel_speed)

def set_left(rosa):
    left_wheel_speed = base_speed * (1 + turn_ratio)
    right_wheel_speed = base_speed * (1 - turn_ratio)
    
    set_speed(rosa,left_wheel_speed, right_wheel_speed)

def combined_follow_line(rosa, near_center, reflected):
    global following_left_edge
    global timer
    if near_center is not None:
        # Utiliser le suivi de ligne par caméra
        follow_line(rosa, near_center)
    else:
        # Utiliser le suivi de ligne par capteur
        left_sensor, right_sensor = reflected
        difference = abs(left_sensor - right_sensor)

        if difference < THRESHOLD_DIFFERENCE:
            if following_left_edge:
                set_right(rosa)
            else:
                set_left(rosa)
        else:
            set_straight(rosa)
            following_left_edge = left_sensor > right_sensor

    if time.time() - timer > 3:
        left_sensor, right_sensor = reflected
        following_left_edge = left_sensor > right_sensor
        timer = time.time()


if __name__ == '__main__':
    rosa = Rosa('rosa.local', local_robot=False)
    rosa.leds.bottom.left.color = [0, 0, 16] 
    rosa.leds.bottom.right.color = [0, 0, 16]

    while True:

        near_center  = None
        # Mise à jour des données de la caméra
        img = rosa.camera.last_frame
        
        if img is not None:
            height, width, _ = img.shape
            near_center = get_line_centers(img, near_band_center_y=height - 10, band_height=200, band_width_ratio=0.5, vmax=70, render=True)

        # Mise à jour des données des capteurs
        reflected = rosa.ground_reflected

        # Combinaison des méthodes de suivi de ligne
        combined_follow_line(rosa, near_center, reflected)

        time.sleep(0.1)
        if img is not None:
            cv.imshow('Line Following', img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()