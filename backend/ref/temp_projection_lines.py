import cv2
import numpy as np
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
img = cv2.imread(r'MDD.jpg')
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)

if len(contours) == 0:
    raise SystemExit('No contours')

pointContour = np.zeros((4, 2), dtype=np.float32)
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)
pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarp = cv2.warpPerspective(img, matrix, (WIDTH_IMG, HEIGHT_IMG))
perX1, perX2, perY1, perY2 = 15, 480, 35, 680
imgPer = imgWarp[perY1:perY2, perX1:perX2]
gray = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)[1]

col_sum = np.sum(imgThresh == 255, axis=0)
row_sum = np.sum(imgThresh == 255, axis=1)
print('width', imgThresh.shape[::-1])
print('min col sum', np.min(col_sum), 'max', np.max(col_sum), 'mean', np.mean(col_sum))
print('min row sum', np.min(row_sum), 'max', np.max(row_sum), 'mean', np.mean(row_sum))

col_valleys = np.where(col_sum < np.percentile(col_sum, 10))[0]
row_valleys = np.where(row_sum < np.percentile(row_sum, 10))[0]

print('col_valleys count', len(col_valleys))
print('row_valleys count', len(row_valleys))


def collapse(lines):
    if len(lines) == 0:
        return []
    groups = []
    cur = [lines[0]]
    for x in lines[1:]:
        if x - cur[-1] > 1:
            groups.append(int(np.mean(cur)))
            cur = [x]
        else:
            cur.append(x)
    groups.append(int(np.mean(cur)))
    return groups

col_lines = collapse(col_valleys)
row_lines = collapse(row_valleys)
print('col_lines', col_lines)
print('row_lines', row_lines)

h, w = imgThresh.shape
overlay = cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR)
for x in col_lines:
    cv2.line(overlay, (x, 0), (x, h), (0, 0, 255), 1)
for y in row_lines:
    cv2.line(overlay, (0, y), (w, y), (255, 0, 0), 1)
cv2.imwrite('debug_projection_lines.png', overlay)
print('saved debug_projection_lines.png')
