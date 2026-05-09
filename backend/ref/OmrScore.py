import cv2
import numpy as np
import support as sp
def ReadScore(img, score, questions):
    widthImg = 500
    heightImg = 700
    img = cv2.resize(img, (widthImg, heightImg))
    imgContour = img.copy()
    imgDraw = img.copy()
    imgAns = img.copy()
    imgFinal = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, 50, 150)
    contours, h = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 1)
    # cv2.imshow('Canny', imgContour)

    rectCon = sp.rectContour(contours)
    for i in rectCon:
        cv2.drawContours(imgDraw, sp.getCornerPoint(i), -1, (0, 255, 0), 5)
    # cv2.imshow('imgDraw', imgDraw)

    x1, x2, x5, x6 = 10, 70, 290, 350
    y1, y2, y5, y6 = 180, 240, 0, 60

    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.rectangle(img, (x1, y5), (x2, y6), (0, 0, 255), 2)
    cv2.rectangle(img, (x5, y5), (x6, y6), (0, 0, 255), 2)
    cv2.rectangle(img, (x5, y1), (x6, y2), (0, 0, 255), 2)

    count = 0
    pointContourG = np.zeros((4, 2))
    for contour in rectCon:
        x, y, w, h = cv2.boundingRect(contour)
        if x1 <= x <= x2 and y5 <= y <= y6 and x1 <= x + w <= x2 and y5 <= y + h <= y6:
            cv2.rectangle(img, (x1, y5), (x2, y6), (0, 255, 0), 2)
            for pointG in contour:
                pointContourG[0][0], pointContourG[0][1] = pointG[0]
            count += 1
        if x5 <= x <= x6 and y5 <= y <= y6 and x5 <= x + w <= x6 and y5 <= y + h <= y6:
            cv2.rectangle(img, (x5, y5), (x6, y6), (0, 255, 0), 2)
            for pointG in contour:
                pointContourG[1][0], pointContourG[1][1] = pointG[0]
            count += 1

        if x1 <= x <= x2 and y1 <= y <= y2 and x1 <= x + w <= x2 and y1 <= y + h <= y2:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            for pointG in contour:
                pointContourG[2][0], pointContourG[2][1] = pointG[0]
            count += 1
        if x5 <= x <= x6 and y1 <= y <= y2 and x5 <= x + w <= x6 and y1 <= y + h <= y2:
            cv2.rectangle(img, (x5, y1), (x6, y2), (0, 255, 0), 2)
            for pointG in contour:
                pointContourG[3][0], pointContourG[3][1] = pointG[0]
            count += 1
    # cv2.imshow('camera', img)

    pt1G = np.float32([pointContourG[0], pointContourG[1], pointContourG[2], pointContourG[3]])
    pt2G = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrixG = cv2.getPerspectiveTransform(pt1G, pt2G)
    imgWarpColoredG = cv2.warpPerspective(imgAns, matrixG, (widthImg, heightImg))
    # cv2.imshow('anh grade', imgWarpColoredG)

    imgRawGrade = np.zeros_like(imgWarpColoredG)
    cv2.putText(imgRawGrade,str(int(score))+"/"+str(int(questions)), (100, 150), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 2)

    imgFinal = cv2.addWeighted(imgFinal, 1, imgRawGrade, 1, 0)
    # cv2.imshow('Ans', imgFinal)
    return imgFinal