import numpy as np
import cv2 
# import the necessary packages
from skimage import measure
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2




def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")
	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")
	# show the images
	plt.show()


#img_1,img_2=input("input your images ").split()

img_1='0image.jpg'
img_2='1image.jpg'

img_irOn = cv2.imread(img_1)
img_irOn = cv2.cvtColor(img_irOn, cv2.COLOR_BGR2GRAY)
img_irOff = cv2.imread(img_2)
img_irOff = cv2.cvtColor(img_irOff, cv2.COLOR_BGR2GRAY)

height,width=img_irOn.shape
img_out=np.zeros((height,width,))

'''
# output the ssim and mse scores 
fig = plt.figure("Images")
images = ("IR On", img_irOn), ("IR Off", img_irOff)
# loop over the images
for (i, (name, image)) in enumerate(images):
	# show the image
	ax = fig.add_subplot(1, 3, i + 1)
	ax.set_title(name)
	plt.imshow(image, cmap = plt.cm.gray)
	plt.axis("off")
# show the figure
plt.show()
# compare the images
compare_images(img_irOn, img_irOff, "IR on vs. IR off")
#######################################################
'''


'''
subtracted=img_irOn - img_irOff
cv2.imwrite('simpleSubtractat.jpg',subtracted)


height,width,channel = img_irOn.shape

img_out = np.zeros([height,width,channel],dtype=np.uint8)
img_out.fill(0)

for line in range(height):
	for pixel in range(width,10):
		if max([img_irOn[line,pixel][0],img_irOff[line,pixel][0]])-min([img_irOn[line,pixel][0],img_irOff[line,pixel][0]])>30:
			img_out[line,pixel][0] = 255

print(abs(int(img_irOn[1,10][1])-int(img_irOff[1,10][1]))

#threshold = 50

for line in range(height):
	for pixel in range(width):
		
		if (abs(int(img_irOn[line,pixel][1])-int(img_irOff[line,pixel][1]) < threshold)
			img_out[line,pixel][1]=0
		else :
			img_out[line,pixel][1]=255


cv2.imshow('binary difference',img_out)
cv2.waitKey(10000)
cv2.destroyAllWindows()
'''
			