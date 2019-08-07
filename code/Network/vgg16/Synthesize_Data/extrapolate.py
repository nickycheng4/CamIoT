import tensorflow as tf
import numpy as np
from math_calc import calc_dim
from math import *
from math_calc import calc_dim

def extrapolate_avg(img,pos,fillsize):
	img_1 = img[:]
	vertical_size = fillsize[0]
	horizontal_size = fillsize[1]
	shape_o=img.shape
	height = shape_o[0]
	width = shape_o[1]
	channel = shape_o[2]
	smooth_size = 10
	#print(height)
	#print(width)
	if pos == 'ul':
		#print('it is in ul')
		start_v = height-vertical_size
		start_h = width-horizontal_size

		for line in range(start_v,height):
			#print('-',line)
			for pixel in range(start_h):
				#print(pixel)
				k = float(pixel+1)/(line+1)
				pixel_clr = [0,0,0]
				total_weight = 0
				for num in range(line):
					hrzt_grid = int(round(k*num))
					#print((num,hrzt_grid))
					pixel_clr[0] += img[num,hrzt_grid][0] * num
					pixel_clr[1] += img[num,hrzt_grid][1] * num
					pixel_clr[2] += img[num,hrzt_grid][2] * num
					total_weight += num
				img_1[line,pixel][0] = int(float(pixel_clr[0])/total_weight)
				img_1[line,pixel][1] = int(float(pixel_clr[1])/total_weight)
				img_1[line,pixel][2] = int(float(pixel_clr[2])/total_weight)
				#print((line,pixel,img_1[line,pixel]))
		for line in range(start_v - smooth_size,start_v + smooth_size):
			for pixel in range(start_h):
				img_1[line,pixel][0] = int(np.mean([img_1[line-1,pixel][0],img_1[line+1,pixel][0],img_1[line-2,pixel][0],img_1[line+2,pixel][0]]))
				img_1[line,pixel][1] = int(np.mean([img_1[line-1,pixel][1],img_1[line+1,pixel][1],img_1[line-2,pixel][1],img_1[line+2,pixel][1]]))
				img_1[line,pixel][2] = int(np.mean([img_1[line-1,pixel][2],img_1[line+1,pixel][2],img_1[line-2,pixel][2],img_1[line+2,pixel][2]]))

		#print('Vertical extrapolation finished!')
		for line in range(0,height):
			#print('-',line)
			for pixel in range(start_h,width):
				#print(pixel)
				k = float(line+1)/(pixel+1)
				pixel_clr = [0,0,0]
				total_weight = 0
				for num in range(pixel):
					vtl_grid = int(round(k*num))
					#print((num,hrzt_grid))
					pixel_clr[0] += img[vtl_grid,num][0] * num
					pixel_clr[1] += img[vtl_grid,num][1] * num
					pixel_clr[2] += img[vtl_grid,num][2] * num
					total_weight += num
				img_1[line,pixel][0] = int(float(pixel_clr[0])/total_weight)
				img_1[line,pixel][1] = int(float(pixel_clr[1])/total_weight)
				img_1[line,pixel][2] = int(float(pixel_clr[2])/total_weight)

		for pixel in range(start_h - smooth_size,start_h + smooth_size):
			for line in range(height):
				img_1[line,pixel][0] = int(np.mean([img_1[line,pixel-1][0],img_1[line,pixel+1][0],img_1[line,pixel-2][0],img_1[line,pixel+2][0]]))
				img_1[line,pixel][1] = int(np.mean([img_1[line,pixel-1][1],img_1[line,pixel+1][1],img_1[line,pixel-2][1],img_1[line,pixel+2][1]]))
				img_1[line,pixel][2] = int(np.mean([img_1[line,pixel-1][2],img_1[line,pixel+1][2],img_1[line,pixel-2][2],img_1[line,pixel+2][2]]))
				#print((line,pixel,img_1[line,pixel]))
				#print(img[line][pixel])
		#print('Horizontal extrapolation finished!')

	elif pos == 'ur':
		img_1 = img[:]
		img_1 = np.fliplr(img_1)
		#print('it is in ul')
		start_v = height-vertical_size
		start_h = width-horizontal_size

		for line in range(start_v,height):
			#print('-',line)
			for pixel in range(start_h):
				#print(pixel)
				k = float(pixel+1)/(line+1)
				pixel_clr = [0,0,0]
				total_weight = 0
				for num in range(line):
					hrzt_grid = int(round(k*num))
					#print((num,hrzt_grid))
					pixel_clr[0] += img[num,hrzt_grid][0] * num
					pixel_clr[1] += img[num,hrzt_grid][1] * num
					pixel_clr[2] += img[num,hrzt_grid][2] * num
					total_weight += num
				img_1[line,pixel][0] = int(float(pixel_clr[0])/total_weight)
				img_1[line,pixel][1] = int(float(pixel_clr[1])/total_weight)
				img_1[line,pixel][2] = int(float(pixel_clr[2])/total_weight)
				#print((line,pixel,img_1[line,pixel]))
		for line in range(start_v - smooth_size,start_v + smooth_size):
			for pixel in range(start_h):
				img_1[line,pixel][0] = int(np.mean([img_1[line-1,pixel][0],img_1[line+1,pixel][0],img_1[line-2,pixel][0],img_1[line+2,pixel][0]]))
				img_1[line,pixel][1] = int(np.mean([img_1[line-1,pixel][1],img_1[line+1,pixel][1],img_1[line-2,pixel][1],img_1[line+2,pixel][1]]))
				img_1[line,pixel][2] = int(np.mean([img_1[line-1,pixel][2],img_1[line+1,pixel][2],img_1[line-2,pixel][2],img_1[line+2,pixel][2]]))

		print('Vertical extrapolation finished!')
		for line in range(0,height):
			#print('-',line)
			for pixel in range(start_h,width):
				#print(pixel)
				k = float(line+1)/(pixel+1)
				pixel_clr = [0,0,0]
				total_weight = 0
				for num in range(pixel):
					vtl_grid = int(round(k*num))
					#print((num,hrzt_grid))
					pixel_clr[0] += img[vtl_grid,num][0] * num
					pixel_clr[1] += img[vtl_grid,num][1] * num
					pixel_clr[2] += img[vtl_grid,num][2] * num
					total_weight += num
				img_1[line,pixel][0] = int(float(pixel_clr[0])/total_weight)
				img_1[line,pixel][1] = int(float(pixel_clr[1])/total_weight)
				img_1[line,pixel][2] = int(float(pixel_clr[2])/total_weight)

		for pixel in range(start_h - smooth_size,start_h + smooth_size):
			for line in range(height):
				img_1[line,pixel][0] = int(np.mean([img_1[line,pixel-1][0],img_1[line,pixel+1][0],img_1[line,pixel-2][0],img_1[line,pixel+2][0]]))
				img_1[line,pixel][1] = int(np.mean([img_1[line,pixel-1][1],img_1[line,pixel+1][1],img_1[line,pixel-2][1],img_1[line,pixel+2][1]]))
				img_1[line,pixel][2] = int(np.mean([img_1[line,pixel-1][2],img_1[line,pixel+1][2],img_1[line,pixel-2][2],img_1[line,pixel+2][2]]))
				#print((line,pixel,img_1[line,pixel]))
				#print(img[line][pixel])
		print('Horizontal extrapolation finished!')
		img_1 = np.fliplr(img_1)

	elif pos == 'dl':
		img_1 = img[:]
		img_1 = np.flipud(img_1)
		#print('it is in ul')
		start_v = height-vertical_size
		start_h = width-horizontal_size

		for line in range(start_v,height):
			#print('-',line)
			for pixel in range(start_h):
				#print(pixel)
				k = float(pixel+1)/(line+1)
				pixel_clr = [0,0,0]
				total_weight = 0
				for num in range(line):
					hrzt_grid = int(round(k*num))
					#print((num,hrzt_grid))
					pixel_clr[0] += img[num,hrzt_grid][0] * num
					pixel_clr[1] += img[num,hrzt_grid][1] * num
					pixel_clr[2] += img[num,hrzt_grid][2] * num
					total_weight += num
				img_1[line,pixel][0] = int(float(pixel_clr[0])/total_weight)
				img_1[line,pixel][1] = int(float(pixel_clr[1])/total_weight)
				img_1[line,pixel][2] = int(float(pixel_clr[2])/total_weight)
				#print((line,pixel,img_1[line,pixel]))
		for line in range(start_v - smooth_size,start_v + smooth_size):
			for pixel in range(start_h):
				img_1[line,pixel][0] = int(np.mean([img_1[line-1,pixel][0],img_1[line+1,pixel][0],img_1[line-2,pixel][0],img_1[line+2,pixel][0]]))
				img_1[line,pixel][1] = int(np.mean([img_1[line-1,pixel][1],img_1[line+1,pixel][1],img_1[line-2,pixel][1],img_1[line+2,pixel][1]]))
				img_1[line,pixel][2] = int(np.mean([img_1[line-1,pixel][2],img_1[line+1,pixel][2],img_1[line-2,pixel][2],img_1[line+2,pixel][2]]))

		print('Vertical extrapolation finished!')
		for line in range(0,height):
			#print('-',line)
			for pixel in range(start_h,width):
				#print(pixel)
				k = float(line+1)/(pixel+1)
				pixel_clr = [0,0,0]
				total_weight = 0
				for num in range(pixel):
					vtl_grid = int(round(k*num))
					#print((num,hrzt_grid))
					pixel_clr[0] += img[vtl_grid,num][0] * num
					pixel_clr[1] += img[vtl_grid,num][1] * num
					pixel_clr[2] += img[vtl_grid,num][2] * num
					total_weight += num
				img_1[line,pixel][0] = int(float(pixel_clr[0])/total_weight)
				img_1[line,pixel][1] = int(float(pixel_clr[1])/total_weight)
				img_1[line,pixel][2] = int(float(pixel_clr[2])/total_weight)

		for pixel in range(start_h - smooth_size,start_h + smooth_size):
			for line in range(height):
				img_1[line,pixel][0] = int(np.mean([img_1[line,pixel-1][0],img_1[line,pixel+1][0],img_1[line,pixel-2][0],img_1[line,pixel+2][0]]))
				img_1[line,pixel][1] = int(np.mean([img_1[line,pixel-1][1],img_1[line,pixel+1][1],img_1[line,pixel-2][1],img_1[line,pixel+2][1]]))
				img_1[line,pixel][2] = int(np.mean([img_1[line,pixel-1][2],img_1[line,pixel+1][2],img_1[line,pixel-2][2],img_1[line,pixel+2][2]]))
				#print((line,pixel,img_1[line,pixel]))
				#print(img[line][pixel])
		print('Horizontal extrapolation finished!')
		img_1 = np.flipud(img_1)

	elif pos == 'dr':
		img_1 = img[:]
		img_1 = np.fliplr(img_1)
		img_1 = np.flipud(img_1)
		#print('it is in ul')
		start_v = height-vertical_size
		start_h = width-horizontal_size

		for line in range(start_v,height):
			#print('-',line)
			for pixel in range(start_h):
				#print(pixel)
				k = float(pixel+1)/(line+1)
				pixel_clr = [0,0,0]
				total_weight = 0
				for num in range(line):
					hrzt_grid = int(round(k*num))
					#print((num,hrzt_grid))
					pixel_clr[0] += img[num,hrzt_grid][0] * num
					pixel_clr[1] += img[num,hrzt_grid][1] * num
					pixel_clr[2] += img[num,hrzt_grid][2] * num
					total_weight += num
				img_1[line,pixel][0] = int(float(pixel_clr[0])/total_weight)
				img_1[line,pixel][1] = int(float(pixel_clr[1])/total_weight)
				img_1[line,pixel][2] = int(float(pixel_clr[2])/total_weight)
				#print((line,pixel,img_1[line,pixel]))
		for line in range(start_v - smooth_size,start_v + smooth_size):
			for pixel in range(start_h):
				img_1[line,pixel][0] = int(np.mean([img_1[line-1,pixel][0],img_1[line+1,pixel][0],img_1[line-2,pixel][0],img_1[line+2,pixel][0]]))
				img_1[line,pixel][1] = int(np.mean([img_1[line-1,pixel][1],img_1[line+1,pixel][1],img_1[line-2,pixel][1],img_1[line+2,pixel][1]]))
				img_1[line,pixel][2] = int(np.mean([img_1[line-1,pixel][2],img_1[line+1,pixel][2],img_1[line-2,pixel][2],img_1[line+2,pixel][2]]))

		print('Vertical extrapolation finished!')
		for line in range(0,height):
			#print('-',line)
			for pixel in range(start_h,width):
				#print(pixel)
				k = float(line+1)/(pixel+1)
				pixel_clr = [0,0,0]
				total_weight = 0
				for num in range(pixel):
					vtl_grid = int(round(k*num))
					#print((num,hrzt_grid))
					pixel_clr[0] += img[vtl_grid,num][0] * num
					pixel_clr[1] += img[vtl_grid,num][1] * num
					pixel_clr[2] += img[vtl_grid,num][2] * num
					total_weight += num
				img_1[line,pixel][0] = int(float(pixel_clr[0])/total_weight)
				img_1[line,pixel][1] = int(float(pixel_clr[1])/total_weight)
				img_1[line,pixel][2] = int(float(pixel_clr[2])/total_weight)

		for pixel in range(start_h - smooth_size,start_h + smooth_size):
			for line in range(height):
				img_1[line,pixel][0] = int(np.mean([img_1[line,pixel-1][0],img_1[line,pixel+1][0],img_1[line,pixel-2][0],img_1[line,pixel+2][0]]))
				img_1[line,pixel][1] = int(np.mean([img_1[line,pixel-1][1],img_1[line,pixel+1][1],img_1[line,pixel-2][1],img_1[line,pixel+2][1]]))
				img_1[line,pixel][2] = int(np.mean([img_1[line,pixel-1][2],img_1[line,pixel+1][2],img_1[line,pixel-2][2],img_1[line,pixel+2][2]]))
				#print((line,pixel,img_1[line,pixel]))
				#print(img[line][pixel])
		print('Horizontal extrapolation finished!')
		img_1 = np.flipud(img_1)
		img_1 = np.fliplr(img_1)


	return img_1



