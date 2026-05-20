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
FINAL_ANS = [1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2,
             1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2]

def load_image(image_path):
    pil_img = Image.open(image_path)
    image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return cv2.resize(image, (WIDTH_IMG, HEIGHT_IMG))

def evaluate(image_path):
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

    print("--- SIMPLE THRESHOLD ACCURACY ---")
    for th in [135, 140, 145, 150, 155, 160, 165, 170]:
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
            
        correct = 0
        blanks = 0
        for idx in range(QUESTIONS):
            arr = pixel_vals[idx]
            max_value = np.amax(arr)
            if max_value > 50:
                selected = int(np.argmax(arr))
                if selected == FINAL_ANS[idx]:
                    correct += 1
            else:
                blanks += 1
        print(f"Threshold={th}: Blanks={blanks}, Correct={correct}/40 (Score={round(correct/40*10, 1)})")

    print("\n--- ADAPTIVE THRESHOLD ACCURACY ---")
    for block in [11, 21, 31]:
        for c in [2, 5, 8]:
            for min_px in [30, 40, 50]:
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
                    
                correct = 0
                blanks = 0
                for idx in range(QUESTIONS):
                    arr = pixel_vals[idx]
                    max_value = np.amax(arr)
                    if max_value > min_px:
                        selected = int(np.argmax(arr))
                        if selected == FINAL_ANS[idx]:
                            correct += 1
                    else:
                        blanks += 1
                print(f"Adaptive Block={block}, C={c}, MinPixel={min_px}: Blanks={blanks}, Correct={correct}/40 (Score={round(correct/40*10, 1)})")

if __name__ == '__main__':
    evaluate('MDD.jpg')
