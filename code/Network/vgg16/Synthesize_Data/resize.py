
import matplotlib.image as mpimg 
from scipy import misc

def resize_img(img):
	#image_ori = mpimg.imread(img)
	
	
	image_ori = misc.imresize(img, (540,720))
	
	return image_ori



