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

def compare(image_path):
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

    choice_labels = ['A', 'B', 'C', 'D']

    methods = {
        'Thresh_135': lambda: cv2.threshold(imgCvt, 135, 255, cv2.THRESH_BINARY_INV)[1],
        'Thresh_150': lambda: cv2.threshold(imgCvt, 150, 255, cv2.THRESH_BINARY_INV)[1],
        'Thresh_155': lambda: cv2.threshold(imgCvt, 155, 255, cv2.THRESH_BINARY_INV)[1],
        'Thresh_160': lambda: cv2.threshold(imgCvt, 160, 255, cv2.THRESH_BINARY_INV)[1],
        'Adapt_11_2': lambda: cv2.adaptiveThreshold(imgCvt, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2),
        'Adapt_21_2': lambda: cv2.adaptiveThreshold(imgCvt, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 2),
        'Adapt_31_2': lambda: cv2.adaptiveThreshold(imgCvt, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 2),
    }

    results = {}
    for name, method in methods.items():
        imgTh = method()
        boxes = sp.splitImg(imgTh)
        ans_images = sp.splitAns(boxes)
        
        pixel_vals = np.zeros((QUESTIONS, CHOICES), dtype=np.int32)
        max_cells = QUESTIONS * CHOICES
        for index, image_piece in enumerate(ans_images[:max_cells]):
            total_pixels = cv2.countNonZero(image_piece)
            row = index // CHOICES
            col = index % CHOICES
            pixel_vals[row][col] = total_pixels
            
        student_answers = []
        blanks = 0
        min_pixel = 40
        for idx in range(QUESTIONS):
            arr = pixel_vals[idx]
            max_value = np.amax(arr)
            if max_value > min_pixel:
                selected = int(np.argmax(arr))
                student_answers.append(choice_labels[selected])
            else:
                student_answers.append('-')
                blanks += 1
        results[name] = (blanks, student_answers)

    # Print comparison
    print(f"{'Q':<4} | {'Th_135':<8} | {'Th_150':<8} | {'Th_155':<8} | {'Th_160':<8} | {'Ad_11_2':<8} | {'Ad_21_2':<8} | {'Ad_31_2':<8}")
    print("-" * 78)
    for i in range(QUESTIONS):
        row_str = f"Q{i+1:<2} | "
        for name in methods.keys():
            val = results[name][1][i]
            row_str += f"{val:<8} | "
        print(row_str[:-3])

    print("-" * 78)
    blanks_str = f"{'Blk':<4} | "
    for name in methods.keys():
        blanks_str += f"{results[name][0]:<8} | "
    print(blanks_str[:-3])

if __name__ == '__main__':
    compare('MDD.jpg')
