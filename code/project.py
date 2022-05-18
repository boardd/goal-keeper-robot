from dataclasses import dataclass
import numpy as np
import serial
import time
import cv2

from aruco import calculate_position, apply_transform, find_aruco_markers
from threshold import find_ball
from constants import *

vc = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
arduino = serial.Serial(port="COM3", baudrate=1000000, timeout=0.1)


def send_angle(angle):
    arduino.write(bytes(str(angle) + "\n", "utf-8"))


@dataclass
class Rectangle:
    bottom: float
    left: float
    top: float
    right: float


def in_rectangle(point, rect: Rectangle):
    x, y = point
    if x < rect.left:
        return False
    if x > rect.right:
        return False
    if y < rect.bottom:
        return False
    if y > rect.top:
        return False
    return True


BOUNDS_RECT = Rectangle(
    -BOARD_MARGIN,
    -BOARD_MARGIN,
    BOARD_HEIGHT + BOARD_MARGIN,
    BOARD_WIDTH + BOARD_MARGIN,
)


class GoalKeeper:
    def wait_ready(self):
        # Wait until Arduino is ready
        while True:
            data = arduino.readline()
            if b"READY" in data:
                break
            time.sleep(0.1)

    def preprocess(self, img):
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Crop the image using ArUco markers as guide
        crop_aruco_positions = find_aruco_markers(img)
        if crop_aruco_positions is None:
            return None
        crop_aruco_positions = crop_aruco_positions.astype(np.int32)

        _, top_right, bottom_left, _ = crop_aruco_positions
        left, bottom = bottom_left
        right, top = top_right
        width = right - left
        height = bottom - top

        CROP_MARGIN = 50
        img = img[
            top - CROP_MARGIN : top + height + CROP_MARGIN,
            left - CROP_MARGIN : left + width + CROP_MARGIN,
        ]

        return img

    def find_ball_position(self, preprocessed, aruco_positions):
        # Find candidate ball centers
        candidate_centers = find_ball(preprocessed)

        # Compute board space coordinates
        candidate_positions = []
        for center in candidate_centers:
            position = calculate_position(center, aruco_positions)
            candidate_positions.append(position)

        # Filter positions
        filtered_positions = []
        filtered_centers = []
        for center, position in zip(candidate_centers, candidate_positions):
            # Discard points outside of play region
            if not in_rectangle(position, BOUNDS_RECT):
                continue

            # Discard points close to an aruco marker
            bad = False
            for aruco_position in aruco_positions:
                if np.linalg.norm(center - aruco_position) < 50:
                    bad = True
                    break
            if bad:
                continue

            filtered_positions.append(position)
            filtered_centers.append(center)

        # If we do not have a single ball position, wait until the next frame
        if len(filtered_positions) > 1:
            print("Multiple balls detected:", filtered_positions)
            return None, None
        if len(filtered_positions) != 1:
            return None, None

        return filtered_centers[0], filtered_positions[0]

    def estimate_end_position(self, position_history):
        GOAL_Y = BOARD_HEIGHT + ARUCO_MARKER_SIZE / 2

        target_x = None
        if len(position_history) == 1:
            # Just use the x coordinate of the current position
            position = position_history[0]
            target_x = position[0]
        else:
            # Estimate the trajectory of the ball
            n = len(position_history) - 1
            target_x = 0
            for i in range(n):
                start = position_history[i]
                end = position_history[i + 1]
                velocity = end - start

                # Estimate when the ball will reach the goal's y coordinate
                y_velocity = velocity[1]
                y_distance = GOAL_Y - end[1]
                y_time = y_distance / y_velocity

                # Special case: the ball is moving backwards or is stationary
                # Just use the ball's x coordinate in this case
                if y_velocity < 1e-3:
                    target_x += end[0]
                    continue

                # Estimate the x coordinate at that time
                estimated_x = end[0] + velocity[0] * y_time

                # Accumulate the average
                target_x += estimated_x
            target_x = target_x / n

        return np.array((target_x, GOAL_Y))

    def compute_arm_angle(self, estimated_end_position):
        # Compute arm angle to target x coordinate
        x, y = estimated_end_position
        board_center = BOARD_WIDTH / 2
        distance_from_center = x - board_center
        ANGLE_COMPENSATION = 1.25
        angle = -ANGLE_COMPENSATION * np.arctan2(distance_from_center, ARM_HEIGHT)
        return angle

    def main(self):
        self.wait_ready()

        # Continually read and process frames
        position_history = []
        while vc.isOpened():
            ret, frame = vc.read()
            if not ret:
                break

            # Preprocess the image
            preprocessed = self.preprocess(frame)
            if preprocessed is None:
                print("Aruco markers are not visible!")
                continue

            # Find the ball's position
            aruco_positions = find_aruco_markers(preprocessed)
            if aruco_positions is None:
                print("Aruco markers are not visible!")
                continue
            center, position = self.find_ball_position(preprocessed, aruco_positions)

            # Set the arm angle
            if center is None:
                # Ball not found
                position_history = []
                send_angle(0)
            else:
                position_history.append(position)
                position_history = position_history[
                    -5:
                ]  # Keep track of the last 5 positions

                estimated_end_position = self.estimate_end_position(position_history)
                angle = self.compute_arm_angle(estimated_end_position)

                # Send the angle to the arduino
                print(f"Sending angle: {angle}")
                send_angle(angle)

            # --- Display the frame ---
            display = preprocessed

            # Draw the ArUco marker locations on the image
            for position in aruco_positions:
                x, y = position
                corner0 = np.array((x - 10, y - 10)).astype(np.int32)
                corner1 = np.array((x + 10, y + 10)).astype(np.int32)
                display = cv2.rectangle(
                    display, corner0, corner1, color=(255, 0, 0), thickness=3
                )

            if center is not None:
                # Draw the ball's position on the image
                x, y = center
                corner0 = np.array((x - 10, y - 10)).astype(np.int32)
                corner1 = np.array((x + 10, y + 10)).astype(np.int32)
                display = cv2.rectangle(
                    display, corner0, corner1, color=(0, 255, 0), thickness=3
                )

                # Draw the estimated trajectory
                trajectory_points = position_history + [estimated_end_position]
                for i in range(len(trajectory_points) - 1):
                    start = trajectory_points[i]
                    end = trajectory_points[i + 1]

                    start = np.array((start[0] / BOARD_WIDTH, start[1] / BOARD_HEIGHT))
                    end = np.array((end[0] / BOARD_WIDTH, end[1] / BOARD_HEIGHT))

                    src = np.array([(0, 1), (1, 1), (0, 0), (1, 0)]).astype(np.float32)
                    dst = aruco_positions
                    transform_mat = cv2.getPerspectiveTransform(src, dst)

                    start_point = apply_transform(transform_mat, start).astype(np.int32)
                    end_point = apply_transform(transform_mat, end).astype(np.int32)

                    display = cv2.line(
                        display,
                        start_point,
                        end_point,
                        color=(255, 255, 0),
                        thickness=3,
                    )

            display = cv2.cvtColor(display, cv2.COLOR_RGB2BGR)
            cv2.imshow("Board", display)
            cv2.waitKey(1)


if __name__ == "__main__":
    gc = GoalKeeper()
    gc.main()
