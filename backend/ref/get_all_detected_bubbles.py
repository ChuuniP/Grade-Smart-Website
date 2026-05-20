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

perX1, perX2, perY1, perY2 = 20, 490, 35, 685
imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)

# Standard split function for 120-layout
def splitImg120(img):
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
            piece = img[y_start:y_end, x_start + 20:x_end]
            boxes.append(piece)
    return boxes

def splitAns120(boxes):
    rows = 15
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

# We will test a few threshold and padding parameters
for th in [135, 140, 150, 160]:
    imgThresh = cv2.threshold(imgCvt, th, 255, cv2.THRESH_BINARY_INV)[1]
    
    # Let's save a thresholded visual debug for this specific threshold to see if bubbles are clear
    cv2.imwrite(f'debug_crops/thresh_{th}.jpg', imgThresh)
    
    boxes = splitImg120(imgThresh)
    ans_images = splitAns120(boxes)
    
    pixel_vals = np.zeros((120, CHOICES), dtype=np.int32)
    for index, cell in enumerate(ans_images):
        total_pixels = cv2.countNonZero(cell)
        row = index // CHOICES
        col = index % CHOICES
        pixel_vals[row][col] = total_pixels
        
    for mp in [20, 30]:
        detected = []
        for idx in range(120):
            arr = pixel_vals[idx]
            max_value = np.amax(arr)
            if max_value > mp:
                selected = int(np.argmax(arr))
                detected.append(selected)
            else:
                detected.append(-1)
                
        # Map to letters
        choice_labels = ['A', 'B', 'C', 'D']
        detected_letters = [choice_labels[x] if x != -1 else '-' for x in detected]
        
        print(f"--- Thresh={th}, MinPixel={mp} ---")
        print("Col 1 (Q1-30):")
        print("Q1-15 :", " ".join(f"{i+1}:{detected_letters[i]}" for i in range(15)))
        print("Q16-30:", " ".join(f"{i+1}:{detected_letters[i]}" for i in range(15, 30)))
        print("Col 2 (Q31-60):")
        print("Q31-45:", " ".join(f"{i+1}:{detected_letters[i]}" for i in range(30, 45)))
        print("Q46-60:", " ".join(f"{i+1}:{detected_letters[i]}" for i in range(45, 60)))
        print("-" * 50)
