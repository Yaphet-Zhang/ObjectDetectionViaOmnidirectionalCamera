import numpy as np
import math
import cv2

img = cv2.imread(r'./data/1panorama_spherical.jpg')

# get center coordinates of the circular area
x0 = img.shape[0] // 2
y0 = img.shape[1] // 2
# construct the expanded image by circular area radius
unwrapped_height = radius = img.shape[0] // 2
unwrapped_width = int(2 * math.pi * radius)
unwrapped_img = np.zeros((unwrapped_height, unwrapped_width, 3), dtype="u1")

except_count = 0
for j in range(unwrapped_width):
    theta = 2 * math.pi * (j / unwrapped_width)  # 1. start position such as "+ math.pi"
    for i in range(unwrapped_height):
        unwrapped_radius = radius - i  # 2. don't forget
        x = unwrapped_radius * math.cos(theta) + x0  # 3. "sin" is clockwise but "cos" is anticlockwise
        y = unwrapped_radius * math.sin(theta) + y0
        x, y = int(x), int(y)
        try:
            unwrapped_img[i, j, :] = img[x, y, :]
        except Exception as e:
            except_count = except_count + 1

cv2.imwrite(r'./data/1panorama_equirectangular.jpg', unwrapped_img)
