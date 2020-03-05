
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
	#print("SSIM: {}".format(score))
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
	cv2.imwrite("output/noIr1.jpg", imageA)
	cv2.imwrite("output/IrBrightnessEdit.jpg", imageB)
	cv2.imwrite("output/Diff1.jpg", diff)
	cv2.imwrite("output/Thresh1.jpg", thresh)
	cv2.waitKey(10000000)
	cv2.destroyAllWindows()