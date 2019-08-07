import numpy as np
import cv2 
from matplotlib import pyplot as plt
import os
from binary_image import binary_image_r
from crop import generate_crop
import time
import shutil

username = 'Evirgen_Phone'

source_dir = 'Data/' + username + '/Original'
res_dir = 'Data/' + username + '/Processed'
for item in os.listdir(source_dir):
	if item !='.DS_Store':
		if item in os.listdir(res_dir):
			shutil.rmtree(res_dir+'/' + item)
		os.mkdir(res_dir+'/' + item)
		detail_dir = source_dir+'/'+item
		desig_dir = res_dir+'/'+item
		#print(os.listdir(detail_dir))
	
		for image in os.listdir(detail_dir):
			if 'jpg' in image or 'JPG' in image or 'jpeg' in image or 'JPEG' in image:
				image_crop,image_bk = generate_crop(detail_dir +'/'+ image,220)
				now = time.time()
				cv2.imwrite(desig_dir+'/'+str(now)+'.jpg',image_crop)
		print('Finished preparing for %s'%(item))

print('Done for all!!!')
