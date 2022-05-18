import matplotlib.pyplot as plt
import cv2
import cv2.aruco
import numpy as np

from constants import *

ARUCO_DICT = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)


def find_aruco_markers(img):
    corners, ids, rejected = cv2.aruco.detectMarkers(img, ARUCO_DICT)

    top_left = None
    top_right = None
    bottom_left = None
    bottom_right = None

    for i in range(len(corners)):
        corner = corners[i]
        id = ids[i]

        corner = np.array(corner).astype(np.int32)
        centroid = np.mean(corner[0], axis=0).astype(np.int32)

        if id == 1:
            top_left = centroid
        elif id == 2:
            top_right = centroid
        elif id == 3:
            bottom_left = centroid
        elif id == 4:
            bottom_right = centroid

    if (
        top_left is None
        or top_right is None
        or bottom_left is None
        or bottom_right is None
    ):
        return None

    result = np.array((top_left, top_right, bottom_left, bottom_right)).astype(
        np.float32
    )

    return result


def apply_transform(transform, point):
    result = np.matmul(transform, [point[0], point[1], 1])
    result_normalized = result / result[2]

    return result[:2]


def calculate_position(point, aruco_positions):
    src = aruco_positions
    dst = np.array([(0, 1), (1, 1), (0, 0), (1, 0)]).astype(np.float32)
    transform_mat = cv2.getPerspectiveTransform(src, dst)

    transformed = apply_transform(transform_mat, point)

    pos = np.array((transformed[0] * BOARD_WIDTH, transformed[1] * BOARD_HEIGHT))

    return pos


if __name__ == "__main__":
    img = cv2.imread("data/img59.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    point = (1500, 1700)
    aruco_positions = find_aruco_markers(img)
    pos = calculate_position(point, aruco_positions)
    print(pos)
    plt.imshow(img)
    plt.show()
