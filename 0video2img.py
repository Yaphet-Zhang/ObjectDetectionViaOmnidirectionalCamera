import cv2


c = 0 # only read 1-frame/1-second
cap = cv2.VideoCapture(r'./data/0panorama_equirectangular.mp4')
while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', int(frame.shape[1]/3), int(frame.shape[0]/3))

    if c % 30 == 0:
        cv2.imshow('frame', frame)
        cv2.imwrite(r'./data/video2img/pano_equi_{}.jpg'.format(c), frame)
    c += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