def extrapolate_ext(img,pos,fillsize):
	img_1 = img.copy()
	buffer_size=2
	shape_o=img.shape
	height = shape_o[0]
	width = shape_o[1]
	channel = shape_o[2]
	easy_trans = ['up','dn','lf','rt']
	if pos !='rot' and pos not in easy_trans:
		vertical_size = fillsize[0]
		horizontal_size = fillsize[1]
		
		if pos =='ur':
			img_1 = np.fliplr(img_1)
		elif pos =='dl':
			
			img_1 = np.flipud(img_1)
		elif pos =='dr':
			
			img_1 = np.flipud(img_1)
			img_1 = np.fliplr(img_1)
		start_v = height-vertical_size
		start_h = width-horizontal_size

		for line in range(start_v,height):
			for pixel in range(start_h+1):
				img_1[line,pixel][0] = img_1[start_v-1,pixel][0]
				img_1[line,pixel][1] = img_1[start_v-1,pixel][1]
				img_1[line,pixel][2] = img_1[start_v-1,pixel][2]

		for line in range(start_v+1):
			for pixel in range(start_h,width):
				img_1[line,pixel][0] = img_1[line,start_h-1][0]
				img_1[line,pixel][1] = img_1[line,start_h-1][1]
				img_1[line,pixel][2] = img_1[line,start_h-1][2]
		
		for line in range(start_v,height):
			for pixel in range(start_h,width):
				img_1[line,pixel][0] = img_1[2*start_v-line,pixel][0]
				img_1[line,pixel][1] = img_1[2*start_v-line,pixel][1]
				img_1[line,pixel][2] = img_1[2*start_v-line,pixel][2]

		if pos == 'ur':
			img_1 = np.fliplr(img_1)
		elif pos =='dl':
			img_1 = np.flipud(img_1)
		elif pos =='dr':
			
			img_1 = np.flipud(img_1)
			img_1 = np.fliplr(img_1)

	elif pos == 'rot':
		img_1=img.copy()
		fill_ori = 1
		if fillsize <0:
			fill_ori = -1
			img_1 = np.fliplr(img)
		
		fillsize = abs(fillsize)
		[hor_l,hor_r] = calc_dim([width,height],abs(fillsize))
		
		#print((hor_l,hor_r))
		#print([hor_l,hor_r])
		k_l = tan(fillsize)
		k_r = 1/tan(fillsize)
		'''
		print(k_l)
		print(k_r)
		'''
		vert_len = abs(hor_l*k_l)
		#print(vert_len)
		blankspace_l=[]
		for line in range(abs(int(vert_len))+buffer_size):
			for pixel in range(abs(int(float(hor_l)*(abs(vert_len) -line)/vert_len))+buffer_size):
				
				blankspace_l.append((line,pixel-1))
		#print(blankspace_l)
		for item in blankspace_l:
			hr_co = item[1]
			vt_co = item[0]
			small_tri_vt = abs(vert_len - vt_co - hr_co*tan(fillsize))
			codif_x = small_tri_vt*cos(fillsize)*sin(fillsize)
			codif_y = small_tri_vt*cos(fillsize)*cos(fillsize)
			img_1[vt_co,hr_co][0] = img_1[int(vt_co+codif_y+1),int(hr_co+codif_x+1)][0] 
			img_1[vt_co,hr_co][1] = img_1[int(vt_co+codif_y+1),int(hr_co+codif_x+1)][1] 
			img_1[vt_co,hr_co][2] = img_1[int(vt_co+codif_y+1),int(hr_co+codif_x+1)][2] 

		vert_len2 = abs(hor_r*k_r)
		#print(vert_len)
		blankspace_l2=[]
		for line in range(abs(int(vert_len2))+buffer_size):
			for pixel in range(abs(int(float(hor_r)*(abs(vert_len2) -line)/vert_len2))+buffer_size):
				
				blankspace_l2.append((line,width - pixel-1))
		#print(blankspace_l2)
		#fillspace = []
		for item in blankspace_l2:
			hr_co = item[1]
			vt_co = item[0]
			small_tri_vt = abs(vert_len2 - vt_co - (width - hr_co)/tan(fillsize))
			codif_x = small_tri_vt*sin(fillsize)*cos(fillsize)
			codif_y = small_tri_vt*sin(fillsize)*sin(fillsize)
			img_1[vt_co,hr_co][0] = img_1[int(vt_co+codif_y+1),int(hr_co-codif_x-1)][0] 
			img_1[vt_co,hr_co][1] = img_1[int(vt_co+codif_y+1),int(hr_co-codif_x-1)][1] 
			img_1[vt_co,hr_co][2] = img_1[int(vt_co+codif_y+1),int(hr_co-codif_x-1)][2] 
			#fillspace.append((vt_co,hr_co,int(vt_co+2*codif_y),int(hr_co-2*codif_x)))
		#print(fillspace)
		img_1 = np.fliplr(img_1)
		img_1 = np.flipud(img_1)

		for item in blankspace_l:
			hr_co = item[1]
			vt_co = item[0]
			small_tri_vt = abs(vert_len - vt_co - hr_co*tan(fillsize))
			codif_x = small_tri_vt*cos(fillsize)*sin(fillsize)
			codif_y = small_tri_vt*cos(fillsize)*cos(fillsize)
			img_1[vt_co,hr_co][0] = img_1[int(vt_co+codif_y+1),int(hr_co+codif_x+1)][0] 
			img_1[vt_co,hr_co][1] = img_1[int(vt_co+codif_y+1),int(hr_co+codif_x+1)][1] 
			img_1[vt_co,hr_co][2] = img_1[int(vt_co+codif_y+1),int(hr_co+codif_x+1)][2] 

		
		for item in blankspace_l2:
			hr_co = item[1]
			vt_co = item[0]
			small_tri_vt = abs(vert_len2 - vt_co - (width - hr_co)/tan(fillsize))
			codif_x = small_tri_vt*sin(fillsize)*cos(fillsize)
			codif_y = small_tri_vt*sin(fillsize)*sin(fillsize)
			img_1[vt_co,hr_co][0] = img_1[int(vt_co+codif_y+1),int(hr_co-codif_x-1)][0] 
			img_1[vt_co,hr_co][1] = img_1[int(vt_co+codif_y+1),int(hr_co-codif_x-1)][1] 
			img_1[vt_co,hr_co][2] = img_1[int(vt_co+codif_y+1),int(hr_co-codif_x-1)][2] 
			
		img_1 = np.fliplr(img_1)
		img_1 = np.flipud(img_1)

		if fill_ori <0:
			img_1 = np.fliplr(img_1)

	elif pos in easy_trans:
		if pos == 'up':
			vertical_size = fillsize[0]
			start_v = height-vertical_size
			for line in range(start_v,height):
				for pixel in range(width):
					img_1[line,pixel][0] = img_1[start_v-1,pixel][0]
					img_1[line,pixel][1] = img_1[start_v-1,pixel][1]
					img_1[line,pixel][2] = img_1[start_v-1,pixel][2]

		elif pos =='dn':
			img_1 = np.flipud(img_1)
			vertical_size = fillsize[0]
			start_v = height-vertical_size
			for line in range(start_v,height):
				for pixel in range(width):
					img_1[line,pixel][0] = img_1[start_v-1,pixel][0]
					img_1[line,pixel][1] = img_1[start_v-1,pixel][1]
					img_1[line,pixel][2] = img_1[start_v-1,pixel][2]
			img_1 = np.flipud(img_1)
		elif pos == 'lf':
			horizontal_size = fillsize[0]
			start_h = width-horizontal_size
			for line in range(height):
				for pixel in range(start_h,width):
					img_1[line,pixel][0] = img_1[line,start_h-1][0]
					img_1[line,pixel][1] = img_1[line,start_h-1][1]
					img_1[line,pixel][2] = img_1[line,start_h-1][2]

		elif pos == 'rt':
			img_1 = np.fliplr(img_1)
			horizontal_size = fillsize[0]
			start_h = width-horizontal_size-1
			for line in range(height):
				for pixel in range(start_h,width):
					img_1[line,pixel][0] = img_1[line,start_h-1][0]
					img_1[line,pixel][1] = img_1[line,start_h-1][1]
					img_1[line,pixel][2] = img_1[line,start_h-1][2]
			img_1 = np.fliplr(img_1)

	return img_1

