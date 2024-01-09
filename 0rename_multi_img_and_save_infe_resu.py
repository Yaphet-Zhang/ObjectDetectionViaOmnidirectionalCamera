
import os
import string
from unittest import result


dir_path_ = r'./data/video2img_processed'

for item in os.listdir(dir_path_):
    os.rename(
        os.path.join(dir_path_, item), 
        os.path.join(dir_path_, (item[:-4] + '_resu.jpg'))
    )


##### read #####
# dir_path = r'./data/video2img/results'
dir_path = r'./data/video2img_processed/results'

vehicle = 0
person = 0
light_red = 0
sign_person = 0
motorcycle = 0
bicycle = 0
sign_cross = 0
sign_single_lane = 0
light_green = 0
sign_no_cross = 0


for item in os.listdir(dir_path):
    file_path = os.path.join(dir_path, item)

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == '0':
                vehicle += 1
            elif line[0] == '1':
                person += 1
            elif line[0] == '2':
                light_red += 1
            elif line[0] == '3':
                sign_person += 1
            elif line[0] == '4':
                motorcycle += 1    
            elif line[0] == '5':
                bicycle += 1  
            elif line[0] == '6':
                sign_cross += 1
            elif line[0] == '7':
                sign_single_lane += 1
            elif line[0] == '8':
                light_green += 1
            elif line[0] == '9':
                sign_no_cross += 1
                              


##### write #####
result_path = r'./data/video2img_processed/results/results.txt'

with open(result_path, 'w') as f:
    f.write('vehicle:'+str(vehicle)+'\n')
    f.write('person:'+str(person)+'\n')
    f.write('light_red:'+str(light_red)+'\n')
    f.write('sign_person:'+str(sign_person)+'\n')
    f.write('motorcycle:'+str(motorcycle)+'\n')
    f.write('bicycle:'+str(bicycle)+'\n')
    f.write('sign_cross:'+str(sign_cross)+'\n')
    f.write('sign_single_lane:'+str(sign_single_lane)+'\n')
    f.write('light_green:'+str(light_green)+'\n')
    f.write('sign_no_cross:'+str(sign_no_cross)+'\n')


    
