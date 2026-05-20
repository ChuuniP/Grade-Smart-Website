import cv2
import numpy as np
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
img = cv2.imread('MDD.jpg')
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)
if len(contours) == 0:
    raise SystemExit('No contours')
pointContour = np.zeros((4, 2), dtype=np.float32)
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)
pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarp = cv2.warpPerspective(img, matrix, (WIDTH_IMG, HEIGHT_IMG))
perX1, perX2, perY1, perY2 = 20, 490, 35, 685
imgPer = imgWarp[perY1:perY2, perX1:perX2]
gray = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)[1]

contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
centroids = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if 50 < area < 3000:
        x,y,w,h = cv2.boundingRect(cnt)
        if 5 < w < 60 and 5 < h < 60:
            M = cv2.moments(cnt)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                centroids.append((cx, cy, area, x, y, w, h))

centroids = sorted(centroids, key=lambda t: (t[1], t[0]))
print('num centroids', len(centroids))
for i, c in enumerate(centroids[:80]):
    print(i, c)

vis = cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR)
for (cx, cy, area, x, y, w, h) in centroids:
    cv2.circle(vis, (cx, cy), 3, (0,255,0), -1)
    cv2.rectangle(vis, (x,y), (x+w, y+h), (0,0,255), 1)
cv2.imwrite('debug_bubbles.png', vis)
print('saved debug_bubbles.png')
