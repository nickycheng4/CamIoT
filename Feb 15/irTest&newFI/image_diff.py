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
	output=cv2.adaptiveThreshold(output, 255, cv2.cv2.ADAPTIVE_THRESH_MEAN, cv2.THRESH_BINARY, 11,2)
	#retval,output=cv2.threshold(output,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	return output



def fignerFinder():
	ap=argparse.ArgumentParser()
	ap.add_argument("-f", "--first", required=True,help="first input image")
	ap.add_argument("-s", "--second", required=True,help="second input image")
	args = vars(ap.parse_args())
	thre=200

	#load the image 
	ir=cv2.imread(args["first"])	
	noIr=cv2.imread(args["second"])
	#convert the image to grayscale 
	irOut=masking(ir,thre)
	noIrOut=masking(noIr,thre)
	cv2.imwrite("results/irOut_ADAPTIVE_THRESH_MEAN.jpg",irOut)
	cv2.imwrite("results/noIrOut_ADAPTIVE_THRESH_MEAN.jpg",noIrOut)
	









'''
def example():
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-f", "--first", required=True,
		help="first input image")
	ap.add_argument("-s", "--second", required=True,
		help="second")
	args = vars(ap.parse_args())

	# load the two input images
	imageA = cv2.imread(args["first"])
	imageB = cv2.imread(args["second"])
	# convert the images to grayscale
	grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
	grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
	cv2.imshow("imag1",grayA)
	cv2.imshow("imag2",grayB)

	(score, diff) = compare_ssim(grayA, grayB, full=True)

	diff = (diff * 255).astype("uint8")
	print("SSIM: {}".format(score))
	cv2.imshow("difference",diff)

	# threshold the difference image, followed by finding contours to
	# obtain the regions of the two input images that differ
	thresh = cv2.threshold(diff, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	cnts = imutils.grab_contours(cnts)

	# loop over the contours
	for c in cnts:
		# compute the bounding box of the contour and then draw the
		# bounding box on both input images to represent where the two
		# images differ
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
		cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
	# show the output images
	cv2.imwrite("output/Original.jpg", imageA)
	cv2.imwrite("output/Modified.jpg", imageB)
	cv2.imwrite("output/Diff.jpg", diff)
	cv2.imwrite("output/Thresh.jpg", thresh)
	cv2.waitKey(10000000)
	cv2.destroyAllWindows()
'''

fignerFinder()
#example()

	
