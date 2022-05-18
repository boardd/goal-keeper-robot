import matplotlib.pyplot as plt
import numpy as np
import cv2

from constants import *


def find_ball(img, display=False):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    thresholded = cv2.adaptiveThreshold(
        img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 30
    )

    if display:
        plt.imshow(thresholded, cmap=plt.gray())
        plt.pause(0.5)
        # plt.show()

    contours, hierarchies = cv2.findContours(
        thresholded, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE
    )
    hierarchies = hierarchies[0]

    # Sort contours in dereasing order by area and pick the top 1000
    indices = sorted(
        range(len(contours)), key=lambda i: cv2.contourArea(contours[i]), reverse=True
    )[:100]

    centers = []

    for index in indices:
        contour = contours[index]

        area = cv2.contourArea(contour)
        if area > AREA_MAX:
            continue
        if area < AREA_MIN:
            break

        rect = cv2.boundingRect(contour)
        x, y, width, height = rect
        if width == 0 or height == 0:
            continue

        how_error = abs(EXPECTED_HEIGHT_OVER_WIDTH - (height / width))
        if how_error > MAX_HEIGHT_OVER_WIDTH_ERROR:
            continue

        if display:
            cv2.rectangle(
                img, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=3
            )

        moments = cv2.moments(contour)
        if moments["m00"] == 0:
            continue
        cX = int(moments["m10"] / moments["m00"])
        cY = int(moments["m01"] / moments["m00"])

        center = (cX, cY)

        centers.append(center)

    return np.array(centers)


def main(img, pause):
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img[:, 45:-20]

    centers = find_ball(img, display=True)
    print(centers)
    plt.figure(2)
    plt.clf()
    plt.imshow(img)
    if pause:
        plt.pause(0.5)
    else:
        plt.show()


if __name__ == "__main__":
    # vc = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
    # ret, frame = vc.read()
    # main(frame, False)

    for i in range(30, 65):
        img = cv2.imread(f"data/img{i}.png")
        main(img, True)
