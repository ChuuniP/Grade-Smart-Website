import cv2
import numpy as np
from PIL import Image
import os
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
QUESTIONS = 40
CHOICES = 4

def test_adaptive(image_path, block, c, min_pixel_threshold=40):
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
    
    imgThresh = cv2.adaptiveThreshold(
        imgCvt, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, block, c
    )
        
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
    choice_labels = ['A', 'B', 'C', 'D']
    for idx in range(QUESTIONS):
        arr = pixel_vals[idx]
        max_value = np.amax(arr)
        if max_value > min_pixel_threshold:
            selected = int(np.argmax(arr))
            student_answers.append(choice_labels[selected])
        else:
            student_answers.append('Bỏ trống')
            
    return student_answers

image_path = 'e:/Antigravity/Grade Smart/backend/MDD.jpg'

for block in [11, 21, 31]:
    for c in [2, 5, 8]:
        ans = test_adaptive(image_path, block, c)
        print(f"Block={block}, C={c}:")
        print(" ".join(f"{i+1}:{ans[i]}" for i in range(20)))
        print(" ".join(f"{i+1}:{ans[i]}" for i in range(20, 40)))
        print("-" * 40)
