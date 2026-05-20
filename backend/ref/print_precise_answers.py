import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(__file__))
import solveImg as si
import support as sp

WIDTH_IMG = 500
HEIGHT_IMG = 700
QUESTIONS = 40
CHOICES = 4

image_path = 'e:/Antigravity/Grade Smart/backend/MDD.jpg'
img = cv2.imread(image_path)
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
imgWarpColored = cv2.warpPerspective(imgAns, matrix, (WIDTH_IMG, HEIGHT_IMG))

perX1, perX2, perY1, perY2 = 20, 490, 35, 685
imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)

choice_labels = ['A', 'B', 'C', 'D']

def print_precise(left_offset, choices_width, th, min_px):
    imgThresh = cv2.threshold(imgCvt, th, 255, cv2.THRESH_BINARY_INV)[1]
    
    height, width = imgThresh.shape[:2]
    piece_height = height // 2
    piece_width = width // 4
    
    ans_images = []
    for y in range(4): # 4 columns
        for x in range(2): # 2 rows
            col_start = piece_width * y
            box_x1 = col_start + left_offset
            box_x2 = box_x1 + choices_width
            
            box_y1 = x * piece_height
            box_y2 = box_y1 + piece_height
            
            box = imgThresh[box_y1:box_y2, box_x1:box_x2]
            
            box_h, box_w = box.shape[:2]
            cell_h = box_h / 5.0
            cell_w = box_w / 4.0
            
            for q in range(5):
                for choice in range(4):
                    cy1 = int(q * cell_h)
                    cy2 = int((q + 1) * cell_h)
                    cx1 = int(choice * cell_w)
                    cx2 = int((choice + 1) * cell_w)
                    cell = box[cy1:cy2, cx1:cx2]
                    ans_images.append(cell)
                    
    pixel_vals = np.zeros((QUESTIONS, CHOICES), dtype=np.int32)
    for index, cell in enumerate(ans_images[:160]):
        total_pixels = cv2.countNonZero(cell)
        row = index // CHOICES
        col = index % CHOICES
        pixel_vals[row][col] = total_pixels
        
    student_answers = []
    for idx in range(QUESTIONS):
        arr = pixel_vals[idx]
        max_value = np.amax(arr)
        if max_value > min_px:
            selected = int(np.argmax(arr))
            student_answers.append(choice_labels[selected])
        else:
            student_answers.append('Blank')
            
    print(f"\n--- ANSWERS AT Offset={left_offset}, Width={choices_width}, Thresh={th}, MinPixel={min_px} ---")
    print(" ".join(f"{i+1}:{student_answers[i]}" for i in range(20)))
    print(" ".join(f"{i+1}:{student_answers[i]}" for i in range(20, 40)))

# Test a few good candidate coordinates
print_precise(38, 65, 135, 15)
print_precise(38, 65, 140, 15)
print_precise(40, 64, 140, 15)
print_precise(42, 62, 140, 15)
