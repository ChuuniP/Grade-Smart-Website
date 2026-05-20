import cv2, numpy as np
import sys
sys.path.insert(0, 'backend/ref')
import support as sp

img = cv2.imread('backend/ref/MDD.jpg')
img = cv2.resize(img, (500, 700))
imgPer = img[35:685, 20:490]
imgGray = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(imgGray, 135, 255, cv2.THRESH_BINARY_INV)[1]

# horizontal profile
hsum = imgThresh.sum(axis=0)
for x in range(0, imgThresh.shape[1], 10):
    print('x', x, 'sum', int(hsum[x]))

# vertical profile every 10 pixels
vsum = imgThresh.sum(axis=1)
for y in range(0, imgThresh.shape[0], 10):
    print('y', y, 'sum', int(vsum[y]))

# Find peaks in horizontal sum to locate bubble columns
from scipy.signal import find_peaks
peaks, _ = find_peaks(hsum, height=max(hsum)*0.1, distance=20)
print('peaks', peaks)
