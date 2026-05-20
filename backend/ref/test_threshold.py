import cv2
import numpy as np
import os
from PIL import Image
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
QUESTIONS = 40
CHOICES = 4

def test_on_image(image_path, thresh_val=135, use_adaptive=False, adaptive_block=21, adaptive_c=5, min_pixel_threshold=50):
    pil_img = Image.open(image_path)
    image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    resized_img = cv2.resize(image, (WIDTH_IMG, HEIGHT_IMG))
    
    img = resized_img.copy()
    imgAns = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, 50, 150)
    contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sp.rectContour(contours)
    
    if len(contours) == 0:
        return "No contours found"
        
    pointContour = np.zeros((4, 2), dtype=np.float32)
    img, pointContour = si.TakeImgAnswer(img, pointContour, contours)
    
    pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
    pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgWarpColored = cv2.warpPerspective(imgAns, matrix, (WIDTH_IMG, HEIGHT_IMG))
    
    perX1, perX2, perY1, perY2 = 20, 490, 35, 685
    imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
    imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
    
    # Try threshold
    if use_adaptive:
        imgThresh = cv2.adaptiveThreshold(
            imgCvt, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, adaptive_block, adaptive_c
        )
    else:
        imgThresh = cv2.threshold(imgCvt, thresh_val, 255, cv2.THRESH_BINARY_INV)[1]
        
    boxes = sp.splitImg(imgThresh)
    ans_images = sp.splitAns(boxes)
    
    pixel_vals = np.zeros((QUESTIONS, CHOICES), dtype=np.int32)
    max_cells = QUESTIONS * CHOICES
    for index, image_piece in enumerate(ans_images[:max_cells]):
        total_pixels = cv2.countNonZero(image_piece)
        row = index // CHOICES
        col = index % CHOICES
        pixel_vals[row][col] = total_pixels
        
    student_answers = []
    blank_count = 0
    for idx in range(QUESTIONS):
        arr = pixel_vals[idx]
        max_value = np.amax(arr)
        if max_value > min_pixel_threshold:
            selected = int(np.argmax(arr))
            student_answers.append(selected)
        else:
            student_answers.append(-1)
            blank_count += 1
            
    return blank_count, student_answers

image_path = 'e:/Antigravity/Grade Smart/backend/MDD.jpg'

print("--- Testing Global Threshold Values ---")
for t in [110, 120, 130, 135, 140, 150, 160, 170, 180]:
    res = test_on_image(image_path, thresh_val=t, use_adaptive=False, min_pixel_threshold=40)
    if isinstance(res, str):
        print(f"Thresh {t}: {res}")
    else:
        print(f"Thresh {t}: Blanks = {res[0]}, Answers = {res[1]}")

print("\n--- Testing Adaptive Threshold ---")
for block in [11, 15, 21, 31, 51]:
    for c in [2, 5, 8, 10]:
        res = test_on_image(image_path, use_adaptive=True, adaptive_block=block, adaptive_c=c, min_pixel_threshold=40)
        if isinstance(res, str):
            print(f"Adaptive Block {block} C {c}: {res}")
        else:
            print(f"Adaptive Block {block} C {c}: Blanks = {res[0]}")
