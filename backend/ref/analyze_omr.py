import sys
import os
import cv2
import numpy as np
from PIL import Image
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
QUESTIONS = 40
CHOICES = 4

def load_image(image_path):
    pil_img = Image.open(image_path)
    image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return cv2.resize(image, (WIDTH_IMG, HEIGHT_IMG))

def analyze(image_path):
    image = load_image(image_path)
    img = image.copy()
    imgAns = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, 50, 150)
    contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sp.rectContour(contours)
    
    if len(contours) == 0:
        print("No contours")
        return

    pointContour = np.zeros((4, 2), dtype=np.float32)
    img, pointContour = si.TakeImgAnswer(img, pointContour, contours)

    pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
    pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgWarpColored = cv2.warpPerspective(imgAns, matrix, (WIDTH_IMG, HEIGHT_IMG))

    perX1, perX2, perY1, perY2 = 20, 490, 35, 685
    imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
    imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)

    print("--- SIMPLE THRESHOLD ANALYSES ---")
    for th in [110, 120, 130, 135, 140, 150, 160, 170]:
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
            
        blanks = 0
        correct_choices = []
        for idx in range(QUESTIONS):
            arr = pixel_vals[idx]
            max_value = np.amax(arr)
            if max_value > 50:
                selected = int(np.argmax(arr))
                correct_choices.append(selected)
            else:
                blanks += 1
                correct_choices.append(-1)
        print(f"Threshold={th}: Blank count = {blanks}")
        if th == 135 or th == 150 or th == 160:
            print(f"  Pixel values for blank questions (at th={th}):")
            for q_idx in range(QUESTIONS):
                if correct_choices[q_idx] == -1:
                    print(f"    Q{q_idx+1}: {pixel_vals[q_idx].tolist()}")

    print("\n--- OTSU THRESHOLD ANALYSIS ---")
    imgThreshOtsu = cv2.threshold(imgCvt, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    boxes = sp.splitImg(imgThreshOtsu)
    ans_images = sp.splitAns(boxes)
    
    pixel_vals = np.zeros((QUESTIONS, CHOICES), dtype=np.int32)
    max_cells = QUESTIONS * CHOICES
    for index, image_piece in enumerate(ans_images[:max_cells]):
        total_pixels = cv2.countNonZero(image_piece)
        row = index // CHOICES
        col = index % CHOICES
        pixel_vals[row][col] = total_pixels
        
    blanks = 0
    for idx in range(QUESTIONS):
        arr = pixel_vals[idx]
        max_value = np.amax(arr)
        if max_value > 50:
            pass
        else:
            blanks += 1
    print(f"Otsu Threshold: Blank count = {blanks}")

    print("\n--- ADAPTIVE THRESHOLD ANALYSES ---")
    for block in [11, 21, 31]:
        for c in [2, 5, 8]:
            for min_px in [20, 30, 40, 50]:
                imgThreshAd = cv2.adaptiveThreshold(
                    imgCvt, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY_INV, block, c
                )
                boxes = sp.splitImg(imgThreshAd)
                ans_images = sp.splitAns(boxes)
                
                pixel_vals = np.zeros((QUESTIONS, CHOICES), dtype=np.int32)
                max_cells = QUESTIONS * CHOICES
                for index, image_piece in enumerate(ans_images[:max_cells]):
                    total_pixels = cv2.countNonZero(image_piece)
                    row = index // CHOICES
                    col = index % CHOICES
                    pixel_vals[row][col] = total_pixels
                    
                blanks = 0
                for idx in range(QUESTIONS):
                    arr = pixel_vals[idx]
                    max_value = np.amax(arr)
                    if max_value <= min_px:
                        blanks += 1
                print(f"Adaptive Block={block}, C={c}, MinPixel={min_px}: Blank count = {blanks}")

if __name__ == '__main__':
    analyze('MDD.jpg')
