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
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = mod.sp.rectContour(contours)
pointContour = np.zeros((4, 2))
img, pointContour = mod.si.TakeImgAnswer(img, pointContour, contours)
pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [mod.WIDTH_IMG, 0], [0, mod.HEIGHT_IMG], [mod.WIDTH_IMG, mod.HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarpColored = cv2.warpPerspective(img, matrix, (mod.WIDTH_IMG, mod.HEIGHT_IMG))
perX1, perX2, perY1, perY2 = 20, 490, 35, 685
imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(imgCvt, 140, 255, cv2.THRESH_BINARY_INV)[1]
imgOverlay = cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR)

boxes = mod.sp.splitImg120(imgThresh)
for bi, box in enumerate(boxes):
    h, w = box.shape[:2]
    row_h = h // 15
    col_w = w // mod.CHOICES
    x0 = (bi % 4) * (imgOverlay.shape[1] // 4)
    y0 = (bi // 4) * (imgOverlay.shape[0] // 2)
    for r in range(15):
        for c in range(mod.CHOICES):
            start_x = x0 + c * col_w + 42 if True else x0 + c*col_w
            start_y = y0 + r * row_h + (-5 if (bi%2)==0 and r==0 else 0)
            end_x = start_x + col_w
            end_y = start_y + row_h
            cv2.rectangle(imgOverlay, (max(0,start_x), max(0,start_y)), (min(imgOverlay.shape[1]-1,end_x), min(imgOverlay.shape[0]-1,end_y)), (0,255,0), 1)

# Save the overlay image
outpath = Path(__file__).resolve().parent / 'debug_overlay.png'
cv2.imwrite(str(outpath), imgOverlay)
print('Saved debug overlay to', outpath)
