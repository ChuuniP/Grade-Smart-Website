import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(__file__))
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
CHOICES = 4

# Target: 40 questions
FINAL_ANS = [1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2,
             1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2]

# Standard OMR helper functions modified to use 15 questions per box
def splitImg120(img):
    height, width = img.shape[:2]
    rows = 2
    cols = 4
    piece_height = height // rows
    piece_width = width // cols
    boxes = []
    # y = cols, x = rows
    for y in range(cols):
        for x in range(rows):
            x_start = piece_width * y + (0 if y == 0 else 10)
            x_end = x_start + piece_width - (0 if y == cols - 1 else 15)
            y_start = x * piece_height
            y_end = y_start + piece_height
            # Add a slight padding to avoid border lines
            piece = img[y_start:y_end, x_start + 20:x_end]
            boxes.append(piece)
    return boxes

def splitAns120(boxes):
    rows = 15 # 15 questions per box!
    cols = 4  # A, B, C, D
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

# Load and warp
image_path = 'MDD.jpg'
img = cv2.imread(image_path)
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgAns = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)

# Import rectContour from support
import support as sp
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)

if len(contours) == 0:
    print("No contours found")
    sys.exit(1)

pointContour = np.zeros((4, 2), dtype=np.float32)
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)

pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarpColored = cv2.warpPerspective(imgAns, matrix, (WIDTH_IMG, HEIGHT_IMG))

# Test combinations of coordinates and threshold
best_score = 0
best_results = []
best_params = {}

print("Testing 120-layout with different crop parameters and thresholds:")
# We can search coordinates around standard ones:
for x1 in [10, 15, 20, 25]:
    for x2 in [480, 485, 490, 495]:
        for y1 in [20, 25, 30, 35, 40]:
            for y2 in [675, 680, 685, 690, 695]:
                imgPer = imgWarpColored[y1:y2, x1:x2]
                imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
                
                for th in [130, 135, 140, 150, 160]:
                    imgThresh = cv2.threshold(imgCvt, th, 255, cv2.THRESH_BINARY_INV)[1]
                    
                    boxes = splitImg120(imgThresh)
                    ans_images = splitAns120(boxes)
                    
                    # Total questions on sheet = 8 * 15 = 120
                    # We only grade the first 40 questions. But wait! How are they ordered?
                    # The boxes are:
                    # box 0 (Q1-15), box 1 (Q16-30), box 2 (Q31-45), box 3 (Q46-60)...
                    # Since we want Q1 to Q40:
                    # Q1-15 is the 15 questions of box 0.
                    # Q16-30 is the 15 questions of box 1.
                    # Q31-40 are the first 10 questions of box 2.
                    # So we map the 40 questions as:
                    # - 0 to 14 -> box 0 (indices 0 to 14)
                    # - 15 to 29 -> box 1 (indices 15 to 29)
                    # - 30 to 39 -> box 2 (indices 30 to 39)
                    # Wait! In our splitAns120 output, the order of elements is:
                    # box 0 (60 elements: 15 questions * 4 choices)
                    # box 1 (60 elements: 15 questions * 4 choices)
                    # box 2 (60 elements: 15 questions * 4 choices)
                    # box 3 ...
                    # So the first 15 questions are indices 0 to 14.
                    # The next 15 questions (Q16-30) are box 1, which are indices 15 to 29.
                    # The next 15 questions (Q31-45) are box 2, which are indices 30 to 44.
                    # So our Q1 to Q40 are exactly the first 40 questions in the flat array!
                    
                    pixel_vals = np.zeros((40, CHOICES), dtype=np.int32)
                    for index, image_piece in enumerate(ans_images[:160]):
                        total_pixels = cv2.countNonZero(image_piece)
                        row = index // CHOICES
                        col = index % CHOICES
                        pixel_vals[row][col] = total_pixels
                        
                    for mp in [20, 30, 40, 50]:
                        correct = 0
                        detected = []
                        blanks = 0
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
                            best_results = detected
                            best_params = {'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2, 'thresh': th, 'min_pixel': mp, 'blanks': blanks}
                            print(f"New Best 120-Layout: Correct={correct}/40, Blanks={blanks}, Params={best_params}", flush=True)

print("\nDone searching 120-layout.")
print("Best Score:", best_score)
print("Best Params:", best_params)
print("Detected answers:", best_results)
print("Expected answers:", FINAL_ANS)
