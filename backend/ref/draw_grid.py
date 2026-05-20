import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(__file__))
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700

image_path = 'MDD.jpg'

img = cv2.imread(image_path)
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgAns = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)

if len(contours) == 0:
    print("Error: No contours found!")
    sys.exit(1)
    
pointContour = np.zeros((4, 2), dtype=np.float32)
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)

pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarpColored = cv2.warpPerspective(imgAns, matrix, (WIDTH_IMG, HEIGHT_IMG))

# Crop the answer region
perX1, perX2, perY1, perY2 = 20, 490, 35, 685
imgPer = imgWarpColored[perY1:perY2, perX1:perX2].copy()

# Let's draw the grid lines on imgPer based on splitImg and splitAns
height, width = imgPer.shape[:2]
rows = 2
cols = 4
piece_height = height // rows
piece_width = width // cols

for y in range(cols):
    for x in range(rows):
        x_start = piece_width * y + (0 if y == 0 else 10)
        x_end = x_start + piece_width - (0 if y == cols - 1 else 15)
        y_start = x * piece_height
        y_end = y_start + piece_height
        
        # Draw box boundary in red
        cv2.rectangle(imgPer, (x_start + 20, y_start), (x_end, y_end), (0, 0, 255), 1)
        
        # Draw individual question cell boundaries in green
        box_width = x_end - (x_start + 20)
        box_height = y_end - y_start
        cell_w = box_width / 4
        cell_h = box_height / 5
        
        for q_row in range(5):
            for choice_col in range(4):
                c_x1 = int(x_start + 20 + choice_col * cell_w)
                c_x2 = int(x_start + 20 + (choice_col + 1) * cell_w)
                c_y1 = int(y_start + q_row * cell_h)
                c_y2 = int(y_start + (q_row + 1) * cell_h)
                cv2.rectangle(imgPer, (c_x1, c_y1), (c_x2, c_y2), (0, 255, 0), 1)

cv2.imwrite('debug_crops/grid_debug.jpg', imgPer)
print("Grid debug image saved to debug_crops/grid_debug.jpg")
