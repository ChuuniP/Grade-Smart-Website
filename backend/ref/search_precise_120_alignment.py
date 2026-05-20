import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(__file__))
import solveImg as si
import support as sp

WIDTH_IMG = 500
HEIGHT_IMG = 700
CHOICES = 4

FINAL_ANS = [1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2,
             1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2]

image_path = 'MDD.jpg'
img = cv2.imread(image_path)
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgAns = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)

contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)

if len(contours) == 0:
    print("No contours")
    sys.exit(1)

pointContour = np.zeros((4, 2), dtype=np.float32)
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)

pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarpColored = cv2.warpPerspective(imgAns, matrix, (WIDTH_IMG, HEIGHT_IMG))

# Pre-warp the answer region
perX1, perX2, perY1, perY2 = 20, 490, 35, 685
imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)

best_score = 0
best_params = {}

print("Searching precise 120-layout alignments...")

# Width of answer region is 470.
# Height of answer region is 650.
# There are 4 columns.
# We will search:
# - col_start_shift: shift to the right for the start of each column (from 15 to 45 pixels)
# - col_width: width of each column containing choices A, B, C, D (from 60 to 90 pixels)
# - y_top_padding: vertical top padding (from -10 to +15 pixels)
# - y_bottom_padding: vertical bottom padding (from -15 to +10 pixels)

for th in [135, 140, 150, 155, 160]:
    imgThresh = cv2.threshold(imgCvt, th, 255, cv2.THRESH_BINARY_INV)[1]
    
    for start_shift in range(20, 50, 2):
        for col_w in range(60, 90, 2):
            for y_top in [-10, -5, 0, 5, 10]:
                for y_bottom in [-10, -5, 0, 5, 10]:
                    
                    height, width = imgThresh.shape[:2]
                    piece_height = height // 2
                    piece_width = width // 4
                    
                    ans_images = []
                    for y in range(4): # 4 columns
                        for x in range(2): # 2 rows (top/bottom)
                            col_start = piece_width * y
                            box_x1 = col_start + start_shift
                            box_x2 = box_x1 + col_w
                            
                            box_y1 = x * piece_height + (y_top if x == 0 else 0)
                            box_y2 = box_y1 + piece_height + (y_bottom if x == 1 else 0)
                            
                            # Bound checks
                            box_x1 = max(0, min(width, box_x1))
                            box_x2 = max(0, min(width, box_x2))
                            box_y1 = max(0, min(height, box_y1))
                            box_y2 = max(0, min(height, box_y2))
                            
                            box = imgThresh[box_y1:box_y2, box_x1:box_x2]
                            
                            box_h, box_w = box.shape[:2]
                            cell_h = box_h / 15.0
                            cell_w = box_w / 4.0
                            
                            for q in range(15):
                                for choice in range(4):
                                    cy1 = int(q * cell_h)
                                    cy2 = int((q + 1) * cell_h)
                                    cx1 = int(choice * cell_w)
                                    cx2 = int((choice + 1) * cell_w)
                                    cell = box[cy1:cy2, cx1:cx2]
                                    ans_images.append(cell)
                                    
                    # Grade first 40 questions (Box 0 Q1-15, Box 1 Q16-30, Box 2 Q31-40)
                    pixel_vals = np.zeros((40, CHOICES), dtype=np.int32)
                    for index, cell in enumerate(ans_images[:160]):
                        total_pixels = cv2.countNonZero(cell)
                        row = index // CHOICES
                        col = index % CHOICES
                        pixel_vals[row][col] = total_pixels
                        
                    for mp in [15, 20, 25, 30, 40]:
                        correct = 0
                        blanks = 0
                        detected = []
                        for idx in range(40):
                            arr = pixel_vals[idx]
                            max_value = np.amax(arr)
                            if max_value > mp:
                                selected = int(np.argmax(arr))
                                detected.append(selected)
                                if selected == FINAL_ANS[idx]:
                                    correct += 1
                            else:
                                detected.append(-1)
                                blanks += 1
                                
                        if correct > best_score:
                            best_score = correct
                            best_params = {
                                'thresh': th,
                                'start_shift': start_shift,
                                'col_w': col_w,
                                'y_top': y_top,
                                'y_bottom': y_bottom,
                                'min_pixel': mp,
                                'blanks': blanks
                            }
                            print(f"New Best Precise: Correct={correct}/40, Blanks={blanks}, Params={best_params}", flush=True)
                            if correct == 40:
                                print("FOUND 100% ACCURACY!", flush=True)
                                print("Detected answers:", detected, flush=True)
                                sys.exit(0)

print("\nDone searching precise 120-layout alignments.")
print("Best Score:", best_score)
print("Best Params:", best_params)
