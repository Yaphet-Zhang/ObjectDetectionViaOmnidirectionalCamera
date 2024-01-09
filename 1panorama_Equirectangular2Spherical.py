import math
import cv2
import numpy as np




def equir_2_spher(img):
    '''
    (panorama) equirectangure to spherical
    '''
    rows,cols,c = img.shape
    R = np.int(cols/2/math.pi)
    D = R*2
    cx = R
    cy = R
    # print(rows,cols,c,R,D,cx,cy)
    new_img = np.zeros((D,D,c),dtype = np.uint8) 
    for i in range(D):
        for j in range(D):
            r = math.sqrt((i-cx)**2+(j-cy)**2)
            if r > R:
                continue
            tan_inv = np.arctan((j-cy)/(i-cx+1e-10))
            if(i<cx):
                theta = math.pi/2+tan_inv
            else:
                theta = math.pi*3/2+tan_inv  
            xp = np.int(np.floor(theta/2/math.pi*cols))
            yp = np.int(np.floor(r/R*rows))
            new_img[j,i] = img[rows-yp-1,xp]

    return new_img




img = cv2.imread(r'./data/1panorama_equirectangular.jpg')
img = equir_2_spher(img)

cv2.imwrite(r'./data/1panorama_spherical.jpg', img)
