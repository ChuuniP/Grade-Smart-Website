import cv2
import numpy as np
import os
import sys

# Append paths
sys.path.append(os.path.dirname(__file__))
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
QUESTIONS = 40
CHOICES = 4
FINAL_ANS = [1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2,
             1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2]

image_path = 'e:/Antigravity/Grade Smart/backend/MDD.jpg'
img = cv2.imread(image_path)
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgAns = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)

contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
import support as sp
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

def splitImg_custom(img, left_offset):
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
            # Test left_offset instead of 20
            piece = img[y_start:y_end, x_start + left_offset:x_end]
            boxes.append(piece)
    return boxes

def splitAns_custom(boxes):
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

# Sweep left_offset and threshold
print(f"{'Offset':<8} | {'Thresh':<8} | {'MinPixel':<8} | {'Blanks':<8} | {'Correct':<8}")
print("-" * 55)
for offset in range(20, 42, 2):
    for th in [135, 140, 145, 150, 155]:
        imgThresh = cv2.threshold(imgCvt, th, 255, cv2.THRESH_BINARY_INV)[1]
        boxes = splitImg_custom(imgThresh, offset)
        ans_images = splitAns_custom(boxes)
        
        pixel_vals = np.zeros((QUESTIONS, CHOICES), dtype=np.int32)
        for index, cell in enumerate(ans_images[:160]):
            total_pixels = cv2.countNonZero(cell)
            row = index // CHOICES
            col = index % CHOICES
            pixel_vals[row][col] = total_pixels
            
        for mp in [15, 20, 25, 30]:
            correct = 0
            blanks = 0
            for idx in range(QUESTIONS):
                arr = pixel_vals[idx]
                max_value = np.amax(arr)
                if max_value > mp:
                    selected = int(np.argmax(arr))
                    if selected == FINAL_ANS[idx]:
                        correct += 1
                else:
                    blanks += 1
            if correct > 10:
                print(f"{offset:<8} | {th:<8} | {mp:<8} | {blanks:<8} | {correct:<8}/40")
