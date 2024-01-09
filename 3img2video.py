import cv2
import os 


# root 
# dir_path = r'./data/video2img/' # original
dir_path = r'./data/video2img_processed/' # processed

# read 1 image for check size
file_paths = os.listdir(dir_path)
# img = cv2.imread(dir_path + 'pano_equi_0.jpg') # original
img = cv2.imread(dir_path + 'pano_corr_0.jpg') # processed
size = img.shape[1], img.shape[0]

# write video
videoWrite = cv2.VideoWriter(dir_path + 'pano_equi.mp4', -1, 5, size) # file name, encoder, frame, size
for file_path in file_paths:
    if file_path[-8:] == 'resu.jpg':
        img = cv2.imread(dir_path + file_path)
    videoWrite.write(img)
videoWrite.release()