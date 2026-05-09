import cv2
import numpy as np
def TakeImgAnswer(img, pointContour, contours):
    time, a, b, c, d = 0, 0, 0, 0, 0

    ori_x1, ori_x2, ori_x3, ori_x4 = 10, 60, 460, 500
    ori_y1, ori_y2, ori_y3, ori_y4 = 150, 210, 640, 700

    per = 5

    x1, x2, x3, x4 = 10, 60, 460, 500
    y1, y2, y3, y4 = 150, 210, 640, 700

    while (a !=1 or b != 1 or c != 1 or d != 1) or time == 10:
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if a != 1:
                x2 = ori_x2 + (per * time)
                y2 = ori_y2 + (per * time)
                if x1 <= x <= x2 and y1 <= y <= y2 and x1 <= x + w <= x2 and y1 <= y + h <= y2:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    for point in contour:
                        pointContour[0][0], pointContour[0][1] = point[0]
                    a = 1
            if b != 1:
                x3 = ori_x3 - (per * time)
                y2 = ori_y2 + (per * time)
                if x3 <= x <= x4 and y1 <= y <= y2 and x3 <= x + w <= x4 and y1 <= y + h <= y2:
                    cv2.rectangle(img, (x3, y1), (x4, y2), (0, 255, 0), 2)
                    for point in contour:
                        pointContour[1][0], pointContour[1][1] = point[0]
                    b = 1
            if c != 1:
                y3 = ori_y3 - (per * time)
                x2 = ori_x2 + (per * time)
                if x1 <= x <= x2 and y3 <= y <= y4 and x1 <= x + w <= x2 and y3 <= y + h <= y4:
                    cv2.rectangle(img, (x1, y3), (x2, y4), (0, 255, 0), 2)
                    for point in contour:
                        pointContour[2][0], pointContour[2][1] = point[0]
                    c = 1
            if d != 1:
                y3 = ori_y3 - (per * time)
                x3 = ori_x3 - (per * time)
                if x3 <= x <= x4 and y3 <= y <= y4 and x3 <= x + w <= x4 and y3 <= y + h <= y4:
                    cv2.rectangle(img, (x3, y3), (x4, y4), (0, 255, 0), 2)
                    for point in contour:
                        pointContour[3][0], pointContour[3][1] = point[0]
                    d = 1
        time += 1
    return img, pointContour

def TakeImgMDD(img, pointContour, contours):
    time, a, b, c, d = 0, 0, 0, 0, 0

    ori_x1, ori_x2, ori_x3, ori_x4 = 10, 50, 440, 490
    ori_y1, ori_y2, ori_y3, ori_y4 = 0, 50, 170, 250

    per = 5

    x1, x2, x3, x4 = 10, 40, 440, 490
    y1, y2, y3, y4 = 0, 60, 180, 250

    while (a !=1 or b != 1 or c != 1 or d != 1) or time == 10:
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if a != 1:
                x2 = ori_x2 + (per * time)
                y2 = ori_y2 + (per * time)
                if x1 <= x <= x2 and y1 <= y <= y2 and x1 <= x + w <= x2 and y1 <= y + h <= y2:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.drawContours(img, contour, -1, (255, 255, 0), 2)
                    for point in contour:
                        pointContour[0][0], pointContour[0][1] = point[0]
                    a = 1
            if b != 1:
                x3 = ori_x3 - (per * time)
                y2 = ori_y2 + (per * time)
                if x3 <= x <= x4 and y1 <= y <= y2 and x3 <= x + w <= x4 and y1 <= y + h <= y2:
                    cv2.rectangle(img, (x3, y1), (x4, y2), (0, 255, 0), 2)
                    cv2.drawContours(img, contour, -1, (255, 255, 0), 2)
                    for point in contour:
                        pointContour[1][0], pointContour[1][1] = point[0]
                    b = 1
            if c != 1:
                y3 = ori_y3 - (per * time)
                x2 = ori_x2 + (per * time)
                if x1 <= x <= x2 and y3 <= y <= y4 and x1 <= x + w <= x2 and y3 <= y + h <= y4:
                    cv2.rectangle(img, (x1, y3), (x2, y4), (0, 255, 0), 2)
                    cv2.drawContours(img, contour, -1, (255, 255, 0), 2)
                    for point in contour:
                        pointContour[2][0], pointContour[2][1] = point[0]
                    c = 1
            if d != 1:
                y3 = ori_y3 - (per * time)
                x3 = ori_x3 - (per * time)
                if x3 <= x <= x4 and y3 <= y <= y4 and x3 <= x + w <= x4 and y3 <= y + h <= y4:
                    cv2.rectangle(img, (x3, y3), (x4, y4), (0, 255, 0), 2)
                    cv2.drawContours(img, contour, -1, (255, 255, 0), 2)
                    for point in contour:
                        pointContour[3][0], pointContour[3][1] = point[0]
                    d = 1
        time += 1
    return img, pointContour

def TakeImgFinal(img, pointContour, contours):
    time, a, b, c, d = 0, 0, 0, 0, 0

    ori_x1, ori_x2, ori_x3, ori_x4 = 10, 50, 440, 490
    ori_y1, ori_y2, ori_y3, ori_y4 = 0, 50, 640, 700

    per = 5

    x1, x2, x3, x4 = 10, 40, 440, 490
    y1, y2, y3, y4 = 0, 50, 640, 700

    while (a !=1 or b != 1 or c != 1 or d != 1) or time == 10:
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if a != 1:
                x2 = ori_x2 + (per * time)
                y2 = ori_y2 + (per * time)
                if x1 <= x <= x2 and y1 <= y <= y2 and x1 <= x + w <= x2 and y1 <= y + h <= y2:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.drawContours(img, contour, -1, (255, 255, 0), 2)
                    for point in contour:
                        pointContour[0][0], pointContour[0][1] = point[0]
                    a = 1
            if b != 1:
                x3 = ori_x3 - (per * time)
                y2 = ori_y2 + (per * time)
                if x3 <= x <= x4 and y1 <= y <= y2 and x3 <= x + w <= x4 and y1 <= y + h <= y2:
                    cv2.rectangle(img, (x3, y1), (x4, y2), (0, 255, 0), 2)
                    cv2.drawContours(img, contour, -1, (255, 255, 0), 2)
                    for point in contour:
                        pointContour[1][0], pointContour[1][1] = point[0]
                    b = 1
            if c != 1:
                y3 = ori_y3 - (per * time)
                x2 = ori_x2 + (per * time)
                if x1 <= x <= x2 and y3 <= y <= y4 and x1 <= x + w <= x2 and y3 <= y + h <= y4:
                    cv2.rectangle(img, (x1, y3), (x2, y4), (0, 255, 0), 2)
                    cv2.drawContours(img, contour, -1, (255, 255, 0), 2)
                    for point in contour:
                        pointContour[2][0], pointContour[2][1] = point[0]
                    c = 1
            if d != 1:
                y3 = ori_y3 - (per * time)
                x3 = ori_x3 - (per * time)
                if x3 <= x <= x4 and y3 <= y <= y4 and x3 <= x + w <= x4 and y3 <= y + h <= y4:
                    cv2.rectangle(img, (x3, y3), (x4, y4), (0, 255, 0), 2)
                    cv2.drawContours(img, contour, -1, (255, 255, 0), 2)
                    for point in contour:
                        pointContour[3][0], pointContour[3][1] = point[0]
                    d = 1
        time += 1
    return img, pointContour
