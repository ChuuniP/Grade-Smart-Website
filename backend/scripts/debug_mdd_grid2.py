import cv2
import numpy as np
import os
import sys

root = r'e:\Antigravity\Grade Smart\\backend\\ref'
os.chdir(root)
sys.path.insert(0, os.getcwd())
import solveImg as si
import support as sp

WIDTH_IMG = 500
HEIGHT_IMG = 700
img = cv2.imread(r'MDD.jpg')
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgAns = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)
pointContour = np.zeros((4, 2), dtype=np.float32)
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)
pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarp = cv2.warpPerspective(imgAns, matrix, (WIDTH_IMG, HEIGHT_IMG))
perX1, perX2, perY1, perY2 = 20, 490, 35, 675
crop = imgWarp[perY1:perY2, perX1:perX2]
gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
th = 150
thresh = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY_INV)[1]

output_dir = r'e:\Antigravity\Grade Smart\\backend\\ref'
cv2.imwrite(os.path.join(output_dir, 'debug_crop.png'), crop)
cv2.imwrite(os.path.join(output_dir, 'debug_thresh.png'), thresh)
vis = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
h, w = thresh.shape
rows = 2
cols = 4
ph = h // rows
pw = w // cols
for y in range(cols):
    for x in range(rows):
        x_start = pw * y + (0 if y == 0 else 10)
        x_end = x_start + pw - (0 if y == cols - 1 else 15)
        y_start = x * ph
        y_end = y_start + ph
        cv2.rectangle(vis, (x_start, y_start), (x_end, y_end), (0, 255, 0), 1)
        for ry in range(1, 15):
            yy = y_start + ry * (ph // 15)
            cv2.line(vis, (x_start, yy), (x_end, yy), (255, 0, 0), 1)
        for cx in range(1, 4):
            xx = x_start + cx * ((x_end - x_start) // 4)
            cv2.line(vis, (xx, y_start), (xx, y_end), (255, 0, 0), 1)
cv2.imwrite(os.path.join(output_dir, 'debug_grid.png'), vis)
print('saved debug_crop.png debug_thresh.png debug_grid.png to', output_dir)
