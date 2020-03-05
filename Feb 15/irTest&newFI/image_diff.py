#https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/


import numpy as np
from skimage import filters
from skimage.measure import compare_ssim  
import argparse
import imutils
import cv2
import matplotlib.pyplot as plt  



def masking(image,thre):
	output=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	output=cv2.adaptiveThreshold(output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)
	retval=cv2.threshold(output,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	return retval,output


def fingerBottom(image):
	height,width = image.shape

	white_thr = 230
	black_thr = 10
	counter=0
	counter_2=0
	left=0
	right=0
	thickness=0
	ls=0
	rs=0
	t=0
	w=470
	print("height: ",height," width: ",width)
	cv2.imshow("GaussianBlurpic",image)

	print(image[:,w])

	# get the white range for each line
	for j in range(width):
			 if image[j,w] >white_thr:
			 	if (counter_2==0):
			 		left=j
			 	elif (counter_2 > 0):
			 		right=j
			 		thickness=right-left
			 	counter_2=counter_2+1	
			 else:
			 	if (t<thickness):
			 		ls=left
			 		rs=right
			 		t=rs-ls
			 	left=0
			 	right=0
			 	counter=counter+1
			 	counter_2=0

	print("ls: ",ls,"rs: ", rs, "t: ",t)
	
	midPixel=(rs+ls)/2
	print(midPixel)
	return midPixel,w
	
def fignerFinder():
	ap=argparse.ArgumentParser()
	ap.add_argument("-f", "--first", required=True,help="first input image")
	#ap.add_argument("-s", "--second", required=True,help="second input image")
	args = vars(ap.parse_args())
	#setting the threshold value in case we use cv2.THRESH_BINARY
	thre=200
	radius=101


	#load the image 
	ir=cv2.imread(args["first"])	
	#noIr=cv2.imread(args["second"])
	#apply different thresholding so far gussian and adaptive means are better  
	#irRet,irOut=masking(ir,thre)
	#noirRet,noIrOut=masking(noIr,thre)

	#cv2.imwrite("results/irOut_ADAPTIVE_THRESH_MEAN.jpg",irOut)
	#cv2.imwrite("results/noIrOut_ADAPTIVE_THRESH_MEAN.jpg",noIrOut)
	retval,irG=masking(ir,thre)
	bx,by=fingerBottom(irG)
	bx=int(bx)
	print(bx)
	print(by)
	#bottom=(bx,int(by)
	irG = cv2.GaussianBlur(irG, (radius, radius), 0)
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(irG)
	cv2.arrowedLine(ir, (bx,by), maxLoc, (0,0,255),2)
	h,w=irG.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	cv2.floodFill(ir, mask,(0,0), 255)
	ir_inv = cv2.bitwise_not(ir)
	ir_out=ir && ir_inv
	#cv2.imshow("arrowDirection",ir)
	cv2.imshow("FloodFill",ir)
	cv2.imshow("inv added",ir_out)
	cv2.imwrite("arrows/arrowDirection2.jpg",ir)
	cv2.waitKey(0)
	# find the white area of the finger 









fignerFinder()







	
