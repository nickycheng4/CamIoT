import mmcv
import cv2
import os
import numpy as np
import os.path as osp
from skimage.measure import label
from scipy.ndimage import filters
from skimage.segmentation import flood, flood_fill


INPUT_PATH = '/yuanProject/CAMIOT/fingure_data'
OUTPUT_PATH = '/yuanProject/CAMIOT/fingure_data_results'


mmcv.mkdir_or_exist(OUTPUT_PATH)

for item in os.listdir(INPUT_PATH):
    if '.jpg' in item:
        image = cv2.imread(osp.join(INPUT_PATH, item))
        imageYCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)

        # skin detection
        min_YCrCb = np.array([0, 133, 77], np.uint8)
        max_YCrCb = np.array([255, 173, 127], np.uint8)
        skinRegionYCrCb = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)

        # # preprocessing
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        skinRegionYCrCb = cv2.erode(skinRegionYCrCb, kernel, iterations=2)
        skinRegionYCrCb = cv2.dilate(skinRegionYCrCb, kernel, iterations=2)
        skinRegionYCrCb = cv2.GaussianBlur(skinRegionYCrCb, (3, 3), 0)

        # largest island
        skinRegionYCrCb = label(skinRegionYCrCb)
        # if cur_label_map.max() == 0:
        #     continue
        skinRegionYCrCb = skinRegionYCrCb == np.argmax(np.bincount(skinRegionYCrCb.flat)[1:]) + 1

        # get a starting point
        points_x, points_y = np.where(skinRegionYCrCb == 1)
        selected_x = points_x[np.argmax(points_x)]
        selected_y = points_y[np.argmax(points_x)]

        # flooding
        image = image.astype('int32')
        cat_sobel_x = filters.sobel(image, axis=0).astype(np.float32)
        cat_sobel_y = filters.sobel(image, axis=1).astype(np.float32)
        cat_sobel = cat_sobel_x * cat_sobel_x + cat_sobel_y * cat_sobel_y
        cat_sobel *= 255.0 / np.max(cat_sobel)
        cat_sobel = (cat_sobel[:, :, 0] + cat_sobel[:, :, 1] + cat_sobel[:, :, 2]) / 3.0
        cat_nose = flood(cat_sobel, (selected_x-8, selected_y), tolerance=0.2)
        # postprocessing
        cat_nose = cat_nose.astype(np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        cat_nose = cv2.erode(cat_nose, kernel, iterations=2)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
        cat_nose = cv2.dilate(cat_nose, kernel, iterations=2)
        # cat_nose = cv2.GaussianBlur(cat_nose, (3, 3), 0)

        cat_nose = cat_nose.astype(np.int32)
        cat_nose = cat_nose * 255
        #

        cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_flood_mask.jpg'.format(item.split('.')[0], 'skin')), cat_nose)

        # skinYCrCb = cv2.bitwise_and(image, image, mask=np.uint8(cat_nose))
        # # skinYCrCb = cv2.circle(skinYCrCb, (selected_y, selected_x-8), 8, (255, 0, 0), 2)
        #
        #
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_new.jpg'.format(item.split('.')[0], 'skin')), skinYCrCb)




        # lower = np.array([0, 48, 80], dtype="uint8")
        # upper = np.array([20, 255, 255], dtype="uint8")
        # converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # skinMask = cv2.inRange(converted, lower, upper)
        # skin = cv2.bitwise_and(image, image, mask=skinMask)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'newskin')), skin)

        # image = image.astype('int32')
        # cat_sobel_x = filters.sobel(image, axis=0)
        # cat_sobel_y = filters.sobel(image, axis=1)
        # mag = np.hypot(cat_sobel_x, cat_sobel_y)
        # mag *= 255.0 / np.max(mag)
        # cat_sobel = cat_sobel_x^2 + cat_sobel_y^2
        # print(cat_sobel.shape)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'sobel')), cat_sobel)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'sobel0')), cat_sobel[:, :, 0])
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'sobel1')), cat_sobel[:, :, 1])
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'sobel2')), cat_sobel[:, :, 2])
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'sobelall')), (cat_sobel[:, :, 0]+cat_sobel[:, :, 1]+cat_sobel[:, :, 2])/3.0)

