'''
1. set parameters (0, 1, ..., 18)
e.g. 
cap.set(3, 1920): set width to 1920
cap.set(4, 1080): set width to 1080

2. get parameters
cap.get(a, b)

3. encoding format
cv2.VideoWriter_fourcc(a, b, c, d)

edit code in "./utils/datasets.py"
'''

import cv2


cap = cv2.VideoCapture(cv2.CAP_DSHOW)
# cap.set(6, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(3, 1920) 
cap.set(4, 960)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out_video = cv2.VideoWriter('./data/0panorama_equirectangular.mp4', 
    cv2.VideoWriter_fourcc('m','p','4','v'), 20, (frame_width, frame_height))

while (cap.isOpened()):
    ret, frame = cap.read() # (frame.shape) 360 cam: (1920, 3840, 3), dell cam: (480, 640, 3)

    # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('frame', int(frame.shape[1]/3), int(frame.shape[0]/3))
    cv2.imshow('frame', frame)
    out_video.write(frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
out_video.release()
cv2.destroyAllWindows()

