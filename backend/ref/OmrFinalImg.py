import cv2
import numpy as np
import support as sp
import solveImg as si

def WarpImg(img, MDD, MD):
    widthImg = 500
    heightImg = 700
    imgAns = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, 50, 150)
    contours, h = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sp.rectContour(contours)
    pointContour = np.zeros((4, 2))
    img, pointContour = si.TakeImgFinal(img, pointContour, contours)
    pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    warpImg = cv2.warpPerspective(imgAns, matrix, (widthImg, heightImg))
    finalImg = warpImg[25:690, 15:495]
    finalImg = cv2.resize(finalImg, (widthImg, heightImg))
    cv2.putText(finalImg, str(int(MDD[0])) + str(int(MDD[1])) + str(int(MDD[2])) + str(int(MDD[3])) + str(int(MDD[4])) + str(int(MDD[5])), (375, 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)
    cv2.putText(finalImg, str(int(MD[0])) + str(int(MD[1])) + str(int(MD[2])), (455, 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)
    cv2.imshow('FinalImg', finalImg)
    return finalImg