import cv2
import numpy as np
import support as sp
import solveImg as si


def ReadMDD(img):
    widthImg = 500
    heightImg = 700
    img = cv2.resize(img, (widthImg, heightImg))
    # cv2.imshow('goc', img)
    imgContour = img.copy()
    imgDraw = img.copy()
    imgAns = img.copy()
    imgFinal = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, 50, 150)
    contours, h = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sp.getContourInSize(contours)
    cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 1)
    # cv2.imshow('Canny', imgContour)

    rectCon = sp.rectContour(contours)
    for i in contours:
        cv2.drawContours(imgDraw, sp.getCornerPoint(i), -1, (0, 255, 0), 5)
    # cv2.imshow('imgDraw', imgDraw)
    pointContour = np.zeros((4, 2))
    img, pointContour = si.TakeImgMDD(img, pointContour, contours)
    # cv2.imshow('camera', img)
    widthImg = 1000
    pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgWarpColored = cv2.warpPerspective(imgAns, matrix, (widthImg, heightImg))
    # cv2.imshow('blank', imgWarpColored)
    perX1, perX2, perY1, perY2= 760, 995, 175, 680
    imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
    # cv2.imshow('Per', imgPer)
    imgRevert = imgPer.copy()
    imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgCvt, 130, 255, cv2.THRESH_BINARY_INV)[1]
    # cv2.imshow('Thresh', imgThresh)
    MDDImg = imgThresh[0:505, 2:135]
    # cv2.imshow('MDDImg', MDDImg)
    MDImg = imgThresh[0:505, 160:230]
    # cv2.imshow('MDImg', MDImg)


    boxMDD = sp.splitMDD(MDDImg)
    boxMD = sp.splitMD(MDImg)

    pixelValsMDD = np.zeros((6, 10))
    countC = 0
    countR = 0

    for image in boxMDD:
        totalPixels = cv2.countNonZero(image)
        pixelValsMDD[countR][countC] = totalPixels
        countC +=1
        if(countC == 10):
            countR +=1
            countC = 0

    myIndexMDD = []
    for x in range(0, 6):
        arr = pixelValsMDD[x]
        myIndexVal = np.where(arr == np.amax(arr))
        myIndexMDD.append(myIndexVal[0][0])

    pixelValsMD = np.zeros((3, 10))
    countC = 0
    countR = 0

    for image in boxMD:
        totalPixels = cv2.countNonZero(image)
        pixelValsMD[countR][countC] = totalPixels
        countC +=1
        if(countC == 10):
            countR +=1
            countC = 0

    myIndexMD = []
    for x in range(0, 3):
        arr = pixelValsMD[x]
        myIndexVal = np.where(arr == np.amax(arr))
        myIndexMD.append(myIndexVal[0][0])

    imgResultMDD = imgRevert[0:505, 0:130]
    imgRawMDD = np.zeros_like(imgResultMDD)
    oriWidth = imgRawMDD.shape[1]
    oriHeight = imgRawMDD.shape[0]
    imgRawMDD = sp.ResizeImg(imgRawMDD, 600, 1000)
    imgRawMDD = sp.showMDD(imgRawMDD, myIndexMDD, 10, 6)
    imgRawMDD = sp.ResizeImg(imgRawMDD, oriWidth, oriHeight)
    # cv2.imshow('imgRawMDD', imgRawMDD)

    imgResultMD = imgRevert[0:505, 160:230]
    imgRawMD = np.zeros_like(imgResultMD)
    oriWidth = imgRawMD.shape[1]
    oriHeight = imgRawMD.shape[0]
    imgRawMD = sp.ResizeImg(imgRawMD, 300, 1000)
    imgRawMD = sp.showMDD(imgRawMD, myIndexMD, 10, 3)
    imgRawMD = sp.ResizeImg(imgRawMD, oriWidth, oriHeight)
    # cv2.imshow('imgRawMD', imgRawMD)

    imgRawRevert1 = np.zeros_like(imgWarpColored)
    imgRawRevert1[175:680, 760:890] = imgRawMDD
    imgRawRevert1[175:680, 920:990] = imgRawMD
    # cv2.imshow('imgRawRevert1', imgRawRevert1)

    invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
    imgInvWarp = cv2.warpPerspective(imgRawRevert1, invMatrix, (500, heightImg))
    # cv2.imshow('imgInvWarp', imgInvWarp)
    imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
    # cv2.imshow('step2', imgFinal)
    return imgFinal, myIndexMDD, myIndexMD
