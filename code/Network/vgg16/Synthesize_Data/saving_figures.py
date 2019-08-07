import matplotlib.pyplot as plt
import time

def save_fig(title,imgname,direc):
	#plt.rcParams['figure.figsize'] = (1.0, 1.0)
	#plt.rcParams['savefig.dpi'] = 224
	#plt.rcParams['figure.dpi'] = 224
	plt.figure('title')
	plt.imshow(imgname)
	plt.axis('off')
	#plt.subplots_adjust(left=0,right=1,bottom=0,top=1,hspace = 0, wspace = 0)
	plt.savefig(direc + str(time.time())+ '.jpg',bbox_inches='tight',pad_inches = 0)
	plt.close()