import cv2
import numpy as np
import os

img1_path = 'MDD.jpg'
img2_path = 'E:/OMR/MDD.jpg'

if not os.path.exists(img1_path):
    print("MDD.jpg does not exist locally")
if not os.path.exists(img2_path):
    print("E:/OMR/MDD.jpg does not exist")

if os.path.exists(img1_path) and os.path.exists(img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    print("Local MDD shape:", img1.shape)
    print("E:/OMR MDD shape:", img2.shape)
    print("Are identical?", np.array_equal(img1, img2))
