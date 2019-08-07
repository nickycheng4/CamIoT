from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from sklearn.neural_network import MLPClassifier
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
import numpy as np
import os
from sklearn import svm
from joblib import dump
import cv2
import time
sys.path.insert(0, 'Finger_Detection')
from crop import generate_crop

owd = os.getcwd()

os.chdir('train_data/Simon')
rootdir = 'Aug'

layer = 'fc2'
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer).output)

total_tag = []
total_set = []

counter = 0
red_bias = 30
blue_bias = 40
green_bias = -10

for subdir, dirs, files in os.walk(rootdir):
	tag = subdir.partition('/')[-1]
	print('The tag is',tag,'\n')
	files_size = len(files)
	for i, file in enumerate(files):
		file_path = os.path.join(subdir, file)
		if 'jpg' in file_path or 'JPG' in file_path:
			'''
			img = cv2.imread(file_path)
			img_out,img_bk = = generate_crop(file_path,220)
			cv2.imwrite('train0.jpg',img_out)
			'''
			img = image.load_img(file_path, target_size=(224, 224))
			img_data = image.img_to_array(img)
			img_data = np.expand_dims(img_data, axis=0)
			img_data = preprocess_input(img_data)
			vgg16_feature = model.predict(img_data)
			total_set.append(np.ndarray.tolist(vgg16_feature[0]))
			total_tag.append(tag)
			print ('\r >> preprocessing class#%d %4.2f' % (counter,(i/files_size)*100),'%',end='')
	counter += 1

print(total_tag)
print(np.shape(total_tag))
print(np.shape(total_set))
os.chdir(owd)


# classification
print('Training the model...')
# probability will slow down the process
clf = MLPClassifier(alpha=1, max_iter=1000)
clf.fit(total_set, total_tag)
dump(clf, 'Simon_Aug.joblib')
print('Model is ready.')