import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(__file__))
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
QUESTIONS = 40
CHOICES = 4
FINAL_ANS = [1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2,
             1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2]

image_path = 'MDD.jpg'

# 1. Load image and do perspective transform ONCE
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
pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, height_img if 'height_img' in locals() else HEIGHT_IMG], [WIDTH_IMG, height_img if 'height_img' in locals() else HEIGHT_IMG]])
pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarpColored = cv2.warpPerspective(imgAns, matrix, (WIDTH_IMG, HEIGHT_IMG))

best_score = 0
best_params = {}

print("Searching parameters...")

# Pre-define ranges for fast iteration
x1_range = [15, 20, 25]
x2_range = [485, 490, 495]
y1_range = [30, 35, 40]
y2_range = [680, 685, 690]
thresh_range = [130, 135, 140, 150, 160]
min_pixel_range = [30, 40, 50]

for x1 in x1_range:
    for x2 in x2_range:
        for y1 in y1_range:
            for y2 in y2_range:
                # Crop image once for this coordinate combination
                imgPer = imgWarpColored[y1:y2, x1:x2]
                imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
                
                for th in thresh_range:
                    imgThresh = cv2.threshold(imgCvt, th, 255, cv2.THRESH_BINARY_INV)[1]
                    boxes = sp.splitImg(imgThresh)
                    ans_images = sp.splitAns(boxes)
                    
                    pixel_vals = np.zeros((QUESTIONS, CHOICES), dtype=np.int32)
                    max_cells = QUESTIONS * CHOICES
                    for index, image_piece in enumerate(ans_images[:max_cells]):
                        total_pixels = cv2.countNonZero(image_piece)
                        row = index // CHOICES
                        col = index % CHOICES
                        pixel_vals[row][col] = total_pixels
                    
                    for mp in min_pixel_range:
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
                                
                        if correct > best_score:
                            best_score = correct
                            best_params = {'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2, 'thresh': th, 'min_pixel': mp, 'blanks': blanks}
                            print(f"New Best: Correct={correct}/40, Blanks={blanks}, Params={best_params}", flush=True)

print("\nDone searching.", flush=True)
print("Best Score:", best_score, flush=True)
print("Best Params:", best_params, flush=True)
