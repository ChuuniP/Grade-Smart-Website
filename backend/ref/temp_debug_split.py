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
pointContour = np.zeros((4,2),dtype=np.float32)
img2, pointContour = si.TakeImgAnswer(img.copy(), pointContour, contours)
pt1=np.float32([pointContour[0],pointContour[1],pointContour[2],pointContour[3]])
pt2=np.float32([[0,0],[WIDTH_IMG,0],[0,HEIGHT_IMG],[WIDTH_IMG,HEIGHT_IMG]])
matrix=cv2.getPerspectiveTransform(pt1,pt2)
imgWarp=cv2.warpPerspective(img, matrix, (WIDTH_IMG,HEIGHT_IMG))
perX1,perX2,perY1,perY2=20,490,35,685
imgPer=imgWarp[perY1:perY2,perX1:perX2]
imgCvt=cv2.cvtColor(imgPer,cv2.COLOR_BGR2GRAY)
imgThresh=cv2.threshold(imgCvt, 135, 255, cv2.THRESH_BINARY_INV)[1]

vis = cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR)
height, width = imgThresh.shape[:2]
rows = 2
cols = 4
piece_height = height // rows
piece_width = width // cols
for y in range(cols):
    for x in range(rows):
        col_start = piece_width * y
        left_offset = 38
        choices_width = 65
        x_start = col_start + left_offset
        x_end = x_start + choices_width
        y_start = x * piece_height
        y_end = y_start + piece_height
        cv2.rectangle(vis, (x_start, y_start), (x_end, y_end), (0,255,0), 1)
        cv2.putText(vis, str(y*rows+x), (x_start+3, y_start+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0),1)
        # show cell boundaries for this box
        bw = x_end - x_start
        bh = y_end - y_start
        for row in range(15):
            for col in range(4):
                sx = x_start + int(col*bw/4)
                ex = x_start + int((col+1)*bw/4)
                sy = y_start + int(row*bh/15)
                ey = y_start + int((row+1)*bh/15)
                cv2.rectangle(vis, (sx, sy), (ex, ey), (255,0,0),1)

cv2.imwrite('debug_split_current.png', vis)
print('saved debug_split_current.png')
