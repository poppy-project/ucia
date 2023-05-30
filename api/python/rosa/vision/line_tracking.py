import cv2 as cv


def get_line_center(img,
                    band_center_y=325,
                    band_height=50, band_width_ratio=0.75,
                    vmax=75,
                    render=False):

    y1, y2 = (band_center_y - band_height // 2,
              band_center_y + band_height // 2)

    height, width, _ = img.shape
    band_width = int(width * band_width_ratio)
    x1 = (width - band_width) // 2
    x2 = width - x1

    band = img[y1:y2, x1:x2]

    _, _, v = cv.split(cv.cvtColor(band, cv.COLOR_BGR2HSV))
    v[v > vmax] = 0

    _, contours, _ = cv.findContours(v, 1, 2)
    if len(contours) == 0:
        return None

    contours = sorted(contours, key=cv.contourArea, reverse=True)
    cnt = contours[0]

    m = cv.moments(cnt)
    if m['m00'] > 0:
        x, y = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
        x, y = x + x1, y + y1

        if render:
            cv.circle(img, (x, y), 10, (0, 0, 255), -1)

        return (x, y)

    return None
