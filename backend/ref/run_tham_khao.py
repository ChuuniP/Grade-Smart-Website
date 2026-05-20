import cv2
import numpy as np
import sys
import os

# Add ref to path to import support, solveImg
sys.path.append(os.path.dirname(__file__))
import support as sp
import solveImg as si

path = 'MDD.jpg'
widthImg = 500
heightImg = 700
questions = 40
choices = 4

finalAns = [1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2, 1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2]

img = cv2.imread(path)
img = cv2.resize(img, (widthImg, heightImg))

imgAns = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)

contours, h = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)

pointContour = np.zeros((4, 2))
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)

pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarpColored = cv2.warpPerspective(imgAns, matrix, (widthImg, heightImg))

perX1, perX2, perY1, perY2 = 20, 490, 35, 685
imgPer = imgWarpColored[perY1:perY2, perX1:perX2]

imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(imgCvt, 135, 255, cv2.THRESH_BINARY_INV)[1]

boxes = sp.splitImg(imgThresh)
ans = sp.splitAns(boxes)

pixelVals = np.zeros((120, choices))
countC = 0
countR = 0

for image in ans:
    totalPixels = cv2.countNonZero(image)
    pixelVals[countR][countC] = totalPixels
    countC += 1
    if(countC == choices):
        countR += 1
        countC = 0

myIndex = []
for x in range(0, questions):
    arr = pixelVals[x]
    myIndexVal = np.where(arr == np.amax(arr))
    if np.amax(arr) > 50:
        myIndex.append(myIndexVal[0][0])
    else:
        myIndex.append(-1)

grading = []
for x in range(0, questions):
    if( myIndex[x] == finalAns[x] ):
        grading.append(1)
    else:
        grading.append(0)

score = (sum(grading)/questions) * 100

print(f"Total Blanks: {myIndex.count(-1)}")
print(f"Score: {score}%")
print("Detected answers:", myIndex)
