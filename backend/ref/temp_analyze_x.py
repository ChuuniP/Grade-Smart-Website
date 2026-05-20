import cv2
import numpy as np
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
img = cv2.imread('MDD.jpg')
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
perX1, perX2, perY1, perY2 = 20, 490, 35, 685
imgPer = imgWarp[perY1:perY2, perX1:perX2]
gray = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)[1]

h, w = imgThresh.shape
print('region size', w, h)
rows = 2
cols = 4
piece_w = w // cols
piece_h = h // rows
for y in range(cols):
    for x in range(rows):
        x0 = piece_w * y
        x1 = x0 + piece_w
        y0 = x * piece_h
        y1 = y0 + piece_h
        box = imgThresh[y0:y1, x0:x1]
        col_sum = np.sum(box, axis=0)
        col_sm = np.convolve(col_sum, np.ones(9) / 9, mode='same')
        thr = 0.3 * col_sm.max()
        peaks = np.where(col_sm > thr)[0]
        if len(peaks) == 0:
            print('box', y, x, 'no peaks')
            continue
        groups = []
        cur = [peaks[0]]
        for i in peaks[1:]:
            if i - cur[-1] > 1:
                groups.append((cur[0], cur[-1]))
                cur = [i]
            else:
                cur.append(i)
        groups.append((cur[0], cur[-1]))
        print('box', y, x, 'groups', [(a+b+2)/2 for a,b in groups], 'widths', [b-a+1 for a,b in groups])
        nz = np.where(np.any(box > 0, axis=0))[0]
        print('   nz min/max', nz.min(), nz.max(), 'span', nz.max()-nz.min()+1)
