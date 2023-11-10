import cv2 as cv
from rosa import Rosa
import time

def nothing(x):
    pass

def get_line_centers(img, near_band_center_y, far_band_center_y, band_height, band_width_ratio, vmax, render=False):
    height, width, _ = img.shape
    band_width = int(width * band_width_ratio)
    x1 = (width - band_width) // 2
    x2 = x1 + band_width

    # Adjust the near band to be closer to the bottom of the image (closer to the robot)
    near_y1, near_y2 = (near_band_center_y - band_height // 2, near_band_center_y + band_height // 2)
    near_band = img[near_y1:near_y2, x1:x2]

    # Position the far band closer to the top of the image (closer to the 'wall')
    far_y1, far_y2 = (far_band_center_y - band_height // 2, far_band_center_y + band_height // 2)
    far_band = img[far_y1:far_y2, x1:x2]

    # Draw debugging rectangles
    if render:
        cv.rectangle(img, (x1, near_y1), (x2, near_y2), (255, 0, 0), 2)  # Near band (blue rectangle)
        cv.rectangle(img, (x1, far_y1), (x2, far_y2), (0, 255, 0), 2)    # Far band (green rectangle)

    def process_band(band, offset_y):
        _, _, v = cv.split(cv.cvtColor(band, cv.COLOR_BGR2HSV))
        v[v > vmax] = 0
        _, contours, _ = cv.findContours(v, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
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
    far_center = process_band(far_band, far_y1)

    return near_center, far_center

def follow_line(rosa, near_center, far_center, base_speed=0.1, gain=0.1, img_width=640):
    if near_center is None:
        # If no near center, stop or look around
        look_around(rosa)
        return

    # Calculate dx for near center
    near_dx = ((near_center[0] / img_width) - 0.5) * 2

    # Start with the base speed
    ls = rs = base_speed

    # If far center is detected, check alignment
    if far_center:
        far_dx = ((far_center[0] / img_width) - 0.5) * 2
        # Check if far center is aligned with near center
        if abs(far_dx - near_dx) < 0.1:
            # If aligned, maintain or increase speed
            ls += gain * near_dx
            rs -= gain * near_dx
        else:
            # If not aligned, slow down
            ls = rs = base_speed * 0.5
    else:
        # If no far center, slow down
        ls = rs = base_speed * 0.5

    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def look_around(rosa, speed=0.1):
    rosa.left_wheel.speed = speed
    rosa.right_wheel.speed = -speed

cv.namedWindow('settings')
cv.createTrackbar('Vmax', 'settings', 75, 255, nothing)

if __name__ == '__main__':
    rosa = Rosa('rosa.local', local_robot=False)

    while True:
        vmax = cv.getTrackbarPos('Vmax', 'settings')
        img = rosa.camera.last_frame
        if img is None:
            continue

        height, width, _ = img.shape  # Get the height and width from the image shape

        near_center, far_center = get_line_centers(img, near_band_center_y=height-50, far_band_center_y=height - 150, band_height=50, band_width_ratio=0.75, vmax=vmax, render=True)
        print(f"Near Center: {near_center}, Far Center: {far_center}")

        follow_line(rosa, near_center, far_center)

        time.sleep(0.16)
        # rosa.left_wheel.speed = 0
        # rosa.right_wheel.speed = 0

        cv.imshow('Line Following', img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()
