import math
import cv2
import numpy as np
import time



def equir_2_cube(img_equir, SIZE, BLOCK, EXTEND):
    HSIZE = SIZE / 2.0

    # cubemap: 6 planes
    cubemap = []
    for i in range(0, BLOCK): # 4/6

        # start = time.time()

        side_img = np.zeros((SIZE, SIZE), np.uint8) # grayscale
        img_cube = np.zeros((SIZE, SIZE, 3), np.uint8) # BGR

        it = np.nditer(side_img, flags=['multi_index'], op_flags=['readwrite']) # just for fast to traverse ndarray

        # small bloack img size**2, (e.g. 300*300=90,000times)
        while not it.finished:

            # traverse axis, e.g. (0, 0), (0, 1), ... , (0, 299), (1, 0), (1, 1), ... , (1, 299), ... , (299, 299).
            axA = it.multi_index[0] # x
            axB = it.multi_index[1] # y
            z = -axA + HSIZE # z

            # because RGB is 1 axis, we access each pixel for 3 times(RGB) & decide each plane to represent what axis (x, y, z) 
            if i == 0:
                x = HSIZE
                y = -axB + HSIZE
            elif i == 1:
                x = -HSIZE
                y = axB - HSIZE
            elif i == 2:
                x = axB - HSIZE
                y = HSIZE
            elif i == 3:
                x = -axB + HSIZE
                y = -HSIZE
            elif i == 4:
                x = axB - HSIZE
                y = axA - HSIZE
                z = HSIZE
            elif i == 5:
                x = axB - HSIZE
                y = -axA + HSIZE
                z = -HSIZE

            # conver to spherical for all pixels(x,y,z)
            r = math.sqrt(x*x + y*y + z*z)
            theta = math.acos(z / r)
            phi = -math.atan2(y, x)

            # get input img pixel
            ix = int((img_equir.shape[1] - 1) * phi / (2*np.pi)) # width
            iy = int((img_equir.shape[0] - 1) * (theta) / np.pi) # height

            b = img_equir[iy, ix, 0]
            g = img_equir[iy, ix, 1]
            r = img_equir[iy, ix, 2]

            img_cube[axA, axB, 0] = b
            img_cube[axA, axB, 1] = g
            img_cube[axA, axB, 2] = r

            it.iternext() # just for fast

        # end = time.time()
        # print('{:.2f}s'.format(end-start))

        # 6 cubemap img results, e.g. (300, 300, 3) * 6
        cubemap.append(img_cube)


    if BLOCK == 4:
        # concatenate 4 cubemap to 1 cubemap
        final_img_cube = np.zeros((SIZE, SIZE*4, 3), np.uint8) 

        final_img_cube[0:SIZE, SIZE*3:SIZE*4, :] = cubemap[0]
        final_img_cube[0:SIZE, SIZE:SIZE*2, :] = cubemap[1]
        final_img_cube[0:SIZE, SIZE*2:SIZE*3, :] = cubemap[2]
        final_img_cube[0:SIZE, 0:SIZE, :] = cubemap[3]

    elif BLOCK == 6:
        # concatenate 6 cubemap to 1 cubemap     
        final_img_cube = np.zeros((SIZE*3, SIZE*4, 3), np.uint8)
        
        final_img_cube[SIZE:SIZE*2, SIZE*3:SIZE*4, :] = cubemap[0]
        final_img_cube[SIZE:SIZE*2, SIZE:SIZE*2, :] = cubemap[1]
        final_img_cube[SIZE:SIZE*2, SIZE*2:SIZE*3, :] = cubemap[2]
        final_img_cube[SIZE:SIZE*2, 0:SIZE, :] = cubemap[3]
        final_img_cube[0:SIZE, SIZE*2:SIZE*3, :] = cubemap[4]
        final_img_cube[SIZE*2:SIZE*3, SIZE*2:SIZE*3, :] = cubemap[5]


    # extend
    final_img_cube = cv2.resize(final_img_cube, dsize=None, fx=1, fy=EXTEND, interpolation=cv2.INTER_CUBIC)


    return final_img_cube




########## image ##########
for img_ID in range(0, 3000, 30):
    # read  
    img = cv2.imread(r'./data/video2img/pano_equi_{}.jpg'.format(img_ID))

    # transform
    SIZE = 900 # 1 cubemap img size
    BLOCK = 4 # 4/6 cubemap 
    EXTEND = 1.5 # extend y axis

    img = equir_2_cube(img, SIZE, BLOCK, EXTEND)

    # write
    cv2.imwrite(r'./data/video2img_processed/pano_corr_{}.jpg'.format(img_ID), img)




########## video ##########
# read video
cap = cv2.VideoCapture(r'./data/0panorama_equirectangular.mp4')

SIZE = 300 # 4/6 cubemap img size

# write videl
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter(r'./data/2panorama_correction.mp4', fourcc, 20.0, (SIZE*4, SIZE*1))

while (cap.isOpened()):
    start = time.time()
    ret, frame = cap.read()

    # transform
    frame = equir_2_cube(frame, SIZE)
    # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('frame', int(frame.shape[1]/3), int(frame.shape[0]/3))

    # write frame
    out.write(frame)

    # show frame
    cv2.imshow('frame', frame)

    end = time.time()
    print('FPS:{:.2f}'.format(1/(end-start)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()






