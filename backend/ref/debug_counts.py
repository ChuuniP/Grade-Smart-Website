import importlib.util
from pathlib import Path
import cv2
import numpy as np

path = Path(__file__).resolve().parent / 'mainOmr.py'
spec = importlib.util.spec_from_file_location('mainOmr', path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

image_path = Path(__file__).resolve().parent / 'MDD.jpg'
image = mod.load_image(str(image_path))
img = image.copy()
imgAns = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = mod.sp.rectContour(contours)
pointContour = np.zeros((4, 2))
img, pointContour = mod.si.TakeImgAnswer(img, pointContour, contours)
pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [mod.WIDTH_IMG, 0], [0, mod.HEIGHT_IMG], [mod.WIDTH_IMG, mod.HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarpColored = cv2.warpPerspective(imgAns, matrix, (mod.WIDTH_IMG, mod.HEIGHT_IMG))
perX1, perX2, perY1, perY2 = 20, 490, 35, 685
imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(imgCvt, 140, 255, cv2.THRESH_BINARY_INV)[1]

boxes = mod.sp.splitImg120(imgThresh)
print('boxes', len(boxes))
for i, box in enumerate(boxes):
    print(f'box {i}: shape {box.shape}')

ans_images = []
for image in boxes:
    height, width = image.shape[:2]
    row_height = height // 15
    col_width = width // mod.CHOICES
    for row in range(15):
        for col in range(mod.CHOICES):
            start_x = col * col_width
            end_x = start_x + col_width
            start_y = row * row_height
            end_y = start_y + row_height
            ans_images.append(image[start_y:end_y, start_x:end_x])

pixel_vals = np.zeros((mod.QUESTIONS, mod.CHOICES), dtype=np.int32)
countC = 0
countR = 0
for image_piece in ans_images[:mod.QUESTIONS*mod.CHOICES]:
    total_pixels = cv2.countNonZero(image_piece)
    if countR < mod.QUESTIONS:
        pixel_vals[countR][countC] = total_pixels
    countC += 1
    if countC == mod.CHOICES:
        countR += 1
        countC = 0

for q in range(mod.QUESTIONS):
    print(q+1, pixel_vals[q].tolist(), 'pred', int(np.argmax(pixel_vals[q])) if np.max(pixel_vals[q]) > mod.BLANK_PIXEL_THRESHOLD else -1, 'exp', mod.FINAL_ANS[q])
