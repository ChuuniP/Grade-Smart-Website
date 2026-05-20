import cv2
import numpy as np
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
FINAL_ANS = [1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2,1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2]

img = cv2.imread('MDD.jpg')
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)
pointContour = np.zeros((4, 2), dtype=np.float32)
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)
pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarp = cv2.warpPerspective(img, matrix, (WIDTH_IMG, HEIGHT_IMG))
imgPer = imgWarp[35:685,20:490]
gray = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)[1]
boxes = sp.splitImg120(imgThresh)
print('num boxes', len(boxes))
for i, box in enumerate(boxes):
    h,w = box.shape[:2]
    print('box', i, 'shape', (h,w))

# current mainOmr mapping: first 40 cells from all boxes in order (boxes across)
# proposed correct mapping: boxes 0,1,2 with only first 10 rows of box2
pixel_vals_current = np.zeros((40,4), dtype=int)
idx = 0
for box in boxes:
    h,w = box.shape[:2]
    row_h = h // 15
    col_w = w // 4
    for r in range(15):
        for c in range(4):
            if idx < 40:
                cell = box[r*row_h:(r+1)*row_h, c*col_w:(c+1)*col_w]
                pixel_vals_current[idx,c] = cv2.countNonZero(cell)
            idx += 1

current = []
for i in range(40):
    arr = pixel_vals_current[i]
    current.append(int(np.argmax(arr)) if arr.max() > 15 else -1)
print('current mapping answers', current)
print('current score', sum(1 for i,a in enumerate(current) if a == FINAL_ANS[i]))

# proposed mapping
pixel_vals_prop = np.zeros((40,4), dtype=int)
q=0
for bidx in [0,1,2]:
    box = boxes[bidx]
    h,w = box.shape[:2]
    row_h = h // 15
    col_w = w // 4
    max_rows = 15 if bidx in [0,1] else 10
    for r in range(max_rows):
        for c in range(4):
            if q >= 40:
                break
            cell = box[r*row_h:(r+1)*row_h, c*col_w:(c+1)*col_w]
            pixel_vals_prop[q,c] = cv2.countNonZero(cell)
            q += 1
        if q >= 40:
            break

prop = []
for i in range(40):
    arr = pixel_vals_prop[i]
    prop.append(int(np.argmax(arr)) if arr.max() > 15 else -1)
print('proposed mapping answers', prop)
print('proposed score', sum(1 for i,a in enumerate(prop) if a == FINAL_ANS[i]))

# debug first 40 counts
for i in range(40):
    print(i+1, pixel_vals_prop[i].tolist(), '->', prop[i], 'ans', FINAL_ANS[i])
