from synthesize_image import generate_imgs
from copy_images import copy_image
import os
import shutil

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

objects = []
for item in os.listdir('Image_To_Train'):
	if 'DS' not in item:
		objects.append(item)

process = ['Aug','Copy']

everything = ''
for item in objects:
	if item == objects[-1]:
		everything += item + '.'
	else:
		everything += item + ', '

if 'Aug' in process:
	print('Start preparing augmentation dataset.')
	total_img = 0
	for item in objects:
		if item in os.listdir('Synthesized_Data/Aug'):
			shutil.rmtree('Synthesized_Data/Aug/' + item)
			print('\nFinished Deleting Older Data for %s.' %(item))
		directory = 'Image_To_Train/' + item + '/'
		os.mkdir('Synthesized_Data/Aug/' + item)
		#print(item)
		print('\nSynthesizing for appliance %s.' %(item))
		for filename in os.listdir(directory):
			if 'jpg' not in filename and 'jpeg' not in filename and 'JPG' not in filename and 'JPEG' not in filename and 'Screen Shot' not in filename:
				continue
			
			generate_imgs(directory + filename,item)
			total_img +=1
		print('-'*(len('Synthesizing for appliance  DONE!!!')+len(item)+2))
		print('|Synthesizing for appliance %s DONE!!!|' %(item))
		print('-'*(len('Synthesizing for appliance  DONE!!!')+len(item)+2))

	print('\nFinished Synthesizing Images for appliances: \n%s' %(everything))

	print('Total of %d images processed.\n' %(total_img))


if 'Copy' in process:
	print('Start preparing copy dataset.')
	for item in objects:
		if item in os.listdir('Synthesized_Data/Raw'):
			shutil.rmtree('Synthesized_Data/Raw/' + item)
			print('\nFinished Deleting Older Data for %s.' %(item))
		directory = 'Image_To_Train/' + item + '/'
		os.mkdir('Synthesized_Data/Raw/' + item)
		#print(item)
		print('\nStart copying for appliance %s.' %(item))
		for filename in os.listdir(directory):
			if 'jpg' not in filename and 'jpeg' not in filename and 'JPG' not in filename and 'JPEG' not in filename and 'Screen Shot' not in filename:
				continue
			
			copy_image(item,directory + filename,63)
			
		print('-'*(len('Copying for appliance  DONE!!!')+len(item)+2))
		print('|Copying for appliance %s DONE!!!|' %(item))
		print('-'*(len('Copying for appliance  DONE!!!')+len(item)+2))

	print('\nFinished Copying Images for appliances: \n%s' %(everything))

print('\nAll Done!!!')