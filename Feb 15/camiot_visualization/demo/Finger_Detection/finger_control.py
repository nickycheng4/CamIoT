import numpy as np
import cv2 
# from pyimagesearch import imutils
from matplotlib import pyplot as plt

from binary_image import binary_image_r

def finger_control_f(img_dir,thre, down_thr=30,left_thr=-9., right_thr=2.):
	img_o = cv2.imread(img_dir)
	img = binary_image_r(img_o,thre)
	
	#img = cv2.cvtColor(img_in.copy(),cv2.COLOR_BGR2GRAY)
	height,width = img.shape
	#print(width-9)
	all_ct_pt =[]
	slope = []


	white_areas=[]
	start_point = 8
	current_point = 8
	white_thr = 230
	black_thr = 10

	# get the white range for each line
	for pixel in range(4,width-4,4):
		#print((pixel,img[height-1,pixel]))
		if img[height-1,pixel] >white_thr:
			if img[height-1, pixel - 4] < black_thr :
				start_point = pixel
			elif img[height-1, pixel - 4] >white_thr or img[height-1, pixel + 4] > white_thr:
				current_point = pixel
			
			if pixel > width -9:
				current_point = pixel
				white_areas.append((start_point,current_point))
		elif img[height-1,pixel] == 0:
			if img[height-1, pixel - 4] >white_thr and start_point < current_point:
				white_areas.append((start_point,current_point))
	#print('White areas: ',white_areas)
	# if no white area, return the original image
	if white_areas ==[]:
		general_k = 1000
		to_crop_v = height / 2
		to_crop_h = width / 2
		control_signal = 'Down'
		return img, general_k, to_crop_v, to_crop_h, control_signal
	# find the mean point of each line
	else:
		
		max_dif = 0
		for item in white_areas:
			if item[1] - item[0] > max_dif:
				max_dif = item[1] - item[0]
				mid_point = int(np.mean(item))
		#print(max_dif)
		# if the length of the white line exceed a upper bound, the white line is not accurate. 
		# Do the while line detection from the beginning
		if max_dif > width // 3:
			
			#print('Cropping!')
			img_o = img_o[:height*80//100,:]
			img = binary_image_r(img_o,thre)
	
			#img = cv2.cvtColor(img_in.copy(),cv2.COLOR_BGR2GRAY)
			height,width = img.shape
			all_ct_pt =[]
			slope = []


			white_areas=[]
			start_point = 8
			current_point = 8
			white_thr = 230
			black_thr = 10
			for pixel in range(4,width-4,4):
				#print((pixel,img[height-1,pixel]))
				if img[height-1,pixel] > white_thr:
					if img[height-1, pixel - 4] < black_thr :
						start_point = pixel
					elif img[height-1, pixel - 4] >white_thr or img[height-1, pixel + 4] > white_thr:
						current_point = pixel
					elif pixel > width -9:
						current_point = pixel
						if current_point - start_point >12:
							white_areas.append((start_point,current_point))
				elif img[height-1,pixel] == 0:
					if img[height-1, pixel - 4] >white_thr and current_point - start_point >12:
						white_areas.append((start_point,current_point))

			
		if white_areas ==[]:
			general_k = 1000
			to_crop_v = height / 2
			to_crop_h = width / 2
			control_signal = 'Down'
			return img, general_k, to_crop_v, to_crop_h, control_signal
		else:
			cur_max = height
			choice = white_areas[0]
			for item in white_areas:
				cur_reach = height
				cur_mid = int(np.mean(item))
				for line in range(height-1,0,-4):
					if img[line,cur_mid] < black_thr:
						if line < cur_max:
							choice = item
							cur_max = line
						break

				
		mid_point = int(np.mean(choice))
		# the widest while line is set to be the bottom line
		bottom_mid = mid_point
		
		# find the top of the finger
		to_crop_v = height / 2
		to_crop_h = width / 2
		for line in range(height-1,0,-4):
			#print('Here we are')
			if img[line,mid_point] <10:
				
				if img[max(0,line-15),mid_point] <10 and img[max(0,line-30),mid_point] <10 and img[max(0,line-15),max(0,mid_point-15)] <10\
				 and img[max(0,line-15),min(width-1,mid_point+15)] <10 and img[max(0,line-30),min(mid_point+30,width-1)] <10:
					to_crop_v = line
					to_crop_h = mid_point
					to_crop_width = int(line / float(398) * 532)
					break
				else:
					continue
			# find the left and right bound of each white line
			# and find the middle point of the line
			for pixel in range(mid_point,width):
				if img[line,pixel] <10 or pixel > width-9:
					rt_most = (line,pixel)
					break
			for pixel in range(mid_point,0,-1):
				if img[line,pixel] <10 or pixel < 9:
					lf_most = (line,pixel)
					break
			#print((lf_most,rt_most))
			mid_point = int(np.mean([lf_most[1],rt_most[1]]))

			#print(lf_most[1])
			#print(rt_most[1])
			
			# record the middle point coordinates
			# also calculate the slopt from current point to the base point
			if line == height-1:
				base_pt = (line,mid_point)
				all_ct_pt.append(base_pt)
			else:
				if img[line,mid_point] > 10:
					ct_pt = (line,mid_point)
					all_ct_pt.append(ct_pt)
					if ct_pt[1] - base_pt[1] != 0:
						slope.append(float(-(ct_pt[0] - base_pt[0]))/(ct_pt[1] - base_pt[1]))
					else:
						if not slope:
							slope.append(float(-(ct_pt[0] - base_pt[0]))/1)
						
				#print(ct_pt)
			#print(base_pt)
		#print(all_ct_pt)

		# shows the middle point on the original image
		for item in all_ct_pt:
			img[item[0],item[1]] = 127
			img[item[0],item[1]+1] = 127
			img[item[0],item[1]-1] = 127
			img[item[0],item[1]+2] = 127
			img[item[0],item[1]-2] = 127

		# show the top line
		# for pix_i in range(5):
		# 	for pix_j in range(5):
		# 		img[to_crop_v-2+pix_i,to_crop_h-2+pix_j] = 127

		#print((base_pt,ct_pt))
		#print(slope)
		# the output slope is the values for the top 5 points
		general_k = np.median(slope[-5:])


		#print (slope)
		if general_k > right_thr or general_k < left_thr or np.isnan(general_k):
			direc = 'Middle'
		elif general_k < right_thr and general_k > 0:
			direc = 'Right'
		elif general_k > left_thr:
			direc = 'Left'



	# control signal classification
	control_signal = 'Down'
	# if finger doesn't show up
	if to_crop_v > height - down_thr:
		control_signal = 'Down'
	# if have finger
	else:
		control_signal = direc



		# print('General Direction of Finger is: %s with k value: %.2f' %(direc,general_k))
	return img, general_k, to_crop_v, to_crop_h, control_signal, bottom_mid


def finger_control_f1(img_dir):
	image = cv2.imread(img_dir)
	height,width,_ = image.shape
	height = int(height/2)
	# use only the lower half
	image = image[height:]
	bg = image.copy()
	bg[:,:,:] = 0
	bg2 = bg.copy()

	# sharp and edge
	kernel_sharpening = np.array([[-1,0,-1], 
                              [-1, 7,-1],
                              [-1,0,-1]])
	sharpened = cv2.filter2D(image, -1, kernel_sharpening)

	gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 11, 17, 17)
	edged = cv2.Canny(gray, 30, 200)

	# blur the background
	im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# for cnt in contours:
	#     hull = cv2.convexHull(cnt)
	#     cv2.drawContours(bg, [hull], -1, (0, 0, 255), 1) 
	cv2.drawContours(bg, contours, -1, (0,255,0), 1)
	smooth = np.ones((30, 30), np.float32) / (30*30) * 10
	bg = cv2.filter2D(bg, -1, smooth)

	# edge again
	gray2 = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray2, 127, 255, 0)
	im3, contours2, hierarchy2 = cv2.findContours(gray2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(bg2, contours2, -1, (255,255,0), 1)

	# find the lines in the background2
	# gray2 = cv2.cvtColor(bg2, cv2.COLOR_BGR2GRAY)
	# edges2 = cv2.Canny(gray2,50,255,apertureSize = 3) 
	bg3 = bg2[:,:,0]
	mid_record = []
	width_record = []
	prev_point = 0
	mid_point = 0
	mid_width = 0
	toggle = False
	# middle point at the bottom line
	h_point = height-10
	bott_mid = []
	bott_width = []
	for w_point in range(10,width-10):
		if bg3[h_point, w_point] > 0 and toggle:
			mid_point = int((prev_point + w_point)/2)
			mid_width = w_point - prev_point 
			bott_mid.append(mid_point)
			bott_width.append(mid_width)
			prev_point = w_point
			toggle = False
		elif bg3[h_point, w_point] == 0:
			toggle = True
		else:
			toggle = toggle
	bg3[h_point, bott_mid] = 255

	max_height = []
	top_mid = []
	for start_point,start_width in zip(bott_mid,bott_width):
		mid_list = [start_point]
		width_list = [start_width]
		new_mid_point = start_point
		for h_point in range(height-20,5,-5):
			# left
			left = 0
			right = 0
			for x in range(new_mid_point, np.max(new_mid_point-int(width/4),0), -1):
				if bg3[h_point, x]  > 0:
					left = x
					break
			# right
			for x in range(new_mid_point, np.max(new_mid_point+int(width/4),0), 1):
				if bg3[h_point, x]  > 0:
					right = x
					break
			mid_line = int((left+right)/2)
			width_line = right-left
			bg3[h_point, mid_line] = 255
			if np.abs(mid_line-mid_list[-1]>20) or width_line > width_list[-1]+10:
				print('break at ', h_point, mid_line,mid_list[-1])
				top_mid.append(mid_line)
				break
			else:
				mid_list.append(mid_line)
				width_list.append(width_line)
				new_mid_point = mid_line
		max_height.append(h_point)
	# bg3[max_height, bott_mid] = 255
	print(max_height)
	print(bott_mid)
	print(top_mid)
	out_index = np.argmax(max_height)
	height_out = max_height[out_index]
	bott_out = bott_mid[out_index]
	topmid_out = top_mid[out_index]
	return bg3, height_out, bott_out, topmid_out


	# height,width,_ = img_o.shape
	# img_o = img_o[int(height/2):]
	# img = cv2.cvtColor(img_o, cv2.COLOR_BGR2GRAY)
	# ret, thresh = cv2.threshold(img, 127, 255, 0)
	# im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# cv2.drawContours(img, contours, -1, (0,255,0), 3)
	# return img


if __name__ == "__main__":

	# img_bk,k,top,mid,control, bottom_mid = finger_control_f('IRBOT1crp.jpg',200, 30,-70,3)
	# print('slope is ',k,'top y value is ',top, 'mid value is ', mid)
	# print('control signal is', control)

	img_bk, height_out, bott_out, topmid_out = finger_control_f1('WALL1.jpg') 
	print('result: top ', height_out,' bottom middle ', bott_out,' top middle ' , topmid_out)
	cv2.imshow('Binary Image', img_bk)

	cv2.waitKey(0)
	# cv2.destroyAllWindows()
	# while True:
	# 	num = '36'
	# 	if num != '0':
	# 		img_bk,k,top,mid,control, bottom_mid = finger_control_f(num+'image.jpg',200, 30,-70,3)
	# 		print('slope is ',k,'top y value is ',top, 'mid value is ', mid)
	# 		print('control signal is', control)
	# 		cv2.imshow('Binary Image', img_bk)

	# 		cv2.waitKey(0)
	# 		cv2.destroyAllWindows()
	# 	else:
	# 		break