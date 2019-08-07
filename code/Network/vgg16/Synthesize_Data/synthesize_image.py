import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import numpy as np
import math
import os
import time
from extrapolate import extrapolate_flp, extrapolate_ext,extrapolate_avg
from saving_figures import save_fig
from resize import resize_img
import cv2

plt.close('all')

def generate_imgs(imgname,item):
	direc = 'Synthesized_Data/Aug/' + item +'/'
	########################################################### Original Related ###########################################################
	image_ori = mpimg.imread(imgname)
	
	print('\nFor image name %s: ' %(imgname))
	print('Image Reading Success.')
	########################################################### End Original Related ###########################################################

	shape = image_ori.shape

	x = tf.placeholder(dtype = tf.uint8, shape = shape)

	cropped1 = tf.image.central_crop(x,central_fraction = 0.8)
	cropped2 = tf.image.central_crop(x,central_fraction = 0.7)
	cropped3 = tf.image.central_crop(x,central_fraction = 0.5)
	cropped4 = tf.image.central_crop(x,central_fraction = 0.4)

	with tf.Session() as sess:
		image_2 = sess.run(cropped1,feed_dict = {x: image_ori})
		image_3 = sess.run(cropped2,feed_dict = {x: image_ori})
		image_4 = sess.run(cropped3,feed_dict = {x: image_ori})
		image_5 = sess.run(cropped4,feed_dict = {x: image_ori})

	if item.lower() == 'tv':
		image_to_process = [image_ori,image_2,image_3,image_4]
	else:
		image_to_process = [image_3, image_5,image_4]


	counter = 1
	for image in image_to_process:
		image_1 = resize_img(image)
		cv2.imwrite('0.jpg',image_1)
		image_1=cv2.imread('0.jpg',1)
		print('Synthesis starts for item %s source image %s sub-image # %d' %(item,imgname,counter))
		counter +=1 

		shape = image_1.shape
		height = shape[0]
		width  = shape[1]
		channel = shape[2]

		offset_height = 20
		offset_width  = 20
		target_height = height
		target_width = width

		x = tf.placeholder(dtype = tf.uint8, shape = shape)
		tl_1 = tf.placeholder(dtype = tf.uint8, shape = [target_height+offset_height, target_width+offset_width, channel])
		rot_angle = tf.placeholder(dtype = tf.float32, shape =())

		flip_updown = tf.image.flip_up_down(x)
		flip_leftright = tf.image.flip_left_right(x)

		'''
		rot_90 = tf.image.rot90(x, k=1)
		rot_180 = tf.image.rot90(x, k=2)
		rot_270 = tf.image.rot90(x, k=3)
		'''
		rot_any = tf.contrib.image.rotate(x,rot_angle)
		rot_any_reverse = tf.contrib.image.rotate(x,rot_angle)
		
		
		translate_dr = tf.image.pad_to_bounding_box(x, offset_height=offset_height, offset_width=offset_width, target_height=target_height+offset_height, target_width=target_width+offset_width)
		translate_dr2 = tf.image.crop_to_bounding_box(tl_1, offset_height=0, offset_width=0, target_height=target_height, target_width=target_width)
		translate_ul = tf.image.pad_to_bounding_box(x, offset_height=0, offset_width=0, target_height=target_height+offset_height, target_width=target_width+offset_width)
		translate_ul2 = tf.image.crop_to_bounding_box(tl_1, offset_height=offset_height, offset_width=offset_width, target_height=target_height, target_width=target_width)
		translate_ur = tf.image.pad_to_bounding_box(x, offset_height=0, offset_width=offset_width, target_height=target_height+offset_height, target_width=target_width+offset_width)
		translate_ur2 = tf.image.crop_to_bounding_box(tl_1, offset_height=offset_height, offset_width=0, target_height=target_height, target_width=target_width)
		translate_dl = tf.image.pad_to_bounding_box(x, offset_height=offset_height, offset_width=0, target_height=target_height+offset_height, target_width=target_width+offset_width)
		translate_dl2 = tf.image.crop_to_bounding_box(tl_1, offset_height=0, offset_width=offset_width, target_height=target_height, target_width=target_width)
		translate_up = tf.image.pad_to_bounding_box(x, offset_height=0, offset_width=0, target_height=target_height+offset_height, target_width=target_width+offset_width)
		translate_up2 = tf.image.crop_to_bounding_box(tl_1, offset_height=offset_height, offset_width=0, target_height=target_height, target_width=target_width)
		translate_dn = tf.image.pad_to_bounding_box(x, offset_height=offset_height, offset_width=0, target_height=target_height+offset_height, target_width=target_width+offset_width)
		translate_dn2 = tf.image.crop_to_bounding_box(tl_1, offset_height=0, offset_width=0, target_height=target_height, target_width=target_width)
		translate_lf = tf.image.pad_to_bounding_box(x, offset_height=0, offset_width=0, target_height=target_height+offset_height, target_width=target_width+offset_width)
		translate_lf2 = tf.image.crop_to_bounding_box(tl_1, offset_height=0, offset_width=offset_width, target_height=target_height, target_width=target_width)
		translate_rt = tf.image.pad_to_bounding_box(x, offset_height=0, offset_width=offset_width, target_height=target_height+offset_height, target_width=target_width+offset_width)
		translate_rt2 = tf.image.crop_to_bounding_box(tl_1, offset_height=0, offset_width=0, target_height=target_height, target_width=target_width)
		#print('Building Synthesis Models Completed.')
		
		with tf.Session() as sess:
		########################################################### Flips ###########################################################
			'''
			flip_2 = sess.run(flip_updown, feed_dict ={x:image_1})
			flip_3 = sess.run(flip_leftright, feed_dict ={x:image_1})
			print('Flipping Process Completed.')
			'''
		########################################################### End Flips ###########################################################

		########################################################### Rotations ###########################################################
			'''
			rot_1  = sess.run(rot_90, feed_dict = {x: image_1})
			rot_2  = sess.run(rot_180,feed_dict = {x: image_1})
			rot_9  = sess.run(rot_270,feed_dict = {x: image_1})
			'''
			'''
			rot_3  = sess.run(rot_any,feed_dict = {x: image_1, rot_angle: 0.58})
			rot_4  = sess.run(rot_any,feed_dict = {x: image_1, rot_angle: -0.58})
			rot_7  = sess.run(rot_any,feed_dict = {x: image_1, rot_angle: 0.3925})
			rot_8  = sess.run(rot_any,feed_dict = {x: image_1, rot_angle: -0.3925})
			'''
			rot_5  = sess.run(rot_any,feed_dict = {x: image_1, rot_angle: 0.261})
			rot_6  = sess.run(rot_any,feed_dict = {x: image_1, rot_angle: -0.261})
			
			
			print('Rotating Process Without Synthesizing Completed.')
			
		########################################################### End Rotations ###########################################################

			
			

		########################################################### Crop ###########################################################
			
		########################################################### End Crop ###########################################################
			
			translate_11 = sess.run(translate_dr,feed_dict = {x: image_1})
			translate_12 = sess.run(translate_dr2,feed_dict = {tl_1: translate_11})
			translate_21 = sess.run(translate_ul,feed_dict = {x: image_1})
			translate_22 = sess.run(translate_ul2,feed_dict = {tl_1: translate_21})
			translate_31 = sess.run(translate_ur,feed_dict = {x: image_1})
			translate_32 = sess.run(translate_ur2,feed_dict = {tl_1: translate_31})
			translate_41 = sess.run(translate_dl,feed_dict = {x: image_1})
			translate_42 = sess.run(translate_dl2,feed_dict = {tl_1: translate_41})
			translate_51 = sess.run(translate_up,feed_dict = {x: image_1})
			translate_52 = sess.run(translate_up2,feed_dict = {tl_1: translate_51})
			translate_61 = sess.run(translate_dn,feed_dict = {x: image_1})
			translate_62 = sess.run(translate_dn2,feed_dict = {tl_1: translate_61})
			translate_71 = sess.run(translate_lf,feed_dict = {x: image_1})
			translate_72 = sess.run(translate_lf2,feed_dict = {tl_1: translate_71})
			translate_81 = sess.run(translate_rt,feed_dict = {x: image_1})
			translate_82 = sess.run(translate_rt2,feed_dict = {tl_1: translate_81})
			print('Translation Process Without Synthesizing Completed.')


		########################################################### Translation ###########################################################


		translate_24 = extrapolate_ext(translate_22.copy(),'ul',[offset_height,offset_width])
		translate_25 = extrapolate_flp(translate_22.copy(),'ul',[offset_height,offset_width])
		'''
		translate_26 = extrapolate_ext(translate_22.copy(),'ul',[2*offset_height,2*offset_width])
		translate_27 = extrapolate_flp(translate_22.copy(),'ul',[2*offset_height,2*offset_width])
		translate_28 = extrapolate_ext(translate_22.copy(),'ul',[3*offset_height,3*offset_width])
		translate_29 = extrapolate_flp(translate_22.copy(),'ul',[3*offset_height,3*offset_width])
		'''
		#print('Data Synthesis for Upper Left Translation Completed.')

		translate_14 = extrapolate_ext(translate_12.copy(),'dr',[offset_height,offset_width])
		translate_15 = extrapolate_flp(translate_12.copy(),'dr',[offset_height,offset_width])
		'''
		translate_16 = extrapolate_ext(translate_12.copy(),'dr',[2*offset_height,2*offset_width])
		translate_17 = extrapolate_flp(translate_12.copy(),'dr',[2*offset_height,2*offset_width])
		translate_18 = extrapolate_ext(translate_12.copy(),'dr',[3*offset_height,3*offset_width])
		translate_19 = extrapolate_flp(translate_12.copy(),'dr',[3*offset_height,3*offset_width])
		'''
		#print('Data Synthesis for Lower Right Translation Completed.')

		translate_34 = extrapolate_ext(translate_32.copy(),'ur',[offset_height,offset_width])
		translate_35 = extrapolate_flp(translate_32.copy(),'ur',[offset_height,offset_width])
		'''
		translate_36 = extrapolate_ext(translate_32.copy(),'ur',[2*offset_height,2*offset_width])
		translate_37 = extrapolate_flp(translate_32.copy(),'ur',[2*offset_height,2*offset_width])
		translate_38 = extrapolate_ext(translate_32.copy(),'ur',[3*offset_height,3*offset_width])
		translate_39 = extrapolate_flp(translate_32.copy(),'ur',[3*offset_height,3*offset_width])
		'''
		#print('Data Synthesis for Upper Right Translation Completed.')



		translate_44 = extrapolate_ext(translate_42.copy(),'dl',[offset_height,offset_width])
		translate_45 = extrapolate_flp(translate_42.copy(),'dl',[offset_height,offset_width])
		'''
		translate_46 = extrapolate_ext(translate_42.copy(),'dl',[2*offset_height,2*offset_width])
		translate_47 = extrapolate_flp(translate_42.copy(),'dl',[2*offset_height,2*offset_width])
		translate_48 = extrapolate_ext(translate_42.copy(),'dl',[3*offset_height,3*offset_width])
		translate_49 = extrapolate_flp(translate_42.copy(),'dl',[3*offset_height,3*offset_width])
		'''
		#print('Data Synthesis for Lower Left Translation Completed.')
		print('Data Synthesis for Corner Translation Completed.')

		translate_54 = extrapolate_ext(translate_52.copy(),'up',[offset_height])
		translate_55 = extrapolate_flp(translate_52.copy(),'up',[offset_height])
		'''
		translate_56 = extrapolate_ext(translate_52.copy(),'up',[2*offset_height])
		translate_57 = extrapolate_flp(translate_52.copy(),'up',[2*offset_height])
		translate_58 = extrapolate_ext(translate_52.copy(),'up',[3*offset_height])
		translate_59 = extrapolate_flp(translate_52.copy(),'up',[3*offset_height])
		'''
		translate_64 = extrapolate_ext(translate_62.copy(),'dn',[offset_height])
		translate_65 = extrapolate_flp(translate_62.copy(),'dn',[offset_height])
		'''
		translate_66 = extrapolate_ext(translate_62.copy(),'dn',[2*offset_height])
		translate_67 = extrapolate_flp(translate_62.copy(),'dn',[2*offset_height])
		translate_68 = extrapolate_ext(translate_62.copy(),'dn',[3*offset_height])
		translate_69 = extrapolate_flp(translate_62.copy(),'dn',[3*offset_height])
		'''
		translate_74 = extrapolate_ext(translate_72.copy(),'lf',[offset_width])
		translate_75 = extrapolate_flp(translate_72.copy(),'lf',[offset_width])
		'''
		translate_76 = extrapolate_ext(translate_72.copy(),'lf',[2*offset_width])
		translate_77 = extrapolate_flp(translate_72.copy(),'lf',[2*offset_width])
		translate_78 = extrapolate_ext(translate_72.copy(),'lf',[3*offset_width])
		translate_79 = extrapolate_flp(translate_72.copy(),'lf',[3*offset_width])
		'''

		translate_84 = extrapolate_ext(translate_82.copy(),'rt',[offset_width])
		translate_85 = extrapolate_flp(translate_82.copy(),'rt',[offset_width])
		'''
		translate_86 = extrapolate_ext(translate_82.copy(),'rt',[2*offset_width])
		translate_87 = extrapolate_flp(translate_82.copy(),'rt',[2*offset_width])
		translate_88 = extrapolate_ext(translate_82.copy(),'rt',[3*offset_width])
		translate_89 = extrapolate_flp(translate_82.copy(),'rt',[3*offset_width])
		'''
		print('Data Synthesis for Edge Translation Completed.')
		
		'''
		translate_24 = extrapolate_avg(translate_22.copy(),'ul',[offset_height,offset_width])
		print('Data Synthesis for Image Extrapolation 25% Completed.')
		translate_14 = extrapolate_avg(translate_12.copy(),'dr',[offset_height,offset_width])
		print('Data Synthesis for Image Extrapolation 50% Completed.')
		translate_34 = extrapolate_avg(translate_32.copy(),'ur',[offset_height,offset_width])
		print('Data Synthesis for Image Extrapolation 75% Completed.')
		translate_44 = extrapolate_avg(translate_42.copy(),'dl',[offset_height,offset_width])
		print('Data Synthesis for Image Extrapolation 100% Completed.')
		'''
		########################################################### End Translation ###########################################################

		########################################################### Flip & Extend ###########################################################

		'''
		flipped_3 = extrapolate_flp(rot_3.copy(),'rot',0.58)
		extended_3 = extrapolate_ext(rot_3.copy(),'rot',0.58)
		flipped_4 = extrapolate_flp(rot_4.copy(),'rot',-0.58)
		extended_4 = extrapolate_ext(rot_4.copy(),'rot',-0.58)
		flipped_7 = extrapolate_flp(rot_7.copy(),'rot',0.3925)
		extended_7 = extrapolate_ext(rot_7.copy(),'rot',0.3925)
		flipped_8 = extrapolate_flp(rot_8.copy(),'rot',-0.3925)
		extended_8 = extrapolate_ext(rot_8.copy(),'rot',-0.3925)
		'''
		flipped_5 = extrapolate_flp(rot_5.copy(),'rot',0.261)
		extended_5 = extrapolate_ext(rot_5.copy(),'rot',0.261)
		flipped_6 = extrapolate_flp(rot_6.copy(),'rot',-0.261)
		extended_6 = extrapolate_ext(rot_6.copy(),'rot',-0.261)
		print('Data Synthesis for Rotated Images Completed.')
		
		print('Saving Data...')
		
		save_fig('Original',image_1,direc)
		'''
		save_fig('Flipped Up Down',flip_2,direc)
		save_fig('Flipped Left Right',flip_3,direc)
		save_fig('Rotate Left 90 Degrees',rot_1,direc)
		save_fig('Rotate 180 Degrees',rot_2,direc)
		save_fig('Rotate Right 90 Degrees',rot_9,direc)
		'''
		save_fig('Translation Lower Right Extending',translate_14,direc)
		save_fig('Translation Lower Right Flipping',translate_15,direc)
		save_fig('Translation Upper Left Extending',translate_24,direc)
		save_fig('Translation Upper Left Flipping',translate_25,direc)
		save_fig('Translation Upper Right Extending',translate_34,direc)
		save_fig('Translation Upper Right Flipping',translate_35,direc)
		save_fig('Translation Lower Left Extending',translate_44,direc)
		save_fig('Translation Lower Left Flipping',translate_45,direc)
		save_fig('Translation Up Extending',translate_54,direc)
		save_fig('Translation Up Flipping',translate_55,direc)
		save_fig('Translation Down Extending',translate_64,direc)
		save_fig('Translation Down Flipping',translate_65,direc)
		save_fig('Translation Left Extending',translate_74,direc)
		save_fig('Translation Left Flipping',translate_75,direc)
		save_fig('Translation Right Extending',translate_84,direc)
		save_fig('Translation Right Flipping',translate_85,direc)
		'''
		save_fig('Translation Upper Left 2x Extending',translate_26,direc)
		save_fig('Translation Upper Left 2x Flipping',translate_27,direc)
		save_fig('Translation Upper Left 3x Extending',translate_28,direc)
		save_fig('Translation Upper Left 3x Flipping',translate_29,direc)
		
		save_fig('Translation Lower Right 2x Extending',translate_16,direc)
		save_fig('Translation Lower Right 2x Flipping',translate_17,direc)
		save_fig('Translation Lower Right 3x Extending',translate_18,direc)
		save_fig('Translation Lower Right 3x Flipping',translate_19,direc)
		
		save_fig('Translation Upper Right 2x Extending',translate_36,direc)
		save_fig('Translation Upper Right 2x Flipping',translate_37,direc)
		save_fig('Translation Upper Right 3x Extending',translate_38,direc)
		save_fig('Translation Upper Right 3x Flipping',translate_39,direc)

		save_fig('Translation Lower Left 2x Extending',translate_46,direc)
		save_fig('Translation Lower Left 2x Flipping',translate_47,direc)
		save_fig('Translation Lower Left 3x Extending',translate_48,direc)
		save_fig('Translation Lower Left 3x Flipping' ,translate_49,direc)
		
		save_fig('Translation Up 2x Extending',translate_56,direc)
		save_fig('Translation Up 2x Flipping',translate_57,direc)
		save_fig('Translation Up 3x Extending',translate_58,direc)
		save_fig('Translation Up 3x Flipping',translate_59,direc)
		
		save_fig('Translation Down 2x Extending',translate_66,direc)
		save_fig('Translation Down 2x Flipping',translate_67,direc)
		save_fig('Translation Down 3x Extending',translate_68,direc)
		save_fig('Translation Down 3x Flipping',translate_69,direc)
		
		save_fig('Translation Left 2x Extending',translate_76,direc)
		save_fig('Translation Left 2x Flipping',translate_77,direc)
		save_fig('Translation Left 3x Extending',translate_78,direc)
		save_fig('Translation Left 3x Flipping',translate_79,direc)
		
		save_fig('Translation Right 2x Extending',translate_86,direc)
		save_fig('Translation Right 2x Flipping',translate_87,direc)
		save_fig('Translation Right 3x Extending',translate_88,direc)
		save_fig('Translation Right 3x Flipping',translate_89,direc)
		'''
		'''
		save_fig('Rot Left 33.25 Flipped',flipped_3,direc)
		save_fig('Rot Left 33.25 Extended',extended_3,direc)
		save_fig('Rot Right 33.25 Flipped',flipped_4,direc)
		save_fig('Rot Right 33.25 Extended',extended_4,direc)
		save_fig('Rot Left 22.5 Flipped',flipped_7,direc)
		save_fig('Rot Left 22.5 Extended',extended_7,direc)
		save_fig('Rot Right 22.5 Flipped',flipped_8,direc)
		save_fig('Rot Right 22.5 Extended',extended_8,direc)
		'''
		save_fig('Rot Left 15 Flipped',flipped_5,direc)
		save_fig('Rot Left 15 Extended',extended_5,direc)
		save_fig('Rot Right 15 Flipped',flipped_6,direc)
		save_fig('Rot Right 15 Extended',extended_6,direc)
		
		


		print('Saving Completed.\n')

		

	print('Synthesize Image for Image %s All Completed!!!\n' %(imgname))

	#plt.show()
