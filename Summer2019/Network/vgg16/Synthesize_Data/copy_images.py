import tensorflow as tf
import numpy as np
import math
import os
import time
from resize import resize_img
import cv2

def copy_image(item,source_img,copy_num):
	img_in = cv2.imread(source_img,1)
	
	for i in range(copy_num):
		current_time = time.time()
		save_dir = 'Synthesized_Data/Raw/%s/%s.jpg'%(item,current_time)
		cv2.imwrite(save_dir,img_in)
		cv2.waitKey(5)

if __name__ == "__main__":
	copy_image('AC','Image_to_Train/AC/IMG_3874.jpg',20)

