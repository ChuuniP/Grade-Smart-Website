import cv2
import numpy as np
import support as sp
import OmrMDD as mdd
import OmrScore as sc
import solveImg as si
import OmrFinalImg as omf

path = r'E:\OMR\MDD.jpg'
widthImg = 500
heightImg = 700
questions = 40
choices = 4
stack = questions//5
MDD = []
MD = []
finalAns = [1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2, 1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2, 2, 3, 1, 0, 2]
img = cv2.imread(path)
img = cv2.resize(img, (widthImg, heightImg))
cv2.imshow('goc', img)
imgContour = img.copy()
imgDraw = img.copy()
imgAns = img.copy()
imgFinal = img.copy()



# Ảnh xám
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('imgGray', imgGray)
imgCanny = cv2.Canny(imgGray, 50, 150)
# cv2.imshow('imgCanny', imgCanny)


contours, h = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# contours = sp.getContourInSize(contours)
contours = sp.rectContour(contours)
cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 1)
cv2.imshow('imgContour', imgContour)

rectCon = sp.rectContour(contours)
for i in contours:
    cv2.drawContours(imgDraw, i, -1, (0, 255, 0), 5)
# cv2.imshow('imgDraw', imgDraw)

pointContour = np.zeros((4, 2))
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)

# cv2.imshow('camera', img)

pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarpColored = cv2.warpPerspective(imgAns, matrix, (widthImg, heightImg))
# cv2.imshow('blank', imgWarpColored)

perX1, perX2, perY1, perY2= 20, 490, 35, 685
imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
cv2.imshow('Per', imgPer)


imgRevert = imgPer.copy()
imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(imgCvt, 135, 255, cv2.THRESH_BINARY_INV)[1]
# cv2.imshow('imgThresh', imgThresh)

boxes = sp.splitImg(imgThresh)
# cv2.imshow('boxpiece', boxes[0])

ans = sp.splitAns(boxes)
# cv2.imshow('anspiece', ans[0])
# cv2.imshow('anspiece1', ans[1])
# cv2.imshow('anspiece2', ans[2])
# cv2.imshow('anspiece3', ans[3])

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



newBoxes = sp.splitImg(imgRevert)
for x in range(questions//5):
    stackAns = finalAns[x*5:x*5+5]
    stackIndex = myIndex[x*5:x*5+5]
    stackGrading = grading[x*5:x*5+5]

    oriWidth = newBoxes[x].shape[1]
    oriHeight = newBoxes[x].shape[0]
    newBoxes[x] = sp.ResizeImg(newBoxes[x], 500, 500)
    newBoxes[x] = sp.showAnswer(newBoxes[x], stackIndex, stackGrading, stackAns, 5, 4)
    newBoxes[x] = sp.ResizeImg(newBoxes[x], oriWidth, oriHeight)
reImg = sp.restoreImg(imgRevert, newBoxes, stack)
# cv2.imshow('restore', reImg)

imgRawRevert = np.zeros_like(imgRevert)
rawBoxes = sp.splitImg(imgRawRevert)
for x in range(questions//5):
    stackAns = finalAns[x*5:x*5+5]
    stackIndex = myIndex[x*5:x*5+5]
    stackGrading = grading[x*5:x*5+5]

    oriWidth = newBoxes[x].shape[1]
    oriHeight = newBoxes[x].shape[0]
    rawBoxes[x] = sp.ResizeImg(rawBoxes[x], 500, 500)
    rawBoxes[x] = sp.showAnswer(rawBoxes[x], stackIndex, stackGrading, stackAns, 5, 4)
    rawBoxes[x] = sp.ResizeImg(rawBoxes[x], oriWidth, oriHeight)
reRawImg = sp.restoreImg(imgRawRevert, rawBoxes, stack)


imgRawRevert1 = np.zeros_like(imgWarpColored)
imgRawRevert1[perY1:perY2, perX1:perX2] = reRawImg

invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
imgInvWarp = cv2.warpPerspective(imgRawRevert1, invMatrix, (widthImg, heightImg))
# cv2.imshow('inv', imgInvWarp)

imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
# cv2.imshow('step1', imgFinal)
imgFinal, MDD, MD = mdd.ReadMDD(imgFinal)
imgFinal = sc.ReadScore(imgFinal, sum(grading), questions)
imgFinal = omf.WarpImg(imgFinal, MDD, MD)
if cv2.waitKey(0) == ord('x'):
    cv2.destroyAllWindows()
