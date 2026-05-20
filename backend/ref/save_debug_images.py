import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(__file__))
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
QUESTIONS = 40
CHOICES = 4

image_path = 'MDD.jpg'
output_dir = 'debug_crops'
os.makedirs(output_dir, exist_ok=True)

img = cv2.imread(image_path)
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgAns = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)

if len(contours) == 0:
    print("Error: No contours found!")
    sys.exit(1)
    
pointContour = np.zeros((4, 2), dtype=np.float32)
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)

pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarpColored = cv2.warpPerspective(imgAns, matrix, (WIDTH_IMG, HEIGHT_IMG))

cv2.imwrite(os.path.join(output_dir, 'warp.jpg'), imgWarpColored)

# Main OMR coordinates from tham_khao_omr.py
perX1, perX2, perY1, perY2 = 20, 490, 35, 685
imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
cv2.imwrite(os.path.join(output_dir, 'crop_per.jpg'), imgPer)

imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(imgCvt, 135, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imwrite(os.path.join(output_dir, 'thresh.jpg'), imgThresh)

# Let's save the 8 main boxes
boxes = sp.splitImg(imgThresh)
for idx, box in enumerate(boxes):
    cv2.imwrite(os.path.join(output_dir, f'box_{idx}.jpg'), box)

print("Saved debug crop images in folder:", output_dir)