def extrapolate_flp(img,pos,fillsize):
	img_1 = img.copy()
	buffer_size=2
	shape_o=img.shape
	height = shape_o[0]
	width = shape_o[1]
	channel = shape_o[2]
	easy_trans = ['up','dn','lf','rt']
	if pos !='rot' and pos not in easy_trans:
		vertical_size = fillsize[0]
		horizontal_size = fillsize[1]
		if pos == 'ur':
			img_1 = np.fliplr(img_1)
		elif pos =='dl':
			
			img_1 = np.flipud(img_1)
		elif pos =='dr':
			
			img_1 = np.flipud(img_1)
			img_1 = np.fliplr(img_1)


		start_v = height-vertical_size-1
		start_h = width-horizontal_size
		for line in range(start_v+1,height):
			for pixel in range(start_h+1):
				img_1[line,pixel][0] = img_1[2*start_v-line,pixel][0]
				img_1[line,pixel][1] = img_1[2*start_v-line,pixel][1]
				img_1[line,pixel][2] = img_1[2*start_v-line,pixel][2]

		for line in range(height):
			for pixel in range(start_h+1,width):
				img_1[line,pixel][0] = img_1[line,2*start_h-pixel][0]
				img_1[line,pixel][1] = img_1[line,2*start_h-pixel][1]
				img_1[line,pixel][2] = img_1[line,2*start_h-pixel][2]

		if pos == 'ur':
			img_1 = np.fliplr(img_1)
		elif pos =='dl':
			img_1 = np.flipud(img_1)
		elif pos =='dr':
			img_1 = np.flipud(img_1)
			img_1 = np.fliplr(img_1)

	elif pos == 'rot':
		img_1 = img.copy()
		fill_ori = 1
		if fillsize <0:
			fill_ori = -1
			img_1 = np.fliplr(img)

		fillsize = abs(fillsize)
		[hor_l,hor_r] = calc_dim([width,height],fillsize)
		
		#print([hor_l,hor_r])
		k_l = tan(fillsize)
		k_r = 1/tan(fillsize)
		'''
		print(k_l)
		print(k_r)
		'''
		vert_len = abs(hor_l*k_l)
		#print(vert_len)
		#print(int(float(hor_l)*(vert_len -line)/vert_len))
		blankspace_l=[]
		for line in range(abs(int(vert_len))+buffer_size):
			for pixel in range(int(abs(float(hor_l)*(abs(vert_len) -line)/vert_len))+buffer_size):
				
				blankspace_l.append((line,pixel-1))
		#print(len(blankspace_l))
		for item in blankspace_l:
			hr_co = item[1]
			vt_co = item[0]
			small_tri_vt = abs(vert_len - vt_co - hr_co*tan(fillsize))
			codif_x = small_tri_vt*cos(fillsize)*sin(fillsize)
			codif_y = small_tri_vt*cos(fillsize)*cos(fillsize)
			img_1[vt_co,hr_co][0] = img_1[int(vt_co+2*codif_y+1),int(hr_co+2*codif_x-1)][0] 
			img_1[vt_co,hr_co][1] = img_1[int(vt_co+2*codif_y+1),int(hr_co+2*codif_x-1)][1] 
			img_1[vt_co,hr_co][2] = img_1[int(vt_co+2*codif_y+1),int(hr_co+2*codif_x-1)][2] 

		vert_len2 = abs(hor_r*k_r)
		#print(vert_len)
		blankspace_l2=[]
		for line in range(abs(int(vert_len2))+buffer_size):
			for pixel in range(abs(int(float(hor_r)*(abs(vert_len2) -line)/vert_len2))+buffer_size):
				
				blankspace_l2.append((line,width - pixel-1))
		#print(blankspace_l2)
		#fillspace = []
		for item in blankspace_l2:
			hr_co = item[1]
			vt_co = item[0]
			small_tri_vt = abs(vert_len2 - vt_co - (width - hr_co)/tan(fillsize))
			codif_x = small_tri_vt*sin(fillsize)*cos(fillsize)
			codif_y = small_tri_vt*sin(fillsize)*sin(fillsize)
			img_1[vt_co,hr_co][0] = img_1[int(vt_co+2*codif_y+1),int(hr_co-2*codif_x-1)][0] 
			img_1[vt_co,hr_co][1] = img_1[int(vt_co+2*codif_y+1),int(hr_co-2*codif_x-1)][1] 
			img_1[vt_co,hr_co][2] = img_1[int(vt_co+2*codif_y+1),int(hr_co-2*codif_x-1)][2] 
			#fillspace.append((vt_co,hr_co,int(vt_co+2*codif_y),int(hr_co-2*codif_x)))
		#print(fillspace)
		img_1 = np.fliplr(img_1)
		img_1 = np.flipud(img_1)

		for item in blankspace_l:
			hr_co = item[1]
			vt_co = item[0]
			small_tri_vt = abs(vert_len - vt_co - hr_co*tan(fillsize))
			codif_x = small_tri_vt*cos(fillsize)*sin(fillsize)
			codif_y = small_tri_vt*cos(fillsize)*cos(fillsize)
			img_1[vt_co,hr_co][0] = img_1[int(vt_co+2*codif_y+1),int(hr_co+2*codif_x+1)][0] 
			img_1[vt_co,hr_co][1] = img_1[int(vt_co+2*codif_y+1),int(hr_co+2*codif_x+1)][1] 
			img_1[vt_co,hr_co][2] = img_1[int(vt_co+2*codif_y+1),int(hr_co+2*codif_x+1)][2] 

		
		for item in blankspace_l2:
			hr_co = item[1]
			vt_co = item[0]
			small_tri_vt = abs(vert_len2 - vt_co - (width - hr_co)/tan(fillsize))
			codif_x = small_tri_vt*sin(fillsize)*cos(fillsize)
			codif_y = small_tri_vt*sin(fillsize)*sin(fillsize)
			img_1[vt_co,hr_co][0] = img_1[int(vt_co+2*codif_y+1),int(hr_co-2*codif_x-1)][0] 
			img_1[vt_co,hr_co][1] = img_1[int(vt_co+2*codif_y+1),int(hr_co-2*codif_x-1)][1] 
			img_1[vt_co,hr_co][2] = img_1[int(vt_co+2*codif_y+1),int(hr_co-2*codif_x-1)][2] 
			
		img_1 = np.fliplr(img_1)
		img_1 = np.flipud(img_1)

		if fill_ori <0:
			img_1 = np.fliplr(img_1)

	elif pos in easy_trans:
		if pos =='up':
			vertical_size = fillsize[0]
			start_v = height-vertical_size-1
			for line in range(start_v+1,height):
				for pixel in range(width):
					img_1[line,pixel][0] = img_1[2*start_v-line,pixel][0]
					img_1[line,pixel][1] = img_1[2*start_v-line,pixel][1]
					img_1[line,pixel][2] = img_1[2*start_v-line,pixel][2]

		elif pos =='dn':
			img_1 = np.flipud(img_1)
			vertical_size = fillsize[0]
			start_v = height-vertical_size
			for line in range(start_v,height):
				for pixel in range(width):
					img_1[line,pixel][0] = img_1[2*start_v-line,pixel][0]
					img_1[line,pixel][1] = img_1[2*start_v-line,pixel][1]
					img_1[line,pixel][2] = img_1[2*start_v-line,pixel][2]
			img_1 = np.flipud(img_1)
		elif pos == 'lf':
			horizontal_size = fillsize[0]
			start_h = width-horizontal_size
			for line in range(height):
				for pixel in range(start_h,width):
					img_1[line,pixel][0] = img_1[line,2*start_h-pixel][0]
					img_1[line,pixel][1] = img_1[line,2*start_h-pixel][1]
					img_1[line,pixel][2] = img_1[line,2*start_h-pixel][2]

		elif pos == 'rt':
			img_1 = np.fliplr(img_1)
			horizontal_size = fillsize[0]
			start_h = width-horizontal_size-1
			for line in range(height):
				for pixel in range(start_h,width):
					img_1[line,pixel][0] = img_1[line,2*start_h-pixel][0]
					img_1[line,pixel][1] = img_1[line,2*start_h-pixel][1]
					img_1[line,pixel][2] = img_1[line,2*start_h-pixel][2]
			img_1 = np.fliplr(img_1)




	return img_1
	

