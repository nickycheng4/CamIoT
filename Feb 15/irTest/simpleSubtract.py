import numpy as np
import cv2 


#img_1,img_2=input("input your images ").split()

img_1='0image.jpg'
img_2='1image.jpg'

img_irOn = cv2.imread(img_1)
img_irOff = cv2.imread(img_2)

subtracted=img_irOn - img_irOff
cv2.imwrite('simpleSubtractat.jpg',subtracted)


height,width,channel = img_irOn.shape

img_out = np.zeros([height,width,channel],dtype=np.uint8)
img_out.fill(0)
	
for line in range(height):
	for pixel in range(width,10):
		if max([img_irOn[line,pixel][0],img_irOff[line,pixel][0]])-min([img_irOn[line,pixel][0],img_irOff[line,pixel][0]])>30:
			img_out[line,pixel][0] = 255
cv2.imshow('binary difference',img_out)
cv2.waitKey(10000)
cv2.destroyAllWindows()

			