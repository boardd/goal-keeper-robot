import time
import cv2

SAVE = True

vc = cv2.VideoCapture(1 + cv2.CAP_DSHOW)

next_time = time.perf_counter()
img_i = 0

while(vc.isOpened()):
    prev = time.perf_counter()
    # Capture frame-by-frame
    ret, frame = vc.read()
    if ret == True:
        print(frame.shape)
        # Display the resulting frame
        cv2.imshow('Frame',frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        if SAVE:
            if time.perf_counter() >= next_time:
                cv2.imwrite(f"data/img{img_i}.png", frame)
                img_i += 1
                next_time += 0.1

        curr = time.perf_counter()
        print(1/(curr - prev))
        prev = curr

    # Break the loop
    else: 
        break