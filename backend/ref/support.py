import cv2
import numpy as np

def rectContour(contours):
    rectCon = []
    for i in contours:
        area = cv2.contourArea(i)
        # print("Area : ", area)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.04*peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea, reverse=True)
    return rectCon

def getCornerPoint(cont):
    peri = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.04 * peri, True)
    return approx

def getContourInSize(contours):
    newContours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            newContours.append(i)
    return newContours

def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew

def splitImg(img):
    height, width = img.shape[:2]
    rows = 2
    cols = 4
    piece_height = height // rows
    piece_width = width // cols
    boxes = []
    for y in range(cols):
        for x in range(rows):
            col_start = piece_width * y
            left_offset = 38
            choices_width = 65
            x_start = col_start + left_offset
            x_end = x_start + choices_width
            y_start = x * piece_height
            y_end = y_start + piece_height
            piece = img[y_start:y_end, x_start:x_end]
            boxes.append(piece)
    return boxes

def splitImg120(img):
    height, width = img.shape[:2]
    rows = 2
    cols = 4
    piece_height = height // rows
    piece_width = width // cols
    boxes = []
    for y in range(cols):
        for x in range(rows):
            x_start = piece_width * y + (0 if y == 0 else 10)
            x_end = x_start + piece_width - (0 if y == cols - 1 else 15)
            y_start = x * piece_height
            y_end = y_start + piece_height
            piece = img[y_start:y_end, x_start + 20:x_end]
            boxes.append(piece)
    return boxes

def splitAns(boxes):
    rows = 5
    cols = 4
    ans = []
    for image in boxes:
        height, width = image.shape[:2]
        piece_height = height // rows
        piece_width = width // cols
        for y in range(rows):
            for x in range(cols):
                start_x = x * piece_width
                end_x = start_x + piece_width
                start_y = y * piece_height
                end_y = start_y + piece_height
                piece = image[start_y:end_y, start_x:end_x]
                ans.append(piece)
    return ans

def splitAns120(boxes):
    rows = 15
    cols = 4
    ans = []
    for image in boxes:
        height, width = image.shape[:2]
        piece_height = height // rows
        piece_width = width // cols
        for y in range(rows):
            for x in range(cols):
                start_x = x * piece_width
                end_x = start_x + piece_width
                start_y = y * piece_height
                end_y = start_y + piece_height
                piece = image[start_y:end_y, start_x:end_x]
                ans.append(piece)
    return ans

def ResizeImg(img, width, height):
    img = cv2.resize(img, (width, height))
    return img

def getPointAnswer(secW, secH, x, y):
    cX, cY =0,0
    if x == 0:
        cX = (x * secW) + secW // 2 + 25
    if x == 1:
        cX = (x * secW) + secW // 2 + 45
    if x == 2:
        cX = (x * secW) + secW // 2 + 65
    if x == 3:
        cX = (x * secW) + secW // 2 + 85

    if y == 0:
        cY = ((y * secH) + secH // 2) - 10
    if y == 1:
        cY = ((y * secH) + secH // 2) - 30
    if y == 2:
        cY = ((y * secH) + secH // 2) - 60
    if y == 3:
        cY = ((y * secH) + secH // 2) - 80
    if y == 4:
        cY = ((y * secH) + secH // 2) - 110


    point = [cX, cY]
    return point
def showAnswer(img, myIndex, grading, ans, questions, choices):
    secW = int(img.shape[1] / questions)
    secH = int(img.shape[0] / choices)
    for x in range(0, questions):

        myAns = myIndex[x]
        point = getPointAnswer(secW, secH, myAns, x)
        if (grading[x] == 1):
            myColor = (0, 255, 0)
        else:
            myColor = (0, 0, 255)
            correctAns = ans[x]
            correctPoint = getPointAnswer(secW, secH, correctAns, x)
            if myIndex[x] != -1:
                cv2.circle(img, (correctPoint[0], correctPoint[1]), 30, (0, 255, 0), cv2.FILLED)
            else:
                cv2.circle(img, (correctPoint[0], correctPoint[1]), 30, (0, 100, 255), cv2.FILLED)
        if myIndex[x] != -1:
            cv2.circle(img, (point[0], point[1]), 30, myColor, cv2.FILLED)
    return img

def restoreImg(img, boxes, stack):
    height, width = img.shape[:2]
    rows = 6
    cols = 4
    count = 0
    piece_height = height // rows
    piece_width = width // cols
    for y in range(cols):
        for x in range(rows):
            x_start = piece_width * y + (0 if y == 0 else 10)
            x_end = x_start + piece_width - (0 if y == cols - 1 else 15)
            y_start = x * piece_height
            y_end = y_start + piece_height

            width_box = x_end - (x_start + 20)
            height_box = y_end - y_start
            boxes_resized = cv2.resize(boxes[count], (width_box, height_box))
            img[y_start:y_end, x_start + 20:x_end] = boxes_resized
            count += 1
            if count ==  stack:
                break
        if count == stack:
            break
    return img

def splitMDD(img):
    height, width = img.shape[:2]
    rows = 10
    cols = 6
    piece_height = height // rows
    piece_width = width // cols
    boxes = []
    for x in range(cols):
        for y in range(rows):
            x_start = piece_width * x
            x_end = x_start + piece_width
            y_start = y * piece_height
            y_end = y_start + piece_height
            piece = img[y_start:y_end, x_start:x_end]
            boxes.append(piece)
    return boxes

def splitMD(img):
    height, width = img.shape[:2]
    rows = 10
    cols = 3
    piece_height = height // rows
    piece_width = width // cols
    boxes = []
    for x in range(cols):
        for y in range(rows):
            x_start = piece_width * x
            x_end = x_start + piece_width
            y_start = y * piece_height
            y_end = y_start + piece_height
            piece = img[y_start:y_end, x_start:x_end]
            boxes.append(piece)
    return boxes

def showMDD(img, myIndex, rows, cols):
    secW = int(img.shape[1] / cols)
    secH = int(img.shape[0] / rows)
    cX, cY = 0, 0
    for x in range(0, cols):
        cX = ((x * secW) + secW // 2) - 10
        cY = (myIndex[x] * secH) + secH // 2
        myColor = (0, 255, 0)
        cv2.circle(img, (cX, cY), 35, myColor, cv2.FILLED)
    return img

def FilterContourt(contours):
    newContours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > 30:
            newContours.append(i)
    return newContours