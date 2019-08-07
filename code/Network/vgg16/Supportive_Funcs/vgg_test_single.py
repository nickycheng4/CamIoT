from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
import numpy as np
from joblib import load

# model = VGG16(weights='imagenet', include_top=False)
# model.summary()
layer = 'fc2'
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer).output)
clf = load('svm_classifier.joblib') 
print('classes',clf.classes_)

test_set = []

img_path = '0image.jpg'
img = image.load_img(img_path, target_size=(224, 224))
img_data = image.img_to_array(img)
img_data = np.expand_dims(img_data, axis=0)
img_data = preprocess_input(img_data)

vgg16_feature = model.predict(img_data)
test_set.append(np.ndarray.tolist(vgg16_feature[0]))
# print (np.shape(test_set))


predict_target = clf.predict(test_set)
predict_prob = clf.predict_proba(test_set)
print(predict_target)
print(predict_prob)